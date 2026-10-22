#!/usr/bin/env python3
"""Fixed pinned Mem0 stdio child. Stdout is reserved for RPC, native noise -> stderr."""
import contextlib
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import sys
from rc005_common import Ledger, PIN, key, query_text, stamp, vectors


def serve(config_path, state_path):
    cfg = json.loads(Path(config_path).read_text())
    state = Path(state_path).resolve()
    state.mkdir(parents=True, exist_ok=True)
    secrets = {kind: key(cfg[kind]) for kind in ('chat', 'embedding')}
    for name in list(os.environ):
        if name.startswith(('OPENAI_', 'OPENROUTER_')):
            os.environ.pop(name)
    os.environ['MEM0_TELEMETRY'] = 'false'
    os.environ['MEM0_DIR'] = str(state / 'mem0-home')
    upstream = Path(cfg['upstream']).resolve()
    if subprocess.check_output(['git', '-C', str(upstream), 'rev-parse', 'HEAD'], text=True).strip() != PIN:
        raise ValueError('upstream pin mismatch')
    if subprocess.check_output(['git', '-C', str(upstream), 'status', '--porcelain'], text=True).strip():
        raise ValueError('upstream must be clean')
    sys.path.insert(0, str(upstream))
    ledger = Ledger(cfg['ledger'])
    operation = ['initialization']
    with contextlib.redirect_stdout(sys.stderr):
        import httpx
        from mem0 import Memory
        import mem0
        if not Path(mem0.__file__).resolve().is_relative_to(upstream):
            raise ValueError('Mem0 import escaped pinned checkout')
        if importlib.util.find_spec('spacy') or importlib.util.find_spec('fastembed'):
            raise ValueError('study runtime must omit optional NLP/model download packages')

        class RecordedTransport(httpx.BaseTransport):
            def __init__(self, kind):
                self.kind = kind
                self.inner = httpx.HTTPTransport(retries=0)

            def handle_request(self, request):
                raw = request.read()
                body = json.loads(raw)
                if self.kind == 'chat' and max(body.get('max_tokens', 0), body.get('max_completion_tokens', 0)) > 2048:
                    raise ValueError('native output cap exceeded')
                dispatch = ledger.reserve(self.kind, raw, operation[0])
                try:
                    response = self.inner.handle_request(request)
                    data = response.read()
                    ledger.returned(dispatch, response.status_code, data)
                    if self.kind == 'embedding' and response.status_code < 400:
                        parsed = json.loads(data)
                        normalized = vectors(parsed, len(body['input']))
                        for item in parsed['data']:
                            item['embedding'] = normalized[item['index']]
                        data = json.dumps(parsed).encode()
                    return httpx.Response(response.status_code, content=data, request=request,
                        headers={'content-type': 'application/json'})
                except Exception as error:
                    ledger.note(event='http-error', dispatch=dispatch, error=type(error).__name__)
                    raise

        config = {'llm': {'provider': 'openai', 'config': {
            'model': cfg['chat']['model'], 'api_key': secrets['chat'],
            'openai_base_url': cfg['chat']['base_url'], 'temperature': 0, 'top_p': 1, 'max_tokens': 2048}},
            'embedder': {'provider': 'openai', 'config': {'model': cfg['embedding']['model'],
                'api_key': secrets['embedding'], 'openai_base_url': cfg['embedding']['base_url'], 'embedding_dims': 1024}},
            'vector_store': {'provider': 'qdrant', 'config': {'path': str(state / 'qdrant'),
                'collection_name': 'rc005', 'embedding_model_dims': 1024, 'on_disk': True}},
            'history_db_path': str(state / 'history.sqlite')}
        memory = Memory.from_config(config)
        for component, kind in [(memory.llm, 'chat'), (memory.embedding_model, 'embedding')]:
            component.client = component.client.with_options(max_retries=0, timeout=60,
                http_client=httpx.Client(transport=RecordedTransport(kind), timeout=60, trust_env=False))
        # Common encoder policy: normalize source newlines first; add instruction after.
        # Wrapping the SDK seam avoids upstream embed() flattening the instruction.
        class CommonEncoder:
            def embed_batch(self, texts, memory_action='add'):
                inputs = [t.replace('\n', ' ') for t in texts]
                if memory_action == 'search':
                    inputs = [query_text(t, cfg['embedding']) for t in inputs]
                response = memory.embedding_model_client.embeddings.create(
                    model=cfg['embedding']['model'], input=inputs, encoding_format='float')
                return [item.embedding for item in sorted(response.data, key=lambda item: item.index)]
            def embed(self, text, memory_action=None):
                return self.embed_batch([text], memory_action)[0]
        memory.embedding_model_client = memory.embedding_model.client
        memory.embedding_model = CommonEncoder()
    ready = dict(event='ready', state=str(state), source=str(upstream), pin=PIN,
        versions={p: importlib.metadata.version(p) for p in ['mem0ai', 'openai', 'qdrant-client']},
        visibility='source-native; no spaCy/fastembed; native fallback; tool role ignored by upstream parse_messages', **stamp())
    print(json.dumps(ready), flush=True)
    for line in sys.stdin:
        request = json.loads(line)
        operation[0] = request['operation']
        try:
            with contextlib.redirect_stdout(sys.stderr):
                if request['method'] == 'add':
                    result = memory.add(request['messages'], user_id='rc005-synthetic', infer=True)
                elif request['method'] == 'search':
                    result = memory.search(request['query'], filters={'user_id': 'rc005-synthetic'}, top_k=10, rerank=False)
                else:
                    raise ValueError('unknown fixed study operation')
            response = dict(ok=True, operation=request['operation'], result=result, **stamp())
        except Exception as error:
            response = dict(ok=False, operation=request['operation'], error=type(error).__name__ + ': ' + str(error), **stamp())
        print(json.dumps(response, ensure_ascii=False, default=str), flush=True)

if __name__ == '__main__':
    serve(sys.argv[1], sys.argv[2])
