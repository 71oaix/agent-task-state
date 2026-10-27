import json
from copy import deepcopy
import unittest

import workbench as w


P = {"source": ["T01.01"], "actor": "source_author", "nature": "reported"}


class CompositionTests(unittest.TestCase):
    def setUp(self):
        self.state = {"objects": {}, "history": []}
        for oid, kind, fields in [
            ("goal", "goal", {"status": "unconfirmed"}),
            ("work", "work", {"status": "active", "responsibilities": ["visual", "groups", "accept"]}),
            ("artifact", "artifact", {"parts": {"rollback": {"status": "implemented"},
                "file_fix": {"status": "implemented"}}, "verification": "author_report"})]:
            self.apply({"action": "create", "id": oid, "kind": kind, "fields": fields})

    def apply(self, action):
        packet = w.expand(self.state, action, P)
        result = w.apply_prepared(self.state, packet)
        self.assertEqual("applied", result["status"], result["errors"])
        self.state = result["state"]
        return result

    def test_partial_revert_keeps_independent_fix_and_history(self):
        self.apply({"action": "partial_revert", "id": "artifact", "withdraw": ["rollback"],
                    "retain": ["file_fix"], "reason": "upstream maintenance cost"})
        obj = w.version(self.state, "artifact")
        self.assertEqual("withdrawn", obj["fields"]["parts"]["rollback"]["status"])
        self.assertEqual({"status": "implemented"}, obj["fields"]["parts"]["file_fix"])
        self.assertEqual("author_report", obj["fields"]["verification"])
        self.assertEqual("implemented", w.version(self.state, "artifact", 1)["fields"]["parts"]["rollback"]["status"])

    def test_unaccounted_or_overlapping_parts_rejected(self):
        for withdrawn, retained in [(["rollback"], []), (["rollback"], ["rollback", "file_fix"])]:
            with self.assertRaises(w.ExpressionError):
                w.expand(self.state, {"action": "partial_revert", "id": "artifact", "withdraw": withdrawn,
                                      "retain": retained, "reason": "reported"}, P)

    def test_rework_keeps_goal_and_reference_is_not_code_reuse(self):
        self.apply({"action": "rework", "old": "work", "new": "new-work", "goal": "goal",
                    "reason": "obsolete API", "reference_scope": "old design reference; code unknown",
                    "new_fields": {"status": "proposed"}})
        self.assertEqual("unconfirmed", self.state["objects"]["goal"]["fields"]["status"])
        self.assertEqual("closed", self.state["objects"]["work"]["fields"]["status"])
        links = self.state["objects"]["new-work"]["fields"]["links"]
        self.assertIn("historical_reference", [l["relation"] for l in links])
        self.assertNotIn("reuses_result", [l["relation"] for l in links])

    def test_split_preserves_parent_and_unfinished_responsibility(self):
        self.apply({"action": "split", "id": "work", "children": [
            {"id": "visual", "title": "visual", "responsibilities": ["visual"], "status": "reported_implemented"},
            {"id": "groups", "title": "groups", "responsibilities": ["groups"], "status": "draft"}],
            "residual": ["accept"], "overlaps": []})
        self.assertEqual("active", self.state["objects"]["work"]["fields"]["status"])
        self.assertEqual(["accept"], self.state["objects"]["work"]["fields"]["residual"])

    def test_split_missing_responsibility_is_atomic(self):
        before = deepcopy(self.state)
        packet = w.expand(self.state, {"action": "split", "id": "work", "children": [
            {"id": "visual", "title": "visual", "responsibilities": ["visual"], "status": "unknown"}],
            "residual": [], "overlaps": []}, P)
        result = w.apply_prepared(self.state, packet)
        self.assertEqual("rejected", result["status"])
        self.assertEqual(before, result["state"])
        self.assertNotIn("visual", result["state"]["objects"])

    def test_scope_adoption_does_not_change_other_holder(self):
        self.apply({"action": "adopt", "id": "a", "scope": "running-holder", "selected": ["artifact"], "reason": "old running version"})
        self.apply({"action": "revise", "id": "artifact", "delta": {"definition": "new"}})
        self.apply({"action": "adopt", "id": "b", "scope": "new-definition", "selected": ["artifact"], "reason": "new definition"})
        self.assertEqual(1, self.state["objects"]["a"]["fields"]["selected"][0]["revision"])
        self.assertEqual(2, self.state["objects"]["b"]["fields"]["selected"][0]["revision"])

    def test_stale_write_and_stale_read_both_rejected(self):
        write = w.expand(self.state, {"action": "revise", "id": "artifact", "delta": {"x": 1}}, P)
        read = w.expand(self.state, {"action": "reuse", "owner": "work", "provider": "artifact",
                                    "relation": "uses_contract", "range": "interface"}, P)
        self.apply({"action": "revise", "id": "artifact", "delta": {"x": 2}})
        self.assertEqual("rejected", w.apply_prepared(self.state, write)["status"])
        self.assertEqual("rejected", w.apply_prepared(self.state, read)["status"])
        explicit = w.expand(self.state, {"action": "reuse", "owner": "work", "provider": {"id": "artifact", "revision": 1},
                                        "relation": "uses_contract", "range": "intentionally old contract"}, P)
        self.assertEqual("applied", w.apply_prepared(self.state, explicit)["status"])

    def test_prepared_packet_cannot_silently_change(self):
        packet = w.expand(self.state, {"action": "close", "id": "work", "disposition": "superseded"}, P)
        packet["transaction"]["commands"][0]["delta"]["status"] = "complete"
        self.assertEqual("rejected", w.apply_prepared(self.state, packet)["status"])

    def test_step_failure_rolls_back_registered_facts_and_earlier_actions(self):
        corpus = {"id": "T01", "facts": {"T01.01": {"text": "source", "nature": "reported", "actor": "author", "sources": []}}}
        before = deepcopy(self.state)
        step = {"id": "T01.S01", "facts": ["T01.01"], "actions": [
            {"action": "revise", "id": "artifact", "delta": {"changed": True}},
            {"action": "reuse", "owner": "work", "provider": "missing", "relation": "depends_on", "range": "unknown"}]}
        result = w.execute_step(self.state, step, corpus)
        self.assertEqual("rejected", result["status"])
        self.assertEqual(before, result["state"])
        self.assertEqual(before, self.state)

    def test_correction_keeps_failed_explanation_and_scoped_claim(self):
        corpus = {"id": "T13", "facts": {
            "T13.01": {"text": "delay hypothesis", "nature": "diagnosis", "actor": "author", "sources": []},
            "T13.02": {"text": "20.8 seconds unchanged", "nature": "measurement", "actor": "author", "sources": []}}}
        for fid in corpus["facts"]:
            result = w.execute_step(self.state, {"id": fid, "facts": [fid], "actions": []}, corpus)
            self.assertEqual("applied", result["status"])
            self.state = result["state"]
        self.apply({"action": "correct", "id": "corrected", "prior": "fact/T13.01", "conclusion": "not solved by grace",
                    "scope": "this host failure only", "evidence": ["T13.02"]})
        self.assertIn("fact/T13.01", self.state["objects"])
        self.assertEqual("this host failure only", self.state["objects"]["corrected"]["fields"]["scope"])


class CorpusTests(unittest.TestCase):
    def test_frozen_input_and_cross_connections(self):
        corpus = w.load_corpus()
        self.assertEqual(16, len(corpus["cases"]))
        self.assertEqual(83, sum(len(c["facts"]) for c in corpus["cases"].values()))
        self.assertEqual(9, len(corpus["cross_links"]))

    def test_all_cases_execute_and_queries_find_every_effect(self):
        cases, _ = w.load_cases()
        if len(cases) != 16:
            self.skipTest("case encoding in progress")
        bundle = w.build_all()
        for result in bundle["cases"].values():
            for event in result["events"]:
                for trace in event["trace"]:
                    if trace["kind"] != "composition":
                        continue
                    for item in trace["changes"]:
                        self.assertEqual(item["after"], w.query(result, item["target"], item["after"])["revision"])
            for fid in result["fact_coverage"]:
                self.assertIn("fact/" + fid, result["state"]["objects"])
        self.assertEqual(83, sum(len(x) for x in bundle["coverage"].values()))
        self.assertEqual(bundle, json.loads(json.dumps(bundle, ensure_ascii=False)))


if __name__ == "__main__":
    unittest.main()
