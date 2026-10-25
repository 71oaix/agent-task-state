import unittest
from copy import deepcopy

from checker import apply_transaction, export_projection, replay, resolve_adoptions


P = {"source": "synthetic:1", "actor": "fixture", "nature": "asserted"}


def obj(kind="work", **fields):
    return {"kind": kind, "revision": 1, "fields": fields}


def ref(oid, revision=1):
    return {"id": oid, "revision": revision}


def tx(*commands, **extra):
    return {"commands": list(commands), "provenance": P, **extra}


def cmd(op, target, **extra):
    return {"op": op, "target": target, **extra}


class CheckerTests(unittest.TestCase):
    def test_statement_scope_can_be_revised_without_overwriting_history(self):
        state = {"objects": {"j": obj("statement", type="judgment", conclusion="limited inference",
                 evidence=["source-1"], scope="first visible report")}, "history": []}
        out = apply_transaction(state, tx(cmd("statement", "unused", fields={
            "type": "observation", "subject": "case", "result": "new evidence"})), {"unused": "absent"})
        revised = apply_transaction(out["state"], tx(cmd("revise", "j", delta={
            "scope": "updated visible reports"})), {"j": 1})
        self.assertEqual(revised["status"], "applied")
        self.assertEqual(revised["state"]["objects"]["j"]["fields"]["scope"], "updated visible reports")
        self.assertEqual(revised["state"]["history"][-1]["fields"]["scope"], "first visible report")

    def setUp(self):
        self.state = {"objects": {"parent": obj(status="open", label="keep"),
                                  "child": obj(status="open", parent="parent")}, "history": []}

    def test_close_preserves_fields_parent_and_original(self):
        before = deepcopy(self.state)
        result = apply_transaction(self.state, tx(cmd("close", "child", delta={"status": "closed"})), {"child": 1})
        self.assertEqual(result["status"], "applied")
        self.assertEqual(self.state, before)
        self.assertEqual(result["state"]["objects"]["parent"], before["objects"]["parent"])
        self.assertEqual(result["state"]["objects"]["child"]["fields"]["parent"], "parent")
        self.assertEqual(result["state"]["history"][0], {"id": "child", **before["objects"]["child"]})

    def test_stale_missing_and_bool_bases(self):
        for expected in ({"child": 2}, {}, {"child": True}):
            r = apply_transaction(self.state, tx(cmd("revise", "child", delta={"label": "x"})), expected)
            self.assertEqual(r["status"], "rejected")
            self.assertEqual(r["state"], self.state)

    def test_type_and_effect_failures(self):
        bad = [cmd("open", "new", kind="unknown", fields={}),
               cmd("close", "child", delta={"status": "closed", "parent_status": "closed"}),
               cmd("revise", "child", delta={}, side_effects={"parent": "closed"}),
               cmd("amend", "child", kind="report", delta={}),
               cmd("inline_link", "child", delta={"status": "closed"}),
               cmd("amend", "child", delta={"status": "closed", "parent": "another"})]
        for c in bad:
            r = apply_transaction(self.state, tx(c), {c["target"]: "absent" if c["target"] == "new" else 1})
            self.assertEqual(r["status"], "rejected", c)

    def test_statement_types_and_provenance(self):
        for op, fields in (("observe", {"type": "observation", "subject": "child", "result": "seen"}),
                           ("judge", {"type": "judgment", "conclusion": "ready", "evidence": [ref("child")]})):
            r = apply_transaction(self.state, tx(cmd(op, "s", fields=fields)), {"s": "absent"})
            self.assertEqual(r["status"], "applied")
            self.assertEqual(r["state"]["objects"]["s"]["provenance"]["nature"], "asserted")
            self.assertEqual(apply_transaction(self.state, {"commands": [cmd(op, "s", fields=fields)]}, {"s": "absent"})["status"], "rejected")
        r = apply_transaction(self.state, tx(cmd("observe", "s", fields={"type": "judgment", "result": "x"})), {"s": "absent"})
        self.assertEqual(r["status"], "rejected")

    def test_group_new_refs_atomic_and_required_targets(self):
        commands = [cmd("open", "new", fields={"status": "open"}),
                    cmd("bind", "r", fields={"relation": "depends", "from": ref("child"), "to": ref("new"), "scope": "local"})]
        expected = {"new": "absent", "r": "absent"}
        self.assertEqual(apply_transaction(self.state, tx(*commands), expected)["status"], "applied")
        commands[1]["fields"]["to"]["revision"] = 2
        r = apply_transaction(self.state, tx(*commands), expected)
        self.assertEqual(r["status"], "rejected")
        self.assertEqual(r["state"], self.state)
        r = apply_transaction(self.state, tx(commands[0], required_targets=["new", "r"]), {"new": "absent"})
        self.assertEqual(r["errors"][0]["code"], "group")

    def test_exact_references_and_retained_version(self):
        r = apply_transaction(self.state, tx(cmd("revise", "child", delta={"label": "new"})), {"child": 1})
        base = r["state"]
        for target_ref, verdict in ((ref("child"), "applied"), (ref("child", 2), "applied"),
                                    (ref("child", 3), "rejected"), ({"id": "child"}, "rejected")):
            r = apply_transaction(base, tx(cmd("select", "a", fields={"scope": "local", "selected": target_ref})), {"a": "absent"})
            self.assertEqual(r["status"], verdict)
        r = apply_transaction(base, tx(cmd("revise", "child", delta={}, refs=[ref("missing")])), {"child": 2})
        self.assertEqual(r["status"], "rejected")

    def test_scope_cannot_silently_change(self):
        state = deepcopy(self.state)
        state["objects"]["a"] = obj("adoption", scope="local", selected=ref("child"))
        r = apply_transaction(state, tx(cmd("amend", "a", delta={"scope": "global"})), {"a": 1})
        self.assertEqual(r["errors"][0]["code"], "scope")

    def test_report_content_is_flexible(self):
        fields = {"novel_field": {"source_revision": 96}, "text": "opaque", "status": "draft"}
        r = apply_transaction(self.state, tx(cmd("create", "report", kind="report", fields=fields)), {"report": "absent"})
        self.assertEqual(r["status"], "applied")
        self.assertEqual(r["state"]["objects"]["report"]["fields"], fields)

    def test_explicit_kind_aliases_and_decision_update(self):
        r = apply_transaction(self.state, tx(cmd("observe", "s", kind="observation", fields={"subject": "x", "result": "seen"})), {"s": "absent"})
        self.assertEqual(r["status"], "applied")
        state = deepcopy(self.state)
        state["objects"]["a"] = obj("adoption", scope="local", selected=ref("child"))
        r = apply_transaction(state, tx(cmd("decision", "a", delta={"effective": True, "selected": ref("parent")})), {"a": 1})
        self.assertEqual(r["status"], "applied")
        self.assertEqual(r["state"]["objects"]["a"]["kind"], "adoption")

    def test_allocation_conservation_and_overlap(self):
        f = {"responsibilities": ["a", "b"], "allocations": [{"target": "child", "responsibilities": ["a"]}], "residual": ["b"]}
        c = cmd("revise", "parent", delta=f)
        self.assertEqual(apply_transaction(self.state, tx(c), {"parent": 1})["status"], "applied")
        f["residual"] = []
        self.assertEqual(apply_transaction(self.state, tx(c), {"parent": 1})["status"], "rejected")
        f["residual"] = ["a", "b"]
        self.assertEqual(apply_transaction(self.state, tx(c), {"parent": 1})["status"], "rejected")
        f["overlaps"] = ["a"]
        self.assertEqual(apply_transaction(self.state, tx(c), {"parent": 1})["status"], "applied")
        f["allocations"] = {"child": ["a"]}
        self.assertEqual(apply_transaction(self.state, tx(c), {"parent": 1})["status"], "applied")

    def test_semantic_generic_record_equality(self):
        semantic = tx(cmd("close", "child", delta={"status": "closed"}))
        generic = tx(cmd("amend", "child", delta={"status": "closed"}))
        self.assertEqual(apply_transaction(self.state, semantic, {"child": 1})["state"],
                         apply_transaction(self.state, generic, {"child": 1})["state"])

    def test_common_projection_and_deterministic_replay(self):
        relation = {"relation": "depends", "from": ref("child"), "to": ref("parent"), "scope": "local"}
        adoption = {"scope": "local", "selected": ref("child")}
        a = apply_transaction(self.state, tx(cmd("bind", "r", fields=relation), cmd("select", "a", fields=adoption)), {"r": "absent", "a": "absent"})
        b = apply_transaction(self.state, tx(cmd("inline_link", "parent", delta={"links": [relation]}), cmd("decision", "d", fields=adoption)), {"parent": 1, "d": "absent"})
        self.assertEqual(export_projection(a["state"]), export_projection(b["state"]))
        steps = [{"transaction": tx(cmd("close", "child", delta={"status": "closed"})), "expected": {"child": 1}},
                 {"transaction": tx(cmd("close", "child", delta={"status": "closed"})), "expected": {"child": 1}}]
        r = replay(self.state, steps)
        self.assertEqual([i["status"] for i in r["results"]], ["applied", "rejected"])
        self.assertEqual(r, replay(self.state, steps))

    def adoption_state(self):
        state = deepcopy(self.state)
        state["objects"]["adopt"] = obj("adoption", scope="local", selected=ref("parent"))
        return state

    def decision(self, target, prior, scope="local"):
        return cmd("decision", target, fields={"scope": scope, "selected": ref("child"),
                    "effective": True, "supersedes": prior})

    def test_append_decision_supersedes_seeded_adoption(self):
        state = self.adoption_state()
        r = apply_transaction(state, tx(self.decision("d", ref("adopt"))), {"d": "absent"})
        self.assertEqual(r["status"], "applied")
        self.assertEqual(r["state"]["objects"]["adopt"], state["objects"]["adopt"])
        resolved = resolve_adoptions(r["state"])
        self.assertEqual(resolved["errors"], [])
        self.assertEqual(resolved["scopes"]["local"], {"status": "resolved", "heads": [
            {"record": ref("d"), "selected": ref("child")}]})

    def test_forked_decision_log_is_conflict_not_last_write(self):
        state = self.adoption_state()
        r = apply_transaction(state, tx(self.decision("d1", ref("adopt")), self.decision("d2", ref("adopt"))),
                              {"d1": "absent", "d2": "absent"})
        self.assertEqual(r["status"], "applied")
        scope = resolve_adoptions(r["state"])["scopes"]["local"]
        self.assertEqual(scope["status"], "conflict")
        self.assertEqual([head["record"] for head in scope["heads"]], [ref("d1"), ref("d2")])
        reverse = deepcopy(r["state"])
        reverse["objects"] = dict(reversed(list(reverse["objects"].items())))
        self.assertEqual(resolve_adoptions(reverse), resolve_adoptions(r["state"]))

    def test_current_adoption_and_old_base_log_conflict(self):
        state = self.adoption_state()
        updated = apply_transaction(state, tx(cmd("select", "adopt", delta={"selected": ref("child")})), {"adopt": 1})
        r = apply_transaction(updated["state"], tx(self.decision("d", ref("adopt"))), {"d": "absent"})
        self.assertEqual(r["status"], "applied")
        scope = resolve_adoptions(r["state"])["scopes"]["local"]
        self.assertEqual(scope["status"], "conflict")
        self.assertEqual([h["record"] for h in scope["heads"]], [ref("adopt", 2), ref("d")])

    def test_invalid_decision_predecessors_reject_atomically(self):
        state = self.adoption_state()
        cases = [([self.decision("d", ref("adopt"), scope="other")], {"d": "absent"}, "scope"),
                 ([self.decision("d", ref("d"))], {"d": "absent"}, "cycle"),
                 ([self.decision("d1", ref("d2")), self.decision("d2", ref("d1"))],
                  {"d1": "absent", "d2": "absent"}, "cycle"),
                 ([self.decision("d", ref("missing"))], {"d": "absent"}, "reference"),
                 ([self.decision("d", ref("child"))], {"d": "absent"}, "reference")]
        for commands, expected, code in cases:
            r = apply_transaction(state, tx(*commands), expected)
            self.assertEqual(r["status"], "rejected", commands)
            self.assertEqual(r["errors"][0]["code"], code)
            self.assertEqual(r["state"], state)


if __name__ == "__main__":
    unittest.main()
