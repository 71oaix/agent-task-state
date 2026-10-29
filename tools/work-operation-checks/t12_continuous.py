"""T12 continuous evidence export: historical anchors plus a separate synthetic chain.

The module only reads the controlled study API.  It does not run the DSH, judge
natural-language truth, or turn a synthetic continuation into a historical event.
"""
from copy import deepcopy
from pathlib import Path
import argparse
import json
import t12_study as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CORE_DIR = ROOT / 'artifacts/agent-task-state/maintenance/t12-continuous-validation-2026-10-29/core-v1'
BASELINE_HEAD = '4433b09490daf7ce05b344bfd8092982f9025fc8'
DRAFT = {'completion': 'in_progress', 'implementation': 'reported_draft_written',
         'git': 'unstaged', 'acceptance': 'pending'}


def _require(ok, message):
    if not ok:
        raise ValueError(message)


def _apply_ok(state, actions, label, nature='synthetic'):
    result = s.apply(state, list(actions), state['head'], ['SYN:' + label], nature)
    _require(result['status'] == 'applied', label + ': ' + str(result['error']))
    return result['state']


def _refs_in(value):
    found = []

    def walk(item):
        if isinstance(item, dict):
            if set(item) == {'id', 'revision'} and isinstance(item['id'], str) \
                    and type(item['revision']) is int:
                found.append({'id': item['id'], 'revision': item['revision']})
            else:
                for child in item.values():
                    walk(child)
        elif isinstance(item, list):
            for child in item:
                walk(child)

    walk(value)
    seen, result = set(), []
    for ref in found:
        key = (ref['id'], ref['revision'])
        if key not in seen:
            seen.add(key)
            result.append(ref)
    return result


def _exact_references(state, actions):
    rows = {}
    for ref in _refs_in(actions):
        key = ref['id'] + '@' + str(ref['revision'])
        rows[key] = s.version(state, ref['id'], ref['revision'])
    return rows


def _plan_object(snapshot, plan_id):
    if plan_id in snapshot.get('objects', {}):
        return snapshot['objects'][plan_id]
    for obj in snapshot.get('objects', {}).values():
        if plan_id in obj.get('plan_records', {}):
            return obj['plan_records'][plan_id]
    return None


def _observations(before, after, actions):
    rows = []
    for action in actions:
        op = action['op']
        if op == 'produce':
            product = after['objects'][action['id']]
            rows.append({'action': op, 'product': action['id'],
                         'initial_plan': deepcopy(product.get('initial_plan')),
                         'plan_usage': deepcopy(product.get('plan_usage')),
                         'legacy_plan_present': 'plan' in product,
                         'dimensions': deepcopy(product['dimensions'])})
        elif op == 'adopt_plan':
            attempt = after['objects'][action['id']]
            rows.append({'action': op, 'attempt': action['id'],
                         'adoption': deepcopy(attempt['plan_adoptions'][-1])})
        elif op == 'change_plan':
            old, new = _plan_object(before, action['id']), _plan_object(after, action['id'])
            rows.append({'action': op, 'plan': action['id'],
                         'revision_before': old['revision'] if old else None,
                         'revision_after': new['revision'] if new else None,
                         'sections_after': deepcopy(new['sections']) if new else None})
        elif op == 'report':
            rows.append({'action': op, 'evidence': deepcopy(after['objects'][action['id']])})
        elif op == 'end':
            rows.append({'action': op, 'attempt': deepcopy(after['objects'][action['id']])})
        elif op == 'reopen':
            rows.append({'action': op, 'attempt': deepcopy(after['objects'][action['id']])})
        elif op == 'accept_goal':
            rows.append({'action': op, 'goal': deepcopy(after['objects'][action['id']])})
        elif op == 'register_items':
            rows.append({'action': op, 'item_ids': sorted(after['items'])})
        elif op == 'relate':
            rows.append({'action': op, 'relation': deepcopy(after['relations'][action['id']])})
    return rows


def _step(change, state):
    return {'change': change['number'], 'basis': deepcopy(change['basis']),
            'nature': change['nature'], 'actor': change['actor'],
            'actions': deepcopy(change['actions']),
            'before': deepcopy(change['before']), 'after': deepcopy(change['after']),
            'changed_paths': deepcopy(change['changed_paths']),
            'exact_references': _exact_references(state, change['actions']),
            'observations': _observations(change['before'], change['after'], change['actions'])}


def _reference_index(state):
    rows = {}
    for oid, obj in state['objects'].items():
        revisions = {int(key) for key in state['versions'].get(oid, {})}
        revisions.add(obj['revision'])
        rows[oid] = {'kind': obj['kind'], 'current_revision': obj['revision'],
                     'available_revisions': sorted(revisions)}
    for host in state['objects'].values():
        for pid, obj in host.get('plan_records', {}).items():
            revisions = {int(key) for key in state['versions'].get(pid, {})}
            revisions.add(obj['revision'])
            rows[pid] = {'kind': 'plan', 'current_revision': obj['revision'],
                         'available_revisions': sorted(revisions)}
    return rows


def build_experiment():
    """Return (historical state, synthetic continuation state, synthetic steps)."""
    historical = s.real_path()
    state = deepcopy(historical)
    steps = []

    def run(label, actions):
        nonlocal state
        result = s.apply(state, list(actions), state['head'], ['SYN:' + label], 'synthetic')
        _require(result['status'] == 'applied', label + ': ' + str(result['error']))
        state = result['state']
        row = _step(state['changes'][-1], state)
        row['label'] = label
        steps.append(row)

    run('plan-v2', [
        {'op': 'change_plan', 'id': 'migration-plan',
         'edits': {'turnstep': {'status': 'planned',
                                'description': 'synthetic continuation plan v2'}}}])
    run('adopt-v2', [
        {'op': 'adopt_plan', 'id': 'turnstep', 'plan': {'id': 'migration-plan', 'revision': 2},
         'scope': ['turnstep'], 'basis': ['SYN:adopt-v2']}])
    run('produce-v2', [
        {'op': 'produce', 'id': 'draft-continuation-v2', 'attempt': 'turnstep',
         'parts': ['synthetic continuation draft'], 'dimensions': dict(DRAFT),
         'location': 'synthetic workspace', 'nature': 'synthetic',
         'plan_scope': ['turnstep']}])
    run('report-v2', [
        {'op': 'report', 'id': 'continuation-check',
         'subject': s.actual_ref(state, 'draft-continuation-v2'),
         'scope': 'synthetic continuation only; not a DSH event',
         'findings': ['structural chain check only; no semantic truth claim'],
         'nature': 'synthetic'}])
    run('accept-v2', [
        {'op': 'accept_goal', 'id': 'goal', 'actor_role': 'acceptor',
         'actor': 'synthetic-reviewer',
         'criteria': ['synthetic criteria: exact scope and evidence present'],
         'decision': 'accept', 'evidence': [s.actual_ref(state, 'continuation-check')]}])
    run('adopt-p1', [
        {'op': 'adopt_plan', 'id': 'turnstep', 'plan': {'id': 'migration-plan', 'revision': 1},
         'scope': ['turnstep'], 'basis': ['SYN:explicit-old-plan']}])
    run('produce-p1', [
        {'op': 'produce', 'id': 'draft-continuation-old', 'attempt': 'turnstep',
         'parts': ['synthetic old-plan draft'], 'dimensions': dict(DRAFT),
         'location': 'synthetic workspace', 'nature': 'synthetic',
         'plan_scope': ['turnstep']}])
    run('regress-v2', [
        {'op': 'advance_product', 'id': 'draft-continuation-v2',
         'dimensions': {'completion': 'in_progress'}}])
    run('assign-responsibility', [
        {'op': 'assign', 'token': 'whole_turn_status', 'to': 'turnstep'}])
    run('end-turnstep', [
        {'op': 'end', 'id': 'turnstep',
         'outcome': 'synthetic stop with retained responsibility',
         'remaining': 'retained_unresolved'}])
    run('reopen-turnstep', [{'op': 'reopen', 'id': 'turnstep'}])
    return historical, state, steps


def build_trace(historical=None, synthetic_state=None, synthetic_steps=None):
    if historical is None:
        historical, synthetic_state, synthetic_steps = build_experiment()
    return {
        'schema': 1,
        'case': 'T12',
        'baseline_head': BASELINE_HEAD,
        'historical': {
            'anchor': 'T12.01-T12.06, S029.dependency and S028.partial_replacement',
            'final_head': historical['head'],
            'steps': [_step(change, historical) for change in historical['changes']],
            'reference_index': _reference_index(historical)},
        'synthetic': {
            'starts_from_change': historical['head'],
            'final_head': synthetic_state['head'],
            'steps': deepcopy(synthetic_steps),
            'reference_index': _reference_index(synthetic_state)},
        'separation': 'Historical steps retain source_record nature. Synthetic steps use SYN: basis and synthetic nature; they are not DSH events and have no event time.'}


def _case(case_id, kind, purpose, state, actions, basis=('SYN:check',), nature='synthetic',
          observe=None):
    before = deepcopy(state)
    result = s.apply(state, list(actions), state['head'], list(basis), nature)
    output = {'status': result['status'], 'error': result['error'],
              'changed_paths': deepcopy(result['changed_paths']),
              'state_after': s.snapshot(result['state']),
              'history_length': len(result['state']['changes'])}
    if observe is not None:
        output['observation'] = observe(result['state'])
    return {'id': case_id, 'kind': kind, 'purpose': purpose,
            'input': {'head': state['head'], 'actions': deepcopy(actions),
                      'basis': list(basis), 'nature': nature},
            'output': output,
            'unchanged_on_rejection': result['status'] != 'rejected' or result['state'] == before}


def _query_case(case_id, purpose, query, output):
    return {'id': case_id, 'kind': 'query', 'purpose': purpose,
            'input': deepcopy(query), 'output': deepcopy(output)}


def _product_observation(pid):
    def observe(state):
        product = state['objects'].get(pid)
        if product is None:
            return {'product': pid, 'present': False}
        return {'product': pid, 'present': True, 'revision': product['revision'],
                'initial_plan': deepcopy(product.get('initial_plan')),
                'plan_usage': deepcopy(product.get('plan_usage')),
                'legacy_plan_present': 'plan' in product}
    return observe


def build_checks():
    base = s.real_path()
    p2 = _apply_ok(deepcopy(base), [
        {'op': 'change_plan', 'id': 'migration-plan',
         'edits': {'turnstep': {'status': 'planned', 'description': 'synthetic plan v2'}}},
        {'op': 'adopt_plan', 'id': 'turnstep', 'plan': {'id': 'migration-plan', 'revision': 2},
         'scope': ['turnstep'], 'basis': ['SYN:check-p2']}], 'check-setup-p2')
    other = _apply_ok(deepcopy(base), [
        {'op': 'goal', 'id': 'other', 'scope': ['gamma']},
        {'op': 'begin', 'id': 'other-owner', 'goal': 'other', 'scope': ['gamma']},
        {'op': 'plan', 'id': 'other-plan', 'owner': 'other-owner',
         'sections': {'gamma': {'status': 'planned', 'description': 'gamma v1'}}}],
        'check-setup-other')
    cases = []

    cases.append(_case(
        'legacy-no-explicit-scope', 'positive',
        'The old no-plan_scope path remains legal only before any explicit adoption.',
        base, [{'op': 'produce', 'id': 'check-legacy', 'attempt': 'independent',
                'parts': ['check'], 'dimensions': dict(DRAFT),
                'location': 'synthetic workspace', 'nature': 'synthetic'}],
        observe=_product_observation('check-legacy')))
    cases.append(_case(
        'explicit-single-p2', 'positive',
        'An explicit single-section scope records P2 as the actual used revision.',
        p2, [{'op': 'produce', 'id': 'check-single', 'attempt': 'turnstep',
              'parts': ['check'], 'dimensions': dict(DRAFT),
              'location': 'synthetic workspace', 'nature': 'synthetic',
              'plan_scope': ['turnstep']}],
        observe=_product_observation('check-single')))
    cases.append(_case(
        'explicit-mixed-versions', 'positive',
        'A mixed scope records the version actually used for each section.',
        p2, [{'op': 'produce', 'id': 'check-mixed', 'attempt': 'turnstep',
              'parts': ['check'], 'dimensions': dict(DRAFT),
              'location': 'synthetic workspace', 'nature': 'synthetic',
              'plan_scope': ['channel', 'turnstep']}],
        observe=_product_observation('check-mixed')))
    cases.append(_case(
        'omit-scope-after-adoption', 'negative',
        'Omitting plan_scope after an explicit adoption would hide the choice and is rejected.',
        p2, [{'op': 'produce', 'id': 'check-omit', 'attempt': 'turnstep',
              'parts': ['check'], 'dimensions': dict(DRAFT),
              'location': 'synthetic workspace', 'nature': 'synthetic'}]))
    cases.append(_case(
        'explicit-old-version', 'positive',
        'Continuing P1 is legal through an explicit re-adoption of that exact version and scope.',
        p2, [{'op': 'adopt_plan', 'id': 'turnstep',
              'plan': {'id': 'migration-plan', 'revision': 1},
              'scope': ['turnstep'], 'basis': ['SYN:explicit-p1']},
             {'op': 'produce', 'id': 'check-old', 'attempt': 'turnstep',
              'parts': ['check'], 'dimensions': dict(DRAFT),
              'location': 'synthetic workspace', 'nature': 'synthetic',
              'plan_scope': ['turnstep']}],
        observe=_product_observation('check-old')))
    cases.append(_case(
        'unadopted-scope', 'negative',
        'A scope that was never adopted is rejected rather than attached silently.',
        p2, [{'op': 'adopt_plan', 'id': 'turnstep',
              'plan': {'id': 'migration-plan', 'revision': 2},
              'scope': ['missing'], 'basis': ['SYN:missing']}]))
    cases.append(_case(
        'other-goal-plan', 'negative',
        'A plan owned by another goal is rejected without an explicit adaptation path.',
        other, [{'op': 'adopt_plan', 'id': 'turnstep',
                 'plan': {'id': 'other-plan', 'revision': 1},
                 'scope': ['gamma'], 'basis': ['SYN:other-goal']}]))
    cases.append(_case(
        'atomic-batch', 'negative',
        'A late invalid scope rolls back both the adoption and the proposed product.',
        p2, [{'op': 'adopt_plan', 'id': 'turnstep',
              'plan': {'id': 'migration-plan', 'revision': 1},
              'scope': ['turnstep'], 'basis': ['SYN:rollback']},
             {'op': 'produce', 'id': 'check-atomic', 'attempt': 'turnstep',
              'parts': ['check'], 'dimensions': dict(DRAFT),
              'location': 'synthetic workspace', 'nature': 'synthetic',
              'plan_scope': ['channel', 'missing']}],
        observe=lambda state: {'head': state['head'],
                               'has_product': 'check-atomic' in state['objects'],
                               'adoptions': len(s.version(state, 'turnstep')['plan_adoptions'])}))
    cases.append(_case(
        'old-report-no-drift', 'positive',
        'Changing the plan does not move an old report or an old product to a new revision.',
        base, [{'op': 'change_plan', 'id': 'migration-plan',
                'edits': {'turnstep': {'status': 'planned', 'description': 'synthetic plan v2'}}}],
        observe=lambda state: {'old_report': s.version(state, 'channel-checks'),
                               'old_product': s.version(state, 'independent-code'),
                               'plan_revision': s.current_plan(state, 'migration-plan')['revision']}))
    cases.append(_case(
        'accept-requires-criteria', 'negative',
        'Same-goal evidence is not sufficient without explicit criteria and decision fields.',
        base, [{'op': 'accept_goal', 'id': 'goal', 'actor_role': 'acceptor',
                'actor': 'synthetic-reviewer', 'decision': 'accept',
                'evidence': [s.actual_ref(base, 'channel-checks')]}]))
    cases.append(_query_case(
        'relation-both-ends',
        'The Context/notification dependency is queryable at both precise endpoints.',
        {'queries': ["relations_for_item(state, '9context')",
                     "relations_for_item(state, '8')",
                     "relations_for(state, 'turnstep', 'Turn starts and Inbox claims')"]},
        {'9context': s.relations_for_item(base, '9context'),
         '8': s.relations_for_item(base, '8'),
         'turn_inputs': s.relations_for(base, 'turnstep', 'Turn starts and Inbox claims')}))
    cases.append(_query_case(
        's029-items',
        'S029 item status, work scope and partial reuse are queryable with the current projection.',
        {'query': 's029_items(state)'}, s.s029_items(base)))
    return {'schema': 1,
            'scope': 'structural positive/negative probes only; the checker does not judge natural-language truth or semantic sufficiency',
            'cases': cases}


def _operation_index():
    return [
        {'name': 'current_object', 'call': 't12_study.version(state, id)',
         'meaning': 'current revision only'},
        {'name': 'exact_history', 'call': 't12_study.version(state, id, revision)',
         'meaning': 'one exact historical revision'},
        {'name': 'point_in_time', 'call': 't12_study.at(state, change_number)',
         'meaning': 'state after one recorded change; not an event timestamp'},
        {'name': 'plan_usage', 'call': 'product.plan_usage',
         'meaning': 'only authority for plan revisions actually used'},
        {'name': 'initial_plan', 'call': 'product.initial_plan',
         'meaning': 'begin-time reference; not an adoption result'},
        {'name': 'partial_adoption', 'call': 't12_study.plan_sections(state, attempt_id)',
         'meaning': 'effective section map; later explicit adoption wins per section'},
        {'name': 'relation_query', 'call': 't12_study.relations_for(state, object, scope)',
         'meaning': 'typed relation from either endpoint; not completion or acceptance'},
        {'name': 'item_query', 'call': 't12_study.s029_items(state)',
         'meaning': 'S029 source status plus current product projection'},
        {'name': 'readback', 'call': 't12_study.readback(state)',
         'meaning': 'detached representation and source entry; no answers'}
    ]


def build_readback():
    historical, synthetic_state, _ = build_experiment()
    return {
        'schema': 1,
        'generated_by': 't12_continuous.build_readback',
        'historical': s.readback(historical),
        'synthetic': s.readback(synthetic_state),
        'operations': _operation_index(),
        'query_questions': deepcopy(s.FIXTURE['questions']),
        'representation_note': 'This is a representation, operation and source entry only. It contains no expected answers, truth labels or recommendations.'}


def build_operations():
    return """# T12 连续变化核心查询规则

本文件只说明如何读 `core-v1`，不替读者回答研究问题，也不把合成步骤当作 DSH 事件。

## 当前与历史

- 当前对象：`t12_study.version(state, id)`；只返回当前 revision。
- 精确历史：`t12_study.version(state, id, revision)`；revision 必须是现存正整数，不能用 `None`、“当前”指针或布尔值代替。
- 时点视图：`t12_study.at(state, change_number)`；change 是记录位置，不是事件时间。
- 旧报告、旧成果、旧计划版本都保留各自的精确引用；新版本出现不会改写它们。

## 实际所用计划

- `product.plan_usage` 是唯一权威，按 section 记录实际采用的 Plan 版本。
- `product.initial_plan` 只是 begin 时的计划引用，不表示后续实际采用。
- 旧 `product.plan` 只可能出现在从未显式采用其它版本的兼容路径；它等于 initial plan，不能当作显式采用的结果。
- 单一 P2 scope 读 `plan_usage.sections[name].plan` 为 P2；混合 scope 逐 section 读，不能压成一个版本。

## 部分采用与省略

- `plan_adoptions` 保存每次显式采用的范围、依据和 Change 号；`plan_sections` 给出当前生效的 section 映射，后一次显式采用按 section 覆盖前一次。
- 一旦存在显式采用，`produce` 必须给出 `plan_scope`；省略会被拒绝，因为那会把选择藏回初始版本。
- 继续旧版是合法的，但必须再次显式 `adopt_plan(旧版本, 相关 scope)`，再以该 scope produce；不能靠缺省绕过。

## 关系

- `relations_for(state, object, scope)` 从任一端查询；`relations_for_item(state, item_id)` 先把 S029 item 解析到 product part。
- 关系是产品要求，有精确端点、方向和 basis；它不表示任一端已完成、已转交或已验收。
- S029 第 9-context 项依赖第 8 项通知工作；第 8 项又依赖 Turn starts 与 Inbox claims。关系不会自动把任何一项标成完成。

## S029 清单

- `s029_items(state)` 同时给出 S029 的 source status、工作 scope、产品/part 绑定、当前产品维度和部分复用记录。
- 1-5 与 9 permission/system 是完成/写码/已提交；6、7、8、9 context、10、11 是未完成草稿/未暂存。4A 与 4B 分开可查；第 5 项保留原 PR 的 `latestCompletedParagraphFirstLine`。
- `current.matches_source_status` 只说明当前编码与来源记录一致，不是独立验收。

## 证据与验收

- `report` 只登记 subject、scope、findings 和 nature，不改变 subject 的验收状态。
- `accept_goal` 需要 acceptor 角色、明确 criteria、decision 和可追踪到同一 Goal 的 Evidence。
- 同一 Goal 的关联不等于 Evidence 语义充分；检查器只检查结构和精确引用，不判断自然语言真实性，也不自动扩成验收语义引擎。

## 原子性与边界

- 一批动作要么全部生效并记录 before/after，要么返回原状态；失败批次不会留下部分产品、采用或责任变化。
- 历史步骤使用 `source_record` nature；合成续接使用 `SYN:` basis 和 `synthetic` nature，没有 DSH 事件时间。
- `readback.json` 只提供表示、操作和来源入口，不含 truth/答案/推荐。
"""


def build_manifest(trace=None):
    if trace is None:
        trace = build_trace()
    return {
        'schema': 1,
        'batch': 't12-continuous-validation-2026-10-29',
        'slice': '2a2-core-v1',
        'baseline_head': BASELINE_HEAD,
        'source_cutoff': s.FIXTURE['source_cutoff'],
        'generated_by': {
            'module': 't12_continuous.py',
            'functions': ['build_trace', 'build_checks', 'build_readback',
                          'build_operations', 'build_manifest'],
            'driver': 'test_t12_export.py under unittest discovery',
            'cli_executed_in_this_slice': False,
            'cli_reproduction': 'python Agent任务状态管理/tools/work-operation-checks/t12_continuous.py --out <new-directory>'
        },
        'history': {
            'historical_steps': len(trace['historical']['steps']),
            'historical_anchor': trace['historical']['anchor'],
            'synthetic_steps': len(trace['synthetic']['steps']),
            'synthetic_starts_from_change': trace['synthetic']['starts_from_change'],
            'source_revisions': {sid: source['revision']
                                 for sid, source in s.FIXTURE['sources'].items()}
        },
        'synthetic_boundary': {
            'basis_prefix': 'SYN:',
            'nature': 'synthetic',
            'not_dsh_events': True,
            'no_event_times': True,
            'starts_from': 'T12 historical anchor state',
            'history_remains_source_record': True
        },
        'files': {
            'trace.json': 'step actions, basis, nature, before/after and changed paths, with exact old references',
            'checks.json': 'positive/negative inputs and literal outputs, including errors and state after',
            'readback.json': 'detached current/history/operation/source entry; no expected answers',
            'operations.md': 'concise reading rules for current vs history, partial adoption, relations and item status',
            'manifest.json': 'generation source, version/history counts and synthetic boundary'
        },
        'anti_overwrite': 'export_core refuses an existing output directory; core-v1 is created once and later runs verify the saved files in memory.',
        'model_call_note': 'DeepSeek (this worker) is itself a model invocation. Token and fee receipts are unknown, recorded as unknown rather than zero.',
        'scope_limit': 'No four identity replacements, no remaining 15 process segments and no final recommendation are covered by this slice.'
    }


def _serialize(document):
    if isinstance(document, str):
        return document if document.endswith('\n') else document + '\n'
    return json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + '\n'


def build_documents():
    trace = build_trace()
    return {
        'trace.json': trace,
        'checks.json': build_checks(),
        'readback.json': build_readback(),
        'operations.md': build_operations(),
        'manifest.json': build_manifest(trace)
    }


def export_core(directory):
    """Create a new evidence directory.  Existing directories are never overwritten."""
    out = Path(directory)
    documents = build_documents()
    out.mkdir(parents=True, exist_ok=False)
    for name, document in documents.items():
        (out / name).write_text(_serialize(document), encoding='utf-8')
    return str(out.resolve())


def verify_core(directory):
    """Compare saved evidence with an in-memory rebuild; never writes."""
    out = Path(directory)
    documents = build_documents()
    for name, document in documents.items():
        expected = _serialize(document)
        actual = (out / name).read_text(encoding='utf-8')
        if actual != expected:
            raise AssertionError('saved evidence differs from the current build: ' + name)
    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    print(export_core(Path(args.out)))
