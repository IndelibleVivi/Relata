from copy import deepcopy
import io
import unittest
from unittest.mock import patch

from tools import future_question_inputs as study


class FutureQuestionWitnessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = study.read_json(study.HISTORIES)
        cls.contracts = study.read_json(study.CONTRACTS)
        cls.families = {f["id"]: f for f in cls.source["families"]}
        cls.report = study.audit(cls.source, cls.contracts)

    def cell(self, family, question="later", projection="retained", access="closed"):
        return next(c for c in self.report["cells"] if
                    (c["family"], c["question"], c["projection"], c["archive_access"]) ==
                    (family, question, projection, access))

    def test_recorded_result_is_exactly_reproducible(self):
        self.assertEqual(study.RESULT.read_bytes(), study.canonical(self.report))

    def view(self, family, world=0, question=0, projection="retained", access="closed"):
        f = self.families[family]
        return study.make_view(self.source["context"], f, f["worlds"][world],
                               f["questions"][question], projection, access)

    def test_same_retained_material_supports_present_but_collides_on_changed_question(self):
        for family in study.FAMILY_IDS:
            with self.subTest(family=family):
                self.assertFalse(any(g["incompatible_answer_contract"]
                                     for g in self.cell(family, "present")["groups"]))
                self.assertTrue(any(g["incompatible_answer_contract"]
                                    for g in self.cell(family, "later")["groups"]))
                before = self.view(family, question=0)
                after = self.view(family, question=1)
                self.assertEqual(before["memory"], after["memory"])
                self.assertEqual(before["archive_pointer"], after["archive_pointer"])

    def test_global_intersection_is_not_replaced_with_pairwise_overlap(self):
        group, = self.cell("G-GLOBAL-INTERSECTION")["groups"]
        self.assertEqual(group["worlds"], ["A", "B", "C"])
        self.assertTrue(group["pairwise_intersections_nonempty"])
        self.assertEqual(group["common_choices"], [])
        self.assertEqual(group["witness_kind"], "global-only")

    def test_common_appropriate_uncertainty_is_not_called_an_incompatibility(self):
        group, = self.cell("F-UNRESOLVED-ACCOUNTS", "cautious")["groups"]
        self.assertFalse(group["incompatible_answer_contract"])
        self.assertEqual(group["common_choices"], ["defer-attribution", "request-production-record"])

    def test_roles_ablation_really_erases_authorship_without_erasing_all_text(self):
        a = self.view("A-AUTHORSHIP", world=0, question=1, projection="roles-removed")
        b = self.view("A-AUTHORSHIP", world=1, question=1, projection="roles-removed")
        self.assertEqual(a, b)
        self.assertTrue(all(set(e) == {"scope", "text"} for e in a["memory"]))
        full_a = self.view("A-AUTHORSHIP", world=0, question=1, projection="full")
        full_b = self.view("A-AUTHORSHIP", world=1, question=1, projection="full")
        self.assertNotEqual(full_a, full_b)

    def test_source_resolution_appends_real_text_not_labels_or_success_flags(self):
        family = self.families["C-DISCARDED-RATIONALE"]
        for i, world in enumerate(family["worlds"]):
            view = self.view(family["id"], world=i, question=1, access="allowed")
            self.assertEqual(view["archive"]["events"], world["events"])
            self.assertEqual(set(view["archive"]), {"status", "events"})
        self.assertFalse(any(g["incompatible_answer_contract"]
                             for g in self.cell(family["id"], access="allowed")["groups"]))

    def test_missing_denied_and_stale_sources_do_not_fall_back_to_current_raw(self):
        family = self.families["E-MIGRATION-CAPABILITY"]
        missing = self.view(family["id"], question=1, access="missing")
        denied = self.view(family["id"], question=1, access="denied")
        stale = self.view(family["id"], question=1, access="stale")
        self.assertEqual(missing["archive"], {"status": "missing"})
        self.assertEqual(denied["archive"], {"status": "denied"})
        self.assertEqual(stale["archive"]["status"], "known-stale")
        self.assertEqual(stale["archive"]["events"], family["stale_archive"])
        self.assertNotEqual(stale["archive"]["events"], family["worlds"][0]["events"])
        for access in ("missing", "denied", "stale"):
            self.assertTrue(any(g["incompatible_answer_contract"]
                                for g in self.cell(family["id"], access=access)["groups"]))

    def test_pointer_existence_is_checked_by_resolver_and_does_not_reveal_denied_content(self):
        store = {"archive/one": [{"speaker": "user", "scope": "example", "text": "source"}]}
        self.assertEqual(study.resolve_archive("archive/other", store, {"archive/other"}, set()),
                         {"status": "missing"})
        self.assertEqual(study.resolve_archive("archive/one", store, set(), set()), {"status": "denied"})

    def test_world_ids_and_answer_regions_do_not_enter_source_views(self):
        family = deepcopy(self.families["A-AUTHORSHIP"])
        original = study.make_view(self.source["context"], family, family["worlds"][0],
                                   family["questions"][1], "retained", "allowed")
        family["worlds"][0]["id"] = "SECRET-CONTRACT-CANARY"
        changed = study.make_view(self.source["context"], family, family["worlds"][0],
                                  family["questions"][1], "retained", "allowed")
        self.assertEqual(original, changed)
        self.assertNotIn(b"SECRET-CONTRACT-CANARY", study.canonical(changed))
        self.assertEqual(set(changed), {"context", "current", "memory", "archive_pointer", "archive"})

    def test_source_show_path_does_not_load_contract_file(self):
        class Capture:
            def __init__(self):
                self.buffer = io.BytesIO()
        output = Capture()
        real_read = study.read_json
        def guarded_read(path):
            self.assertEqual(path, study.HISTORIES)
            return real_read(path)
        with patch.object(study, "read_json", guarded_read), patch.object(study.sys, "stdout", output):
            self.assertEqual(study.main(["show", "--family", "A-AUTHORSHIP"]), 0)
        self.assertNotIn(b"originator-companion", output.buffer.getvalue())

    def test_contract_injection_into_event_is_rejected(self):
        source = deepcopy(self.source)
        source["families"][0]["worlds"][0]["events"][0]["answer"] = "originator-companion"
        with self.assertRaisesRegex(ValueError, "event fields"):
            study.validate_histories(source)

    def test_unknown_or_empty_answer_region_is_rejected(self):
        for value in ([], ["unknown-decision"]):
            contracts = deepcopy(self.contracts)
            contracts["families"]["A-AUTHORSHIP"]["later"]["A"] = value
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "answer region"):
                study.validate_contracts(self.source, contracts)


if __name__ == "__main__":
    unittest.main()
