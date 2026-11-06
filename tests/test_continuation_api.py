import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments"))
from continuation_api import StudyAPI, DispatchError, output_text


class ContinuationAPITest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.calls = []
        def transport(endpoint, raw):
            self.calls.append((endpoint, json.loads(raw)))
            return 200, json.dumps({"status": "completed", "model": "gpt-6-luna",
                "usage": {"input_tokens": 10, "output_tokens": 5},
                "output": [{"type": "message", "content": [{"type": "output_text", "text": "ok"}]}]})
        self.api = StudyAPI(self.tmp.name, "/nonexistent", transport=transport)
        self.payload = {"instructions": "Test", "input": "Public synthetic"}

    def test_resume_returns_receipt_without_dispatch_and_rejects_changed_input(self):
        first = self.api.response("reader/one", "gpt-6-luna", self.payload)
        self.assertEqual(self.api.response("reader/one", "gpt-6-luna", self.payload), first)
        self.assertEqual(len(self.calls), 1)
        with self.assertRaisesRegex(ValueError, "different exact request"):
            self.api.response("reader/one", "gpt-6-luna", dict(self.payload, input="Changed"))
        self.assertEqual(len(self.calls), 1)

    def test_uncertain_request_stops_new_dispatch_and_is_not_reissued(self):
        def fail(*args):
            raise TimeoutError()
        self.api.transport = fail
        with self.assertRaises(DispatchError):
            self.api.response("reader/one", "gpt-6-luna", self.payload)
        with self.assertRaises(DispatchError):
            self.api.response("reader/one", "gpt-6-luna", self.payload, retry_known=True)
        with self.assertRaises(DispatchError):
            self.api.response("reader/two", "gpt-6-luna", self.payload)
        self.assertEqual(self.api.status()["states"], {"uncertain": 1})

    def test_explicit_retry_retains_http_failure_and_counts_every_attempt(self):
        self.api.transport = lambda *a: (503, '{"error":{"code":"unavailable"}}')
        for retry in (False, True, True):
            with self.assertRaises(DispatchError):
                self.api.response("reader/one", "gpt-6-luna", self.payload, retry_known=retry)
        with self.assertRaises(DispatchError):
            self.api.response("reader/one", "gpt-6-luna", self.payload, retry_known=True)
        self.assertEqual(self.api.status()["states"], {"http_failed": 3})

    def test_frozen_binding(self):
        self.api.bind("test", {"input": 1})
        self.api.bind("test", {"input": 1})
        with self.assertRaises(ValueError):
            self.api.bind("test", {"input": 2})

    def test_review_of_unknown_preserves_reservation_and_does_not_allow_reissue(self):
        healthy = self.api.transport
        def fail(*args):
            raise TimeoutError()
        self.api.transport = fail
        with self.assertRaises(DispatchError):
            self.api.response("material/one", "gpt-6-luna", self.payload)
        before = self.api.status()["conservative_usd"]
        self.api.acknowledge_transport_uncertainty([1], "client settled; retain unknown, continue independent work")
        self.api.transport = healthy
        with self.assertRaises(DispatchError):
            self.api.response("material/one", "gpt-6-luna", self.payload, retry_known=True)
        self.api.response("material/two", "gpt-6-luna", self.payload)
        self.assertEqual(self.api.status()["states"], {"succeeded": 1, "uncertain": 1})
        self.assertGreater(self.api.status()["conservative_usd"], before)

    def test_caps_and_no_server_history(self):
        with self.assertRaises(ValueError):
            self.api.response("reader/one", "gpt-6-luna", self.payload, cap=5000)
        with self.assertRaises(ValueError):
            self.api.response("reader/one", "other", self.payload)
        self.assertFalse(self.calls)
        self.api.response("reader/one", "gpt-6-luna", self.payload)
        body = self.calls[0][1]
        self.assertFalse(body["store"])
        self.assertNotIn("previous_response_id", body)

    def test_completed_output_is_required(self):
        with self.assertRaises(ValueError):
            output_text({"status": "incomplete", "output": []})
        with self.assertRaises(ValueError):
            output_text({"status": "completed", "output": []})

    def test_json_mode_mentions_format_in_the_actual_input(self):
        self.api.response("review/two", "gpt-6-luna", {"instructions": "Return JSON", "input": "review this"}, json_output=True)
        body = self.calls[-1][1]
        self.assertIn("json", body["input"].lower())
        self.assertEqual(body["text"]["format"]["type"], "json_object")
        self.api.response("review/three", "gpt-6-luna", {"instructions": "Return JSON", "input": "JSON: review this"}, json_output=True)
        self.assertEqual(self.calls[-1][1]["input"], "JSON: review this")

    def test_reported_input_limit_stops_subsequent_requests(self):
        self.api.transport = lambda *a: (200, json.dumps({"usage": {"input_tokens": 40000, "output_tokens": 1}}))
        self.api.response("reader/one", "gpt-6-luna", self.payload)
        with self.assertRaises(DispatchError):
            self.api.response("reader/two", "gpt-6-luna", self.payload)


if __name__ == "__main__":
    unittest.main()
