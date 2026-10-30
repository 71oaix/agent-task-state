"""One continuous, replayable T12 handoff state.

The build starts from the controlled T12 historical anchor produced by
``t12_study.real_path`` and appends a short, explicitly synthetic continuation on
the same linear branch.  It exists because an earlier isolated readback of
boundary-v2 mixed heads from different probe branches, had no complete snapshot,
and read a Plan owner as the plan revision a product actually used.

The export therefore holds one branch, one head, the complete current state, the
per-change record, precise report pointers and the write contract for one next
step.  Expected results, scoring and rejection probes stay in checks.json.  The
module runs no DSH and judges no natural-language truth.

v2 keeps that branch and state but splits the view: readback.json carries the
current objects, the archived object revisions, a compact per-change record and a
schema-only contract, while resume-state.json holds the complete state that
``apply`` needs.  v1's builders and files stay as they were exported.
"""
from copy import deepcopy
from pathlib import Path
import argparse
import hashlib
import json

import t12_study as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BATCH = 't12-continuous-validation-2026-10-29'
SLICE = 'handoff-v1'
HANDOFF_DIR = ROOT / 'artifacts/agent-task-state/maintenance' / BATCH / SLICE
BRANCH = 't12-handoff-mainline'
HISTORICAL_ANCHOR = 'T12.01-T12.06, S029.dependency and S028.partial_replacement'
PLAN = 'migration-plan'
ATTEMPT = 'turnstep'
PRODUCT = 'draft-continuation-v2'
REPORT = 'continuation-record'
BEHAVIOR_PART = 'synthetic continuation behavior'
NOTES_PART = 'synthetic continuation notes'
DRAFT = {'completion': 'in_progress', 'implementation': 'reported_draft_written',
         'git': 'unstaged', 'acceptance': 'pending'}
NEXT_ACTION = {'op': 'advance_parts', 'id': PRODUCT, 'parts': [BEHAVIOR_PART],
               'dimensions': {'implementation': 'reported_code_written'}}
NEXT_BASIS = ['SYN:handoff-next-step']
GENERATED = ('readback.json', 'checks.json')


def _require(ok, message):
    if not ok:
        raise ValueError(message)


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
        rows[ref['id'] + '@' + str(ref['revision'])] = s.version(state, ref['id'], ref['revision'])
    return rows


def _observations(state, actions):
    rows = []
    for action in actions:
        op = action['op']
        if op == 'change_plan':
            plan = s.current_plan(state, action['id'])
            rows.append({'action': op, 'plan': action['id'], 'revision': plan['revision'],
                         'sections': deepcopy(plan['sections'])})
        elif op == 'adopt_plan':
            attempt = s.version(state, action['id'])
            rows.append({'action': op, 'attempt': action['id'],
                         'adoption': deepcopy(attempt['plan_adoptions'][-1]),
                         'adopted_plan_sections': s.plan_sections(state, action['id'])})
        elif op == 'produce':
            product = s.version(state, action['id'])
            rows.append({'action': op, 'product': action['id'],
                         'plan_usage': deepcopy(product.get('plan_usage')),
                         'initial_plan': deepcopy(product.get('initial_plan')),
                         'legacy_plan_present': 'plan' in product,
                         'dimensions': deepcopy(product['dimensions'])})
        elif op == 'report':
            rows.append({'action': op, 'evidence': deepcopy(s.version(state, action['id']))})
        else:
            rows.append({'action': op, 'object': deepcopy(s.version(state, action['id']))})
    return rows


def build_chain():
    """Return (historical anchor, current state, synthetic steps) on one branch."""
    historical = s.real_path()
    state = deepcopy(historical)
    steps = []

    def run(label, actions):
        nonlocal state
        result = s.apply(state, list(actions), state['head'], ['SYN:' + label], 'synthetic')
        _require(result['status'] == 'applied', label + ': ' + str(result['error']))
        state = result['state']
        steps.append({'change': state['head'], 'label': label, 'basis': ['SYN:' + label],
                      'nature': 'synthetic', 'actions': deepcopy(actions),
                      'changed_paths': deepcopy(result['changed_paths']),
                      'observation': _observations(state, actions)})

    run('handoff-plan-v2', [
        {'op': 'change_plan', 'id': PLAN,
         'edits': {'turnstep': {'status': 'planned',
                                'description': 'synthetic continuation plan v2; the original PR stays a reference'}}}])
    run('handoff-adopt-v2', [
        {'op': 'adopt_plan', 'id': ATTEMPT, 'plan': {'id': PLAN, 'revision': 2},
         'scope': ['turnstep'], 'basis': ['SYN:handoff-adopt-v2']}])
    run('handoff-produce-v2', [
        {'op': 'produce', 'id': PRODUCT, 'attempt': ATTEMPT,
         'parts': [BEHAVIOR_PART, NOTES_PART], 'dimensions': dict(DRAFT),
         'location': 'synthetic continuation workspace', 'nature': 'synthetic',
         'plan_scope': ['turnstep']}])
    run('handoff-report-v2', [
        {'op': 'report', 'id': REPORT, 'subject': s.actual_ref(state, PRODUCT),
         'scope': 'synthetic continuation product record only; not a DSH event',
         'findings': ['synthetic structural record; no acceptance or verification claim'],
         'nature': 'synthetic'}])
    return historical, state, steps


def _records(historical, steps, current):
    rows = []
    for change in historical['changes']:
        rows.append({'change': change['number'], 'origin': 'historical_anchor',
                     'anchor': change['basis'][0], 'basis': deepcopy(change['basis']),
                     'nature': change['nature'], 'actions': deepcopy(change['actions']),
                     'changed_paths': deepcopy(change['changed_paths']),
                     'exact_references': _exact_references(current, change['actions'])})
    for step in steps:
        rows.append({'change': step['change'], 'origin': 'synthetic_continuation',
                     'anchor': step['label'], 'basis': deepcopy(step['basis']),
                     'nature': step['nature'], 'actions': deepcopy(step['actions']),
                     'changed_paths': deepcopy(step['changed_paths']),
                     'exact_references': _exact_references(current, step['actions']),
                     'observation': deepcopy(step['observation'])})
    return rows


def _plan_authority(state):
    attempts = {oid: obj for oid, obj in state['objects'].items() if obj['kind'] == 'attempt'}
    products = {oid: obj for oid, obj in state['objects'].items() if obj['kind'] == 'product'}
    plan_ids = sorted({oid for oid, obj in state['objects'].items() if obj['kind'] == 'plan'}
                      | {pid for obj in state['objects'].values() for pid in obj.get('plan_records', {})})
    return {
        'rule': 'product.plan_usage is the only authority for the plan revision a product actually used; '
                'a Plan owner or the plan reference an attempt began with is a different fact',
        'plan_owner': {pid: s.current_plan(state, pid)['owner'] for pid in plan_ids},
        'current_plan_revision': {pid: s.current_plan(state, pid)['revision'] for pid in plan_ids},
        'attempt_begin_plan': {oid: deepcopy(obj.get('plan')) for oid, obj in attempts.items()},
        'plan_adoptions': {oid: deepcopy(obj.get('plan_adoptions', [])) for oid, obj in attempts.items()},
        'adopted_plan_sections': {oid: s.plan_sections(state, oid) for oid in attempts},
        'product_initial_plan': {oid: deepcopy(obj.get('initial_plan')) for oid, obj in products.items()},
        'product_plan_usage': {oid: deepcopy(obj.get('plan_usage')) for oid, obj in products.items()},
        'product_legacy_plan_projection': {oid: deepcopy(obj['plan']) for oid, obj in products.items()
                                           if 'plan' in obj}}


def _report_pointers(state):
    rows = []
    for oid, obj in sorted(state['objects'].items()):
        if obj['kind'] != 'evidence':
            continue
        rows.append({'evidence': {'id': oid, 'revision': obj['revision']},
                     'subject': deepcopy(obj.get('subject')), 'goal': obj.get('goal'),
                     'scope': obj.get('scope'), 'nature': obj.get('nature'),
                     'content_kind': obj.get('content_kind'),
                     'scope_ids': deepcopy(obj.get('scope_ids')),
                     'corrects': deepcopy(obj.get('corrects'))})
    return rows


def _source_entry():
    return {
        'source_cutoff': s.FIXTURE['source_cutoff'],
        'identity_origin': s.FIXTURE['identity_origin'],
        'ordering': s.FIXTURE['ordering'],
        'sources': deepcopy(s.FIXTURE['sources']),
        'fact_index': {fact['id']: [sid for sid in s.FIXTURE['sources'] if sid in fact['source']]
                       for fact in s.FIXTURE['facts'] + s.FIXTURE['supplements']},
        'module': 'Agent任务状态管理/tools/work-operation-checks/t12_handoff.py',
        'builder': 't12_handoff.build_chain',
        'fixture': 'Agent任务状态管理/tools/work-operation-checks/t12_experiment_fixture.json'}


def _operation_index():
    return [
        {'name': 'load_snapshot', 'call': 'json.loads(readback.json)["state"]',
         'meaning': 'the complete current state; the only input the next step needs'},
        {'name': 'current_object', 'call': 't12_study.version(state, id)',
         'meaning': 'current revision only'},
        {'name': 'exact_history', 'call': 't12_study.version(state, id, revision)',
         'meaning': 'one exact earlier revision; old objects are never rewritten'},
        {'name': 'point_in_time', 'call': 't12_study.at(state, change_number)',
         'meaning': 'state after one recorded change of this branch; a record position, not an event time'},
        {'name': 'plan_usage', 'call': 'product.plan_usage',
         'meaning': 'only authority for the plan revision a product used, section by section'},
        {'name': 'plan_owner', 'call': 't12_study.current_plan(state, plan_id)["owner"]',
         'meaning': 'the Goal or Attempt that owns the plan; not the revision a product used'},
        {'name': 'adopted_sections', 'call': 't12_study.plan_sections(state, attempt_id)',
         'meaning': 'effective plan revision per adopted section; a later explicit adoption wins per section'},
        {'name': 'interpretations', 'call': 't12_study.interpretations(state, scope_id)',
         'meaning': 'current interpretation, history and correction basis for one stable scope id'},
        {'name': 'apply', 'call': 't12_study.apply(state, actions, expected_head, basis, nature)',
         'meaning': 'all-or-nothing update; a head other than the current one is rejected'}]


def _write_contract(head):
    return {
        'entry': 't12_study.apply(state, actions, expected_head, basis, nature); the state above is the input',
        'current_head': head,
        'head_rule': 'expected_head must equal current_head; any other value is rejected and the exact input state is returned',
        'basis_rule': 'a non-empty list of known fact ids or SYN:-prefixed labels; this step uses a SYN: label',
        'nature_rule': 'this step uses synthetic nature; historical changes keep source_record and are not rewritten',
        'allowed_operation': deepcopy(NEXT_ACTION),
        'dimensions_rule': 'completion, implementation and git only; acceptance cannot be written through this entry',
        'scope_rule': 'the parts list must name existing parts of the product; the request names one part only',
        'not_in_this_step': ['changing or re-adopting a plan version',
                             'creating another product, report or relation',
                             'accepting the goal',
                             'editing an existing object revision',
                             'advancing the other part or the whole product'],
        'atomicity': 'a batch applies as a whole or returns the exact input state with the head unchanged'}


def _next_step_request():
    return {
        'nature': 'synthetic user request for the next step; it is not a DSH event and not an acceptance',
        'text': '在 ' + PRODUCT + ' 上只登记 `' + BEHAVIOR_PART + '` 这一部分的实现进展：'
                'implementation = reported_code_written。不登记完成、提交或验收，也不改动另一部分、'
                '既有成果、计划版本和历史记录。',
        'target': {'product': PRODUCT, 'part': BEHAVIOR_PART},
        'requested_values': {'implementation': 'reported_code_written'},
        'deliverable': ['完整的 JSON 更新：op、目标对象、part、维度、当前 head、basis、nature',
                        '逐项指出这一步没有改变的对象、计划版本、验收状态和历史 revision']}


def build_readback(chain=None):
    if chain is None:
        chain = build_chain()
    historical, state, steps = chain
    return {
        'schema': 1,
        'batch': BATCH,
        'slice': SLICE,
        'generated_by': 't12_handoff.build_readback',
        'branch': {
            'id': BRANCH,
            'shape': 'one linear branch: every change number from 1 to current head belongs to this branch',
            'historical_anchor': HISTORICAL_ANCHOR,
            'historical_base_head': historical['head'],
            'synthetic_start_change': historical['head'] + 1,
            'current_head': state['head'],
            'parallel_probe_states_included': False,
            'note': 'Probe and rejection states exist only in checks.json; they are not part of this branch.'},
        'head': state['head'],
        'state': deepcopy(state),
        'records': _records(historical, steps, state),
        'plan_authority': _plan_authority(state),
        'report_pointers': _report_pointers(state),
        'source_entry': _source_entry(),
        'operations': _operation_index(),
        'write_contract': _write_contract(state['head']),
        'next_step_request': _next_step_request(),
        'representation_note': 'One branch, one head, the complete snapshot, its record and the write contract. '
                               'No expected result, score, pass label or rejection-probe answer is included; '
                               'those stay in checks.json.'}


def _case(case_id, kind, purpose, state, actions, basis=('SYN:check',), nature='synthetic',
          observe=None, expected=None):
    before = deepcopy(state)
    expected_head = state['head'] if expected is None else expected
    result = s.apply(state, list(actions), expected_head, list(basis), nature)
    output = {'expected_head': expected_head, 'status': result['status'], 'error': result['error'],
              'changed_paths': deepcopy(result['changed_paths']),
              'head_after': result['state']['head'],
              'state_after': s.snapshot(result['state'])}
    if observe is not None:
        output['observation'] = observe(result['state'])
    return {'id': case_id, 'kind': kind, 'purpose': purpose,
            'input': {'head': state['head'], 'actions': deepcopy(actions),
                      'basis': list(basis), 'nature': nature},
            'output': output,
            'unchanged_on_rejection': result['status'] != 'rejected' or result['state'] == before}


def _check(cid, requirement, observed, ok):
    return {'id': cid, 'requirement': requirement, 'observed': deepcopy(observed), 'ok': bool(ok)}


def _preserved(state, base):
    rows = {}
    for oid in ('draft-code', 'independent-code', 'channel-checks', 'grouping-pending', 'goal'):
        rows[oid] = {'revision': s.version(state, oid)['revision'],
                     'unchanged': s.version(state, oid) == s.version(base, oid)}
    for revision in (1, 2):
        rows[PLAN + '@' + str(revision)] = {
            'unchanged': s.version(state, PLAN, revision) == s.version(base, PLAN, revision)}
    return rows


def build_checks():
    _, base, _ = build_chain()
    next_step = _case(
        'next-step-applies', 'positive',
        'The listed synthetic next step is legal at the exported head and stays inside one part.',
        base, [dict(NEXT_ACTION)], NEXT_BASIS,
        observe=lambda state: {
            'part_progress': s.part_progress(state, PRODUCT),
            'product_dimensions': deepcopy(s.version(state, PRODUCT)['dimensions']),
            'goal_acceptance': s.version(state, 'goal')['acceptance'],
            'plan_usage': deepcopy(s.version(state, PRODUCT)['plan_usage']),
            'preserved': _preserved(state, base)})
    stale = _case(
        'stale-head-atomic', 'negative',
        'A predecessor other than the exported head is rejected and the exact input state is returned.',
        base, [dict(NEXT_ACTION)], NEXT_BASIS, expected=base['head'] - 1)
    acceptance = _case(
        'part-acceptance-rejected', 'negative',
        'The same entry cannot record acceptance.',
        base, [{'op': 'advance_parts', 'id': PRODUCT, 'parts': [BEHAVIOR_PART],
                'dimensions': {'acceptance': 'accepted'}}], NEXT_BASIS)
    plan = s.current_plan(base, PLAN)
    attempt = s.version(base, ATTEMPT)
    product = s.version(base, PRODUCT)
    authority = {'plan_owner': plan['owner'],
                 'current_plan_revision': plan['revision'],
                 'attempt_begin_plan': deepcopy(attempt['plan']),
                 'attempt_last_adoption': deepcopy(attempt['plan_adoptions'][-1]),
                 'product_initial_plan': deepcopy(product['initial_plan']),
                 'product_plan_usage': deepcopy(product['plan_usage']),
                 'legacy_plan_present': 'plan' in product}
    observation = next_step['output']['observation']
    checks = [
        _check('next-step-applies', 'The listed next step applies at the exported head.',
               next_step['output'], next_step['output']['status'] == 'applied'),
        _check('next-step-one-part',
               'Only the named part records the implementation value; the other part keeps the draft dimensions.',
               observation['part_progress']['parts'],
               observation['part_progress']['parts'][BEHAVIOR_PART]['dimensions']['implementation']
               == 'reported_code_written'
               and observation['part_progress']['parts'][NOTES_PART]['dimensions'] == DRAFT),
        _check('next-step-no-acceptance',
               'The next step leaves product and goal acceptance unchanged.',
               {'product_dimensions': observation['product_dimensions'],
                'goal_acceptance': observation['goal_acceptance']},
               observation['product_dimensions']['acceptance'] == 'pending'
               and observation['goal_acceptance'] == 'pending'),
        _check('next-step-preserves-history',
               'Old products, reports, the goal and both plan revisions stay exact.',
               observation['preserved'],
               all(row['unchanged'] for row in observation['preserved'].values())),
        _check('next-step-keeps-plan-usage',
               'The updated product still records revision 2 for its adopted turnstep section.',
               observation['plan_usage']['sections']['turnstep']['plan'],
               observation['plan_usage']['sections']['turnstep']['plan'] == {'id': PLAN, 'revision': 2}),
        _check('stale-head-atomic',
               'A stale predecessor is rejected and leaves the exact input state.',
               stale['output'], stale['output']['status'] == 'rejected'
               and stale['unchanged_on_rejection']),
        _check('part-acceptance-rejected',
               'Acceptance cannot be written through the part entry.',
               acceptance['output'], acceptance['output']['status'] == 'rejected'
               and acceptance['unchanged_on_rejection']),
        _check('plan-authority',
               'The plan revision actually used comes from plan_usage, not from the Plan owner or the attempt begin reference.',
               authority,
               authority['plan_owner'] == 'migration'
               and authority['attempt_begin_plan'] == {'id': PLAN, 'revision': 1}
               and authority['product_initial_plan'] == {'id': PLAN, 'revision': 1}
               and authority['product_plan_usage']['sections']['turnstep']['plan']
               == {'id': PLAN, 'revision': 2}),
    ]
    return {'schema': 1, 'batch': BATCH, 'slice': SLICE,
            'generated_by': 't12_handoff.build_checks',
            'branch': BRANCH, 'base_head': base['head'],
            'scope': 'reproduction inputs/outputs and scoring material for the exported next step; '
                     'kept out of readback.json',
            'cases': [next_step, stale, acceptance],
            'checks': checks,
            'summary': {'checks': len(checks),
                        'failed': [check['id'] for check in checks if not check['ok']],
                        'ok': all(check['ok'] for check in checks)}}


def build_documents():
    return {'readback.json': build_readback(), 'checks.json': build_checks()}


def _serialize(document):
    if isinstance(document, str):
        return document if document.endswith('\n') else document + '\n'
    return json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + '\n'


def export_handoff(directory):
    """Create missing generated files once; existing files are verified, never overwritten."""
    out = Path(directory)
    documents = build_documents()
    out.mkdir(parents=True, exist_ok=True)
    for name, document in documents.items():
        path = out / name
        expected = _serialize(document)
        if path.exists():
            if path.read_text(encoding='utf-8') != expected:
                raise AssertionError('existing evidence differs from the current build: ' + name)
            continue
        path.write_text(expected, encoding='utf-8')
    return str(out.resolve())


def verify_handoff(directory):
    """Compare saved evidence with an in-memory rebuild; never writes."""
    out = Path(directory)
    for name, document in build_documents().items():
        expected = _serialize(document)
        actual = (out / name).read_text(encoding='utf-8')
        if actual != expected:
            raise AssertionError('saved evidence differs from the current build: ' + name)
    return True


# --- v2: blind-read handoff view -------------------------------------------
#
# v1 is left exactly as it was exported.  v2 changes only the two payload
# problems of that view: the contract no longer carries a filled next action,
# and the readback no longer repeats the twelve per-change before/after
# snapshots.  The complete state moves to resume-state.json, addressed by path
# and SHA256 so a reader pays for it only when a step needs it.

SLICE_V2 = 'handoff-v2'
HANDOFF_DIR_V2 = ROOT / 'artifacts/agent-task-state/maintenance' / BATCH / SLICE_V2
RESUME_NAME = 'resume-state.json'
GENERATED_V2 = ('readback.json', RESUME_NAME, 'checks.json')
DIMENSION_DOMAIN = {name: sorted(values) for name, values in s.DIMENSION_VALUES.items()}
ACTION_FIELDS = {
    'begin': ('goal', 'plan'),
    'plan': ('owner',),
    'adopt_plan': ('plan', 'scope'),
    'produce': ('attempt',),
    'end': ('outcome',),
    'advance_parts': ('parts',),
    'withdraw_parts': ('parts',),
    'report': ('subject',),
    'relate': ('kind', 'from', 'to'),
    'relate_exact': ('kind', 'from', 'to', 'scope'),
}


def _action_row(action):
    """Name the action and its identifying operands, never its bulk payload."""
    row = {'op': action['op']}
    for key in ('id', 'token'):
        if key in action:
            row[key] = deepcopy(action[key])
    for key in ACTION_FIELDS.get(action['op'], ()):
        if key in action:
            row[key] = deepcopy(action[key])
    if action['op'] == 'change_plan':
        row['sections'] = sorted(set(action.get('edits', {})) | set(action.get('remove', [])))
    elif action['op'] == 'produce':
        row['part_count'] = len(action['parts'])
    elif action['op'] == 'register_items':
        row['item_count'] = len(action['items'])
    return row


def _compact_paths(paths):
    """Collapse field-level changed paths to the object, version or item they hit."""
    keys = []
    for path in paths:
        parts = path.split('/')
        if len(parts) >= 3 and parts[0] == '' and parts[1] in {'objects', 'items'}:
            key = '/'.join(parts[:3])
        elif len(parts) >= 4 and parts[0] == '' and parts[1] == 'versions':
            key = '/'.join(parts[:4])
        else:
            key = path
        if key not in keys:
            keys.append(key)
    return keys


def _record_rows(historical, steps):
    rows = []
    for change in historical['changes']:
        rows.append(_record_row(change['number'], 'historical_anchor', change['basis'][0], change))
    for step in steps:
        rows.append(_record_row(step['change'], 'synthetic_continuation', step['label'], step))
    return rows


def _record_row(number, origin, anchor, change):
    return {'change': number,
            'origin': origin,
            'anchor': anchor,
            'basis': deepcopy(change['basis']),
            'nature': change['nature'],
            'actions': [_action_row(action) for action in change['actions']],
            'references': _refs_in(change['actions']),
            'changed_paths': _compact_paths(change['changed_paths'])}


def _plan_authority_v2(state):
    """The same authority facts as v1 without repeating the object payloads."""
    attempts = {oid: obj for oid, obj in state['objects'].items() if obj['kind'] == 'attempt'}
    products = {oid: obj for oid, obj in state['objects'].items() if obj['kind'] == 'product'}
    plan_ids = sorted({oid for oid, obj in state['objects'].items() if obj['kind'] == 'plan'}
                      | {pid for obj in state['objects'].values() for pid in obj.get('plan_records', {})})
    return {
        'rule': 'product.plan_usage is the only authority for the plan revision a product actually used; '
                'a Plan owner or the plan reference an attempt began with is a different fact',
        'plan_owner': {pid: s.current_plan(state, pid)['owner'] for pid in plan_ids},
        'current_plan_revision': {pid: s.current_plan(state, pid)['revision'] for pid in plan_ids},
        'attempt_begin_plan': {oid: deepcopy(obj.get('plan')) for oid, obj in attempts.items()},
        'attempt_adoptions': {oid: [{'plan': deepcopy(record['plan']),
                                     'scope': deepcopy(record['scope']),
                                     'change': record['change']}
                                    for record in obj.get('plan_adoptions', [])]
                              for oid, obj in attempts.items()},
        'product_initial_plan': {oid: deepcopy(obj.get('initial_plan')) for oid, obj in products.items()},
        'product_plan_usage': {oid: {'mode': obj['plan_usage']['mode'],
                                     'sections': {name: deepcopy(section['plan'])
                                                  for name, section in obj['plan_usage']['sections'].items()}}
                               for oid, obj in products.items()},
        'product_legacy_plan_projection': {oid: deepcopy(obj['plan']) for oid, obj in products.items()
                                           if 'plan' in obj}}


def _view(state):
    """Current objects, archived object revisions and the other live authorities."""
    return {'complete': False,
            'missing': 'changes: the per-change before/after snapshots; read resume-state.json when one is needed',
            'head': state['head'],
            'layout': state['layout'],
            'plans': state['plans'],
            'objects': deepcopy(state['objects']),
            'versions': deepcopy(state['versions']),
            'items': deepcopy(state['items']),
            'relations': deepcopy(state['relations']),
            'responsibility': deepcopy(state['responsibility'])}


def _operation_index_v2():
    return [
        {'name': 'load_view', 'call': 'json.loads(readback.json)["view"]',
         'meaning': 'current objects, archived revisions, items, relations and responsibility'},
        {'name': 'load_complete_state', 'call': 'json.loads(<resume.path>)["state"]',
         'meaning': 'complete state with every per-change before/after; the only apply input; reading it is an extra read'},
        {'name': 'current_object', 'call': 't12_study.version(state, id)',
         'meaning': 'current revision only; the view is enough'},
        {'name': 'exact_history', 'call': 't12_study.version(state, id, revision)',
         'meaning': 'one exact earlier revision, from view.versions; old objects are never rewritten'},
        {'name': 'point_in_time', 'call': 't12_study.at(state, change_number)',
         'meaning': 'state after one recorded change; needs the complete state, the view does not carry it'},
        {'name': 'plan_usage', 'call': 'product.plan_usage',
         'meaning': 'only authority for the plan revision a product used, section by section'},
        {'name': 'plan_owner', 'call': 't12_study.current_plan(state, plan_id)["owner"]',
         'meaning': 'the Goal or Attempt that owns the plan; not the revision a product used'},
        {'name': 'adopted_sections', 'call': 't12_study.plan_sections(state, attempt_id)',
         'meaning': 'effective plan revision per adopted section; a later explicit adoption wins per section'},
        {'name': 'apply', 'call': 't12_study.apply(state, actions, expected_head, basis, nature)',
         'meaning': 'all-or-nothing update on the complete state; a head other than current_head is rejected'}]


def _write_contract_v2(head):
    """Describe the legal shape of the next update; never its filled instance."""
    return {
        'entry': 't12_study.apply(state, actions, expected_head, basis, nature)',
        'input_state': 'the complete state object stored in resume-state.json under "state"',
        'current_head': head,
        'apply_arguments': {
            'state': 'complete state from resume-state.json',
            'actions': 'non-empty list of operation objects',
            'expected_head': 'integer; must equal current_head',
            'basis': 'non-empty list of known fact ids or SYN:-prefixed labels',
            'nature': "'synthetic' for this step"},
        'head_rule': 'expected_head must equal current_head; any other value is rejected and the exact input state is returned',
        'basis_rule': 'a non-empty list of known fact ids or SYN:-prefixed labels',
        'nature_rule': 'this step uses synthetic nature; historical changes keep source_record and are not rewritten',
        'operation': {
            'op': 'advance_parts',
            'fields': {
                'id': {'type': 'string', 'domain': 'id of an existing product object'},
                'parts': {'type': 'array', 'items': 'unique non-empty strings',
                          'domain': 'present parts of that product'},
                'dimensions': {'type': 'object',
                               'allowed_keys': ['completion', 'implementation', 'git'],
                               'nonempty': True,
                               'values': deepcopy(DIMENSION_DOMAIN)}},
            'rules': ['every part named must exist and be present on that product',
                      'only completion, implementation and git can be written here',
                      'acceptance cannot be written through this entry']},
        'scope_rule': 'the parts list must name existing parts of the product; the request names one part only',
        'not_in_this_step': ['changing or re-adopting a plan version',
                             'creating another product, report or relation',
                             'accepting the goal',
                             'editing an existing object revision',
                             'advancing the other part or the whole product'],
        'atomicity': 'a batch applies as a whole or returns the exact input state with the head unchanged'}


def _next_step_request_v2():
    return {
        'nature': 'synthetic user request for the next step; it is not a DSH event and not an acceptance',
        'text': '在 ' + PRODUCT + ' 上只登记 `' + BEHAVIOR_PART + '` 这一部分的实现进展：'
                'implementation = reported_code_written。不登记完成、提交或验收，也不改动另一部分、'
                '既有成果、计划版本和历史记录。',
        'target': {'product': PRODUCT, 'part': BEHAVIOR_PART},
        'deliverable': ['完整的 JSON 更新：op、目标对象、part、维度、当前 head、basis、nature',
                        '逐项指出这一步没有改变的对象、计划版本、验收状态和历史 revision']}


def _serialize_v2(document):
    """Same objects, one indent level instead of two: the fields are unchanged."""
    return json.dumps(document, ensure_ascii=False, indent=1, sort_keys=True) + '\n'


def build_resume_state():
    """The complete recoverable state; the readback only points at it."""
    _, state, _ = build_chain()
    return {'schema': 2, 'batch': BATCH, 'slice': SLICE_V2,
            'generated_by': 't12_handoff.build_resume_state',
            'head': state['head'],
            'role': 'complete recoverable state; load its "state" and pass it to t12_study.apply',
            'state': deepcopy(state)}


def build_readback_v2():
    historical, state, steps = build_chain()
    resume_text = _serialize_v2(build_resume_state())
    return {
        'schema': 2,
        'batch': BATCH,
        'slice': SLICE_V2,
        'generated_by': 't12_handoff.build_readback_v2',
        'branch': {
            'id': BRANCH,
            'shape': 'one linear branch: every change number from 1 to current head belongs to this branch',
            'historical_anchor': HISTORICAL_ANCHOR,
            'historical_base_head': historical['head'],
            'synthetic_start_change': historical['head'] + 1,
            'current_head': state['head'],
            'parallel_probe_states_included': False,
            'note': 'Probe and rejection states exist only in checks.json; they are not part of this branch.'},
        'head': state['head'],
        'view': _view(state),
        'records': _record_rows(historical, steps),
        'plan_authority': _plan_authority_v2(state),
        'source_entry': _source_entry(),
        'operations': _operation_index_v2(),
        'write_contract': _write_contract_v2(state['head']),
        'next_step_request': _next_step_request_v2(),
        'resume': {
            'path': RESUME_NAME,
            'sha256': hashlib.sha256(resume_text.encode('utf-8')).hexdigest(),
            'characters': len(resume_text),
            'contents': 'the complete state: objects, archived revisions, items, relations, responsibility and '
                        'every change with its before/after snapshots',
            'read_when': 'only when a step needs at(), a before/after view or the apply input',
            'cost': 'reading it counts as one extra read of the full evidence'},
        'representation_note': 'One branch, one head, the current view, the compact per-change record and a '
                               'schema-only write contract. No expected result, score, pass label, filled next '
                               'action or rejection-probe answer is included; those stay in checks.json.'}


def build_checks_v2():
    """The v1 scoring material plus proof that the saved resume state executes."""
    base = build_checks()
    restored = json.loads(_serialize_v2(build_resume_state()))['state']
    resumed = s.apply(restored, [dict(NEXT_ACTION)], restored['head'], list(NEXT_BASIS), 'synthetic')
    after = resumed['state']
    observation = {'status': resumed['status'], 'error': resumed['error'],
                   'head_after': after['head'],
                   'part_progress': s.part_progress(after, PRODUCT),
                   'goal_acceptance': s.version(after, 'goal')['acceptance'],
                   'plan_usage': deepcopy(s.version(after, PRODUCT)['plan_usage'])}
    resume_check = _check(
        'resume-state-executes',
        'The complete state saved in resume-state.json, after a JSON round trip, applies the listed next step '
        'and keeps the other part, acceptance and plan usage unchanged.',
        observation,
        resumed['status'] == 'applied'
        and after['head'] == restored['head'] + 1
        and observation['part_progress']['parts'][BEHAVIOR_PART]['dimensions']['implementation']
        == 'reported_code_written'
        and observation['part_progress']['parts'][NOTES_PART]['dimensions'] == DRAFT
        and observation['goal_acceptance'] == 'pending'
        and observation['plan_usage']['sections']['turnstep']['plan'] == {'id': PLAN, 'revision': 2})
    sizes = {'budget': 45000,
             'readback_characters': len(_serialize_v2(build_readback_v2())),
             'resume_characters': len(_serialize_v2(build_resume_state()))}
    size_check = _check(
        'readback-size-budget',
        'The readback stays under the 45000 character budget while the complete state is kept in resume-state.json.',
        sizes, sizes['readback_characters'] < sizes['budget'])
    checks = deepcopy(base['checks']) + [resume_check, size_check]
    return {'schema': 2, 'batch': BATCH, 'slice': SLICE_V2,
            'generated_by': 't12_handoff.build_checks_v2',
            'branch': BRANCH, 'base_head': base['base_head'],
            'scope': base['scope'],
            'cases': deepcopy(base['cases']),
            'checks': checks,
            'summary': {'checks': len(checks),
                        'failed': [check['id'] for check in checks if not check['ok']],
                        'ok': all(check['ok'] for check in checks)}}


def build_documents_v2():
    return {'readback.json': build_readback_v2(), RESUME_NAME: build_resume_state(),
            'checks.json': build_checks_v2()}


def _write_document(path, text):
    """Write UTF-8 text with LF line endings so the recorded SHA256 stays exact."""
    with open(path, 'w', encoding='utf-8', newline='\n') as stream:
        stream.write(text)


def export_handoff_v2(directory):
    """Write this slice's three files; the bytes are always a deterministic rebuild.

    Unlike v1, this slice is this round's own output area: a corrected build
    replaces the earlier one.  Only the three named files are written.
    """
    out = Path(directory)
    documents = build_documents_v2()
    out.mkdir(parents=True, exist_ok=True)
    for name, document in documents.items():
        _write_document(out / name, _serialize_v2(document))
    return str(out.resolve())


def verify_handoff_v2(directory):
    """Compare saved v2 evidence with an in-memory rebuild; never writes."""
    out = Path(directory)
    for name, document in build_documents_v2().items():
        expected = _serialize_v2(document)
        if (out / name).read_text(encoding='utf-8') != expected:
            raise AssertionError('saved v2 evidence differs from the current build: ' + name)
    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    print(export_handoff(Path(args.out)))
