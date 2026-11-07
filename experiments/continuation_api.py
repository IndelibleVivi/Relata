"""Private, resumable official-API accounting for ADR-0012 only.

No registry, alternate endpoint, environment fallback, or automatic retry.
Request bodies and literal responses belong to the private run, never Git.
"""
from __future__ import annotations

import hashlib
from contextlib import contextmanager
import json
import math
import os
from pathlib import Path
import sqlite3
import time
import threading
import urllib.error
import urllib.request

STUDY = "relata.continuation-use/2026-11-07"
MODELS = ("gpt-6.1-sol", "gpt-6-luna")
EMBED_MODEL = "text-embedding-3-small"
DIMENSIONS = 1536
LIMITS = {"generation": 6000, "embedding": 300}
MAX_USD = 120.0
MAX_BODY = 131072
RATES = {MODELS[0]: (2.0, 10.0), MODELS[1]: (0.1, 0.5), EMBED_MODEL: (0.02, 0.0)}
ROOT = Path(__file__).resolve().parents[1]
_SLOTS = {MODELS[0]: threading.BoundedSemaphore(8), MODELS[1]: threading.BoundedSemaphore(8),
          EMBED_MODEL: threading.BoundedSemaphore(1)}


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value):
    """Identity used to reject changed requests on resume, not a quality check."""
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def json_mode_input(value):
    """Responses JSON-object mode requires JSON in an input message too."""
    if not isinstance(value, str):
        raise ValueError("fixed study uses a literal text input")
    return value if "json" in value.lower() else "Return JSON.\n" + value


def private_directory(path):
    path = Path(path).expanduser().resolve()
    if path == ROOT or ROOT in path.parents:
        raise ValueError("run artifacts must be outside the checkout")
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(path, 0o700)
    return path


class DispatchError(RuntimeError):
    pass


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class StudyAPI:
    def __init__(self, run_dir, credential_file, *, transport=None):
        self.run_dir = private_directory(run_dir)
        self.credential_file = Path(credential_file).expanduser()
        self.path = self.run_dir / "dispatch.sqlite"
        self.transport = transport or self._http
        with self._db() as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS meta(key TEXT PRIMARY KEY, value TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS attempts(
                    id INTEGER PRIMARY KEY, operation TEXT NOT NULL, attempt INTEGER NOT NULL,
                    kind TEXT NOT NULL, model TEXT NOT NULL, request_digest TEXT NOT NULL,
                    request_json TEXT NOT NULL, state TEXT NOT NULL, started REAL NOT NULL,
                    finished REAL, http_status INTEGER, response_text TEXT, error_type TEXT,
                    reservation REAL NOT NULL, accounted REAL, input_tokens INTEGER,
                    output_tokens INTEGER, returned_model TEXT,
                    UNIQUE(operation, attempt));
            """)
            old = db.execute("SELECT value FROM meta WHERE key='study'").fetchone()
            if old and old[0] != STUDY:
                raise ValueError("ledger belongs to another study")
            db.execute("INSERT OR IGNORE INTO meta VALUES('study',?)", (STUDY,))
        os.chmod(self.path, 0o600)

    @contextmanager
    def _db(self):
        db = sqlite3.connect(self.path, timeout=30)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA journal_mode=WAL")
        db.execute("PRAGMA synchronous=FULL")
        try:
            with db:
                yield db
        finally:
            db.close()

    def bind(self, name, value):
        """Freeze source/config identities, keeping original material outside Git."""
        key, encoded = "binding:" + name, canonical(value)
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
            if row and row[0] != encoded:
                raise ValueError("changed frozen binding: " + name)
            db.execute("INSERT OR IGNORE INTO meta VALUES(?,?)", (key, encoded))

    def bound(self, name):
        """Read an existing immutable study binding without creating one."""
        with self._db() as db:
            row = db.execute("SELECT value FROM meta WHERE key=?", ("binding:" + name,)).fetchone()
        return json.loads(row[0]) if row else None

    def acknowledge_transport_uncertainty(self, attempt_ids, reason):
        """Explicit coordinator review permits independent work, never reissues a request.

        Original uncertain attempts and their full reservations remain unchanged.
        This is unavailable while any request is active or for input-limit stops.
        """
        if not attempt_ids or not isinstance(reason, str) or not reason.strip():
            raise ValueError("exact uncertain attempts and review reason required")
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            if db.execute("SELECT 1 FROM attempts WHERE state='started'").fetchone():
                raise DispatchError("active requests must settle before transport review")
            stop = db.execute("SELECT value FROM meta WHERE key='dispatch-stop'").fetchone()
            if not stop or json.loads(stop[0]).get("reason") != "uncertain transport":
                raise DispatchError("only a transport stop can be acknowledged")
            actual = {r[0] for r in db.execute("SELECT id FROM attempts WHERE state='uncertain'")}
            if not set(attempt_ids) <= actual:
                raise ValueError("review includes a non-uncertain attempt")
            previous = db.execute("SELECT value FROM meta WHERE key='transport-reviews'").fetchone()
            reviews = json.loads(previous[0]) if previous else []
            reviews.append({"attempt_ids": sorted(set(attempt_ids)), "reason": reason, "at": time.time()})
            db.execute("INSERT INTO meta VALUES('transport-reviews',?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                       (canonical(reviews),))

    def operation_states(self, operation):
        with self._db() as db:
            return [dict(r) for r in db.execute("SELECT id,state,http_status FROM attempts WHERE operation=? ORDER BY attempt", (operation,))]

    def _secret(self):
        values = {}
        for line in self.credential_file.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            values[k.strip()] = v.strip().strip('"').strip("'")
        key = values.get("OPENAI_API_KEY", "")
        if not key:
            raise ValueError("OPENAI_API_KEY missing from selected credential file")
        return key

    def _http(self, endpoint, raw):
        key = self._secret()
        req = urllib.request.Request("https://api.openai.com/v1/" + endpoint, raw,
                                     {"Authorization": "Bearer " + key,
                                      "Content-Type": "application/json"})
        opener = urllib.request.build_opener(_NoRedirect())
        try:
            with opener.open(req, timeout=300) as response:
                return response.status, response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            return exc.code, exc.read().decode("utf-8", "replace").replace(key, "[REDACTED]")

    def call(self, operation, kind, body, *, retry_known=False):
        if body.get("model") not in _SLOTS:
            raise ValueError("model outside fixed study")
        with _SLOTS[body["model"]]:
            return self._call(operation, kind, body, retry_known=retry_known)

    def _call(self, operation, kind, body, *, retry_known=False):
        if kind not in LIMITS or not isinstance(operation, str) or not operation:
            raise ValueError("invalid fixed-study operation")
        model = body.get("model")
        if kind == "generation":
            if model not in MODELS or body.get("store") is not False:
                raise ValueError("only the two stateless official reader models are admitted")
            cap = body.get("max_output_tokens")
            bound = 12000 if operation.startswith("material/") else 4096
            if type(cap) is not int or not 1 <= cap <= bound:
                raise ValueError("output cap outside named operation envelope")
            if any(k in body for k in ("tools", "previous_response_id", "conversation", "background")):
                raise ValueError("study dispatch has no tools or inherited server session")
        elif model != EMBED_MODEL or body.get("dimensions") != DIMENSIONS:
            raise ValueError("fixed embedding space required")
        raw = canonical(body).encode()
        if len(raw) > MAX_BODY:
            raise ValueError("complete request exceeds byte limit")
        identity = hashlib.sha256(raw).hexdigest()
        ir, outr = RATES[model]
        # UTF8 bytes upper-bound token count conservatively; this is not token matching.
        reserve = (len(raw) * ir + body.get("max_output_tokens", 0) * outr) / 1_000_000 * 1.25
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            old = db.execute("SELECT * FROM attempts WHERE operation=? ORDER BY attempt", (operation,)).fetchall()
            if old:
                if any(r["request_digest"] != identity or r["kind"] != kind for r in old):
                    raise ValueError("operation already bound to a different exact request")
                successful = [r for r in old if r["state"] == "succeeded"]
                if successful:
                    return json.loads(successful[-1]["response_text"])
                last = old[-1]
                if (not retry_known or len(old) >= 3 or last["state"] != "http_failed"
                        or last["http_status"] not in (429, 500, 502, 503, 504)):
                    raise DispatchError("operation already attempted; preserve its failure/uncertainty")
                error = json.loads(last["response_text"]).get("error", {})
                if error.get("code") in ("insufficient_quota", "credit_balance_exhausted"):
                    raise DispatchError("account resource failure; no automatic paid fallback")
            stop = db.execute("SELECT value FROM meta WHERE key='dispatch-stop'").fetchone()
            if stop:
                reason = json.loads(stop[0]).get("reason")
                previous = db.execute("SELECT value FROM meta WHERE key='transport-reviews'").fetchone()
                acknowledged = {i for r in (json.loads(previous[0]) if previous else []) for i in r["attempt_ids"]}
                uncertain = {r[0] for r in db.execute("SELECT id FROM attempts WHERE state='uncertain'")}
                if reason != "uncertain transport" or not uncertain <= acknowledged:
                    raise DispatchError("study dispatch is stopped; inspect recorded reason")
            if db.execute("SELECT COUNT(*) FROM attempts WHERE kind=?", (kind,)).fetchone()[0] >= LIMITS[kind]:
                raise DispatchError("cumulative dispatch cap reached")
            used = db.execute("SELECT COALESCE(SUM(COALESCE(accounted,reservation)),0) FROM attempts").fetchone()[0]
            if used + reserve > MAX_USD:
                raise DispatchError("cumulative local cost ceiling reached")
            cursor = db.execute("""INSERT INTO attempts(operation,attempt,kind,model,request_digest,
                request_json,state,started,reservation) VALUES(?,?,?,?,?,?,'started',?,?)""",
                (operation, len(old) + 1, kind, model, identity, raw.decode(), time.time(), reserve))
            attempt_id = cursor.lastrowid
        try:
            status, response_text = self.transport("responses" if kind == "generation" else "embeddings", raw)
        except Exception as exc:
            with self._db() as db:
                db.execute("UPDATE attempts SET state='uncertain',finished=?,error_type=? WHERE id=? AND state='started'",
                           (time.time(), type(exc).__name__, attempt_id))
                db.execute("INSERT OR IGNORE INTO meta VALUES('dispatch-stop',?)",
                           (canonical({"reason": "uncertain transport", "attempt": attempt_id}),))
            raise DispatchError("transport outcome uncertain; no automatic reissue") from exc
        try:
            value = json.loads(response_text)
        except (ValueError, TypeError):
            value = None
        usage = value.get("usage", {}) if isinstance(value, dict) else {}
        inp = usage.get("input_tokens", usage.get("prompt_tokens"))
        out = usage.get("output_tokens", 0 if kind == "embedding" and inp is not None else None)
        valid_usage = all(type(x) is int and x >= 0 for x in (inp, out))
        accounted = (inp * ir + out * outr) / 1_000_000 * 1.25 if valid_usage else None
        state = "succeeded" if 200 <= status < 300 and isinstance(value, dict) else "http_failed"
        if 200 <= status < 300 and value is None:
            state = "invalid_response"
        returned = value.get("model") if isinstance(value, dict) else None
        with self._db() as db:
            db.execute("""UPDATE attempts SET state=?,finished=?,http_status=?,response_text=?,
                accounted=?,input_tokens=?,output_tokens=?,returned_model=? WHERE id=? AND state='started'""",
                (state, time.time(), status, response_text, accounted, inp if valid_usage else None,
                 out if valid_usage else None, returned, attempt_id))
            if valid_usage and inp > 32768:
                db.execute("INSERT INTO meta VALUES('dispatch-stop',?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                           (canonical({"reason": "reported input limit exceeded", "attempt": attempt_id}),))
        if state != "succeeded":
            err = value.get("error", {}) if isinstance(value, dict) else {}
            raise DispatchError("HTTP %s / %s (%s)" % (status, err.get("code"), state))
        return value

    def response(self, operation, model, payload, *, cap=4096, json_output=False, json_schema=None, retry_known=False):
        body = {"model": model, "instructions": payload["instructions"], "input": payload["input"],
                "store": False, "max_output_tokens": cap, "reasoning": {"effort": "low"}}
        if json_schema is not None:
            body["text"] = {"format": {"type": "json_schema", "name": "continuation_material", "strict": True, "schema": json_schema}}
        elif json_output:
            body["text"] = {"format": {"type": "json_object"}}
            body["input"] = json_mode_input(body["input"])
        return self.call(operation, "generation", body, retry_known=retry_known)

    def embed(self, operation, texts):
        if not isinstance(texts, list) or not texts or any(not isinstance(t, str) or not t or len(t.encode()) > 8000 for t in texts):
            raise ValueError("nonempty <=8000-byte synthetic embedding inputs required")
        value = self.call(operation, "embedding", {"model": EMBED_MODEL, "input": texts,
                          "encoding_format": "float", "dimensions": DIMENSIONS})
        data = sorted(value.get("data", []), key=lambda row: row.get("index", -1))
        if [row.get("index") for row in data] != list(range(len(texts))):
            raise ValueError("embedding batch index mismatch")
        vectors = [row.get("embedding", []) for row in data]
        for vector in vectors:
            if len(vector) != DIMENSIONS or any(type(x) not in (int, float) or not math.isfinite(x) for x in vector):
                raise ValueError("invalid embedding dimension or value")
            if sum(x * x for x in vector) == 0:
                raise ValueError("zero embedding")
        return vectors

    def status(self):
        with self._db() as db:
            states = {r[0]: r[1] for r in db.execute("SELECT state,COUNT(*) FROM attempts GROUP BY state")}
            rows = [dict(r) for r in db.execute("""SELECT kind,model,COUNT(*) AS attempts,
                    SUM(input_tokens) AS input_tokens,SUM(output_tokens) AS output_tokens,
                    SUM(COALESCE(accounted,reservation)) AS conservative_usd
                    FROM attempts GROUP BY kind,model""")]
            stop = db.execute("SELECT value FROM meta WHERE key='dispatch-stop'").fetchone()
            review_row = db.execute("SELECT value FROM meta WHERE key='transport-reviews'").fetchone()
            reviews = json.loads(review_row[0]) if review_row else []
            unknown = {r[0] for r in db.execute("SELECT id FROM attempts WHERE state='uncertain'")}
        stop_value = json.loads(stop[0]) if stop else None
        reviewed = {i for review in reviews for i in review["attempt_ids"]}
        return {"study": STUDY, "states": states, "by_model": rows,
                "conservative_usd": sum(r["conservative_usd"] for r in rows),
                "cost_is_invoice": False, "dispatch_stop": stop_value,
                "transport_reviews": reviews,
                "dispatch_blocked": bool(stop_value and (stop_value.get("reason") != "uncertain transport" or not unknown <= reviewed))}


def output_text(value):
    """Separate HTTP success from completed, nonempty answer text."""
    if value.get("status") != "completed":
        raise ValueError("response not completed: " + str(value.get("status")))
    parts = [c.get("text", "") for item in value.get("output", []) if item.get("type") == "message"
             for c in item.get("content", []) if c.get("type") == "output_text"]
    text = "\n".join(parts).strip()
    if not text:
        raise ValueError("completed response has no answer text")
    return text
