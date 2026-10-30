"""T03/T12/T13/T15 object-boundary checks on top of the controlled T12 study.

This slice implements four already-adjudicated gaps in small, named operations:

* T12 part-scoped product progress; the overall product state is no longer a
  second writable authority once parts are subdivided.
* T03 plans may be owned by a Goal or an Attempt, with one goal_of trace.
* T13 evidence content types and scoped correction of an old interpretation.
* T15 delivery dependencies fixed to exact object revisions and scopes.

It does not run the DSH, call a model, use Git, implement conversion jobs or
reader ref-counts, and it does not decide the five object classes or any paper
conclusion.  Synthetic probes and real source facts are kept apart.
"""
from copy import deepcopy
from pathlib import Path
import json

import t12_study as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BATCH = 't12-continuous-validation-2026-10-29'
SLICE = 'boundary-v2'
BOUNDARY_DIR = ROOT / 'artifacts/agent-task-state/maintenance' / BATCH / SLICE
FIXTURE = json.loads((HERE / 'dsh_object_boundary_fixture.json').read_text(encoding='utf-8'))
DRAFT = {'completion': 'in_progress', 'implementation': 'reported_draft_written',
         'git': 'unstaged', 'acceptance': 'pending'}
UNKNOWN = {'completion': 'unknown', 'implementation': 'unknown',
           'git': 'unknown', 'acceptance': 'unknown'}
T13_SCOPES = FIXTURE['t13_scope_ids']
SYN_A = 'SYN:two-scope-a'
SYN_B = 'SYN:two-scope-b'
SYN_C = 'SYN:two-scope-c'


def _need(value, message):
    if not value:
        raise ValueError(message)


def _run(state, actions, basis, nature='synthetic'):
    result = s.apply(state, list(actions), state['head'], list(basis), nature)
    record = {'input': {'head': state['head'], 'actions': deepcopy(list(actions)),
                        'basis': list(basis), 'nature': nature},
              'response': {'status': result['status'], 'error': result['error'],
                           'changed_paths': deepcopy(result['changed_paths'])}}
    return result, record


def _ok(state, actions, basis, nature='synthetic'):
    result, record = _run(state, actions, basis, nature)
    _need(result['status'] == 'applied', record['response']['error'])
    return result['state'], record


def _reject(state, actions, basis, nature='synthetic'):
    result, record = _run(state, actions, basis, nature)
    _need(result['status'] == 'rejected', 'expected a rejection')
    _need(result['state'] == state, 'rejection changed state')
    record['response']['state_unchanged'] = True
    return record


def _check(cid, requirement, observed, ok):
    return {'id': cid, 'requirement': requirement, 'observed': deepcopy(observed), 'ok': bool(ok)}


def _query(name, call, output, question=None):
    row = {'name': name, 'call': call, 'output': deepcopy(output)}
    if question:
        row['question'] = question
    return row


def _legacy_item_projection(state):
    """Frozen reproduction of the pre-fix projection formula, not a DSH run."""
    rows = {}
    for item_id, item in sorted(state['items'].items()):
        product = state['objects'][item['product']]
        rows[item_id] = {
            'dimensions': deepcopy(product['dimensions']),
            'matches_source_status': all(product['dimensions'][name] == item['status'][name]
                                         for name in ('completion', 'implementation', 'git', 'acceptance'))}
    return rows


def _item_state(state, item_id):
    row = s.s029_items(state)['items'][item_id]['current']
    return {'product_revision': row['product_revision'], 'dimensions': deepcopy(row['dimensions']),
            'product_dimensions': deepcopy(row.get('product_dimensions')),
            'part_state': row['part_state'], 'matches_source_status': row['matches_source_status']}


def _registration_state():
    state = s.fresh()
    state, _ = _ok(state, [
        {'op': 'goal', 'id': 'registration-goal', 'scope': ['registration boundary']},
        {'op': 'begin', 'id': 'registration-attempt', 'goal': 'registration-goal',
         'scope': ['registration boundary']},
        {'op': 'produce', 'id': 'registration-product', 'attempt': 'registration-attempt',
         'parts': ['p1', 'p2'], 'dimensions': dict(DRAFT),
         'location': 'synthetic registration probe', 'nature': 'synthetic'}],
        ['SYN:registration-setup'])
    state, _ = _ok(state, [
        {'op': 'advance_parts', 'id': 'registration-product', 'parts': ['p1'],
         'dimensions': {'completion': 'reported_migration_complete',
                        'implementation': 'reported_code_written', 'git': 'reported_committed'}}],
        ['SYN:registration-part'])
    return state


def _registration_items(p1_status):
    return [
        {'id': 'registration-1', 'label': 'part one', 'source': 'S029', 'nature': 'documented_status',
         'product': 'registration-product', 'part': 'p1', 'scope': 'p1',
         'source_status': 'synthetic registration probe', 'status': dict(p1_status)},
        {'id': 'registration-2', 'label': 'part two', 'source': 'S029', 'nature': 'documented_status',
         'product': 'registration-product', 'part': 'p2', 'scope': 'p2',
         'source_status': 'synthetic registration probe', 'status': dict(DRAFT)}]


def _t12_case():
    records, checks, queries = [], [], []
    base = s.real_path()
    old_draft = s.version(base, 'draft-code')

    legacy_state, legacy_record = _ok(
        base, [{'op': 'advance_product', 'id': 'draft-code',
                'dimensions': {'completion': 'reported_migration_complete',
                               'implementation': 'reported_code_written',
                               'git': 'reported_committed'}}],
        ['SYN:t12-legacy-global-update'])
    legacy_projection = _legacy_item_projection(legacy_state)
    records.append({**legacy_record, 'label': 'legacy-global-update',
                    'observation': {'frozen_projection': {
                        item: legacy_projection[item] for item in ('6', '7', '9context')}}})
    raw_failure = {
        'description': 'The pre-fix projection copies one product dimension set to every part, so a notification-only update also reports unrelated drafts as complete.',
        'frozen_formula': "current.dimensions = product['dimensions'] for every S029 item",
        'legacy_projection': {item: legacy_projection[item] for item in ('6', '7', '9context')},
        'note': 'This is a reproduction of the old formula in memory, not a DSH event or a real worktree observation.'}

    corrected, rec = _ok(
        base, [{'op': 'advance_parts', 'id': 'draft-code',
                'parts': ['8_trigger_notifications'],
                'dimensions': {'completion': 'reported_migration_complete',
                               'implementation': 'reported_code_written',
                               'git': 'reported_committed'}}],
        ['SYN:t12-notification-complete'])
    part_view = s.part_progress(corrected, 'draft-code')
    observation = {
        'items': {item: _item_state(corrected, item) for item in ('6', '7', '8', '9context', '10')},
        'product': {'revision': s.version(corrected, 'draft-code')['revision'],
                    'dimensions': deepcopy(s.version(corrected, 'draft-code')['dimensions']),
                    'overall_state': s.version(corrected, 'draft-code').get('overall_state')},
        'part_progress': part_view,
        'goal_acceptance': s.version(corrected, 'goal')['acceptance'],
        'old_product_revision': {'revision': 1,
                                 'dimensions': deepcopy(old_draft['dimensions']),
                                 'parts': deepcopy(old_draft['parts'])}}
    records.append({**rec, 'label': 'notification-part-progress', 'observation': observation})
    checks += [
        _check('t12-notification-is-scoped',
               'Only the notification part advances; the other draft parts keep their draft dimensions.',
               {item: observation['items'][item]['dimensions'] for item in ('6', '7', '8', '9context')},
               all(observation['items'][item]['dimensions'] == old_draft['dimensions']
                   for item in ('6', '7', '9context'))
               and observation['items']['8']['dimensions']['completion'] == 'reported_migration_complete'),
        _check('t12-overall-not-accepted',
               'The product overall state is not silently complete and the goal is not accepted.',
               {'product_dimensions': observation['product']['dimensions'],
                'goal_acceptance': observation['goal_acceptance'],
                'derived': part_view['overall']},
               observation['product']['dimensions']['acceptance'] == 'pending'
               and observation['product']['dimensions']['completion'] == 'unknown'
               and observation['goal_acceptance'] == 'pending'
               and part_view['overall']['completion'] == 'unknown'),
        _check('t12-first-subdivision-initializes-from-old-state',
               'The first subdivision keeps the original shared state as every part state before applying the named part.',
               observation['part_progress'],
               observation['part_progress']['source_revision'] == 1
               and observation['part_progress']['parts']['9_context_hiding']['dimensions'] == old_draft['dimensions']),
        _check('t12-old-product-version-preserved',
               'The exact old product revision with the shared dimensions and part presence remains readable.',
               observation['old_product_revision'],
               s.version(corrected, 'draft-code', 1) == old_draft),
        _check('t12-part-state-is-single-authority',
               'Each S029 item projects its own part state after subdivision, not the product aggregate.',
               {item: observation['items'][item]['dimensions'] for item in ('6', '8')},
               observation['items']['6']['dimensions']['completion'] == 'incomplete'
               and observation['items']['8']['dimensions']['completion'] == 'reported_migration_complete'
               and observation['items']['8']['product_dimensions']['completion'] == 'unknown'),
    ]
    queries.append(_query(
        's029_items-after-notification', "t12_study.s029_items(state)",
        {'items': {item: _item_state(corrected, item) for item in ('6', '7', '8', '9context')}},
        'Which part moved and which drafts stayed unchanged?'))
    queries.append(_query(
        'part_progress', "t12_study.part_progress(state, 'draft-code')", part_view,
        'What is the derived overall state and where does it come from?'))

    regressed, rec = _ok(
        corrected, [{'op': 'advance_parts', 'id': 'draft-code', 'parts': ['8_trigger_notifications'],
                     'dimensions': {'completion': 'incomplete', 'git': 'unstaged'}}],
        ['SYN:t12-legal-regression'])
    revision_before = observation['product']['revision']
    records.append({**rec, 'label': 'legal-part-regression',
                    'observation': {'items': {item: _item_state(regressed, item) for item in ('8', '9context')},
                                    'old_revision_readable': s.version(regressed, 'draft-code', revision_before)['part_states']['8_trigger_notifications']}})
    checks.append(_check(
        't12-legal-regression-keeps-history', 'A part may legally move backwards while the prior exact product revision stays readable.',
        {'item8': _item_state(regressed, '8')['dimensions'],
         'old_revision': s.version(regressed, 'draft-code', revision_before)['part_states']['8_trigger_notifications']},
        _item_state(regressed, '8')['dimensions']['completion'] == 'incomplete'
        and s.version(regressed, 'draft-code', revision_before)['part_states']['8_trigger_notifications']['completion'] == 'reported_migration_complete'))

    full_parts = sorted(s.version(corrected, 'draft-code')['part_states'])
    global_state, rec = _ok(
        corrected, [{'op': 'advance_product', 'id': 'draft-code', 'parts': full_parts,
                     'dimensions': {'git': 'reported_committed'}}],
        ['SYN:t12-global-full-range'])
    records.append({**rec, 'label': 'global-advance-full-range',
                    'observation': {'parts': {p: s.part_progress(global_state, 'draft-code')['parts'][p]['dimensions']
                                              for p in full_parts},
                                    'overall': s.part_progress(global_state, 'draft-code')['overall']}})
    checks.append(_check(
        't12-global-advance-needs-whole-range',
        'The global advance_product writes all active parts only when the whole explicit part range is named.',
        {'parts': full_parts, 'overall': s.part_progress(global_state, 'draft-code')['overall']},
        all(s.part_progress(global_state, 'draft-code')['parts'][p]['dimensions']['git'] == 'reported_committed'
            for p in full_parts)
        and s.part_progress(global_state, 'draft-code')['overall']['git'] == 'reported_committed'))

    for label, action in [
        ('global-omit-range', {'op': 'advance_product', 'id': 'draft-code',
                               'dimensions': {'git': 'reported_committed'}}),
        ('global-partial-range', {'op': 'advance_product', 'id': 'draft-code',
                                  'parts': ['9_context_hiding'],
                                  'dimensions': {'git': 'reported_committed'}}),
        ('global-acceptance', {'op': 'advance_product', 'id': 'draft-code',
                               'parts': full_parts, 'dimensions': {'acceptance': 'accepted'}}),
        ('unknown-part', {'op': 'advance_parts', 'id': 'draft-code',
                          'parts': ['missing-part'], 'dimensions': {'git': 'reported_committed'}}),
        ('part-acceptance', {'op': 'advance_parts', 'id': 'draft-code',
                             'parts': ['9_context_hiding'], 'dimensions': {'acceptance': 'accepted'}})]:
        records.append({**_reject(corrected, [action], ['SYN:t12-negative']), 'label': label})
    checks += [
        _check('t12-global-ambiguous-rejected',
               'Omitting the range or naming only one part on a subdivided product is rejected.',
               {'omit': records[-5]['response'], 'partial': records[-4]['response']},
               'whole explicit part range' in records[-5]['response']['error']
               and 'whole explicit part range' in records[-4]['response']['error']),
        _check('t12-no-direct-acceptance', 'Neither the global nor the part entry can accept a product.',
               {'global': records[-3]['response'], 'part': records[-1]['response']},
               records[-3]['response']['status'] == 'rejected'
               and records[-1]['response']['status'] == 'rejected'),
        _check('t12-unknown-part-rejected', 'An unknown part is rejected without creating state.',
               records[-2]['response'], records[-2]['response']['status'] == 'rejected'),
    ]
    before = deepcopy(corrected)
    atomic, rec = _run(corrected, [
        {'op': 'advance_parts', 'id': 'draft-code', 'parts': ['6_keep_open_after_cancel_failure'],
         'dimensions': {'git': 'reported_committed'}},
        {'op': 'advance_parts', 'id': 'draft-code', 'parts': ['missing-part'],
         'dimensions': {'git': 'reported_committed'}}], ['SYN:t12-atomic'])
    records.append({**rec, 'label': 'atomic-part-batch',
                    'observation': {'head': atomic['state']['head'], 'unchanged': atomic['state'] == before}})
    checks.append(_check(
        't12-atomic-rollback', 'A late invalid part update rolls back the earlier valid part update in the same batch.',
        {'status': atomic['status'], 'unchanged': atomic['state'] == before},
        atomic['status'] == 'rejected' and atomic['state'] == before))

    registration = _registration_state()
    registered, rec = _ok(registration, [{'op': 'register_items',
                                          'items': _registration_items({
                                              'completion': 'reported_migration_complete',
                                              'implementation': 'reported_code_written',
                                              'git': 'reported_committed', 'acceptance': 'pending'})}],
                          ['SYN:t12-register-matching-part'])
    records.append({**rec, 'label': 'register-matching-part-status',
                    'observation': {item: _item_state(registered, item) for item in ('registration-1', 'registration-2')}})
    mismatch = _reject(registration, [{'op': 'register_items',
                                       'items': _registration_items(dict(DRAFT))}],
                       ['SYN:t12-register-mismatch'])
    records.append({**mismatch, 'label': 'register-part-mismatch'})
    checks += [
        _check('t12-registration-obeys-part-authority',
               'register_items accepts item status that agrees with its own part state and rejects the shared-product projection.',
               {'matching': registered['items']['registration-1']['status'], 'mismatch': mismatch['response']},
               'registration-1' in registered['items'] and mismatch['response']['status'] == 'rejected'),
    ]
    return {'id': 'T12-part-progress', 'requirement': 'Explicit part-scoped progress with one authority',
            'source_facts': ['T12.04', 'T12.05', 'T12.06'],
            'raw_failure': raw_failure, 'records': records, 'queries': queries, 'checks': checks}


def _t03_state():
    state = s.fresh()
    state, rec0 = _ok(state, [
        {'op': 'goal', 'id': 't03-goal',
         'scope': ['LogicalSession storage rebuild and streaming session-format migration']},
        {'op': 'plan', 'id': 't03-plan', 'owner': 't03-goal', 'sections': {
            'stage1': {'status': 'draft_work_complete', 'description': 'stage 1 draft work complete'},
            'stage2': {'status': 'draft_work_complete', 'description': 'stage 2 draft work complete'},
            'stage3': {'status': 'draft_with_implementation_and_remote_ci',
                       'description': 'stage 3 records implementation and remote CI but is still draft'},
            'stage4': {'status': 'incomplete', 'description': 'stage 4 incomplete'},
            'stage5': {'status': 'incomplete', 'description': 'stage 5 incomplete'}}}],
        ['T03.06'], 'source_record')
    state, rec1 = _ok(state, [
        {'op': 'report', 'id': 't03-earlier', 'subject': {'id': 't03-plan', 'revision': 1},
         'scope': 'earlier merge and revert', 'findings': [
             'T03.01 main merged #2698 described as a streaming-format migration pipeline',
             'T03.02 the same day #3054 reverted the pipeline; reason unknown'],
         'nature': 'documented', 'content_kind': 'observation', 'scope_ids': ['T03:earlier-attempt']},
        {'op': 'report', 'id': 't03-perf', 'subject': {'id': 't03-plan', 'revision': 1},
         'scope': 'whole-file conversion performance', 'findings': [
             'T03.04 author reports a 116 MB session exhausted a 16 GB Node process'],
         'nature': 'author_report', 'content_kind': 'observation', 'scope_ids': ['T03:conversion-performance']},
        {'op': 'report', 'id': 't03-arrangement', 'subject': {'id': 't03-plan', 'revision': 1},
         'scope': 'stateful conversion arrangement', 'findings': [
             'T03.05 per-session stateful stages; committed files kept; publish only the final generation'],
         'nature': 'documented', 'content_kind': 'observation', 'scope_ids': ['T03:conversion-arrangement']}],
        ['T03.01', 'T03.02', 'T03.04', 'T03.05'], 'source_record')
    state, rec2 = _ok(state, [
        {'op': 'begin', 'id': 't03-streaming', 'goal': 't03-goal',
         'scope': ['later streaming migration implementation (#3585)'],
         'plan': {'id': 't03-plan', 'revision': 1}, 'location': 'S042 commit record'}],
        ['T03.03'], 'source_record')
    state, rec3 = _ok(state, [
        {'op': 'produce', 'id': 't03-streaming-code', 'attempt': 't03-streaming',
         'parts': ['streaming-migration'], 'dimensions': {
             'completion': 'in_progress', 'implementation': 'reported_implemented',
             'git': 'reported_committed', 'acceptance': 'pending'},
         'location': 'S042 commit record', 'nature': 'documented'}],
        ['T03.03'], 'source_record')
    state, rec4 = _ok(state, [
        {'op': 'report', 'id': 't03-impl', 'subject': s.actual_ref(state, 't03-streaming-code'),
         'scope': 'later streaming migration implementation', 'findings': [
             'T03.03 #3585 is the later streaming migration implementation; correspondence and reuse unknown'],
         'nature': 'documented', 'content_kind': 'observation', 'scope_ids': ['T03:streaming-implementation']},
        {'op': 'report', 'id': 't03-status', 'subject': {'id': 't03-plan', 'revision': 1},
         'scope': 'LogicalSession rebuild stage status', 'findings': [
             'T03.06 proposed: stages 1/2 draft work complete; stage 3 implementation and remote CI but draft; stages 4/5 incomplete'],
         'nature': 'documented', 'content_kind': 'observation', 'scope_ids': ['T03:rebuild-stages']},
        {'op': 'plan', 'id': 't03-attempt-plan', 'owner': 't03-streaming',
         'sections': {'streaming': {'status': 'recorded_arrangement',
                                    'description': 'attempt-owned plan compatibility'}}}],
        ['T03.06'], 'source_record')
    return state, [{**rec0, 'label': 't03-goal-and-plan'},
                   {**rec1, 'label': 't03-source-observations'},
                   {**rec2, 'label': 't03-known-implementation-attempt'},
                   {**rec3, 'label': 't03-streaming-product'},
                   {**rec4, 'label': 't03-reports-and-attempt-plan'}]


def _t03_case():
    state, records = _t03_state()
    plan = s.version(state, 't03-plan')
    rejection = _reject(state, [{'op': 'accept_goal', 'id': 't03-goal', 'actor_role': 'acceptor',
                                 'actor': 'synthetic-reviewer',
                                 'criteria': ['plan report alone'], 'decision': 'accept',
                                 'evidence': [s.actual_ref(state, 't03-status')]}],
                        ['SYN:t03-plan-report-not-acceptance'])
    records.append({**rejection, 'label': 'plan-report-cannot-accept-goal'})
    attempt_ids = sorted(oid for oid, obj in state['objects'].items() if obj['kind'] == 'attempt')
    checks = [
        _check('t03-goal-owned-plan', 'A plan may be owned directly by a Goal without fabricating an active attempt.',
               {'owner': plan['owner'], 'attempts_after_plan_only': sorted(
                   oid for oid, obj in s.at(state, 1)['objects'].items() if obj['kind'] == 'attempt')},
               plan['owner'] == 't03-goal'
               and not [oid for oid, obj in s.at(state, 1)['objects'].items() if obj['kind'] == 'attempt']),
        _check('t03-goal-trace', 'One goal_of trace resolves plans owned by either a Goal or an Attempt.',
               {'goal_owned': s.goal_of(state, plan),
                'attempt_owned': s.goal_of(state, s.version(state, 't03-attempt-plan')),
                'attempt_goal': s.version(state, 't03-streaming')['goal']},
               s.goal_of(state, plan) == 't03-goal'
               and s.goal_of(state, s.version(state, 't03-attempt-plan')) == 't03-goal'),
        _check('t03-known-implementation-attempt-only',
               'Only the documented later implementation gets an Attempt; the earlier merge/revert has none.',
               {'attempts': attempt_ids, 'earlier_evidence_subject': s.version(state, 't03-earlier')['subject']},
               attempt_ids == ['t03-streaming']
               and s.version(state, 't03-earlier')['subject']['id'] == 't03-plan'),
        _check('t03-plan-report-subject',
               'An exact plan revision is a legal report subject and the report remains evidence, not acceptance.',
               {'report': s.version(state, 't03-status'), 'goal_acceptance': s.version(state, 't03-goal')['acceptance']},
               s.version(state, 't03-status')['subject'] == {'id': 't03-plan', 'revision': 1}
               and s.version(state, 't03-goal')['acceptance'] == 'pending'),
        _check('t03-plan-report-cannot-accept',
               'Acceptance cannot use a plan-subject report as its evidence.',
               rejection['response'], rejection['response']['status'] == 'rejected'),
        _check('t03-stage-status-separate',
               'Stage 1/2/3/4/5 statuses stay in the plan and are not converted into Goal acceptance.',
               {'sections': deepcopy(plan['sections']), 'acceptance': s.version(state, 't03-goal')['acceptance']},
               plan['sections']['stage1']['status'] == 'draft_work_complete'
               and plan['sections']['stage3']['status'] == 'draft_with_implementation_and_remote_ci'
               and plan['sections']['stage4']['status'] == 'incomplete'
               and s.version(state, 't03-goal')['acceptance'] == 'pending'),
        _check('t03-research-goal-label',
               'The Goal is a research-created annotation, not an upstream identity.',
               {'identity_origin': s.version(state, 't03-goal')['identity_origin'],
                'origin': s.version(state, 't03-goal')['origin']},
               s.version(state, 't03-goal')['identity_origin'] == 'researcher_created'),
        _check('t03-old-owner-attempt-compatible',
               'A plan owned by an Attempt still saves and resolves through the same path.',
               {'saved': s.current_plan(state, 't03-attempt-plan')['owner']},
               s.current_plan(state, 't03-attempt-plan')['owner'] == 't03-streaming'),
    ]
    queries = [
        _query('plan-subject-report', "t12_study.version(state, 't03-status')",
               s.version(state, 't03-status'), 'Can a plan version be a report subject?'),
        _query('goal-of-plan', "t12_study.goal_of(state, t12_study.version(state, 't03-plan'))",
               s.goal_of(state, plan), 'Which Goal owns a Goal-owned plan?'),
        _query('stage-sections', "t12_study.current_plan(state, 't03-plan')['sections']",
               s.current_plan(state, 't03-plan')['sections'], 'Which stage has implementation but remains draft?'),
    ]
    return {'id': 'T03-plan-owner', 'requirement': 'Plan owner may be Goal or Attempt with one goal trace',
            'source_facts': ['T03.01', 'T03.02', 'T03.03', 'T03.04', 'T03.05', 'T03.06'],
            'raw_failure': None, 'records': records, 'queries': queries, 'checks': checks}


def _t13_state():
    state = s.fresh()
    state, rec0 = _ok(state, [
        {'op': 'goal', 'id': 't13-goal', 'scope': ['Windows terminal readiness failure and correction']},
        {'op': 'begin', 'id': 't13-work', 'goal': 't13-goal',
         'scope': ['Windows PTY terminal allocation'], 'location': 'S002/S009/S010'}],
        ['SYN:t13-setup'])
    prior_scope = list(T13_SCOPES['prior'])
    correction_scope = list(T13_SCOPES['correction'])
    state, rec1 = _ok(state, [
        {'op': 'report', 'id': 't13-tail-delay', 'subject': s.actual_ref(state, 't13-work'),
         'scope': 'self-hosted Windows readiness failure', 'findings': [
             'T13.01 early explanation: readiness failure is prompt-tail delay, addressed by waiting grace'],
         'nature': 'author_report', 'content_kind': 'interpretation', 'scope_ids': prior_scope}],
        ['T13.01'], 'source_record')
    state, rec2 = _ok(state, [
        {'op': 'report', 'id': 't13-measurement', 'subject': s.actual_ref(state, 't13-work'),
         'scope': 'Windows readiness measurement and console probe', 'findings': [
             'T13.02 20.8 seconds before and after the fix; waiting grace did not solve this failure',
             'T13.03 host console rewrites the tail after scrolling; the arrived string cannot satisfy the wait'],
         'nature': 'author_report', 'content_kind': 'observation', 'scope_ids': prior_scope}],
        ['T13.02', 'T13.03'], 'source_record')
    state, rec3 = _ok(state, [
        {'op': 'correct_interpretation', 'id': 't13-console-rewrite',
         'prior': s.actual_ref(state, 't13-tail-delay'),
         'scope': 'the measured self-hosted Windows readiness failure only',
         'scope_ids': correction_scope,
         'findings': ['This failure is caused by the host console rewriting the tail after scrolling; '
                      'the readiness wait cannot match the arrived string. Windows PTY now uses bundled OpenConsole.'],
         'basis': ['T13.02', 'T13.03'], 'nature': 'documented'}],
        ['T13.02', 'T13.03'], 'source_record')
    state, rec4 = _ok(state, [
        {'op': 'report', 'id': 't13-decision', 'subject': s.actual_ref(state, 't13-work'),
         'scope': 'bundled console decision', 'findings': [
             'T13.04 Windows PTY uses node-pty bundled OpenConsole; seven normal prompts are only an author report'],
         'nature': 'author_report', 'content_kind': 'decision', 'scope_ids': correction_scope},
        {'op': 'report', 'id': 't13-dependency', 'subject': s.actual_ref(state, 't13-work'),
         'scope': 'desktop terminal allocation dependency', 'findings': [
             'T13.05 the desktop package retains bundled OpenConsole and conpty.dll; other hosts and POSIX scoped separately'],
         'nature': 'documented', 'content_kind': 'observation', 'scope_ids': correction_scope}],
        ['T13.04', 'T13.05'], 'source_record')
    return state, [{**rec0, 'label': 't13-setup'},
                   {**rec1, 'label': 't13-old-interpretation'},
                   {**rec2, 'label': 't13-measurements'},
                   {**rec3, 'label': 't13-correction'},
                   {**rec4, 'label': 't13-decision-and-dependency'}]


def _t13_two_scope_probe():
    """Synthetic A/B/C probe; it never stands in for any T13 source scope."""
    state = s.fresh()
    state, rec0 = _ok(state, [
        {'op': 'goal', 'id': 'syn-two-scope-goal', 'scope': ['synthetic two-scope probe']},
        {'op': 'begin', 'id': 'syn-two-scope-work', 'goal': 'syn-two-scope-goal',
         'scope': ['synthetic two-scope probe']}],
        ['SYN:two-scope'])
    state, rec1 = _ok(state, [
        {'op': 'report', 'id': 'syn-two-scope-old',
         'subject': s.actual_ref(state, 'syn-two-scope-work'),
         'scope': 'synthetic old interpretation explicitly covering A and B',
         'findings': ['synthetic old interpretation covering A and B'],
         'nature': 'synthetic', 'content_kind': 'interpretation',
         'scope_ids': [SYN_A, SYN_B]}],
        ['SYN:two-scope'])
    old_ref = s.actual_ref(state, 'syn-two-scope-old')
    state, rec2 = _ok(state, [
        {'op': 'correct_interpretation', 'id': 'syn-two-scope-fix-a', 'prior': old_ref,
         'scope': 'synthetic scope A only', 'scope_ids': [SYN_A],
         'findings': ['synthetic corrected interpretation A'],
         'basis': ['SYN:two-scope'], 'nature': 'synthetic'}],
        ['SYN:two-scope'])
    after_a = {'A': s.interpretations(state, SYN_A),
               'B': s.interpretations(state, SYN_B),
               'C': s.interpretations(state, SYN_C)}
    conflict = _reject(state, [
        {'op': 'correct_interpretation', 'id': 'syn-two-scope-conflict', 'prior': old_ref,
         'scope': 'synthetic conflicting scope A', 'scope_ids': [SYN_A],
         'findings': ['synthetic conflicting interpretation A'],
         'basis': ['SYN:two-scope'], 'nature': 'synthetic'}],
        ['SYN:two-scope'])
    state, rec3 = _ok(state, [
        {'op': 'correct_interpretation', 'id': 'syn-two-scope-fix-b', 'prior': old_ref,
         'scope': 'synthetic scope B only', 'scope_ids': [SYN_B],
         'findings': ['synthetic corrected interpretation B'],
         'basis': ['SYN:two-scope'], 'nature': 'synthetic'}],
        ['SYN:two-scope'])
    after_b = s.interpretations(state, SYN_B)
    fix_a_ref = s.actual_ref(state, 'syn-two-scope-fix-a')
    state, rec4 = _ok(state, [
        {'op': 'correct_interpretation', 'id': 'syn-two-scope-fix-a2', 'prior': fix_a_ref,
         'scope': 'synthetic further correction of A', 'scope_ids': [SYN_A],
         'findings': ['synthetic further corrected interpretation A'],
         'basis': ['SYN:two-scope'], 'nature': 'synthetic'}],
        ['SYN:two-scope'])
    after_chain = s.interpretations(state, SYN_A)
    records = [{**rec0, 'label': 'synthetic-two-scope-setup'},
               {**rec1, 'label': 'synthetic-two-scope-old'},
               {**rec2, 'label': 'synthetic-two-scope-correct-a'},
               {**conflict, 'label': 'synthetic-two-scope-conflict-rejected'},
               {**rec3, 'label': 'synthetic-two-scope-correct-b'},
               {**rec4, 'label': 'synthetic-two-scope-correct-a-again'}]
    return state, records, {'after_a': after_a, 'after_b': after_b,
                            'after_chain': after_chain, 'conflict': conflict}


def _t13_case():
    state, records = _t13_state()
    covered = s.interpretations(state, T13_SCOPES['correction'][0])
    broader = s.interpretations(state, T13_SCOPES['never_asserted'][0])
    old = s.version(state, 't13-tail-delay', 1)
    before_old = deepcopy(old)
    bad = [
        ('missing-proposition', {'op': 'correct_interpretation', 'id': 't13-bad-missing',
                                'prior': {'id': 'missing-claim', 'revision': 1},
                                'scope': 'x', 'scope_ids': [T13_SCOPES['correction'][0]],
                                'findings': ['x'], 'basis': ['T13.02'], 'nature': 'synthetic'}),
        ('report-occurrence', {'op': 'correct_interpretation', 'id': 't13-bad-occurrence',
                               'prior': s.actual_ref(state, 't13-measurement'),
                               'scope': 'x', 'scope_ids': [T13_SCOPES['correction'][0]],
                               'findings': ['x'], 'basis': ['T13.02'], 'nature': 'synthetic'}),
        ('scope-expansion', {'op': 'correct_interpretation', 'id': 't13-bad-expand',
                             'prior': s.actual_ref(state, 't13-tail-delay'),
                             'scope': 'all delayed failures', 'scope_ids': T13_SCOPES['never_asserted'],
                             'findings': ['x'], 'basis': ['T13.02'], 'nature': 'synthetic'}),
        ('erase-occurrence', {'op': 'report', 'id': 't13-tail-delay',
                              'subject': s.actual_ref(state, 't13-work'),
                              'scope': 'replacement', 'findings': ['replacement'],
                              'nature': 'synthetic'}),
        ('generic-correction-field', {'op': 'report', 'id': 't13-bad-patch',
                                      'subject': s.actual_ref(state, 't13-work'),
                                      'scope': 'x', 'findings': ['x'], 'nature': 'synthetic',
                                      'corrects': s.actual_ref(state, 't13-tail-delay')}),
    ]
    for label, action in bad:
        records.append({**_reject(state, [action], ['SYN:t13-negative']), 'label': label})
    checks = [
        _check('t13-typing', 'Evidence content is classed as observation, interpretation or decision while remaining a subtype of Evidence.',
               {oid: s.version(state, oid).get('content_kind')
                for oid in ('t13-tail-delay', 't13-measurement', 't13-decision', 't13-dependency')},
               s.version(state, 't13-tail-delay')['content_kind'] == 'interpretation'
               and s.version(state, 't13-measurement')['content_kind'] == 'observation'
               and s.version(state, 't13-decision')['content_kind'] == 'decision'
               and all(s.version(state, oid)['kind'] == 'evidence'
                       for oid in ('t13-tail-delay', 't13-measurement', 't13-decision'))),
        _check('t13-covered-scope-corrected',
               'The corrected scope has a current interpretation, an exact correction relation and correction basis.',
               covered, covered['status'] == 'corrected'
               and covered['current']['evidence'] == {'id': 't13-console-rewrite', 'revision': 1}
               and covered['corrections'][0]['corrects'] == {'id': 't13-tail-delay', 'revision': 1}
               and covered['corrections'][0]['basis'] == ['T13.02', 'T13.03']),
        _check('t13-history-keeps-old-claim',
               'The old interpretation remains readable as history at its exact version.',
               {'history': covered['history'], 'old_revision': old},
               covered['history'][0]['evidence'] == {'id': 't13-tail-delay', 'revision': 1}
               and old == before_old),
        _check('t13-real-scope-only',
               'The real T13.01 proposition covers only the measured self-hosted failure; any broader class stays unknown, not source-attributed.',
               {'old_scope_ids': old['scope_ids'], 'fixture_prior': T13_SCOPES['prior'],
                'never_asserted': T13_SCOPES['never_asserted'],
                'fixture_timeout_claims': [fact['id'] for fact in FIXTURE['facts']
                                           if 'windows-ready-timeout-class' in fact['meaning']]},
               old['scope_ids'] == ['T13:windows-hosted-ready-failure']
               and T13_SCOPES['prior'] == ['T13:windows-hosted-ready-failure']
               and T13_SCOPES['never_asserted'] == ['UNKNOWN:all-delayed-failures']
               and not any('windows-ready-timeout-class' in fact['meaning']
                           for fact in FIXTURE['facts'])),
        _check('t13-never-asserted-scope-undetermined',
               'A broader failure class never asserted by the source has no current interpretation and no history.',
               broader, broader['status'] == 'undetermined' and not broader['history']),
        _check('t13-correction-scope-cannot-expand',
               'A correction that widens to all delayed failures is rejected.',
               records[-3]['response'], records[-3]['response']['status'] == 'rejected'),
        _check('t13-missing-proposition-rejected',
               'Correcting a nonexistent proposition is rejected without state.',
               records[-5]['response'], records[-5]['response']['status'] == 'rejected'),
        _check('t13-report-occurrence-not-correctable',
               'A report occurrence is not a correction target; only an interpretation proposition is.',
               records[-4]['response'], records[-4]['response']['status'] == 'rejected'),
        _check('t13-occurrence-not-erasable',
               'Reusing the old evidence identity to replace the report occurrence is rejected.',
               records[-2]['response'], records[-2]['response']['status'] == 'rejected'),
        _check('t13-no-generic-patch',
               'A generic correction field on report is rejected as an unsupported update.',
               records[-1]['response'], records[-1]['response']['status'] == 'rejected'),
        _check('t13-all-five-facts-retained',
               'All five T13 source facts are present in the source fixture and used by a real encoding change.',
               {'fixture': [fact['id'] for fact in FIXTURE['facts'] if fact['id'].startswith('T13.')],
                'used': sorted({b for c in state['changes'] for b in c['basis'] if b.startswith('T13.')})},
               {fact['id'] for fact in FIXTURE['facts'] if fact['id'].startswith('T13.')}
               == {'T13.01', 'T13.02', 'T13.03', 'T13.04', 'T13.05'}
               and {b for c in state['changes'] for b in c['basis'] if b.startswith('T13.')}
               == {'T13.01', 'T13.02', 'T13.03', 'T13.04', 'T13.05'}),
        _check('t13-seven-prompts-author-report',
               'The seven normal prompts remain attributed as an author report, not an independent verification.',
               {'fact': next(f for f in FIXTURE['facts'] if f['id'] == 'T13.04'),
                'decision_evidence': s.version(state, 't13-decision')['nature']},
               'author report' in next(f for f in FIXTURE['facts'] if f['id'] == 'T13.04')['meaning']
               and s.version(state, 't13-decision')['nature'] == 'author_report'),
    ]
    queries = [
        _query('interpretation-covered', "t12_study.interpretations(state, %r)" % T13_SCOPES['correction'][0],
               covered, 'What is the current interpretation and its correction basis?'),
        _query('interpretation-unasserted', "t12_study.interpretations(state, %r)" % T13_SCOPES['never_asserted'][0],
               broader, 'What is recorded for a failure class the source never asserted?'),
        _query('old-evidence', "t12_study.version(state, 't13-tail-delay', 1)", old,
               'Is the old report occurrence still readable unchanged?'),
    ]
    _, syn_records, syn = _t13_two_scope_probe()
    records += syn_records
    checks += [
        _check('syn-two-scope-a-corrected',
               'Correcting A puts only A on the new interpretation.',
               syn['after_a']['A'],
               syn['after_a']['A']['status'] == 'corrected'
               and syn['after_a']['A']['current']['evidence'] == {'id': 'syn-two-scope-fix-a', 'revision': 1}),
        _check('syn-two-scope-b-preserved',
               'The already-recorded B keeps the old interpretation while only A is corrected.',
               syn['after_a']['B'],
               syn['after_a']['B']['status'] == 'recorded'
               and syn['after_a']['B']['current']['evidence'] == {'id': 'syn-two-scope-old', 'revision': 1}
               and [row['evidence']['id'] for row in syn['after_a']['B']['history']] == ['syn-two-scope-old']
               and syn['after_a']['B']['corrections'] == []),
        _check('syn-two-scope-c-undetermined',
               'A scope that was never recorded stays undetermined with no history.',
               syn['after_a']['C'],
               syn['after_a']['C']['status'] == 'undetermined'
               and syn['after_a']['C']['current'] is None
               and syn['after_a']['C']['history'] == []),
        _check('syn-two-scope-independent-b',
               'The second correction on the disjoint B scope is legal and keeps both recorded steps.',
               syn['after_b'],
               syn['after_b']['status'] == 'corrected'
               and syn['after_b']['current']['evidence'] == {'id': 'syn-two-scope-fix-b', 'revision': 1}
               and [row['evidence']['id'] for row in syn['after_b']['history']]
               == ['syn-two-scope-old', 'syn-two-scope-fix-b']),
        _check('syn-two-scope-conflict-rejected',
               'A sibling correction reusing the old prior on already-corrected A is rejected; no last write wins.',
               syn['conflict']['response'],
               syn['conflict']['response']['status'] == 'rejected'
               and syn['conflict']['response'].get('state_unchanged') is True
               and 'current interpretation' in syn['conflict']['response']['error']),
        _check('syn-two-scope-chain-allowed',
               'Correcting the new A interpretation is a legal further step.',
               syn['after_chain'],
               syn['after_chain']['status'] == 'corrected'
               and syn['after_chain']['current']['evidence'] == {'id': 'syn-two-scope-fix-a2', 'revision': 1}
               and [row['evidence']['id'] for row in syn['after_chain']['history']]
               == ['syn-two-scope-old', 'syn-two-scope-fix-a', 'syn-two-scope-fix-a2']),
    ]
    queries += [
        _query('syn-two-scope-a', "t12_study.interpretations(state, %r)" % SYN_A,
               syn['after_a']['A'], 'Which interpretation is current in the corrected A scope?'),
        _query('syn-two-scope-b', "t12_study.interpretations(state, %r)" % SYN_B,
               syn['after_a']['B'], 'What remains recorded for B while only A is corrected?'),
        _query('syn-two-scope-c', "t12_study.interpretations(state, %r)" % SYN_C,
               syn['after_a']['C'], 'What is recorded for a scope never asserted?'),
        _query('syn-two-scope-chain', "t12_study.interpretations(state, %r)" % SYN_A,
               syn['after_chain'], 'Can the new interpretation in A be corrected again?'),
    ]
    return {'id': 'T13-scoped-interpretation', 'requirement': 'Citable evidence types and scoped correction',
            'source_facts': ['T13.01', 'T13.02', 'T13.03', 'T13.04', 'T13.05'],
            'raw_failure': None, 'records': records, 'queries': queries, 'checks': checks}


def _t15_state():
    state = s.fresh()
    state, rec0 = _ok(state, [
        {'op': 'goal', 'id': 't15-goal', 'scope': ['Office conversion and desktop delivery']},
        {'op': 'begin', 'id': 't15-delivery', 'goal': 't15-goal',
         'scope': ['Harness adapter, kit release and desktop runtime delivery'],
         'location': 'S017/S018/S024'}],
        ['SYN:t15-setup'])
    state, rec1 = _ok(state, [
        {'op': 'produce', 'id': 't15-harness', 'attempt': 't15-delivery',
         'parts': ['adapter', 'authorization', 'conversion_lifecycle', 'ui'],
         'dimensions': dict(UNKNOWN), 'location': 'S017 documented dependency', 'nature': 'documented'},
        {'op': 'produce', 'id': 't15-kit', 'attempt': 't15-delivery',
         'parts': ['api', 'engine', 'tests', 'release'],
         'dimensions': dict(UNKNOWN), 'location': 'S017 documented dependency', 'nature': 'documented'},
        {'op': 'produce', 'id': 't15-desktop', 'attempt': 't15-delivery',
         'parts': ['interpreter', 'libraries'],
         'dimensions': dict(UNKNOWN), 'location': 'S024 documented state', 'nature': 'documented'}],
        ['T15.03', 'T15.04'], 'source_record')
    state, rec2 = _ok(state, [
        {'op': 'report', 'id': 't15-kit-boundary', 'subject': s.actual_ref(state, 't15-kit'),
         'scope': 'independent kit ownership and Harness adapter scope', 'findings': [
             'T15.03 kit owns API, engine, tests and release; Harness owns adapter, authorization, lifecycle and UI and locks the exact npm version'],
         'nature': 'documented'},
        {'op': 'report', 'id': 't15-desktop-payload', 'subject': s.actual_ref(state, 't15-desktop'),
         'scope': 'release-bound desktop runtime payload', 'findings': [
             'T15.04 interpreter and libraries ship as a release-bound payload with recorded version and locked input digest; stage before replace'],
         'nature': 'documented'},
        {'op': 'report', 'id': 't15-limit', 'subject': s.actual_ref(state, 't15-harness'),
         'scope': 'bounded conversion and separate checks', 'findings': [
             'T15.05 limits do not cover engine RSS or caller-retained output; signature and final run checks are separate; run success follows the author record'],
         'nature': 'documented'}],
        ['T15.03', 'T15.04', 'T15.05'], 'source_record')
    state, rec3 = _ok(state, [
        {'op': 'relate_exact', 'id': 'T15.dep.harness-kit',
         'kind': 'delivery_dependency',
         'from': {'object': 't15-harness', 'revision': 1, 'scope': 'adapter'},
         'to': {'object': 't15-kit', 'revision': 1, 'scope': 'release'},
         'scope': 'Harness adaptation and conversion lifecycle lock the exact kit npm release',
         'basis': ['T15.03'], 'nature': 'documented_dependency',
         'external': {'name': 'libreoffice-kit-npm'}},
        {'op': 'relate_exact', 'id': 'T15.dep.desktop-kit',
         'kind': 'delivery_dependency',
         'from': {'object': 't15-desktop', 'revision': 1, 'scope': 'interpreter'},
         'to': {'object': 't15-kit', 'revision': 1, 'scope': 'release'},
         'scope': 'Desktop release-bound runtime records version and locked input digest',
         'basis': ['T15.04'], 'nature': 'documented_dependency',
         'external': {'name': 'desktop-runtime-payload'}}],
        ['T15.03', 'T15.04'], 'source_record')
    return state, [{**rec0, 'label': 't15-setup'},
                   {**rec1, 'label': 't15-products'},
                   {**rec2, 'label': 't15-source-reports'},
                   {**rec3, 'label': 't15-exact-relations'}]


def _t15_case():
    state, records = _t15_state()
    fixed = deepcopy(state['relations'])
    current = s.relation_status(state, 'T15.dep.harness-kit')
    updated, rec = _ok(state, [{'op': 'advance_product', 'id': 't15-harness',
                               'dimensions': {'implementation': 'reported_implemented'}}],
                       ['SYN:t15-result-update'])
    after = deepcopy(updated['relations'])
    status_after = s.relation_status(updated, 'T15.dep.harness-kit')
    desktop_after = s.relation_status(updated, 'T15.dep.desktop-kit')
    records.append({**rec, 'label': 'synthetic-result-update',
                    'observation': {'harness_revision': s.version(updated, 't15-harness')['revision'],
                                    'relation_before': fixed['T15.dep.harness-kit'],
                                    'relation_after': after['T15.dep.harness-kit'],
                                    'relation_status': status_after,
                                    'desktop_relation_status': desktop_after}})
    t12 = s.real_path()
    old_relation = s.relation_status(t12, 'S029.dep.9context-on-8')
    t12_after, t12_rec = _ok(t12, [{'op': 'advance_parts', 'id': 'draft-code',
                                    'parts': ['8_trigger_notifications'],
                                    'dimensions': {'git': 'reported_committed'}}],
                             ['SYN:t12-relation-compat'])
    old_after = s.relation_status(t12_after, 'S029.dep.9context-on-8')
    records.append({**t12_rec, 'label': 'legacy-relation-compat',
                    'observation': {'before': t12['relations']['S029.dep.9context-on-8'],
                                    'after': t12_after['relations']['S029.dep.9context-on-8'],
                                    'status': old_after}})
    bad = [
        ('missing-revision', {'op': 'relate_exact', 'id': 'T15.bad.missing',
                              'kind': 'delivery_dependency',
                              'from': {'object': 't15-harness', 'scope': 'adapter'},
                              'to': {'object': 't15-kit', 'revision': 1, 'scope': 'release'},
                              'scope': 'x', 'basis': ['T15.03'],
                              'nature': 'documented_dependency', 'external': {'name': 'kit'}}),
        ('blank-external-version', {'op': 'relate_exact', 'id': 'T15.bad.external',
                                    'kind': 'delivery_dependency',
                                    'from': {'object': 't15-harness', 'revision': 1, 'scope': 'adapter'},
                                    'to': {'object': 't15-kit', 'revision': 1, 'scope': 'release'},
                                    'scope': 'x', 'basis': ['T15.03'],
                                    'nature': 'documented_dependency',
                                    'external': {'name': 'kit', 'version': '  '}}),
        ('unknown-scope', {'op': 'relate_exact', 'id': 'T15.bad.scope',
                           'kind': 'delivery_dependency',
                           'from': {'object': 't15-harness', 'revision': 1, 'scope': 'missing'},
                           'to': {'object': 't15-kit', 'revision': 1, 'scope': 'release'},
                           'scope': 'x', 'basis': ['T15.03'],
                           'nature': 'documented_dependency', 'external': {'name': 'kit'}}),
    ]
    for label, action in bad:
        records.append({**_reject(state, [action], ['SYN:t15-negative']), 'label': label})
    checks = [
        _check('t15-exact-endpoints',
               'The delivery relation stores object, exact revision and scope at both ends.',
               fixed['T15.dep.harness-kit'],
               fixed['T15.dep.harness-kit']['from'] == {'object': 't15-harness', 'revision': 1, 'scope': 'adapter'}
               and fixed['T15.dep.harness-kit']['to'] == {'object': 't15-kit', 'revision': 1, 'scope': 'release'}),
        _check('t15-unknown-external-values',
               'External version and digest stay unknown when the fixed base gives no value.',
               fixed['T15.dep.harness-kit']['external'],
               fixed['T15.dep.harness-kit']['external'] == {'name': 'libreoffice-kit-npm',
                                                            'version': 'unknown', 'digest': 'unknown'}),
        _check('t15-current-before-update', 'The unchanged exact endpoints read as current before the synthetic update.',
               current, current['status'] == 'current'),
        _check('t15-no-drift-after-update',
               'A later product revision does not move the stored dependency endpoints.',
               {'before': fixed['T15.dep.harness-kit'], 'after': after['T15.dep.harness-kit']},
               fixed['T15.dep.harness-kit'] == after['T15.dep.harness-kit']),
        _check('t15-needs-recheck-not-incompatible',
               'The updated endpoint produces needs_recheck, not an automatic engineering incompatibility.',
               status_after,
               status_after['status'] == 'needs_recheck'
               and status_after['automatic_compatibility_conclusion'] is None
               and status_after['endpoints'][0]['current_revision'] == 2
               and status_after['endpoints'][0]['stored']['revision'] == 1),
        _check('t15-unrelated-relation-current',
               'A relation whose endpoints did not change still reads as current.',
               desktop_after, desktop_after['status'] == 'current'),
        _check('t15-legacy-product-requirement-preserved',
               'The old S029 product_requirement relations remain byte-identical after a T12 part update.',
               {'before': t12['relations']['S029.dep.9context-on-8'],
                'after': t12_after['relations']['S029.dep.9context-on-8']},
               t12['relations']['S029.dep.9context-on-8']
               == t12_after['relations']['S029.dep.9context-on-8']),
        _check('t15-legacy-relation-review-status',
               'A scope-only legacy relation needs explicit review and is never auto-declared incompatible.',
               old_after, old_after['status'] == 'needs_explicit_recheck'
               and old_after['automatic_compatibility_conclusion'] is None),
        _check('t15-exact-relation-rejects-bad-input',
               'Missing revision, a blank external version and an unknown scope are rejected.',
               {label: records[-(3 - index)]['response'] for index, label in enumerate(
                   ('missing-revision', 'blank-external-version', 'unknown-scope'))},
               all(records[-(3 - index)]['response']['status'] == 'rejected' for index in range(3))),
    ]
    queries = [
        _query('fixed-dependency', "state['relations']['T15.dep.harness-kit']",
               fixed['T15.dep.harness-kit'], 'Which exact revisions and scope are fixed?'),
        _query('relation-after-update', "t12_study.relation_status(state, 'T15.dep.harness-kit')",
               status_after, 'What changes and what does not after a result update?'),
        _query('legacy-relation-status', "t12_study.relation_status(state, 'S029.dep.9context-on-8')",
               old_after, 'How is an old scope-only requirement relation read now?'),
    ]
    return {'id': 'T15-exact-delivery-dependency', 'requirement': 'Delivery dependency fixed to exact revisions and scope',
            'source_facts': ['T15.03', 'T15.04', 'T15.05'],
            'raw_failure': None, 'records': records, 'queries': queries, 'checks': checks}


def _build_cases():
    return [_t12_case(), _t03_case(), _t13_case(), _t15_case()]


def _fact_index():
    facts = deepcopy(s.FIXTURE['facts'] + s.FIXTURE['supplements'] + FIXTURE['facts'])
    sources = {**deepcopy(s.FIXTURE['sources']), **deepcopy(FIXTURE['sources'])}
    return facts, sources


def build_results():
    cases = _build_cases()
    checks = [check for case in cases for check in case['checks']]
    failed = [check['id'] for check in checks if not check['ok']]
    facts, sources = _fact_index()
    return {
        'schema': 1,
        'batch': BATCH,
        'slice': SLICE,
        'generated_by': 't12_boundary_checks.build_results',
        'source_cutoff': s.FIXTURE['source_cutoff'],
        'source_facts': [{'id': fact['id'], 'source': fact['source'], 'nature': fact.get('nature')}
                         for fact in facts],
        'sources': sources,
        'cases': cases,
        'summary': {'checks': len(checks), 'failed': failed, 'ok': not failed},
        'separation': {'source_record': 'T03/T12/T13/T15 facts use source_record changes and the exact fixture basis',
                       'synthetic': 'probe operations use SYN: basis and synthetic nature; they are not DSH events',
                       'excluded': 'no conversion job, reader ref-count, model call, Git command or final five-class decision'}}


def _readback_records(cases):
    rows = []
    for case in cases:
        for record in case['records']:
            if record['response']['status'] != 'applied':
                continue
            observation = deepcopy(record.get('observation'))
            if isinstance(observation, dict) and 'frozen_projection' in observation:
                # The pre-fix formula reproduction is study evidence, not saved state.
                observation = None
            rows.append({'case': case['id'], 'kind': 'saved_operation',
                         'label': record['label'], 'input': deepcopy(record['input']),
                         'response': deepcopy(record['response']),
                         'observation': observation})
        for query in case['queries']:
            rows.append({'case': case['id'], 'kind': 'question', 'name': query['name'],
                         'call': query['call'], 'question': query.get('question')})
    return rows


def build_readback():
    cases = _build_cases()
    facts, sources = _fact_index()
    return {
        'schema': 1,
        'batch': BATCH,
        'slice': SLICE,
        'generated_by': 't12_boundary_checks.build_readback',
        'operations': _operation_index(),
        'records': _readback_records(cases),
        'evidence': {'sources': sources,
                     'fact_sources': {fact['id']: [sid for sid in sources if sid in fact['source']]
                                      for fact in facts}},
        'scope_ids': deepcopy(T13_SCOPES),
        'synthetic_boundary': {'basis_prefix': 'SYN:', 'nature': 'synthetic',
                               'not_dsh_events': True, 'no_event_times': True,
                               'source_changes_use_exact_fixture_facts': True},
        'questions': [
            'T12: after only the notification part advances, which other draft items moved and what overall product/goal state is recorded?',
            'T12: what happens when the global advance_product entry omits the part range or names only one part on a subdivided product?',
            'T12: which exact product revision still shows the pre-subdivision shared dimensions?',
            'T03: can a Goal directly own a plan, and what evidence shows that no attempt was fabricated for the earlier merge/revert?',
            'T03: can a plan-subject report accept the Goal, and how are stage 1/2/3/4/5 statuses recorded separately?',
            'T13: for the corrected real scope, what is the current interpretation, its exact prior evidence and its basis?',
            'T13: in the synthetic two-scope probe, what remains recorded for B when only A is corrected, and what is recorded for the never-asserted C?',
            'T13: after the synthetic A correction, can the new interpretation be corrected again, and what happens to a conflicting sibling correction?',
            'T13: is the old report occurrence still readable at its exact version after correction?',
            'T15: which object revisions and scopes does the delivery dependency fix, and what external version/digest is recorded?',
            'T15: after a synthetic result update, what is the relation status and is any incompatibility asserted?',
            'T15: how do old scope-only product_requirement relations differ from new exact delivery dependencies?'],
        'representation_note': 'This is an operation-rule, applied saved-record, source-id and question entry only; it contains no expected answers, scoring, rejection probes, raw-failure reproduction or fact meanings.'}


def _operation_index():
    return [
        {'name': 'advance_parts', 'call': 't12_study.apply(state, [{"op":"advance_parts", ...}], head, basis)',
         'effect': 'first use copies the current shared product dimensions into every part, then updates only the named parts',
         'constraint': 'explicit unique known part list; completion/implementation/git only; legal regression allowed'},
        {'name': 'advance_product', 'call': 't12_study.apply(state, [{"op":"advance_product", ...}], head, basis)',
         'effect': 'before subdivision updates the shared dimensions; after subdivision updates every active part',
         'constraint': 'on a subdivided product, the whole explicit active part range is required or the batch is rejected'},
        {'name': 'part_progress', 'call': "t12_study.part_progress(state, product_id)",
         'effect': 'returns per-part dimensions and a derived overall view',
         'constraint': 'the overall view is derived from present parts; acceptance is copied from the product dimension, not propagated from part progress'},
        {'name': 's029_items', 'call': 't12_study.s029_items(state)',
         'effect': 'item current.dimensions is the item part state after subdivision and the shared product dimensions before it',
         'constraint': 'source record text is unchanged; current is a projection, not verification'},
        {'name': 'plan-owner', 'call': 't12_study.apply(state, [{"op":"plan","owner": goal_or_attempt, ...}], head, basis)',
         'effect': 'a plan may be stored under a Goal or an Attempt',
         'constraint': 'goal_of follows the owner chain; old Attempt-owned plans keep their path'},
        {'name': 'report-content-kind', 'call': 't12_study.apply(state, [{"op":"report","content_kind":...,"scope_ids":[...]}], head, basis)',
         'effect': 'evidence records a citable observation, interpretation or decision with stable scope ids',
         'constraint': 'the evidence is an attributed claim, not system-certified truth'},
        {'name': 'correct_interpretation', 'call': 't12_study.apply(state, [{"op":"correct_interpretation", ...}], head, basis)',
         'effect': 'adds a new interpretation evidence that names an exact prior evidence revision and a narrower scope id set',
         'constraint': 'only an interpretation proposition can be corrected; scope cannot expand; the prior must be the current interpretation of every named scope; disjoint scopes and chains are allowed, sibling conflicts are rejected; the old evidence is not edited'},
        {'name': 'interpretations', 'call': 't12_study.interpretations(state, scope_id)',
         'effect': 'returns current interpretation, history and correction basis; untouched scopes keep the old recorded interpretation',
         'constraint': 'a never-asserted scope stays undetermined; the query does not judge natural-language truth or certify a cause'},
        {'name': 'relate_exact', 'call': 't12_study.apply(state, [{"op":"relate_exact", ...}], head, basis)',
         'effect': 'stores a delivery dependency with object+revision+scope at both ends and external name/version/digest',
         'constraint': 'only delivery_dependency; missing external version/digest is recorded as unknown'},
        {'name': 'relation_status', 'call': 't12_study.relation_status(state, relation_id)',
         'effect': 'separates stored exact endpoints from current object revisions',
         'constraint': 'scope-only legacy relations need explicit recheck; moved exact endpoints need recheck; no automatic incompatibility'},
        {'name': 'readback', 'call': 't12_boundary_checks.build_readback()',
         'effect': 'operation definitions, saved records, evidence and questions',
         'constraint': 'no expected answers, scores, pass labels or truth excerpts'}]


def build_rules():
    return """# T12 boundary-v2 读取规则

本目录只记录 T03/T12/T13/T15 四个已裁定难点的可控实现与探针，不运行 DSH，不裁定五逻辑类，也不写主文。boundary-v1 保留为旧输出，本包不覆盖它。

## 合成边界

- 真实来源事实只来自 `dsh_object_boundary_fixture.json` 与既有 T12 fixture；来源 URL 与 revision 可在 `readback.json` 的 `evidence.sources` 查，事实只给 ID 到来源的索引，不附含义答案。
- 所有探针使用 `SYN:` basis 与 `synthetic` nature，不是 DSH 事件，没有事件时间。
- 研究者创建的对象 ID 与 Change 编号不是上游身份；Goal 的 `identity_origin` 明确标为 `researcher_created`。
- T13 的真实旧命题只覆盖 `T13:windows-hosted-ready-failure`；更广的失败类别保持未断言。双 scope 行为由 `SYN:two-scope-*` 探针单独验证，不补造历史。

## T12 局部进展

- `advance_parts` 首次使用时，把当时 Product 的共享维度复制到每个 part，然后只更新列明的 part。
- 细分后 item 的 `current.dimensions` 是该 part 的状态，唯一权威是 `part_states`；Product 的 `dimensions` 不再可独立写，整体只可由 `part_progress` 派生或保持 unknown。
- `part_progress` 的 acceptance 取自 Product 的 `dimensions.acceptance`，不是由 part progress 自动传播，也不自动等于 Goal 验收。
- `advance_product` 在细分后必须列明全部活动 part；省略或只给部分范围会被拒绝。回退是合法更新，旧 Product revision 按精确 revision 保留。
- S029 源记录不变；`current` 是状态投影，不是独立验收。

## T03 计划归属

- Plan 的 owner 可以是 Goal 或 Attempt；`goal_of` 沿 owner 链解析，旧 Attempt-owned Plan 路径保持。
- Plan 精确 revision 可以作为 report 的 subject，但计划报告不构成 Goal 验收；`accept_goal` 仍要求可追踪到同一 Goal 的 Attempt/Product subject。
- 只有来源记录明确实施时才建立 Attempt；T03 阶段状态保存在 Plan sections 中，不转写为 Goal 已验收。

## T13 证据内容与纠正

- Evidence 记录 `content_kind` 为 observation、interpretation 或 decision；它仍是有归属陈述，不是系统认证真理。
- `correct_interpretation` 创建新的 Evidence，精确引用旧 Evidence revision，并只在其 stable scope id 集合内生效。
- 纠正只替换它自己 scope 集合内的当前解释；旧命题覆盖但本次未纠正的 scope 继续显示旧的 `recorded` 解释，不因其他 scope 的纠正变为 undetermined。
- 从未断言的 scope 保持 `undetermined`，没有 history。
- 每个被纠正的 scope 必须仍以该 prior 为当前解释；同 scope 的兄弟纠正若没有冲突选择机制会被明确拒绝，不能由写入顺序决定胜者；对新解释继续纠正形成合法链。
- 旧 report 发生记录不修改；纠正不存在命题、纠正 report 发生记录、扩大 scope 或通用字段 patch 都会被拒绝。

## T15 精确交付依赖

- `relate_exact` 固定两端 object、revision、scope，并记录 external name、version、digest；固定底稿没有给出的版本或摘要记为 `unknown`。
- 后续成果更新不会移动旧关系；`relation_status` 只把未变端点读为 `current`，移动的端点读为 `needs_recheck`，并明确没有自动兼容结论。
- 旧 `product_requirement` 关系保留为 scope-only 历史，状态为 `needs_explicit_recheck`；不能由它自动宣布工程不兼容。
- 本切片不实现转换 job、读者引用计数、签名或运行检查流程。

## 读回包

- `readback.json` 只给操作规则、已应用并保存的操作/状态、来源 ID/URL/revision 与固定问题。
- 不附底稿 fact 的 meaning 列表、评分/期待答案、raw_failure 再现输入或拒绝探针的错误文本；来源原文按来源 ID 定位 URL 后另行查证。
"""


def _serialize(document):
    if isinstance(document, str):
        return document if document.endswith('\n') else document + '\n'
    return json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + '\n'


def build_documents():
    return {'results.json': build_results(),
            'readback.json': build_readback(),
            'rules.md': build_rules()}


def export_boundary(directory):
    """Create one boundary slice once; an existing directory is never overwritten."""
    out = Path(directory)
    documents = build_documents()
    out.mkdir(parents=True, exist_ok=False)
    for name, document in documents.items():
        (out / name).write_text(_serialize(document), encoding='utf-8')
    return str(out.resolve())


def verify_boundary(directory):
    """Compare saved evidence with an in-memory rebuild; never writes."""
    out = Path(directory)
    for name, document in build_documents().items():
        expected = _serialize(document)
        actual = (out / name).read_text(encoding='utf-8')
        if actual != expected:
            raise AssertionError('saved evidence differs from the current build: ' + name)
    return True


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    print(export_boundary(Path(args.out)))
