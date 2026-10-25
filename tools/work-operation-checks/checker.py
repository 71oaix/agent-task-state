"""Small deterministic, offline typed record checker (Python standard library)."""
import argparse
from copy import deepcopy
import json
from pathlib import Path


KINDS = {"work", "goal", "contract", "report", "artifact", "evidence", "statement",
         "observation", "judgment", "relation", "adoption", "decision"}
OPS = {"open", "close", "revise", "observe", "judge", "bind", "select",
       "create", "amend", "statement", "inline_link", "decision"}
COMMAND_KEYS = {"op", "target", "kind", "fields", "delta", "refs"}
TRANSACTION_KEYS = {"commands", "group", "provenance", "required_targets"}
CLOSURE = {"status", "disposition", "successor"}


class Invalid(ValueError):
    def __init__(self, code, message):
        self.code = code
        super().__init__(message)


def require(condition, code, message):
    if not condition:
        raise Invalid(code, message)


def is_revision(value):
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def endpoint(value, label):
    require(isinstance(value, dict) and set(value) == {"id", "revision"}
            and isinstance(value["id"], str) and bool(value["id"])
            and is_revision(value["revision"]), "reference", label + " needs exact id/revision")
    return value["id"], value["revision"]


def known_versions(state):
    versions = {}
    for oid, obj in state["objects"].items():
        versions[(oid, obj["revision"])] = obj
    for snapshot in state.get("history", []):
        if isinstance(snapshot, dict) and "id" in snapshot:
            versions[(snapshot["id"], snapshot["revision"])] = snapshot
    return versions


def validate_object(oid, obj, old, provenance):
    kind, fields = obj["kind"], obj["fields"]
    require(kind in KINDS, "kind", "unsupported kind: " + str(kind))
    require(isinstance(fields, dict), "type", oid + " fields must be an object")
    if old:
        require(kind == old["kind"], "kind", "kind is immutable")
        if "scope" in old["fields"]:
            require(fields.get("scope") == old["fields"]["scope"], "scope", "scope cannot change")
    if kind in {"statement", "observation", "judgment"}:
        stype = fields.get("type", kind)
        require(stype in {"observation", "judgment"}, "statement", "statement type required")
        require(kind == "statement" or kind == stype, "statement", "statement kind/type conflict")
        required = {"subject", "result"} if stype == "observation" else {"conclusion", "evidence"}
        require(required <= fields.keys(), "statement", "statement lacks " + str(sorted(required - fields.keys())))
        require(all(provenance.get(k) for k in ("source", "actor", "nature")), "provenance", "statement provenance required")
        if old:
            require(stype == old["fields"].get("type", old["kind"]), "statement", "statement type is immutable")
    if kind == "relation":
        require({"relation", "from", "to", "scope"} <= fields.keys(), "relation", "relation/from/to/scope required")
    if kind in {"adoption", "decision"}:
        require({"scope", "selected"} <= fields.keys(), "scope", "scope and selected required")
    if kind == "work" and old:
        changed = {k for k in fields.keys() | old["fields"].keys() if fields.get(k) != old["fields"].get(k)}
        if "status" in changed and fields.get("status") == "closed":
            require(changed <= CLOSURE, "effect", "closing work may only change status/disposition/successor")


def field_references(obj):
    """Only declared structural positions are references; prose is uninterpreted."""
    fields, kind = obj["fields"], obj["kind"]
    values = []
    if kind == "relation":
        values += [fields["from"], fields["to"]]
    if kind in {"adoption", "decision"}:
        selected = fields["selected"]
        values += selected if isinstance(selected, list) else [selected]
    for link in fields.get("links", []):
        require(isinstance(link, dict) and {"relation", "from", "to", "scope"} <= link.keys(),
                "reference", "inline links need relation/from/to/scope")
        values += [link["from"], link["to"]]
    for name in ("successor",):
        if fields.get(name) is not None:
            values.append(fields[name])
    return values


def validate_allocations(objects):
    for oid, obj in objects.items():
        f = obj["fields"]
        if "allocations" not in f:
            continue
        require(isinstance(f.get("responsibilities"), list) and isinstance(f["allocations"], (list, dict))
                and isinstance(f.get("residual", []), list), "allocation", "allocation uses token lists")
        original = f["responsibilities"]
        require(all(isinstance(t, str) for t in original) and len(set(original)) == len(original),
                "allocation", "responsibility tokens must be unique strings")
        counts = {t: 0 for t in original}
        tokens = list(f.get("residual", []))
        allocations = f["allocations"]
        if isinstance(allocations, dict):
            allocations = [{"target": child, "responsibilities": tokens} for child, tokens in allocations.items()]
        for allocation in allocations:
            require(isinstance(allocation, dict) and isinstance(allocation.get("responsibilities"), list),
                    "allocation", "each allocation needs responsibilities")
            child = allocation.get("target")
            require(isinstance(child, str) and child in objects, "allocation", "allocation target missing")
            tokens += allocation["responsibilities"]
        for token in tokens:
            require(isinstance(token, str) and token in counts, "allocation", "unknown responsibility token")
            counts[token] += 1
        require(all(counts.values()), "allocation", oid + " leaves responsibility unaccounted")
        overlaps = f.get("overlaps", [])
        require(isinstance(overlaps, list) and all(isinstance(t, str) for t in overlaps), "allocation", "overlaps must be token list")
        require(set(overlaps) == {t for t, n in counts.items() if n > 1}, "allocation", "overlaps must exactly declare duplicated tokens")


def apply_transaction(state, transaction, expected=None):
    """Return a new state on success; rejection returns an unchanged copy."""
    original = deepcopy(state)
    try:
        require(isinstance(state, dict) and isinstance(state.get("objects"), dict)
                and isinstance(state.get("history", []), list), "state", "objects/history required")
        require(isinstance(transaction, dict) and not (set(transaction) - TRANSACTION_KEYS), "effect", "unknown transaction keys")
        commands = transaction.get("commands")
        require(isinstance(commands, list) and bool(commands), "command", "nonempty commands required")
        expected = {} if expected is None else expected
        require(isinstance(expected, dict), "expected", "expected must be an object")
        provenance = transaction.get("provenance", {})
        require(isinstance(provenance, dict), "provenance", "provenance must be an object")
        working = deepcopy(state)
        working.setdefault("history", [])
        targets, changes, explicit_refs = set(), [], []
        for command in commands:
            require(isinstance(command, dict) and not (set(command) - COMMAND_KEYS), "effect", "unknown command keys")
            op, target = command.get("op"), command.get("target")
            require(op in OPS and isinstance(target, str) and bool(target), "command", "supported op and target required")
            require(target not in targets, "command", "one command per target in a transaction")
            targets.add(target)
            old = state["objects"].get(target)
            require(target in expected, "expected", "missing expected revision for " + target)
            base = expected[target]
            require((old is None and base == "absent") or (old is not None and is_revision(base)
                    and base == old["revision"]), "stale", "expected revision mismatch: " + target)
            create = op in {"open", "observe", "judge", "create", "statement"} or (old is None and op in {"bind", "select", "decision"})
            require((old is None) == create, "existence", "target existence conflicts with operation")
            if create:
                require(not any(snapshot.get("id") == target for snapshot in state.get("history", [])
                                if isinstance(snapshot, dict)), "existence", "historical ID cannot be reused")
            payload_key = "fields" if create else "delta"
            require(payload_key in command and ("delta" if create else "fields") not in command
                    and isinstance(command[payload_key], dict), "type", "use fields for creation or delta for patch")
            payload = command[payload_key]
            fixed_kind = {"open": "work", "close": "work", "observe": "statement", "judge": "statement",
                          "statement": "statement", "bind": "relation", "select": "adoption", "decision": "decision"}.get(op)
            kind = command.get("kind", fixed_kind or (old["kind"] if old else None))
            if op in {"observe", "judge"}:
                require(kind in {"statement", "observation" if op == "observe" else "judgment"}, "kind", "operation kind mismatch")
            elif op == "decision" and old is not None and old["kind"] == "adoption":
                kind = command.get("kind", "adoption")
                require(kind == "adoption", "kind", "decision update preserves adoption kind")
            else:
                require(fixed_kind is None or kind == fixed_kind, "kind", "operation kind mismatch")
            if old:
                require(kind == old["kind"], "kind", "operation cannot change kind")
            if op == "close":
                require(set(payload) <= CLOSURE and payload.get("status") == "closed", "effect", "close requires closed status and closure-only fields")
            if op == "inline_link":
                require(set(payload) == {"links"}, "effect", "inline_link may only amend links")
            fields = deepcopy(payload) if create else {**deepcopy(old["fields"]), **deepcopy(payload)}
            if op in {"observe", "judge"}:
                require(fields.get("type", kind) == ("observation" if op == "observe" else "judgment"), "statement", "statement type conflicts with operation")
            obj = {"kind": kind, "revision": 1 if create else old["revision"] + 1, "fields": fields,
                   "provenance": deepcopy(provenance)}
            validate_object(target, obj, old, provenance)
            refs = command.get("refs", [])
            require(isinstance(refs, list), "reference", "refs must be a list")
            explicit_refs.extend(refs)
            if old:
                working["history"].append({"id": target, **deepcopy(old)})
            working["objects"][target] = obj
            changes.append({"target": target, "before": None if create else old["revision"], "after": obj["revision"]})
        require(set(expected) == targets, "expected", "expected targets must exactly match commands")
        if "required_targets" in transaction:
            required = transaction["required_targets"]
            require(isinstance(required, list) and all(isinstance(t, str) for t in required)
                    and len(set(required)) == len(required) and set(required) == targets,
                    "group", "required_targets must exactly match command targets")
        versions = known_versions(working)
        for ref in explicit_refs:
            require(endpoint(ref, "refs") in versions, "reference", "reference revision does not exist")
        for target in targets:
            for ref in field_references(working["objects"][target]):
                require(endpoint(ref, target) in versions, "reference", "field reference revision does not exist")
        validate_allocations(working["objects"])
        return {"status": "applied", "state": working, "errors": [], "changes": changes,
                "group": transaction.get("group")}
    except (Invalid, KeyError, TypeError) as exc:
        return {"status": "rejected", "state": original,
                "errors": [{"code": getattr(exc, "code", "type"), "message": str(exc)}], "changes": []}


def export_projection(state):
    """Expose one common logical view for relation/inline and adoption/decision."""
    objects, relations, adoptions = {}, [], []
    for oid, obj in sorted(state["objects"].items()):
        fields = deepcopy(obj["fields"])
        if obj["kind"] == "relation":
            relations.append(fields)
        elif obj["kind"] in {"adoption", "decision"}:
            adoptions.append(fields)
        else:
            relations.extend(fields.pop("links", []))
            kind = obj["kind"]
            if kind in {"observation", "judgment"}:
                fields.setdefault("type", kind)
                kind = "statement"
            objects[oid] = {"kind": kind, "fields": fields}
    sort_key = lambda value: json.dumps(value, sort_keys=True, ensure_ascii=False)
    return {"objects": objects, "relations": sorted(relations, key=sort_key),
            "adoptions": sorted(adoptions, key=sort_key)}


def replay(initial_state, transactions):
    state, results = deepcopy(initial_state), []
    for item in transactions:
        result = apply_transaction(state, item["transaction"], item.get("expected"))
        state = result["state"]
        results.append({k: v for k, v in result.items() if k != "state"})
    return {"state": state, "results": results, "projection": export_projection(state)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["apply", "replay", "export"])
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8-sig"))
    if args.action == "apply":
        result = apply_transaction(data["state"], data["transaction"], data.get("expected"))
    elif args.action == "replay":
        result = replay(data["initial_state"], data["transactions"])
    else:
        result = export_projection(data.get("state", data))
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
