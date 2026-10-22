"""Private evidence and HTTP-boundary accounting for the fixed RC-005 study."""
import fcntl
import json
import math
import os
from pathlib import Path
import time
import uuid
import urllib.request
import urllib.error

PIN = 'a39a802bbc93e85b820078cd3c4dbaf53af25dbe'
LIMITS = {'chat': 300, 'embedding': 500}

def dump(value):
    return json.dumps(value, ensure_ascii=False, allow_nan=False)

def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix('.tmp')
    tmp.write_text(dump(value) + '\n')
    tmp.replace(path)

def stamp():
    return {'wall': time.time(), 'monotonic': time.monotonic(), 'pid': os.getpid()}

class Ledger:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def transact(self, callback):
        with self.path.open('a+') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            f.seek(0)
            rows = [json.loads(line) for line in f if line.strip()]
            row = callback(rows)
            if row is not None:
                f.seek(0, 2)
                f.write(dump(row) + '\n')
                f.flush()
                os.fsync(f.fileno())
            return row

    def note(self, **row):
        return self.transact(lambda _: dict(row, **stamp()))

    def reserve(self, kind, body, operation):
        def check(rows):
            if any(r.get('event') == 'token-stop' for r in rows):
                raise RuntimeError('reported prompt_tokens exceeded 32768: dispatch stopped')
            if sum(r.get('event') == 'dispatch' and r.get('kind') == kind for r in rows) >= LIMITS[kind]:
                raise RuntimeError(kind + ' dispatch budget exhausted')
            if len(body) > 65536:
                raise ValueError('complete HTTP body exceeds 65536 UTF8 bytes')
            return dict(event='dispatch', id=uuid.uuid4().hex, kind=kind,
                        operation=operation, body=json.loads(body), **stamp())
        return self.transact(check)['id']

    def returned(self, dispatch, status, body):
        try:
            value = json.loads(body)
        except (ValueError, TypeError):
            value = {'unparsed': str(body)}
        self.note(event='return', dispatch=dispatch, status=status, body=value)
        if isinstance(value, dict) and (value.get('usage') or {}).get('prompt_tokens', 0) > 32768:
            self.note(event='token-stop', dispatch=dispatch)

    def bind(self, out, identity):
        def check(rows):
            bindings = [r for r in rows if r.get('event') == 'binding']
            value = {'event': 'binding', 'out': str(Path(out).resolve()), 'identity': identity}
            if bindings:
                if any(r['out'] != value['out'] or r['identity'] != identity for r in bindings):
                    raise ValueError('ledger belongs to a different output/configuration; do not reset budget')
                return None
            return dict(value, **stamp())
        self.transact(check)

def key(config):
    if 'key_file' in config:
        return Path(config['key_file']).read_text().strip()
    return os.environ[config['api_key_env']]

def query_text(text, config):
    return 'Instruct: ' + config['query_instruction'] + '\nQuery: ' + text

def vectors(value, count):
    data = sorted(value['data'], key=lambda item: item['index'])
    if [d['index'] for d in data] != list(range(count)):
        raise ValueError('embedding batch indices/order invalid')
    result = [d['embedding'] for d in data]
    if any(len(v) != 1024 or not all(isinstance(x, (int, float)) and math.isfinite(x) for x in v) or sum(x*x for x in v) == 0 for v in result):
        raise ValueError('invalid 1024-dimensional finite nonzero embedding')
    return [[x / math.sqrt(sum(y*y for y in v)) for x in v] for v in result]

class HTTP:
    def __init__(self, config, ledger):
        self.config, self.ledger = config, ledger

    def call(self, kind, body, operation):
        cfg = self.config[kind]
        raw = dump(body).encode()
        dispatch = self.ledger.reserve(kind, raw, operation)
        url = cfg['base_url'].rstrip('/') + ('/chat/completions' if kind == 'chat' else '/embeddings')
        request = urllib.request.Request(url, raw, {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + key(cfg)})
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                data = response.read()
                self.ledger.returned(dispatch, response.status, data)
                return json.loads(data)
        except urllib.error.HTTPError as error:
            self.ledger.returned(dispatch, error.code, error.read())
            raise
        except Exception as error:
            self.ledger.note(event='http-error', dispatch=dispatch, error=type(error).__name__)
            raise

    def embed(self, texts, operation, query=False):
        cfg = self.config['embedding']
        inputs = [query_text(t.replace('\n', ' '), cfg) if query else t.replace('\n', ' ') for t in texts]
        value = self.call('embedding', {'model': cfg['model'], 'input': inputs, 'encoding_format': 'float'}, operation)
        return vectors(value, len(inputs))

    def reader(self, admitted, operation):
        return self.call('chat', {'model': self.config['chat']['model'], 'temperature': 0, 'top_p': 1,
            'max_tokens': 1024, 'stream': False, 'messages': [
                {'role': 'system', 'content': admitted['context']},
                {'role': 'user', 'content': dump({'history': admitted['history'], 'current': admitted['current']})}]}, operation)
