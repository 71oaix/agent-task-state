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

    def test_saved_step_detaches_from_inputs_and_keeps_original_source(self):
        corpus = {"id": "T01", "facts": {"T01.01": {"text": "original source", "nature": "reported",
            "actor": "author", "sources": [{"id": "S001", "url": "https://example.test/source"}]}}}
        step = {"id": "T01.S01", "facts": ["T01.01"], "actions": [
            {"action": "revise", "id": "fact/T01.01", "delta": {"result": "later interpretation"}}]}
        applied = w.execute_step(self.state, step, corpus)
        self.assertEqual("applied", applied["status"])
        result = {"id": "T01", "title": "history", "state": applied["state"],
                  "initial_state": self.state, "events": [{k: v for k, v in applied.items() if k != "state"}]}
        step["facts"].clear()
        corpus["facts"]["T01.01"]["sources"][0]["url"] = "changed-after-call"
        self.assertEqual(["T01.01"], result["events"][0]["facts"])
        self.assertEqual("https://example.test/source", result["events"][0]["trace"][0]["transaction"]["commands"][0]["fields"]["sources"][0]["url"])
        self.assertIn("original source", w.timeline_markdown(result))
        self.assertEqual(result["state"], w.state_at(result, "T01.S01"))

    def test_malformed_action_rejects_whole_step(self):
        corpus = {"id": "T01", "facts": {"T01.01": {"text": "source", "nature": "reported", "actor": "author", "sources": []}}}
        result = w.execute_step(self.state, {"id": "T01.S01", "facts": ["T01.01"], "actions": [None]}, corpus)
        self.assertEqual("rejected", result["status"])
        self.assertEqual(self.state, result["state"])

    def test_correction_keeps_failed_explanation_and_scoped_claim(self):
        corpus = {"id": "T13", "facts": {
            "T13.01": {"text": "delay hypothesis", "nature": "diagnosis", "actor": "author", "sources": []},
            "T13.02": {"text": "20.8 seconds unchanged", "nature": "measurement", "actor": "author", "sources": []}}}
        for fid in corpus["facts"]:
            result = w.execute_step(self.state, {"id": fid, "facts": [fid], "actions": []}, corpus)
            self.assertEqual("applied", result["status"])
            self.state = result["state"]
        with self.assertRaises(w.ExpressionError):
            w.expand(self.state, {"action": "correct", "id": "wrong", "prior": "fact/T13.01",
                "conclusion": "not solved", "scope": "this failure", "evidence": ["T13.02"]}, P)
        self.apply({"action": "statement", "id": "old-judgment", "fields": {"type": "judgment",
                    "conclusion": "delay hypothesis", "evidence": ["T13.01"], "domain": "development_judgment"}})
        self.apply({"action": "correct", "id": "corrected", "prior": "old-judgment", "conclusion": "not solved by grace",
                    "scope": "this host failure only", "evidence": ["T13.02"]})
        self.assertIn("fact/T13.01", self.state["objects"])
        self.assertEqual("this host failure only", self.state["objects"]["corrected"]["fields"]["scope"])
        self.assertEqual({"id": "old-judgment", "revision": 1}, self.state["objects"]["corrected"]["fields"]["links"][0]["to"])


class CorpusTests(unittest.TestCase):
    def case_result(self, cid):
        cases, _ = w.load_cases()
        if cid not in cases:
            self.skipTest("case encoding in progress")
        return w.run_case(cases[cid], w.load_corpus()["cases"][cid])

    def test_loader_decision_does_not_pretend_implementation_changed(self):
        result = self.case_result("T01")
        decided = w.state_at(result, "T01.S02")
        self.assertTrue(decided["objects"]["T01/loader"]["fields"]["transactional"])
        self.assertFalse(decided["objects"]["T01/loader"]["fields"]["planned_transactional"])
        landed = w.state_at(result, "T01.S04")
        self.assertEqual("reported_revert_landed", landed["objects"]["T01/loader"]["fields"]["implementation"])
        self.assertEqual("reverted_nontransactional", landed["objects"]["T01/work"]["fields"]["implementation"])
        retained = w.state_at(result, "T01.S03")["objects"]["T01/attempt"]["fields"]["parts"]
        self.assertEqual("withdrawn", retained["transactional_reload"]["status"])
        self.assertEqual("reported_retained", retained["file_init_patch"]["status"])

    def test_query_and_readback_cannot_mutate_saved_state(self):
        result = self.case_result("T01")
        before = deepcopy(result)
        view = w.query(result)
        view["objects"][0]["fields"]["status"] = "changed_by_reader"
        scope = w.query(result, scope="T01/documented_loader_policy_at_cutoff")
        scope["heads"][0]["selected"][0]["revision"] = 999
        readback = w.readback_view(result)
        readback["steps"][0]["facts"].clear()
        readback["steps"][0]["effects"][0]["action"]["action"] = "changed_by_reader"
        self.assertEqual(before, result)

    def test_runtime_revision_is_not_previous_architecture(self):
        result = self.case_result("T02")
        legacy = result["state"]["objects"]["T02/legacy-revision"]["fields"]
        self.assertTrue(legacy["definition_ref"].startswith("unknown"))
        self.assertEqual("T02/preset-declarative", legacy["links"][0]["to"]["id"])
        self.assertEqual("uses_contract", legacy["links"][0]["relation"])
        self.assertEqual("recovery_failure", legacy["missing_definition"])
        self.assertTrue(all(v["fields"]["scope"].startswith("T02/") for v in result["state"]["objects"].values()
                            if v["kind"] == "adoption"))
        selected = w.query(result, scope="T02/documented_design")["record_views"][0]
        self.assertEqual(1, selected["snapshot"]["revision"])
        self.assertEqual(3, selected["latest_description"]["revision"])

    def test_unassigned_detail_is_not_inferred_from_later_source(self):
        result = self.case_result("T12")
        first = w.state_at(result, "T12.S01")
        self.assertNotEqual("reported_merged", first["objects"]["T12/pr"]["fields"]["status"])
        split = w.state_at(result, "T12.S03")["objects"]["T12/work"]["fields"]
        self.assertEqual(set(split["responsibilities"]), set(split["residual"]))
        self.assertTrue(all(not allocation for allocation in split["allocations"].values()))
        self.assertEqual("pending", result["state"]["objects"]["T12/grouping"]["fields"]["acceptance"])

    def test_ui_rework_retains_backend_without_asserting_code_reuse(self):
        result = self.case_result("T14")
        at_decision = w.state_at(result, "T14.S03")
        ui = at_decision["objects"]["T14/ui"]["fields"]
        self.assertTrue(ui["implementation"].startswith("unknown_at_decision"))
        self.assertEqual("closed", at_decision["objects"]["T14/old"]["fields"]["status"])
        relations = [l["relation"] for l in ui["links"]]
        self.assertIn("uses_contract", relations)
        self.assertIn("historical_reference", relations)
        self.assertNotIn("reuses_result", relations)

    def test_accepted_notification_limit_is_not_new_dedup_task(self):
        result = self.case_result("T08")
        objects = result["state"]["objects"]
        part = objects["T08/session-contract"]["fields"]["parts"]["one_shot_provider_path"]
        self.assertIn("unified_entry", part["status"])
        goal = objects["T08/goal"]["fields"]
        self.assertNotIn("notification_dedupe_decision", goal.get("remaining", []))
        self.assertIn("完成通知允许重复", goal["accepted_limits"])

    def test_shared_delivery_has_different_storage_guarantees(self):
        team = self.case_result("T04")["state"]["objects"]
        schedule = self.case_result("T06")["state"]["objects"]
        self.assertEqual("none", team["T04/outbox"]["fields"]["pending_delivery"])
        self.assertEqual("duplicate_delivery_possible", schedule["T06/delivery"]["fields"]["crash_effect"])
        self.assertEqual("unknown", schedule["T06/delivery"]["fields"]["model_completion"])
        self.assertEqual("retained", schedule["T06/history"]["fields"]["session_message_after_delete"])

    def test_storage_phases_have_identity_without_completing_parent(self):
        result = self.case_result("T03")
        objects = result["state"]["objects"]
        self.assertEqual("proposed", objects["T03/rebuild"]["fields"]["status"])
        self.assertEqual("draft", objects["T03/stage3"]["fields"]["proposal_status"])
        self.assertEqual("reported_implemented", objects["T03/stage3"]["fields"]["implementation"])
        self.assertEqual("incomplete", objects["T03/stage5"]["fields"]["status"])
        self.assertEqual("unknown", objects["T03/rebuild"]["fields"]["acceptance"])

    def test_terminal_correction_targets_proposition_not_report(self):
        result = self.case_result("T13")
        objects = result["state"]["objects"]
        judgment = objects["T13/judgment"]
        self.assertEqual({"id": "T13/early-judgment", "revision": 1}, judgment["fields"]["links"][0]["to"])
        self.assertEqual("source_record", objects["fact/T13.01"]["fields"]["domain"])
        self.assertEqual("judgment", objects["T13/early-judgment"]["fields"]["type"])
        self.assertIn({"id": "fact/T13.02", "revision": 1}, judgment["refs"])

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
            replayed = w.state_at(result, result["events"][-1]["step"])
            final_without_gap = deepcopy(result["state"])
            del final_without_gap["objects"]["fact/" + result["id"] + ".GAP"]
            self.assertEqual(final_without_gap, replayed)
            first = w.state_at(result, result["events"][0]["step"])
            future = set(result["fact_coverage"]) - set(result["events"][0]["facts"])
            self.assertTrue(all("fact/" + fid not in first["objects"] for fid in future))
        self.assertEqual(83, sum(len(x) for x in bundle["coverage"].values()))
        self.assertEqual(16, len(bundle["gap_coverage"]))
        relations = [v for v in bundle["state"]["objects"].values() if v["kind"] == "relation"]
        self.assertEqual(14, len(relations))
        self.assertTrue(all(v["refs"] for v in relations))
        self.assertTrue(all(v["status"] == "resolved" for v in w.resolve_adoptions(bundle["state"])["scopes"].values()))
        self.assertEqual(bundle, json.loads(json.dumps(bundle, ensure_ascii=False)))


if __name__ == "__main__":
    unittest.main()
