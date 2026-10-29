import unittest
from copy import deepcopy

import t12_responsibility as responsibility


LAYOUTS = ("parent", "relation", "child")
TOKENS = ("X", "Y")
HOLDERS = ("甲", "乙", "丙")
CURRENT = object()


def make(layout, tokens=TOKENS, holders=HOLDERS, unknown=True, scope_known=False):
    return responsibility.new(layout, list(tokens), list(holders),
                              unknown=unknown, scope_known=scope_known)


def act(op, token, **fields):
    return {"op": op, "token": token, **fields}


class ResponsibilityTests(unittest.TestCase):
    def applied(self, state, action, revision=CURRENT):
        revision = state["revision"] if revision is CURRENT else revision
        result = responsibility.apply(state, action, revision)
        self.assertEqual("applied", result["status"], result["error"])
        self.assertIsNone(result["error"])
        self.assertEqual(state["revision"] + 1, result["state"]["revision"])
        self.assertIsNot(result["state"], state)
        return result

    def rejected(self, state, action, revision=CURRENT):
        revision = state["revision"] if revision is CURRENT else revision
        before = deepcopy(state)
        result = responsibility.apply(state, action, revision)
        self.assertEqual("rejected", result["status"])
        self.assertTrue(result["error"])
        self.assertEqual([], result["changed_paths"])
        self.assertEqual(before, result["state"])
        self.assertIsNot(result["state"], state)
        self.assertEqual(before, state)
        return result

    def test_new_initial_modes_and_declared_scope(self):
        for layout in LAYOUTS:
            state = make(layout)
            self.assertEqual(0, state["revision"])
            self.assertEqual(layout, state["layout"])
            self.assertIs(False, state["scope_known"])
            view = responsibility.project(state)
            self.assertEqual(set(TOKENS), set(view))
            for token in TOKENS:
                self.assertEqual({"state": "unknown", "holders": []}, view[token])

            unassigned = responsibility.project(make(layout, unknown=False))
            for token in TOKENS:
                self.assertEqual({"state": "unassigned", "holders": []},
                                 unassigned[token])

            declared = make(layout, tokens=("only",), holders=(), scope_known=True)
            self.assertIs(True, declared["scope_known"])
            self.assertEqual({"only"}, set(responsibility.project(declared)))
            self.assertEqual({"state": "unknown", "holders": []},
                             responsibility.project(declared)["only"])

    def test_new_rejects_invalid_scope_and_flags(self):
        cases = [
            ("bogus", ["X"], ["甲"], {}),
            ("parent", ["X", "X"], ["甲"], {}),
            ("parent", [""], ["甲"], {}),
            ("parent", [1], ["甲"], {}),
            ("parent", ["X"], ["甲", "甲"], {}),
            ("parent", ["X"], [""], {}),
            ("parent", ["X"], [1], {}),
            ("parent", "X", ["甲"], {}),
            ("parent", ["X"], ["甲"], {"unknown": 1}),
            ("parent", ["X"], ["甲"], {"scope_known": 0}),
        ]
        for layout, tokens, holders, kwargs in cases:
            with self.assertRaises(ValueError):
                responsibility.new(layout, tokens, holders, **kwargs)

    def test_new_does_not_alias_input_sequences(self):
        tokens, holders = ["X"], ["甲"]
        state = responsibility.new("parent", tokens, holders)
        tokens.append("Y")
        holders.append("乙")
        view = responsibility.project(state)
        self.assertEqual({"X"}, set(view))
        self.assertEqual("unknown", view["X"]["state"])

    def test_each_layout_uses_a_different_authority_location(self):
        parent = make("parent")
        self.assertEqual({"revision", "layout", "scope_known", "parent"}, set(parent))
        self.assertEqual("unknown", parent["parent"]["records"]["X"]["state"])
        self.assertEqual([], parent["parent"]["records"]["X"]["holders"])
        self.assertNotIn("relation", parent)
        self.assertNotIn("child", parent)

        relation = make("relation")
        self.assertEqual({"revision", "layout", "scope_known", "relation"}, set(relation))
        record = relation["relation"]["relations"]["X"]
        self.assertTrue(record["id"])
        self.assertEqual(0, record["version"])
        self.assertEqual("unknown", record["state"])
        self.assertNotIn("parent", relation)
        self.assertNotIn("child", relation)

        child = make("child")
        self.assertEqual({"revision", "layout", "scope_known", "child"}, set(child))
        self.assertEqual({"X": "unknown", "Y": "unknown"}, child["child"]["modes"])
        self.assertEqual({"甲": [], "乙": [], "丙": []}, child["child"]["accepted"])
        for mode in child["child"]["modes"].values():
            self.assertIsInstance(mode, str)
        self.assertNotIn("parent", child)
        self.assertNotIn("relation", child)

        # No layout carries a universal current-ownership table.
        for state in (parent, relation, child):
            self.assertNotIn("assignments", state)
            self.assertNotIn("owners", state)
            self.assertNotIn("current", state)

    def test_assign_sequence_in_every_layout(self):
        for layout in LAYOUTS:
            state = make(layout)
            first = self.applied(state, act("assign", "X", to="甲"))
            self.assertTrue(first["changed_paths"])
            self.assertFalse(any("Y" in path for path in first["changed_paths"]))
            self.assertEqual({"state": "assigned", "holders": ["甲"]},
                             responsibility.project(first["state"])["X"])

            second = self.applied(first["state"], act("assign", "Y", to="乙"))
            self.assertEqual(2, second["state"]["revision"])
            view = responsibility.project(second["state"])
            self.assertEqual({"state": "assigned", "holders": ["甲"]}, view["X"])
            self.assertEqual({"state": "assigned", "holders": ["乙"]}, view["Y"])

            from_unassigned = self.applied(make(layout, unknown=False),
                                            act("assign", "X", to="甲"))
            self.assertEqual({"state": "assigned", "holders": ["甲"]},
                             responsibility.project(from_unassigned["state"])["X"])

    def test_transfer_moves_only_the_single_assignment(self):
        for layout in LAYOUTS:
            state = make(layout)
            state = self.applied(state, act("assign", "X", to="甲"))["state"]
            state = self.applied(state, act("assign", "Y", to="乙"))["state"]
            before = responsibility.project(state)
            result = self.applied(state, act("transfer", "X", **{"from": "甲", "to": "丙"}))
            after = responsibility.project(result["state"])
            self.assertEqual({"state": "assigned", "holders": ["丙"]}, after["X"])
            self.assertEqual(before["Y"], after["Y"])
            self.assertTrue(result["changed_paths"])
            self.assertFalse(any("Y" in path for path in result["changed_paths"]))

    def test_share_grows_roster_and_unassign_needs_exact_holders(self):
        for layout in LAYOUTS:
            from_unassigned = make(layout, unknown=False)
            opened = self.applied(from_unassigned,
                                  act("share", "X", holders=["甲", "乙"]))
            self.assertEqual({"state": "shared", "holders": sorted(["甲", "乙"])},
                             responsibility.project(opened["state"])["X"])

            state = make(layout)
            state = self.applied(state, act("share", "X", holders=["甲", "乙"]))["state"]
            view = responsibility.project(state)
            self.assertEqual("shared", view["X"]["state"])
            self.assertEqual(sorted(["甲", "乙"]), view["X"]["holders"])

            state = self.applied(state, act("share", "X", holders=["甲", "乙", "丙"]))["state"]
            view = responsibility.project(state)
            self.assertEqual("shared", view["X"]["state"])
            self.assertEqual(sorted(["甲", "乙", "丙"]), view["X"]["holders"])

            self.rejected(state, act("share", "X", holders=["甲", "乙"]))
            self.rejected(state, act("share", "X", holders=["甲"]))
            self.rejected(state, act("share", "X", holders=["甲", "甲", "乙"]))
            self.rejected(state, act("share", "X", holders=["甲", "乙", "丁"]))
            self.rejected(state, act("unassign", "X", **{"from": ["甲", "乙"]}))
            self.rejected(state, act("unassign", "X", **{"from": ["甲", "乙", "丙", "甲"]}))

            released = self.applied(state, act("unassign", "X",
                                                **{"from": ["丙", "甲", "乙"]}))
            self.assertEqual({"state": "unassigned", "holders": []},
                             responsibility.project(released["state"])["X"])

    def test_share_from_assigned_must_keep_original_holder(self):
        for layout in LAYOUTS:
            state = make(layout)
            state = self.applied(state, act("assign", "X", to="甲"))["state"]
            self.rejected(state, act("share", "X", holders=["乙", "丙"]))
            state = self.applied(state, act("share", "X", holders=["甲", "乙"]))["state"]
            self.assertEqual({"state": "shared", "holders": sorted(["甲", "乙"])},
                             responsibility.project(state)["X"])

    def test_unknown_differs_from_unassigned_and_cannot_erase_ownership(self):
        for layout in LAYOUTS:
            unknown = make(layout)
            unassigned = make(layout, unknown=False)
            self.assertEqual("unknown", responsibility.project(unknown)["X"]["state"])
            self.assertEqual("unassigned", responsibility.project(unassigned)["X"]["state"])
            self.assertNotEqual(responsibility.project(unknown)["X"],
                                responsibility.project(unassigned)["X"])

            changed = self.applied(unassigned, act("unknown", "X"))
            self.assertEqual({"state": "unknown", "holders": []},
                             responsibility.project(changed["state"])["X"])

            again = self.applied(unknown, act("unknown", "X"))
            self.assertEqual({"state": "unknown", "holders": []},
                             responsibility.project(again["state"])["X"])

            assigned = self.applied(unknown, act("assign", "X", to="甲"))["state"]
            self.rejected(assigned, act("unknown", "X"))

            shared = self.applied(unknown, act("share", "X",
                                               holders=["甲", "乙"]))["state"]
            self.rejected(shared, act("unknown", "X"))

    def test_stale_revisions_and_bad_expected_values_are_rejected(self):
        for layout in LAYOUTS:
            state = make(layout)
            self.rejected(state, act("assign", "X", to="甲"),
                          revision=state["revision"] + 1)
            current = self.applied(state, act("assign", "X", to="甲"))["state"]
            self.rejected(current, act("assign", "Y", to="乙"), revision=0)
            for revision in (True, False, 0.0, "1", None, ()):
                self.rejected(current, act("assign", "Y", to="乙"), revision=revision)

    def test_bad_tokens_holders_and_bypasses_are_rejected(self):
        for layout in LAYOUTS:
            state = make(layout)
            current = self.applied(state, act("assign", "X", to="甲"))["state"]
            bad_actions = [
                act("assign", "Q", to="甲"),
                act("assign", "X", to="丁"),
                act("assign", "X", to=True),
                act("assign", True, to="甲"),
                act("assign", "", to="甲"),
                act("assign", "X"),
                act("assign", "X", to="甲", note="extra"),
                act("transfer", "X"),
                act("transfer", "X", **{"from": "甲"}),
                act("transfer", "X", **{"from": ["甲"], "to": "乙"}),
                act("share", "X", holders="甲乙"),
                act("share", "X", holders=[]),
                act("unassign", "X"),
                act("unassign", "X", **{"from": "甲"}),
                act("unknown", "X", extra=True),
                act("revise", "X"),
                act("patch", "X"),
                {"op": "assign", "token": "X", "to": "甲", "expected": 1},
                {},
                [],
                None,
            ]
            for action in bad_actions:
                self.rejected(current, action)

    def test_preemption_and_illegal_transfers_are_rejected(self):
        for layout in LAYOUTS:
            assigned = self.applied(make(layout), act("assign", "X", to="甲"))["state"]
            self.rejected(assigned, act("assign", "X", to="乙"))
            self.rejected(assigned, act("assign", "X", to="甲"))

            shared = self.applied(assigned, act("share", "X",
                                                holders=["甲", "乙"]))["state"]
            self.rejected(shared, act("assign", "X", to="丙"))
            self.rejected(shared, act("transfer", "X", **{"from": "甲", "to": "丙"}))

            self.rejected(assigned, act("transfer", "X", **{"from": "乙", "to": "丙"}))
            self.rejected(assigned, act("transfer", "X", **{"from": "甲", "to": "甲"}))
            self.rejected(make(layout),
                          act("transfer", "X", **{"from": "甲", "to": "乙"}))

            self.rejected(assigned, act("unassign", "X", **{"from": ["甲", "乙"]}))
            self.rejected(shared, act("unassign", "X", **{"from": ["甲"]}))
            self.rejected(shared, act("unassign", "X", **{"from": ["甲", "丙"]}))
            self.rejected(shared, act("unassign", "X",
                                     **{"from": ["甲", "乙", "丙"]}))

    def test_results_and_projection_are_detached_copies(self):
        for layout in LAYOUTS:
            state = make(layout)
            before = deepcopy(state)
            view = responsibility.project(state)
            view["X"]["state"] = "shared"
            view["X"]["holders"].append("甲")
            view.pop("Y")
            self.assertEqual(before, state)

            result = self.applied(state, act("assign", "X", to="甲"))
            result["state"]["revision"] = 99
            self.assertEqual(0, state["revision"])

            rejected = self.rejected(state, act("assign", "Q", to="甲"))
            rejected["state"]["revision"] = 99
            self.assertEqual(0, state["revision"])

    def test_relation_version_and_stable_id_track_only_that_token(self):
        state = make("relation")
        records = state["relation"]["relations"]
        ids = {token: records[token]["id"] for token in TOKENS}
        self.assertEqual({"X": 0, "Y": 0},
                         {token: records[token]["version"] for token in TOKENS})

        state = self.applied(state, act("assign", "X", to="甲"))["state"]
        self.assertEqual(1, state["relation"]["relations"]["X"]["version"])
        self.assertEqual(0, state["relation"]["relations"]["Y"]["version"])

        state = self.applied(state, act("assign", "Y", to="乙"))["state"]
        self.assertEqual(1, state["relation"]["relations"]["X"]["version"])
        self.assertEqual(1, state["relation"]["relations"]["Y"]["version"])

        state = self.applied(state, act("transfer", "X",
                                        **{"from": "甲", "to": "乙"}))["state"]
        self.assertEqual(2, state["relation"]["relations"]["X"]["version"])
        self.assertEqual(1, state["relation"]["relations"]["Y"]["version"])

        result = self.applied(state, act("share", "X", holders=["乙", "丙"]))
        state = result["state"]
        self.assertEqual(3, state["relation"]["relations"]["X"]["version"])
        self.assertEqual(1, state["relation"]["relations"]["Y"]["version"])
        self.assertIn("relation.relations.X.version", result["changed_paths"])
        self.assertEqual(ids, {token: state["relation"]["relations"][token]["id"]
                               for token in TOKENS})

        state = self.applied(state, act("share", "X",
                                        holders=["乙", "丙", "甲"]))["state"]
        self.assertEqual(4, state["relation"]["relations"]["X"]["version"])
        self.assertEqual(1, state["relation"]["relations"]["Y"]["version"])

    def test_child_layout_keeps_authority_in_each_holder(self):
        state = make("child")
        state = self.applied(state, act("assign", "X", to="甲"))["state"]
        state = self.applied(state, act("assign", "Y", to="乙"))["state"]
        child = state["child"]
        self.assertEqual({"X": "assigned", "Y": "assigned"}, child["modes"])
        self.assertEqual(["X"], child["accepted"]["甲"])
        self.assertEqual(["Y"], child["accepted"]["乙"])
        self.assertEqual([], child["accepted"]["丙"])
        for mode in child["modes"].values():
            self.assertNotIsInstance(mode, (list, dict))

        state = self.applied(state, act("share", "X", holders=["甲", "乙"]))["state"]
        child = state["child"]
        self.assertEqual("shared", child["modes"]["X"])
        self.assertEqual(["X"], child["accepted"]["甲"])
        self.assertEqual(["X", "Y"], child["accepted"]["乙"])
        view = responsibility.project(state)
        self.assertEqual("shared", view["X"]["state"])
        self.assertEqual(sorted(["甲", "乙"]), view["X"]["holders"])

        state = self.applied(state, act("transfer", "Y",
                                        **{"from": "乙", "to": "丙"}))["state"]
        child = state["child"]
        self.assertEqual(["X"], child["accepted"]["甲"])
        self.assertEqual(["X"], child["accepted"]["乙"])
        self.assertEqual(["Y"], child["accepted"]["丙"])

        before = deepcopy(state)
        responsibility.project(state)
        self.assertEqual(before, state)

    def test_changed_paths_describe_each_layout_storage(self):
        parent = self.applied(make("parent"), act("assign", "X", to="甲"))
        self.assertIn("parent.records.X.state", parent["changed_paths"])
        self.assertIn("parent.records.X.holders", parent["changed_paths"])

        relation = self.applied(make("relation"), act("assign", "X", to="甲"))
        self.assertIn("relation.relations.X.state", relation["changed_paths"])
        self.assertIn("relation.relations.X.holders", relation["changed_paths"])
        self.assertIn("relation.relations.X.version", relation["changed_paths"])

        child = self.applied(make("child"), act("assign", "X", to="甲"))
        self.assertIn("child.modes.X", child["changed_paths"])
        self.assertIn("child.accepted.甲", child["changed_paths"])

        for result in (parent, relation, child):
            self.assertTrue(result["changed_paths"])
            self.assertFalse(any(path.split(".")[-1] == "revision"
                                 for path in result["changed_paths"]))

    def test_one_token_transition_keeps_other_tokens_exactly(self):
        for layout in LAYOUTS:
            state = make(layout)
            state = self.applied(state, act("assign", "X", to="甲"))["state"]
            state = self.applied(state, act("assign", "Y", to="乙"))["state"]
            before = responsibility.project(state)
            result = self.applied(state, act("transfer", "X",
                                             **{"from": "甲", "to": "丙"}))
            after = responsibility.project(result["state"])
            self.assertEqual(before["Y"], after["Y"])
            self.assertNotEqual(before["X"], after["X"])
            self.assertTrue(result["changed_paths"])
            self.assertFalse(any("Y" in path for path in result["changed_paths"]))
            self.assertFalse(any(path.split(".")[-1] == "revision"
                                 for path in result["changed_paths"]))

    def test_long_legal_path_in_every_layout(self):
        steps = [
            act("assign", "X", to="甲"),
            act("assign", "Y", to="乙"),
            act("transfer", "X", **{"from": "甲", "to": "乙"}),
            act("share", "X", holders=["乙", "丙"]),
            act("unassign", "Y", **{"from": ["乙"]}),
            act("unknown", "Y"),
            act("assign", "Y", to="丙"),
        ]
        for layout in LAYOUTS:
            original = make(layout)
            state = original
            for step in steps:
                state = self.applied(state, step)["state"]
            self.assertEqual(len(steps), state["revision"])
            view = responsibility.project(state)
            self.assertEqual("shared", view["X"]["state"])
            self.assertEqual(sorted(["乙", "丙"]), view["X"]["holders"])
            self.assertEqual("assigned", view["Y"]["state"])
            self.assertEqual(["丙"], view["Y"]["holders"])
            self.assertEqual(original, make(layout))
            self.assertEqual(0, original["revision"])

    def test_scope_known_does_not_infer_parent_completion(self):
        for layout in LAYOUTS:
            state = make(layout)
            state = self.applied(state, act("assign", "X", to="甲"))["state"]
            state = self.applied(state, act("assign", "Y", to="乙"))["state"]
            self.assertIs(False, state["scope_known"])
            view = responsibility.project(state)
            self.assertEqual(set(TOKENS), set(view))
            self.assertEqual("assigned", view["X"]["state"])
            self.assertEqual("assigned", view["Y"]["state"])
            self.assertNotIn("done", state)
            self.assertNotIn("complete", state)

            declared = make(layout, tokens=("X",), scope_known=True)
            self.assertIs(True, declared["scope_known"])
            self.assertEqual({"X"}, set(responsibility.project(declared)))


if __name__ == "__main__":
    unittest.main()
