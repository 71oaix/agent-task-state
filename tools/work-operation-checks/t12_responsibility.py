"""Deterministic responsibility layout comparison (Python standard library only).

The same responsibility semantics are stored with one authoritative location per
layout:

* ``parent``   -- one parent allocation table maps ``token -> record``.
* ``relation`` -- one assignment relation per token with a stable id and a
                  per-token version.
* ``child``    -- every holder keeps its own accepted tokens; the root keeps
                  only the per-token ownership mode.  ``project`` derives the
                  holder list by scanning the children.

``project`` is a read-only view.  ``apply`` projects the current state, checks
one token transition, and then writes only the entries affected by the chosen
layout.  It never keeps a second, universal current-ownership table.

``scope_known`` records whether the caller declares the token scope complete.
It defaults to ``False``; even when every declared token is assigned, the module
does not infer that the parent work is complete from this token set.
"""

from copy import deepcopy


LAYOUTS = ("parent", "relation", "child")
MODES = ("unknown", "unassigned", "assigned", "shared")
ACTION_FIELDS = {
    "assign": frozenset({"op", "token", "to"}),
    "transfer": frozenset({"op", "token", "from", "to"}),
    "share": frozenset({"op", "token", "holders"}),
    "unassign": frozenset({"op", "token", "from"}),
    "unknown": frozenset({"op", "token"}),
}


class Invalid(ValueError):
    """Internal validation failure; ``apply`` turns it into a rejection."""


def _require(condition, message):
    if not condition:
        raise Invalid(message)


def _is_int(value):
    return isinstance(value, int) and not isinstance(value, bool)


def _names(value, label):
    _require(isinstance(value, (list, tuple)) and not isinstance(value, str),
             label + " must be a sequence of unique nonempty strings")
    items = list(value)
    _require(all(isinstance(item, str) and bool(item) for item in items),
             label + " must contain only nonempty strings")
    _require(len(set(items)) == len(items), label + " must not contain duplicates")
    return items


def new(layout, tokens, holders, unknown=True, scope_known=False):
    """Create revision 0 state for one layout.

    ``unknown`` selects the initial mode for every declared token: ``True``
    (the default) gives ``unknown``, ``False`` gives ``unassigned``.  Neither
    initial mode has a holder.  ``tokens`` only declares this project's visible
    range; it is not evidence that parent work is complete.
    """
    _require(isinstance(layout, str) and layout in LAYOUTS,
             "layout must be one of " + ", ".join(LAYOUTS))
    _require(isinstance(unknown, bool), "unknown must be a boolean")
    _require(isinstance(scope_known, bool), "scope_known must be a boolean")
    token_names = _names(tokens, "tokens")
    holder_names = _names(holders, "holders")
    initial = "unknown" if unknown else "unassigned"

    if layout == "parent":
        data = {
            "tokens": token_names,
            "holders": holder_names,
            "records": {
                token: {"state": initial, "holders": []}
                for token in token_names
            },
        }
    elif layout == "relation":
        data = {
            "tokens": token_names,
            "holders": holder_names,
            "relations": {
                token: {
                    "id": "relation:" + token,
                    "version": 0,
                    "state": initial,
                    "holders": [],
                }
                for token in token_names
            },
        }
    else:
        data = {
            "tokens": token_names,
            "holders": holder_names,
            "modes": {token: initial for token in token_names},
            "accepted": {holder: [] for holder in holder_names},
        }

    return {
        "revision": 0,
        "layout": layout,
        "scope_known": scope_known,
        layout: data,
    }


def _mode_and_holders(mode, holders, declared_holders, label):
    _require(isinstance(mode, str) and mode in MODES,
             label + " has an invalid ownership mode")
    _require(isinstance(holders, (list, tuple)) and not isinstance(holders, str),
             label + " holders must be a list")
    values = list(holders)
    _require(all(isinstance(holder, str) and bool(holder) for holder in values),
             label + " holders must be nonempty strings")
    _require(len(set(values)) == len(values),
             label + " holders must not contain duplicates")
    _require(set(values) <= set(declared_holders),
             label + " uses an undeclared holder")
    consistent = (
        (mode in ("unknown", "unassigned") and not values)
        or (mode == "assigned" and len(values) == 1)
        or (mode == "shared" and len(values) >= 2)
    )
    _require(consistent, label + " has inconsistent holders for mode " + mode)


def _validate_state(state):
    _require(isinstance(state, dict), "state must be an object")
    layout = state.get("layout")
    _require(isinstance(layout, str) and layout in LAYOUTS,
             "state layout must be one of " + ", ".join(LAYOUTS))
    _require(_is_int(state.get("revision")) and state["revision"] >= 0,
             "state revision must be a nonnegative integer")
    _require(isinstance(state.get("scope_known"), bool),
             "state scope_known must be a boolean")
    _require(isinstance(state.get(layout), dict), "state lacks " + layout + " data")
    data = state[layout]
    tokens = _names(data.get("tokens"), "state tokens")
    holders = _names(data.get("holders"), "state holders")

    if layout == "parent":
        records = data.get("records")
        _require(isinstance(records, dict), "parent records must be an object")
        _require(set(records) == set(tokens), "parent records must cover exactly the tokens")
        for token in tokens:
            record = records[token]
            _require(isinstance(record, dict) and set(record) == {"state", "holders"},
                     "parent record for " + token + " has invalid fields")
            _mode_and_holders(record["state"], record["holders"], holders,
                              "parent record for " + token)
    elif layout == "relation":
        relations = data.get("relations")
        _require(isinstance(relations, dict), "relation table must be an object")
        _require(set(relations) == set(tokens), "relation table must cover exactly the tokens")
        seen_ids = set()
        for token in tokens:
            record = relations[token]
            _require(isinstance(record, dict)
                     and set(record) == {"id", "version", "state", "holders"},
                     "relation record for " + token + " has invalid fields")
            relation_id = record["id"]
            _require(isinstance(relation_id, str) and bool(relation_id),
                     "relation id for " + token + " must be a nonempty string")
            _require(relation_id not in seen_ids, "relation ids must be unique")
            seen_ids.add(relation_id)
            _require(_is_int(record["version"]) and record["version"] >= 0,
                     "relation version for " + token + " must be a nonnegative integer")
            _mode_and_holders(record["state"], record["holders"], holders,
                              "relation record for " + token)
    else:
        modes = data.get("modes")
        accepted = data.get("accepted")
        _require(isinstance(modes, dict), "child modes must be an object")
        _require(set(modes) == set(tokens), "child modes must cover exactly the tokens")
        _require(isinstance(accepted, dict), "child accepted table must be an object")
        _require(set(accepted) == set(holders), "child accepted table must cover exactly the holders")
        token_set = set(tokens)
        accepted_sets = {}
        for holder in holders:
            accepted_tokens = _names(accepted[holder], "accepted tokens for " + holder)
            _require(set(accepted_tokens) <= token_set,
                     "holder " + holder + " accepts an undeclared token")
            accepted_sets[holder] = set(accepted_tokens)
        for token in tokens:
            owners = [holder for holder in holders if token in accepted_sets[holder]]
            _mode_and_holders(modes[token], owners, holders,
                              "child token " + token)


def _scope(state):
    data = state[state["layout"]]
    return data["tokens"], data["holders"]


def project(state):
    """Return a detached ``{token: {state, holders}}`` view.

    ``unknown`` and ``unassigned`` are distinct and both have an empty holder
    list.  ``assigned`` has exactly one holder and ``shared`` has at least two.
    For the child layout the holder lists are derived by scanning the holders'
    accepted tokens; this does not write back into the state.
    """
    _validate_state(state)
    layout = state["layout"]
    data = state[layout]
    tokens = data["tokens"]
    holders = data["holders"]
    view = {}

    if layout == "parent":
        for token in tokens:
            record = data["records"][token]
            view[token] = {"state": record["state"],
                           "holders": sorted(record["holders"])}
    elif layout == "relation":
        for token in tokens:
            record = data["relations"][token]
            view[token] = {"state": record["state"],
                           "holders": sorted(record["holders"])}
    else:
        accepted = {holder: set(data["accepted"][holder]) for holder in holders}
        for token in tokens:
            owners = sorted(holder for holder in holders if token in accepted[holder])
            view[token] = {"state": data["modes"][token], "holders": owners}
    return view


def _transition(current, action, declared_holders):
    """Validate one token's semantic transition and return (mode, holders)."""
    op = action["op"]
    mode = current["state"]
    current_holders = current["holders"]
    declared = set(declared_holders)

    def holder(value, label):
        _require(isinstance(value, str) and bool(value),
                 label + " must be a nonempty holder string")
        _require(value in declared, label + " is not a declared holder: " + value)
        return value

    if op == "assign":
        target = holder(action["to"], "to")
        _require(mode in ("unknown", "unassigned"),
                 "assign requires an unknown or unassigned token, not " + mode)
        return "assigned", [target]

    if op == "transfer":
        source = holder(action["from"], "from")
        target = holder(action["to"], "to")
        _require(source != target, "transfer source and target must differ")
        _require(mode == "assigned",
                 "transfer requires a singly assigned token, not " + mode)
        _require(current_holders == [source],
                 "transfer source does not match the current holder")
        return "assigned", [target]

    if op == "share":
        raw = action["holders"]
        _require(isinstance(raw, (list, tuple)) and not isinstance(raw, str),
                 "share holders must be a list")
        new_holders = _names(raw, "share holders")
        _require(len(new_holders) >= 2, "share requires at least two holders")
        _require(set(new_holders) <= declared, "share uses an undeclared holder")
        if mode == "assigned":
            _require(current_holders[0] in new_holders,
                     "share must retain the current holder")
        elif mode == "shared":
            _require(set(current_holders) <= set(new_holders),
                     "share must not drop an existing holder")
        return "shared", sorted(new_holders)

    if op == "unassign":
        raw = action["from"]
        _require(isinstance(raw, (list, tuple)) and not isinstance(raw, str),
                 "unassign from must be a holder list")
        source = _names(raw, "unassign from")
        _require(set(source) <= declared, "unassign uses an undeclared holder")
        _require(mode in ("assigned", "shared"),
                 "unassign requires an assigned or shared token, not " + mode)
        _require(len(source) == len(current_holders)
                 and set(source) == set(current_holders),
                 "unassign from must exactly match all current holders")
        return "unassigned", []

    # The only remaining operation is "unknown".
    _require(mode in ("unknown", "unassigned"),
             "unknown cannot erase a known allocation")
    return "unknown", []


def _write(state, token, mode, holders):
    """Write one token to the authority owned by the configured layout."""
    layout = state["layout"]
    data = state[layout]
    holders = list(holders)

    if layout == "parent":
        data["records"][token] = {"state": mode, "holders": holders}
    elif layout == "relation":
        record = data["relations"][token]
        if record["state"] != mode or record["holders"] != holders:
            record["version"] += 1
        record["state"] = mode
        record["holders"] = holders
    else:
        accepted = data["accepted"]
        for holder, accepted_tokens in accepted.items():
            if holder in holders:
                if token not in accepted_tokens:
                    accepted_tokens.append(token)
                    accepted_tokens.sort()
            elif token in accepted_tokens:
                accepted_tokens.remove(token)
        data["modes"][token] = mode


def _changed_paths(before, after):
    """Return sorted leaf paths that actually differ, excluding the global revision."""
    paths = []

    def walk(left, right, path):
        if isinstance(left, dict) and isinstance(right, dict):
            for key in sorted(set(left) | set(right), key=str):
                if key in left and key in right:
                    walk(left[key], right[key], path + [str(key)])
                else:
                    paths.append(".".join(path + [str(key)]))
        elif left != right:
            paths.append(".".join(path))

    walk({key: value for key, value in before.items() if key != "revision"},
         {key: value for key, value in after.items() if key != "revision"}, [])
    return sorted(paths)


def apply(state, action, expected_revision):
    """Apply one token transition atomically.

    Successful calls return a new state whose global revision is incremented by
    one, ``error=None`` and the storage paths that really changed.  Stale
    revisions, malformed actions and illegal transitions return a deep copy of
    the input state with ``status='rejected'``, a reason and no changed paths.
    The input state is never modified.
    """
    original = deepcopy(state)
    try:
        _validate_state(state)
        _require(_is_int(expected_revision),
                 "expected_revision must be an integer, not a boolean")
        _require(expected_revision == state["revision"],
                 "stale revision: expected " + str(expected_revision)
                 + " but state is " + str(state["revision"]))
        _require(isinstance(action, dict), "action must be an object")

        op = action.get("op")
        _require(isinstance(op, str) and op in ACTION_FIELDS,
                 "unsupported operation: " + str(op))
        _require(set(action) == ACTION_FIELDS[op],
                 "action " + op + " accepts exactly: "
                 + ", ".join(sorted(ACTION_FIELDS[op])))

        token = action.get("token")
        _require(isinstance(token, str) and bool(token),
                 "token must be a nonempty string")
        tokens, holders = _scope(state)
        _require(token in tokens, "unknown token: " + token)

        current = project(state)[token]
        mode, new_holders = _transition(current, action, holders)

        working = deepcopy(state)
        _write(working, token, mode, new_holders)
        working["revision"] += 1

        before_view = project(state)
        after_view = project(working)
        for other in tokens:
            if other != token:
                _require(before_view[other] == after_view[other],
                         "internal error: unrelated token changed: " + other)

        return {
            "status": "applied",
            "state": working,
            "error": None,
            "changed_paths": _changed_paths(state, working),
        }
    except Exception as exc:  # every malformed request becomes an atomic rejection
        return {
            "status": "rejected",
            "state": deepcopy(original),
            "error": str(exc),
            "changed_paths": [],
        }
