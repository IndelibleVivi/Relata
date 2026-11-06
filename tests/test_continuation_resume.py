import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from continuation_study import read_tasks, form_memories, save_once, save_answer, parallel
from continuation_api import StudyAPI
from test_continuation_core import bundle


class ContinuationResumeTest(unittest.TestCase):
    def test_first_error_stops_unstarted_work_in_the_same_batch(self):
        called = []
        def fail(item):
            called.append(item)
            raise ValueError("invalid request")
        with contextlib.redirect_stdout(io.StringIO()), self.assertRaises(RuntimeError):
            parallel([{"id": str(i)} for i in range(60)], fail, 2)
        self.assertLessEqual(len(called), 2)

    def test_concurrent_materialization_preserves_one_complete_private_artifact(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "receipt.json"
            value = {"literal": "已落盘的原始内容" * 1000}
            with ThreadPoolExecutor(max_workers=4) as executor:
                list(executor.map(lambda _: save_once(path, value), range(8)))
            self.assertEqual(json.loads(path.read_text()), value)
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            self.assertEqual(list(Path(directory).glob(".pending-*")), [])
            with self.assertRaises(ValueError):
                save_once(path, {"literal": "另一个结果"})
            self.assertEqual(json.loads(path.read_text()), value)

    def test_roundoff_keeps_original_receipt_but_changed_ranking_or_text_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "answer.json"
            value = {"answer": "原话", "ranking": [
                {"episode_id": "E1", "dense": 0.4, "lexical": 17.366241646211243, "rrf": 0.03}]}
            save_answer(path, value)
            before = path.read_bytes()
            candidate = json.loads(json.dumps(value))
            candidate["ranking"][0]["lexical"] = 17.366241646211247
            save_answer(path, candidate)
            self.assertEqual(before, path.read_bytes())
            candidate["answer"] = "改过的答案"
            with self.assertRaises(ValueError):
                save_answer(path, candidate)
            candidate["answer"] = "原话"
            candidate["ranking"][0]["episode_id"] = "E2"
            with self.assertRaises(ValueError):
                save_answer(path, candidate)

    def test_uncertain_position_survives_resume_without_duplicate_dispatch(self):
        with tempfile.TemporaryDirectory() as directory:
            calls = []
            timed_out = False

            def transport(endpoint, raw):
                nonlocal timed_out
                body = json.loads(raw)
                calls.append((endpoint, body))
                if endpoint == "embeddings":
                    return 200, json.dumps({"data": [
                        {"index": i, "embedding": [1.0] + [0.0] * 1535}
                        for i in range(len(body["input"]))]})
                if not timed_out:
                    timed_out = True
                    raise TimeoutError()
                return 200, json.dumps({"status": "completed", "model": body["model"],
                    "id": str(len(calls)), "output": [{"type": "message", "content": [
                        {"type": "output_text", "text": "完成本次工作。"}]}],
                    "usage": {"input_tokens": 5, "output_tokens": 5}})

            api = StudyAPI(directory, "/unused", transport=transport)
            roots = bundle()
            values = (roots[0]["histories"], roots[1]["probes"], roots[2]["oracles"])
            for arm in ("summary", "notes"):
                save_once(Path(directory) / "memory" / "D01" / arm / "E6.json", {"text": "已有记忆。"})
            args = SimpleNamespace(split="development", ids=None, workers=1)
            with patch("continuation_study.freeze_sources", return_value=values), contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaises(RuntimeError):
                    read_tasks(args, api)
                self.assertEqual(len(calls), 2)
                api.acknowledge_transport_uncertainty([2], "offline test: owning call settled")
                read_tasks(args, api)
                self.assertEqual(len(calls), 31)  # One index plus 30 answer positions, one unknown.
                paths = list((Path(directory) / "answers").rglob("*.json"))
                self.assertEqual(len(paths), 30)
                records = [json.loads(p.read_text()) for p in paths]
                self.assertEqual(sum(r["state"] == "uncertain" for r in records), 1)
                self.assertEqual(sum(r["state"] == "completed" for r in records), 29)
                before = {str(p): p.read_bytes() for p in paths}
                read_tasks(args, api)
                self.assertEqual(len(calls), 31)
                self.assertEqual(before, {str(p): p.read_bytes() for p in paths})

    def test_failed_memory_trajectory_does_not_erase_other_conditions(self):
        with tempfile.TemporaryDirectory() as directory:
            calls = []
            def transport(endpoint, raw):
                body = json.loads(raw)
                calls.append(body)
                if len(calls) == 1:
                    raise TimeoutError()
                if endpoint == "embeddings":
                    return 200, json.dumps({"data": [{"index": i, "embedding": [1.0] + [0.0]*1535}
                        for i in range(len(body["input"]))]})
                return 200, json.dumps({"status": "completed", "id": str(len(calls)), "model": body["model"],
                    "output": [{"type": "message", "content": [{"type": "output_text", "text": "实际产物"}]}]})
            api = StudyAPI(directory, "/unused", transport=transport)
            roots = bundle()
            values = (roots[0]["histories"], roots[1]["probes"], roots[2]["oracles"])
            args = SimpleNamespace(split="development", ids=None, workers=1)
            with patch("continuation_study.freeze_sources", return_value=values), contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaises(RuntimeError):
                    form_memories(args, api)
                api.acknowledge_transport_uncertainty([1], "test: writer request settled without observable output")
                form_memories(args, api)
                self.assertEqual(len(calls), 7)  # Original unknown plus six notes writes; no summary reissue.
                self.assertFalse((Path(directory)/"memory/D01/summary/E6.json").exists())
                self.assertTrue((Path(directory)/"memory/D01/notes/E6.json").exists())
                read_tasks(args, api)
                records = [json.loads(p.read_text()) for p in (Path(directory)/"answers").rglob("*.json")]
                self.assertEqual(len(records), 24)
                self.assertEqual({r["condition"] for r in records}, {"current", "search", "notes", "full"})
                self.assertEqual(len(calls), 32)


if __name__ == "__main__":
    unittest.main()
