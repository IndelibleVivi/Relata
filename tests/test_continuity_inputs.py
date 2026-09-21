"""Regression coverage for the CT-AUTHORSHIP offline input preparation module.

All fixture data is public synthetic adult material. No subject, model, adapter,
corpus, command, network call, or score exists in this tooling.
"""
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

from tools import continuity_inputs as c

sys.path.insert(0, str(Path(c.__file__).resolve().parent))


def packets(bundle):
    """Every (variant, probe) pair in authored order."""
    return [(variant, probe)
            for variant in c.the_family(bundle)["variants"]
            for probe in variant["probes"]]


def quiet_main(argv):
    """Run the CLI entry point while suppressing its JSON stdout."""
    with contextlib.redirect_stdout(io.StringIO()):
        return c.main(argv)


class FixtureTests(unittest.TestCase):
    def setUp(self):
        self.bundle = c.load_case()

    def test_fixture_identity_and_status_are_unpromoted(self):
        self.assertEqual(self.bundle["bundle_id"], "relata-ct-authorship-candidate-1")
        self.assertIn("not-accepted", self.bundle["status"])
        self.assertEqual(self.bundle["semantic_validation"], "not-run")
        self.assertEqual(self.bundle["system_evaluation"], "not-run")
        self.assertEqual(self.bundle["human_review"], "not-run")

    def test_check_counts_and_pairing_invariants(self):
        counts = c.validate(self.bundle)
        self.assertEqual(counts["histories"], 2)
        self.assertEqual(counts["checkpoints"], 6)
        self.assertEqual(counts["subject_inputs"], 18)
        # One reviewer packet file per prepared input; one distinct body per checkpoint.
        self.assertEqual(counts["reviewer_packets"], 18)
        self.assertEqual(counts["reviewer_packet_bodies"], 6)
        self.assertEqual(counts["contrast_pairs"], 3)
        self.assertEqual(counts["invariance_pairs"], 0)

    def test_check_rejects_semantic_or_result_claims(self):
        for field in ("semantic_validation", "system_evaluation", "human_review"):
            bundle = json.loads(json.dumps(self.bundle))
            bundle[field] = "passed"
            with self.subTest(field=field), self.assertRaises(ValueError):
                c.validate(bundle)

    def test_only_bundled_fixture_is_accepted(self):
        with tempfile.TemporaryDirectory() as temp:
            other = Path(temp).resolve() / "copy.json"
            other.write_text(c.CASE_SOURCE.read_text(encoding="utf-8"), encoding="utf-8")
            with self.assertRaises(ValueError):
                c.load_case(other)

    def test_fixture_has_exactly_one_family(self):
        two = json.loads(json.dumps(self.bundle))
        two["families"].append(json.loads(json.dumps(two["families"][0])))
        with self.assertRaises(ValueError):
            c.validate(two)


class SubjectInputTests(unittest.TestCase):
    def setUp(self):
        self.bundle = c.load_case()
        self.left, self.right = c.the_family(self.bundle)["variants"]

    def test_current_twins_are_identical(self):
        for lp, rp in zip(self.left["probes"], self.right["probes"]):
            self.assertEqual(lp["current"], rp["current"])
            for condition in c.CONDITIONS:
                a = c.subject_input(self.bundle, self.left, lp, condition)
                b = c.subject_input(self.bundle, self.right, rp, condition)
                self.assertEqual(a["current"], b["current"])
                self.assertEqual(a["context"], b["context"])

    def test_current_only_exposes_no_history(self):
        for variant, probe in packets(self.bundle):
            self.assertEqual(c.subject_input(self.bundle, variant, probe, "current-only")["history"], [])

    def test_full_history_exposes_ordered_prefix(self):
        for variant, probe in packets(self.bundle):
            prefix = c.history_prefix(variant, probe)
            self.assertEqual(
                c.subject_input(self.bundle, variant, probe, "full-history")["history"],
                c.source_view(prefix))

    def test_speaker_only_difference_between_historic_twins(self):
        # A and B differ only in the speaker role of the two earliest title events.
        la = c.source_view(c.history_prefix(self.left, self.left["probes"][0]))
        lb = c.source_view(c.history_prefix(self.right, self.right["probes"][0]))
        self.assertNotEqual(la, lb)
        for a, b in zip(la, lb):
            self.assertEqual({k: v for k, v in a.items() if k != "role"},
                             {k: v for k, v in b.items() if k != "role"})
        roles = [row["role"] for row in la]
        self.assertNotEqual(roles, [row["role"] for row in lb])

    def test_source_excerpt_is_ordered_raw_subset(self):
        for variant, probe in packets(self.bundle):
            excerpt = c.subject_input(self.bundle, variant, probe, "source-excerpt")["history"]
            prefix_ids = [event["id"] for event in c.history_prefix(variant, probe)]
            subset_ids = probe["review"]["source_event_ids"]
            expected_ids = [event_id for event_id in prefix_ids if event_id in set(subset_ids)]
            self.assertEqual(len(excerpt), len(subset_ids))
            expected_view = c.source_view(
                [event for event in variant["history"] if event["id"] in set(expected_ids)])
            self.assertEqual(excerpt, expected_view)

    def test_subject_input_exposes_context_history_current_only(self):
        for variant, probe in packets(self.bundle):
            for condition in c.CONDITIONS:
                subject = c.subject_input(self.bundle, variant, probe, condition)
                self.assertEqual(set(subject), set(c.SUBJECT_FIELDS))
                for hidden in ("role", "condition", "variant", "probe", "review", "source_event_ids"):
                    self.assertNotIn(hidden, subject)
                for event in subject["history"]:
                    self.assertEqual(set(event), set(c.HISTORY_FIELDS))

    def test_unknown_condition_is_rejected(self):
        variant, probe = packets(self.bundle)[0]
        with self.assertRaises(ValueError):
            c.subject_input(self.bundle, variant, probe, "scripted-native")

    def test_packets_carry_authoring_metadata_that_subjects_must_not_see(self):
        subject = c.subject_input(self.bundle, *packets(self.bundle)[0], "full-history")
        blob = json.dumps(subject, ensure_ascii=False)
        for canary in ("e1", "e2", "after_event", "source_event_ids", "required_meanings",
                       "prohibited_meanings", "hinge_value", "pair_relation", "semantic_status",
                       "authored-unvalidated", "CT-AUTHORSHIP"):
            self.assertNotIn(canary, blob)

    def test_future_events_and_prior_probes_never_reach_subject(self):
        variant, probe = packets(self.bundle)[0]
        visible_ids = {e["id"] for e in c.history_prefix(variant, probe)}
        after = [event for event in variant["history"] if event["id"] not in visible_ids]
        for condition in c.CONDITIONS:
            subject = c.subject_input(self.bundle, variant, probe, condition)
            texts = [event["text"] for event in subject["history"]]
            for future in after:
                self.assertNotIn(future["text"], texts)
            for other in variant["probes"]:
                if other["id"] != probe["id"]:
                    self.assertNotIn(other["current"]["text"], texts)

    def test_unknown_current_metadata_does_not_leak(self):
        bundle = json.loads(json.dumps(self.bundle))
        probe = c.the_family(bundle)["variants"][0]["probes"][0]
        probe["current"]["gold_answer"] = "REVIEWER-ONLY-CANARY"
        probe["review"]["hidden_note"] = "REVIEWER-ONLY-CANARY"
        subject = c.subject_input(bundle, c.the_family(bundle)["variants"][0], probe, "full-history")
        blob = json.dumps(subject, ensure_ascii=False)
        self.assertNotIn("REVIEWER-ONLY-CANARY", blob)
        self.assertEqual(set(subject["current"]), {"surface", "text"})


class ReviewerPacketTests(unittest.TestCase):
    def setUp(self):
        self.bundle = c.load_case()

    def test_reviewer_packet_has_complete_governing_history(self):
        for variant, probe in packets(self.bundle):
            packet = c.reviewer_packet(self.bundle, variant, probe)
            self.assertEqual(set(packet), set(c.REVIEW_FIELDS))
            self.assertEqual(packet["governing_history"],
                             c.source_view(c.history_prefix(variant, probe)))
            self.assertEqual(packet["current"]["text"], probe["current"]["text"])
            # Explicit unanswered state: the key must be present and null.
            self.assertIn("response", packet)
            self.assertIsNone(packet["response"])
            self.assertIn("review_status", packet)
            self.assertEqual(packet["review_status"], "pending-no-response")
            self.assertEqual(packet["instructions"], c.REVIEW_INSTRUCTIONS)

    def test_reviewer_packet_has_no_authoring_ids_or_labels(self):
        for variant, probe in packets(self.bundle):
            blob = json.dumps(c.reviewer_packet(self.bundle, variant, probe), ensure_ascii=False)
            for hidden in ('"e1"', '"e2"', "after_event", "source_event_ids",
                           "required_meanings", "prohibited_meanings", "hinge_value",
                           "authored-unvalidated", "pair_relation",
                           "authoring_review_contract", "review_guidance"):
                self.assertNotIn(hidden, blob)


class ProjectionAuditTests(unittest.TestCase):
    def setUp(self):
        self.bundle = c.load_case()

    def test_without_speaker_changes_only_role(self):
        for variant, probe in packets(self.bundle):
            full = c.project(self.bundle, variant, probe, "full-history")
            bare = c.project(self.bundle, variant, probe, "without-speaker")
            self.assertEqual(len(full["history"]), len(bare["history"]))
            for a, b in zip(full["history"], bare["history"]):
                self.assertNotIn("role", b)
                self.assertEqual({k: v for k, v in a.items() if k != "role"}, b)

    def test_expected_collision_counts(self):
        report = c.audit(self.bundle)
        observed = {row["projection"]: row["collisions_on_contrast_pairs"]
                    for row in report["projections"]}
        self.assertEqual(observed, c.EXPECTED_COLLISIONS)
        for row in report["projections"]:
            self.assertEqual(row["contrast_pairs"], 3)
            self.assertTrue(row["matches_expected"])

    def test_full_history_distinguishes_every_contrast(self):
        row = next(r for r in c.audit(self.bundle)["projections"] if r["projection"] == "full-history")
        self.assertEqual(row["collisions_on_contrast_pairs"], 0)
        self.assertTrue(all(not record["identical_projected_inputs"] for record in row["records"]))

    def test_unknown_projection_is_rejected(self):
        variant, probe = packets(self.bundle)[0]
        with self.assertRaises(ValueError):
            c.project(self.bundle, variant, probe, "native-retrieval")


class BuildVerifyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        self.bundle = c.load_case()

    def tearDown(self):
        self.temp.cleanup()

    def build(self):
        return c.build(self.bundle, self.root / "run", salt="a" * 64)

    def test_build_writes_isolated_inputs_and_verify_accepts(self):
        key = self.build()
        subject_files = list((self.root / "run" / "subjects").iterdir())
        reviewer_files = list((self.root / "run" / "reviewers").iterdir())
        # Returned counts must equal actual generated directory membership.
        self.assertEqual(key["counts"]["subject_inputs"], len(subject_files))
        self.assertEqual(key["counts"]["reviewer_packets"], len(reviewer_files))
        # One reviewer packet per prepared input, sharing the input's opaque ID.
        self.assertEqual({p.name for p in subject_files}, {p.name for p in reviewer_files})
        self.assertEqual(len(key["records"]), len(subject_files))
        # The reviewer packet body depends only on (variant, probe): six distinct bodies.
        bodies = {path.read_bytes() for path in reviewer_files}
        self.assertEqual(key["counts"]["reviewer_packet_bodies"], len(bodies))
        result = c.verify(self.root / "run", self.bundle)
        self.assertEqual(result["status"], "prepared-material-valid")
        self.assertEqual(result["semantic_status"], "authored-unvalidated")

    def test_verify_accepts_relative_build_and_verify_paths(self):
        # Build and verify using paths relative to the current working directory.
        relative = Path("rel-run")
        previous = Path.cwd()
        self.addCleanup(lambda: __import__("os").chdir(previous))
        __import__("os").chdir(self.root)
        self.assertEqual(quiet_main(["build", "--out", str(relative)]), 0)
        self.assertEqual(quiet_main(["verify", str(relative)]), 0)
        self.assertTrue((self.root / "rel-run" / "subjects").is_dir())

    def test_opaque_filenames_and_no_role_metadata(self):
        self.build()
        names = {p.name for p in (self.root / "run" / "subjects").iterdir()}
        self.assertEqual(len(names), 18)
        for name in names:
            self.assertRegex(name, r"^[0-9a-f]{24}\.json$")
        for path in (self.root / "run" / "subjects").iterdir():
            text = path.read_text(encoding="utf-8")
            for canary in ("CT-AUTHORSHIP", "current-only", "source-excerpt"):
                self.assertNotIn(canary, text)

    def test_fresh_digest_matches_build(self):
        key = self.build()
        packet = key["records"][0]
        raw = (self.root / "run" / "subjects" / (packet["packet_id"] + ".json")).read_bytes()
        self.assertEqual(c.digest(raw), packet["subject_sha256"])

    def test_every_prepared_item_matches_intended_source(self):
        key = self.build()
        salt = key["id_salt"]
        expected = {}
        for variant, probe in packets(self.bundle):
            for condition in c.CONDITIONS:
                identifier = c.packet_id(salt, c.FAMILY_ID, variant["id"], probe["id"], condition)
                expected[identifier] = (
                    c.encoded(c.subject_input(self.bundle, variant, probe, condition)),
                    c.encoded(c.reviewer_packet(self.bundle, variant, probe)),
                    probe["review"])
        for identifier, (subject_bytes, reviewer_bytes, contract) in expected.items():
            self.assertEqual((self.root / "run" / "subjects" / (identifier + ".json")).read_bytes(),
                             subject_bytes)
            self.assertEqual((self.root / "run" / "reviewers" / (identifier + ".json")).read_bytes(),
                             reviewer_bytes)
        records = {record["packet_id"]: record for record in key["records"]}
        self.assertEqual(set(records), set(expected))
        for identifier, (subject_bytes, reviewer_bytes, contract) in expected.items():
            record = records[identifier]
            self.assertEqual(record["subject_sha256"], c.digest(subject_bytes))
            self.assertEqual(record["reviewer_sha256"], c.digest(reviewer_bytes))
            self.assertEqual(record["authoring_review_contract"], contract)

    def test_key_has_single_source_digest_field(self):
        key = self.build()
        self.assertEqual(set(key), set(c.KEY_FIELDS))
        self.assertIn("source_revision", key)
        self.assertNotIn("bundle_sha256", key)
        self.assertEqual(set(key["records"][0]), set(c.KEY_RECORD_FIELDS))

    def test_overwrite_is_refused_and_content_preserved(self):
        self.build()
        sentinel = self.root / "run" / "subjects" / "sentinel"
        sentinel.write_text("unchanged", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            c.build(self.bundle, self.root / "run", salt="b" * 64)
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "unchanged")

    def test_missing_parent_is_not_created(self):
        with self.assertRaises(ValueError):
            c.build(self.bundle, self.root / "missing" / "run")
        self.assertFalse((self.root / "missing").exists())

    def test_symlink_output_is_rejected(self):
        target = self.root / "target"
        target.mkdir()
        link = self.root / "link"
        link.symlink_to(target, target_is_directory=True)
        with self.assertRaises(ValueError):
            c.build(self.bundle, link / "child")
        self.assertEqual(list(target.iterdir()), [])

    def _copy_run(self, name):
        source = self.root / "run"
        c.build(self.bundle, source, salt="a" * 64)
        clone = self.root / name
        clone.mkdir()
        for part in ("subjects", "reviewers", "audit"):
            (clone / part).mkdir()
            for item in (source / part).iterdir():
                (clone / part / item.name).write_bytes(item.read_bytes())
        return clone

    def test_missing_input_is_rejected(self):
        clone = self._copy_run("missing")
        next((clone / "subjects").iterdir()).unlink()
        with self.assertRaises(ValueError):
            c.verify(clone, self.bundle)

    def test_extra_input_is_rejected(self):
        clone = self._copy_run("extra")
        (clone / "subjects" / ("f" * 24 + ".json")).write_text("{}", encoding="utf-8")
        with self.assertRaises(ValueError):
            c.verify(clone, self.bundle)

    def test_tampered_input_is_rejected(self):
        clone = self._copy_run("tampered")
        victim = next((clone / "subjects").iterdir())
        data = json.loads(victim.read_text(encoding="utf-8"))
        data["context"] = "tampered context"
        victim.write_text(json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                          encoding="utf-8")
        with self.assertRaises(ValueError):
            c.verify(clone, self.bundle)

    def test_self_consistent_reseal_is_still_rejected(self):
        # Rewrite a subject and re-seal its stored hash in the key; verify must
        # still reject it because the bytes differ from the intended projection.
        clone = self._copy_run("resealed")
        victim = next((clone / "subjects").iterdir())
        data = json.loads(victim.read_text(encoding="utf-8"))
        data["current"]["text"] = "edited but internally re-hashed"
        raw = (json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
        victim.write_bytes(raw)
        key_path = clone / "audit" / "preparation-key.json"
        key = json.loads(key_path.read_text(encoding="utf-8"))
        for record in key["records"]:
            if record["packet_id"] == victim.stem:
                record["subject_sha256"] = c.digest(raw)
        key_path.write_text(json.dumps(key, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                            encoding="utf-8")
        with self.assertRaises(ValueError):
            c.verify(clone, self.bundle)

    def test_tampered_key_rejected(self):
        clone = self._copy_run("keyed")
        key_path = clone / "audit" / "preparation-key.json"
        key = json.loads(key_path.read_text(encoding="utf-8"))
        key["records"][0]["condition"] = "scripted-native"
        key_path.write_text(json.dumps(key, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                            encoding="utf-8")
        with self.assertRaises(ValueError):
            c.verify(clone, self.bundle)

    def test_key_carries_authoring_review_contract_and_rejects_tampering(self):
        clone = self._copy_run("contract")
        key_path = clone / "audit" / "preparation-key.json"
        key = json.loads(key_path.read_text(encoding="utf-8"))
        probe = c.the_family(self.bundle)["variants"][0]["probes"][0]
        self.assertEqual(key["records"][0]["authoring_review_contract"], probe["review"])
        key["records"][0]["authoring_review_contract"]["hinge_value"] = "tampered"
        key_path.write_text(json.dumps(key, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                            encoding="utf-8")
        with self.assertRaises(ValueError):
            c.verify(clone, self.bundle)

    def test_reviewer_packet_rejects_non_null_response(self):
        clone = self._copy_run("answered")
        victim = next((clone / "reviewers").iterdir())
        data = json.loads(victim.read_text(encoding="utf-8"))
        data["response"] = "an answer"
        victim.write_text(json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                          encoding="utf-8")
        with self.assertRaises(ValueError):
            c.verify(clone, self.bundle)

    def test_reviewer_packet_rejects_changed_review_status(self):
        clone = self._copy_run("status")
        victim = next((clone / "reviewers").iterdir())
        data = json.loads(victim.read_text(encoding="utf-8"))
        data["review_status"] = "completed"
        victim.write_text(json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                          encoding="utf-8")
        with self.assertRaises(ValueError):
            c.verify(clone, self.bundle)

    def test_stored_revision_tamper_is_identified(self):
        clone = self._copy_run("revision")
        key_path = clone / "audit" / "preparation-key.json"
        key = json.loads(key_path.read_text(encoding="utf-8"))
        key["source_revision"] = "0" * 64
        key_path.write_text(json.dumps(key, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                            encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "source revision mismatch"):
            c.verify(clone, self.bundle)

    def test_real_source_revision_change_is_named_before_generic_errors(self):
        # A bundle built from the original source then verified against a valid
        # changed source must report the source revision mismatch, not a per-input
        # hash/byte error, even though inputs would also differ.
        clone = self._copy_run("sourcechange")
        changed = json.loads(json.dumps(self.bundle))
        changed["families"][0]["variants"][0]["history"][3]["text"] = "changed body text"
        self.assertNotEqual(c.source_revision(changed), c.source_revision(self.bundle))
        with self.assertRaisesRegex(ValueError, "source revision mismatch"):
            c.verify(clone, changed)

    def test_verify_is_bound_to_current_source_not_only_stored_hashes(self):
        # A bundle built from a different source cannot pass verification against
        # this bundled source even if its own stored hashes are self-consistent.
        other = json.loads(json.dumps(self.bundle))
        other["families"][0]["variants"][0]["history"][1]["role"] = "user"
        with tempfile.TemporaryDirectory() as raw:
            out = Path(raw).resolve() / "other"
            c.build(other, out, salt="c" * 64)
            with self.assertRaises(ValueError):
                c.verify(out, self.bundle)


class CliTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()

    def tearDown(self):
        self.temp.cleanup()

    def test_build_then_verify_commands(self):
        out = self.root / "run"
        self.assertEqual(quiet_main(["build", "--out", str(out)]), 0)
        self.assertEqual(quiet_main(["verify", str(out)]), 0)

    def test_wrong_command_errors_nonzero(self):
        with self.assertRaises(SystemExit) as exit_state:
            c.main(["nonsense"])
        self.assertNotEqual(exit_state.exception.code, 0)

    def test_build_without_out_errors_nonzero(self):
        with self.assertRaises(SystemExit) as exit_state:
            c.main(["build"])
        self.assertNotEqual(exit_state.exception.code, 0)

    def test_missing_directory_and_overwrite_are_clean_nonzero(self):
        self.assertEqual(quiet_main(["verify", str(self.root / "nope")]), 1)
        out = self.root / "run"
        self.assertEqual(quiet_main(["build", "--out", str(out)]), 0)
        self.assertEqual(quiet_main(["build", "--out", str(out)]), 1)

    def test_audit_out_is_new_file_only(self):
        report = self.root / "audit.json"
        self.assertEqual(quiet_main(["audit", "--out", str(report)]), 0)
        self.assertTrue(report.is_file())
        self.assertEqual(quiet_main(["audit", "--out", str(report)]), 1)
        self.assertEqual(quiet_main(["audit", "--out", str(self.root / "missing" / "a.json")]), 1)


if __name__ == "__main__":
    unittest.main()
