"""Executable work compositions, source ledger and version queries. Standard library only."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re

from checker import apply_transaction, known_versions, resolve_adoptions


HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1] / "docs/research/change-graph-task-state"
PACKS = HERE / "cases"
RELATIONS = {"implements", "uses_contract", "reuses_result", "historical_reference",
             "depends_on", "shared_mechanism", "contains"}
ACTIONS = {"create", "revise", "partial_revert", "replace_parts", "split", "rework",
           "close", "reuse", "adopt", "correct"}
QUESTIONS = ["目标与工作", "提议、实施、观察与采用", "替代与保留", "变化原因与未知",
             "未完成与责任", "跨工作联系"]


class ExpressionError(ValueError):
    pass


def need(value, message):
    if not value:
        raise ExpressionError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def load_corpus(path=None):
    """Keep the original source text; classification is an attributed study extraction."""
    path = Path(path or RESEARCH / "dsh-process-truth-v1.md")
    text = path.read_text(encoding="utf-8-sig")
    cases = {}
    blocks = re.split(r"(?m)^### (T\d{2}) · (.+)$", text)
    for i in range(1, len(blocks), 3):
        cid, title, body = blocks[i:i+3]
        body = body.split("## 跨过程联系")[0]
        facts = {}
        for match in re.finditer(r"(?m)^\*\*(T\d{2}\.\d{2})\*\*\s*(.+)$", body):
            fid, content = match.groups()
            nature = re.search(r"（([^；（）]+)；", content)
            facts[fid] = {"text": content, "nature": nature.group(1) if nature else "source_report",
                          "sources": [{"id": a, "url": b} for a, b in re.findall(r"\[(S\d+)\]\(([^)]+)\)", content)],
                          "actor": "source_author_or_commit_record; decision_actor_unknown_unless_stated"}
        gap = re.search(r"\*\*未决与使用边界：\*\*(.+)", body)
        cases[cid] = {"id": cid, "title": title, "facts": facts,
                      "gap": gap.group(1).strip() if gap else "unknown"}
    cross = []
    section = text.split("## 跨过程联系", 1)[1].split("## 固定", 1)[0]
    for line in section.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if line.startswith("| T") and len(cells) == 3:
            ids = list(dict.fromkeys(re.findall(r"T\d{2}", cells[0])))
            cross.append({"endpoints": ids, "label": cells[0], "meaning": cells[1], "basis": cells[2]})
    return {"cutoff": "2026-10-15", "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "cases": cases, "cross_links": cross}


def load_cases():
    cases = {}
    difficulties = []
    for path in sorted(PACKS.glob("pack*.json")):
        pack = json.loads(path.read_text(encoding="utf-8-sig"))
        need(pack.get("schema") == 1, f"{path.name}: schema must be 1")
        for case in pack["cases"]:
            need(case["id"] not in cases, "duplicate case " + case["id"])
            cases[case["id"]] = case
        difficulties.extend(pack.get("difficulties", []))
    return cases, difficulties


def version(state, oid, revision=None):
    if revision is None:
        need(oid in state["objects"], "missing object " + oid)
        return deepcopy({"id": oid, **state["objects"][oid]})
    value = known_versions(state).get((oid, revision))
    need(value is not None, f"missing object version {oid}@{revision}")
    return deepcopy({"id": oid, **value})


def expand(state, action, provenance):
    """Prepare exact writes and reads without mutating input; every composition is visible."""
    commands, expected, reads = [], {}, {}
    name = action.get("action")
    need(name in ACTIONS, "unsupported action " + str(name))

    def obj(oid):
        value = version(state, oid)
        reads[oid] = value["revision"]
        return value

    def ref(value):
        if isinstance(value, str):
            item = obj(value)
            return {"id": value, "revision": item["revision"]}
        need(isinstance(value, dict) and set(value) == {"id", "revision"}, "exact reference required")
        version(state, value["id"], value["revision"])
        return deepcopy(value)

    def add(oid, kind, fields, op="create", refs=None):
        need(oid not in state["objects"], "object already exists " + oid)
        need(oid not in expected, "duplicate write " + oid)
        expected[oid] = "absent"
        commands.append({"op": op, "target": oid, "kind": kind, "fields": deepcopy(fields), "refs": refs or []})

    def change(oid, delta, op="revise", refs=None):
        old = obj(oid)
        need(oid not in expected, "duplicate write " + oid)
        expected[oid] = old["revision"]
        cmd = {"op": op, "target": oid, "delta": deepcopy(delta)}
        if refs is not None:
            cmd["refs"] = refs
        commands.append(cmd)

    def link(owner, provider, relation, scope):
        old = obj(owner)
        target = ref(provider)
        need(relation in RELATIONS, "unsupported relation " + str(relation))
        need(isinstance(scope, str) and scope.strip(), "relation scope required")
        links = deepcopy(old["fields"].get("links", []))
        links.append({"relation": relation, "from": {"id": owner, "revision": old["revision"] + 1},
                      "to": target, "scope": scope})
        change(owner, {"links": links})

    if name == "create":
        add(action["id"], action["kind"], action["fields"])
    elif name == "revise":
        need(bool(action["delta"]), "empty revision")
        change(action["id"], action["delta"])
    elif name in {"partial_revert", "replace_parts"}:
        oid = action["id"]
        old = obj(oid)
        parts = deepcopy(old["fields"].get("parts"))
        need(isinstance(parts, dict) and parts, "component boundary must be recorded first")
        removed = action["withdraw"] if name == "partial_revert" else action["remove"]
        retained = action["retain"]
        need(len(removed) == len(set(removed)) and len(retained) == len(set(retained)), "duplicate part")
        need(not set(removed) & set(retained), "withdraw/retain overlap")
        need(set(removed) | set(retained) == set(parts), "every known part needs a disposition")
        need(bool(action["reason"]), "reason required (use explicit unknown if unavailable)")
        for key in removed:
            value = parts[key]
            need(isinstance(value, dict), "part value must be an object")
            parts[key] = {**value, "status": "withdrawn"}
        additions = action.get("add", {}) if name == "replace_parts" else {}
        need(not set(additions) & set(parts), "replacement additions need distinct component identities")
        parts.update(deepcopy(additions))
        change(oid, {"parts": parts, "last_change": {"action": name, "reason": action["reason"],
                       "removed": removed, "retained": retained, "added": list(additions)}})
    elif name == "split":
        parent = obj(action["id"])
        need(parent["kind"] == "work", "split targets work")
        need("responsibilities" in parent["fields"], "record original responsibilities first")
        allocations = {}
        for child in action["children"]:
            need(child["id"] not in allocations, "duplicate child")
            allocations[child["id"]] = child["responsibilities"]
            add(child["id"], "work", {"title": child["title"], "status": child["status"],
                "responsibilities": child["responsibilities"], "domain": "development",
                "links": [{"relation": "child_of", "from": {"id": child["id"], "revision": 1},
                           "to": {"id": action["id"], "revision": parent["revision"] + 1},
                           "scope": "recorded responsibility allocation"}]})
        change(action["id"], {"allocations": allocations, "residual": action["residual"],
                             "overlaps": action.get("overlaps", [])})
    elif name == "rework":
        old = obj(action["old"])
        goal = ref(action["goal"])
        need(old["kind"] == "work" and old["fields"].get("status") != "closed", "rework needs open work")
        need(state["objects"][goal["id"]]["kind"] == "goal", "rework goal must be a goal")
        need(bool(action["reason"]) and bool(action["reference_scope"]), "rework reason/reference scope required")
        fields = deepcopy(action["new_fields"])
        fields["links"] = fields.get("links", []) + [
            {"relation": "continues_goal", "from": {"id": action["new"], "revision": 1}, "to": goal,
             "scope": "same user goal; completion unchanged"},
            {"relation": "historical_reference", "from": {"id": action["new"], "revision": 1},
             "to": {"id": action["old"], "revision": old["revision"]}, "scope": action["reference_scope"]}]
        add(action["new"], "work", fields, refs=[goal])
        change(action["old"], {"status": "closed", "disposition": action["reason"],
                              "successor": {"id": action["new"], "revision": 1}})
    elif name == "close":
        need(obj(action["id"])["kind"] == "work", "close targets work")
        change(action["id"], {"status": "closed", "disposition": action["disposition"]})
    elif name == "reuse":
        link(action["owner"], action["provider"], action["relation"], action["range"])
    elif name == "adopt":
        selected = [ref(v) for v in action["selected"]]
        need(selected and isinstance(action["scope"], str) and action["scope"].strip(), "adoption scope/selection required")
        fields = {"scope": action["scope"], "selected": selected, "reason": action["reason"]}
        if action["id"] in state["objects"]:
            need(obj(action["id"])["kind"] == "adoption", "adopt target must be adoption")
            change(action["id"], fields, op="select")
        else:
            add(action["id"], "adoption", fields, op="select")
    elif name == "correct":
        prior = ref(action["prior"])
        need(version(state, prior["id"], prior["revision"])["kind"] in {"statement", "judgment", "observation"},
             "correction needs a previous statement")
        evidence = [{"id": "fact/" + fid, "revision": 1} for fid in action["evidence"]]
        for item in evidence:
            version(state, item["id"], 1)
        add(action["id"], "statement", {"type": "judgment", "conclusion": action["conclusion"],
            "evidence": action["evidence"], "scope": action["scope"], "links": [
                {"relation": "corrects", "from": {"id": action["id"], "revision": 1},
                 "to": prior, "scope": action["scope"]}]}, op="statement", refs=[prior] + evidence)

    # Exact source-record links are carried by the represented version as well as its provenance.
    basis = [{"id": "fact/" + fid, "revision": 1} for fid in provenance.get("source", [])
             if isinstance(fid, str) and "fact/" + fid in state["objects"]] if isinstance(provenance.get("source"), list) else []
    for command in commands:
        old = state["objects"].get(command["target"], {})
        references = command.get("refs", deepcopy(old.get("refs", [])))
        for item in basis:
            if item not in references:
                references.append(item)
        if references:
            command["refs"] = references
    transaction = {"commands": commands, "provenance": deepcopy(provenance),
                   "required_targets": list(expected), "group": provenance.get("step", name)}
    packet = {"action": deepcopy(action), "transaction": transaction, "expected": expected, "read_set": reads}
    packet["seal"] = digest(packet)
    return packet


def apply_prepared(state, packet):
    check = {k: v for k, v in packet.items() if k != "seal"}
    if digest(check) != packet.get("seal"):
        return {"status": "rejected", "state": deepcopy(state), "errors": [{"code": "prepared", "message": "prepared packet changed"}], "changes": []}
    for oid, revision in packet["read_set"].items():
        if state["objects"].get(oid, {}).get("revision") != revision:
            return {"status": "rejected", "state": deepcopy(state), "errors": [{"code": "stale_read", "message": oid}], "changes": []}
    return apply_transaction(state, packet["transaction"], packet["expected"])


def execute_step(state, step, corpus_case):
    before = deepcopy(state)
    current = deepcopy(state)
    trace = []
    provenance = {"source": step["facts"], "actor": "source_report; semantic_mapping_by_researcher",
                  "nature": "attributed_extraction", "step": step["id"]}
    try:
        commands = []
        for fid in step["facts"]:
            need(fid in corpus_case["facts"], "unknown source fact " + fid)
            fact = corpus_case["facts"][fid]
            commands.append({"op": "statement", "target": "fact/" + fid, "fields": {
                "type": "observation", "subject": corpus_case["id"], "result": fact["text"],
                "source_fact": fid, "source_nature": fact["nature"], "source_actor": fact["actor"],
                "sources": fact["sources"], "domain": "source_record", "event_time": "as_stated_in_source_else_unknown",
                "visibility": "controlled_local_order; retrospective_reports_keep_attribution"}})
        need(bool(commands), "step needs source facts")
        result = apply_transaction(current, {"commands": commands, "provenance": provenance},
                                   {c["target"]: "absent" for c in commands})
        need(result["status"] == "applied", str(result["errors"]))
        current = result["state"]
        trace.append({"kind": "source_registration", "transaction": commands, "changes": result["changes"]})
        for action in step["actions"]:
            packet = expand(current, action, provenance)
            result = apply_prepared(current, packet)
            trace.append({"kind": "composition", "prepared": packet, "status": result["status"],
                          "changes": result["changes"], "errors": result["errors"]})
            need(result["status"] == "applied", str(result["errors"]))
            current = result["state"]
        return {"status": "applied", "state": current, "step": step["id"], "facts": step["facts"], "trace": trace}
    except (ExpressionError, KeyError, TypeError, ValueError) as exc:
        return {"status": "rejected", "state": before, "step": step["id"], "facts": step.get("facts", []),
                "trace": trace, "error": str(exc)}


def run_case(case, corpus_case):
    state = {"objects": {}, "history": []}
    provenance = {"source": "research_identity_scaffold", "actor": "researcher", "nature": "identity_not_upstream_event"}
    for item in case["objects"]:
        packet = expand(state, {"action": "create", **item}, provenance)
        result = apply_prepared(state, packet)
        need(result["status"] == "applied", str(result["errors"]))
        state = result["state"]
    initial = deepcopy(state)
    events = []
    seen = []
    for step in case["steps"]:
        result = execute_step(state, step, corpus_case)
        events.append({k: v for k, v in result.items() if k != "state"})
        need(result["status"] == "applied", f"{step['id']}: {result.get('error')}")
        state = result["state"]
        seen += step["facts"]
    need(len(seen) == len(set(seen)) and set(seen) == set(corpus_case["facts"]), "fact coverage " + case["id"])
    gap_id = "fact/" + case["id"] + ".GAP"
    result = apply_transaction(state, {"commands": [{"op": "statement", "target": gap_id, "fields": {
        "type": "observation", "subject": case["id"], "result": corpus_case["gap"], "source_fact": case["id"] + ".GAP",
        "domain": "research_gap", "source_actor": "researcher", "source_nature": "research_gap_recorded_2026-10-20"}}],
        "provenance": {"source": "dsh-process-truth-v1.md", "actor": "researcher", "nature": "research_gap"}}, {gap_id: "absent"})
    need(result["status"] == "applied", str(result["errors"]))
    return {"id": case["id"], "title": case["title"], "initial_state": initial,
            "state": result["state"], "events": events, "fact_coverage": seen}


def query(result, oid=None, revision=None):
    state = result["state"]
    if oid:
        return version(state, oid, revision)
    return {"id": result["id"], "objects": [{"id": k, **v} for k, v in state["objects"].items()
             if not k.startswith("fact/")], "adoptions": resolve_adoptions(state),
            "unknowns": [v["fields"]["result"] for k, v in state["objects"].items() if k.endswith(".GAP")]}


def coverage(result, corpus_case):
    rows = []
    for fid in corpus_case["facts"]:
        event = next(e for e in result["events"] if fid in e["facts"])
        effects = [c for t in event["trace"] if t["kind"] == "composition" for c in t["changes"]]
        rows.append({"fact": fid, "statement": "fact/" + fid, "step": event["step"],
                     "effect_versions": effects, "alignment": "source_mapping_requires_semantic_review"})
    return rows


def build_all():
    corpus = load_corpus()
    cases, difficulties = load_cases()
    need(set(cases) == set(corpus["cases"]), "all 16 cases required")
    results = {cid: run_case(case, corpus["cases"][cid]) for cid, case in sorted(cases.items())}
    rows = {cid: coverage(value, corpus["cases"][cid]) for cid, value in results.items()}
    # Cross-work links reference the precise final represented versions, not runtime instances.
    cross = []
    shared_state = {"objects": {}, "history": []}
    for value in results.values():
        need(not set(shared_state["objects"]) & set(value["state"]["objects"]), "case namespaces collide")
        shared_state["objects"].update(deepcopy(value["state"]["objects"]))
        shared_state["history"].extend(deepcopy(value["state"]["history"]))
    kinds = ["uses_contract", "constrains", "enables", "shared_mechanism", "requires_adaptation",
             "uses_contract", "depends_on", "contains", "contains"]
    for index, item in enumerate(corpus["cross_links"]):
        refs = []
        for cid in item["endpoints"]:
            state = results[cid]["state"]
            oid = cid + "/work"
            need(oid in state["objects"], "each case needs a work identity")
            refs.append({"id": oid, "revision": state["objects"][oid]["revision"]})
        cross.append({**item, "relation": kinds[index], "record_endpoints": refs, "domain": "development_record_connection",
                      "interpretation": "meaning_as_stated; no_extra_causality"})
        if len(refs) == 2:
            oid = "cross/" + str(index + 1)
            tx = {"commands": [{"op": "create", "target": oid, "kind": "relation", "fields": {
                "relation": kinds[index], "from": refs[0], "to": refs[1], "scope": item["meaning"],
                "basis": item["basis"], "domain": "development_record_connection"}}],
                "provenance": {"source": item["basis"], "actor": "researcher", "nature": "source_backed_connection"}}
            result = apply_transaction(shared_state, tx, {oid: "absent"})
            need(result["status"] == "applied", str(result["errors"]))
            shared_state = result["state"]
    return {"corpus": corpus, "cases": results, "coverage": rows, "cross_links": cross,
            "state": shared_state, "difficulties": difficulties, "rules": "EXPRESSION.md", "schema": 1}


def readback_view(result):
    """Primary records for an independent reader; source prose lives in the evidence packet."""
    state = result["state"]
    return {"id": result["id"], "title": result["title"],
        "objects": {k: deepcopy(v) for k, v in state["objects"].items() if not k.startswith("fact/")},
        "history": [deepcopy(v) for v in state["history"] if not v["id"].startswith("fact/")],
        "steps": [{"id": e["step"], "facts": e["facts"],
                   "effects": [{"action": t["prepared"]["action"], "changes": t["changes"]}
                               for t in e["trace"] if t["kind"] == "composition"]} for e in result["events"]],
        "research_gap": state["objects"]["fact/" + result["id"] + ".GAP"]["fields"]["result"],
        "questions": QUESTIONS}


def timeline_markdown(result):
    lines = ["# " + result["id"] + " · " + result["title"], "",
             "每步显示来源报告、实际展开及保存后的版本；对象身份由研究者建立。", ""]
    versions = known_versions(result["state"])
    for event in result["events"]:
        lines += ["## " + event["step"], ""]
        for fid in event["facts"]:
            fact = result["state"]["objects"]["fact/" + fid]["fields"]
            lines += [f"**{fid}** {fact['result']}", ""]
        for trace in event["trace"]:
            if trace["kind"] != "composition":
                continue
            packet = trace["prepared"]
            action = packet["action"]
            ops = " → ".join(cmd["op"] + "(" + cmd["target"] + ")" for cmd in packet["transaction"]["commands"])
            lines += ["**" + action["action"] + "**：" + ops, ""]
            for change in trace["changes"]:
                obj = versions[(change["target"], change["after"])]
                lines += ["```json", json.dumps({"id": change["target"], "revision": change["after"],
                    "fields": obj["fields"]}, ensure_ascii=False, indent=2), "```", ""]
    lines += ["## 尚需确认", "", *query(result)["unknowns"], ""]
    return "\n".join(lines)


def render_html(bundle):
    """Standalone reader built only from the saved bundle; no network dependencies."""
    payload = json.dumps(bundle, ensure_ascii=False).replace('<', '\\u003c')
    return (HERE / 'reader.html').read_text(encoding='utf-8').replace('__BUNDLE__', payload)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    build = sub.add_parser("build")
    build.add_argument("--out", required=True)
    check = sub.add_parser("case")
    check.add_argument("id")
    check.add_argument("--object")
    check.add_argument("--revision", type=int)
    args = parser.parse_args()
    if args.command == "build":
        out = Path(args.out)
        need(not out.exists(), "output must be a new directory")
        bundle = build_all()
        out.mkdir(parents=True)
        (out / "bundle.json").write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding="utf-8")
        (out / "index.html").write_text(render_html(bundle), encoding="utf-8")
        for cid, value in bundle["cases"].items():
            (out / (cid + ".md")).write_text(timeline_markdown(value), encoding="utf-8")
        print(json.dumps({"out": str(out.resolve()), "cases": len(bundle["cases"]),
                          "facts": sum(len(v["fact_coverage"]) for v in bundle["cases"].values()),
                          "cross_links": len(bundle["cross_links"])}, ensure_ascii=False))
    else:
        corpus = load_corpus()
        cases, _ = load_cases()
        result = run_case(cases[args.id], corpus["cases"][args.id])
        print(json.dumps(query(result, args.object, args.revision), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
