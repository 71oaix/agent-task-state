"""T12 stage 2b: four single-variable object identity comparisons.

Each group changes exactly one identity choice and keeps the other four at S0.
A and B are separate in-memory storage shapes: B never reads A's records, and
the independent identity under test is absent from B's store.  The module does
not run the DSH, call models, touch Git or judge natural-language truth.
"""
from copy import deepcopy
from pathlib import Path
import json

BATCH = 't12-continuous-validation-2026-10-29'
SLICE = 'identity-v1'
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
IDENTITY_DIR = ROOT / 'artifacts/agent-task-state/maintenance' / BATCH / SLICE
STUDY_BASELINE = '4433b09490daf7ce05b344bfd8092982f9025fc8'

FEATURES = ['detail_modes', 'process_grouping', 'whole_turn_status',
            'trigger_notifications', 'tool_visuals', 'row_hiding']
REVISED_SCOPE = ['detail_modes', 'process_grouping', 'whole_turn_status']
PLAN_V1 = {
    'channel': {'status': 'recorded_arrangement',
                'description': 'completed independent features stay in the presentation channel'},
    'turnstep': {'status': 'recorded_arrangement',
                 'description': 'unfinished drafts continue in the turnstep worktree'},
    'reference': {'status': 'recorded_arrangement',
                  'description': 'original PR retained as reference; experiments are not transferred'}}
PLAN_V2_TURNSTEP = {'status': 'revised_local_scope',
                    'description': 'unfinished drafts continue in the turnstep worktree in smaller staged parts'}
DRAFT = {'completion': 'in_progress', 'implementation': 'reported_draft_written',
         'git': 'unstaged', 'acceptance': 'pending'}
CODE_WRITTEN = {'completion': 'reported_complete', 'implementation': 'reported_code_written',
                'git': 'unstaged', 'acceptance': 'pending'}
DIMENSION_VALUES = {
    'completion': {'unknown', 'not_started', 'incomplete', 'in_progress',
                   'reported_complete', 'complete'},
    'implementation': {'unknown', 'not_started', 'reported_draft_written',
                       'reported_code_written', 'reported_implemented', 'implemented'},
    'git': {'unknown', 'not_started', 'unstaged', 'reported_committed', 'committed'},
    'acceptance': {'unknown', 'pending', 'accepted'}}
CHAIN_LABELS = ['L0-establish', 'L1-local-plan-edit', 'L2-adopt-new-version',
                'L3-new-result', 'L4-exact-check', 'L5-end-with-responsibility', 'L6-rework']

CAP_MEANING = {
    'independent_plan_record': '存在独立 Plan 记录，而不是宿主内的内容',
    'old_plan_text_resolvable': '旧成果所用的计划文本仍可按精确版本读出',
    'partial_section_adoption': '只采用计划中的一个 section，其余 section 不受影响',
    'plan_edit_advances_attempt_version': '局部改计划同时推进宿主 Attempt 的内容版本',
    'shared_plan_version_across_attempts': '两个尝试指向同一个计划版本（同一身份，而不是内容相同）',
    'independent_product_record': '存在独立 Product 记录，而不是尝试结果',
    'old_result_resolvable_after_end': '尝试结束后旧成果仍按精确版本可读',
    'partial_withdraw_single_slot': '只撤回列明的成果部分，其余部分保留',
    'result_correction_while_attempt_ended': '尝试保持 ended 时记录成果修正，不虚假 reopen',
    'same_result_identity_across_attempts': '另一个尝试推进同一成果时身份/定位不变',
    'slot_local_identity_required': '需要稳定 slot 名（局部身份）才能区分并定位结果',
    'independent_evidence_record': '存在独立 Evidence 记录，而不是 Change 内陈述',
    'report_locator_survives_subject_update': 'subject 更新后旧报告仍指向报告时版本',
    'correction_retains_old_statement': '新解释纠正旧结论时旧陈述仍保留',
    'same_report_referenced_twice': '同一份报告可被两处引用',
    'subject_query_returns_all_statements': '按 subject 能查回全部相关陈述',
    'naive_latest_by_subject_returns_original': '只按 subject 取最新仍能返回原报告（而不是最新修正）',
    'reference_needs_change_number': '引用一份报告需要 Change 号与语句序号两项',
    'independent_goal_record': '存在独立 Goal 记录，而不是 Work 内的目标字段',
    'attempt_ended_goal_continues': '尝试结束后目标继续存在且未验收',
    'two_attempts_same_goal': '同一目标下有第二次尝试',
    'parallel_attempts': '两个尝试可以同时处于 active',
    'old_attempt_keeps_old_goal_scope': '目标范围修订后旧尝试仍按修订前范围解释',
    'attempt_key_reintroduced': '所谓合并的表示内部仍需要 attempt key/index 与独立状态',
}

SPEC = {
    'C1': {
        'changed': 'Plan 的身份：独立 Plan 对象 vs 内嵌在 Attempt 内容修订中',
        'fixed': ['Product 独立', 'Evidence 独立', 'Goal 与 Attempt 分离', 'Change append-only'],
        'alt_a': '独立 Plan 记录 P，带 revision 与历史；采用记录写在 Attempt 上',
        'alt_b': '没有 Plan 记录；计划 section 保存在 Attempt 内容修订中，定位为 (attempt, revision, section)',
        'open': ['同一计划被多个 Attempt 编辑时，共享宿主是否比复制更可维护',
                 'section 定位是否足够表达跨 section 的顺序约束']},
    'C2': {
        'changed': 'Product 的身份：独立 Product 对象 vs Attempt 内的结果 slot',
        'fixed': ['Plan 独立', 'Evidence 独立', 'Goal 与 Attempt 分离', 'Change append-only'],
        'alt_a': '独立 Product 记录 Q，带 revision、parts 与四维',
        'alt_b': '没有 Product 记录；结果保存在 Attempt 内容修订的 slot 中，定位为 (attempt, revision, slot)',
        'open': ['成果跨尝试延续时，slot 定位是否等于重新引入 Product 身份',
                 '局部撤回在 slot 表示中是否需要 per-slot 版本']},
    'C3': {
        'changed': 'Evidence 的身份：独立 Evidence 对象 vs Change 内可定位陈述',
        'fixed': ['Plan 独立', 'Product 独立', 'Goal 与 Attempt 分离', 'Change append-only'],
        'alt_a': '独立 Evidence 记录 E，带 subject 的精确版本与 nature',
        'alt_b': '没有 Evidence 记录；陈述写在 Change 内，定位为 (change number, statement index)',
        'open': ['Evidence ID 是否为验收所必需，还是 (change, statement) 已足够',
                 'Change 编号若出现空洞或压缩，locator 的稳定性如何保证']},
    'C4': {
        'changed': 'Goal 与 Attempt 的身份：分开 vs 合并为一个 Work 记录',
        'fixed': ['Plan 独立', 'Product 独立', 'Evidence 独立', 'Change append-only'],
        'alt_a': '独立 Goal 记录 + 独立 Attempt 记录（每次尝试一个 ID）',
        'alt_b': '一个 Work 记录：目标按 revision 保存，尝试是可寻址条目 (key/index)',
        'open': ['Work 内的 attempt key 是否就是重新引入的 Attempt 身份',
                 '目标范围修订与旧尝试依据的对应是否必须逐尝试保存 goal revision']},
}


class Reject(Exception):
    pass


def need(ok, message):
    if not ok:
        raise Reject(message)


def exact_revision(value, label):
    need(type(value) is int and value > 0, label + ' must be a positive integer revision')


def differences(before, after, prefix=''):
    if isinstance(before, dict) and isinstance(after, dict):
        result = []
        for key in sorted(set(before) | set(after), key=str):
            name = prefix + '/' + str(key)
            if key not in before or key not in after:
                result.append(name)
            else:
                result.extend(differences(before[key], after[key], name))
        return result
    if isinstance(before, list) and isinstance(after, list):
        result = []
        for index in range(max(len(before), len(after))):
            name = prefix + '/' + str(index)
            if index >= len(before) or index >= len(after):
                result.append(name)
            else:
                result.extend(differences(before[index], after[index], name))
        return result
    return [] if before == after else [prefix]


def touched_identifiers(paths):
    rows = set()
    for path in paths:
        parts = [part for part in path.strip('/').split('/') if part]
        if not parts or parts[0] == 'head':
            continue
        if parts[0] == 'store' and len(parts) > 1:
            rows.add(parts[1])
        elif parts[0] == 'change_statements' and len(parts) > 1:
            rows.add('change:' + parts[1])
        elif parts[0] in {'refs', 'tokens'} and len(parts) > 1:
            rows.add(parts[0] + ':' + parts[1])
        else:
            rows.add(parts[0])
    return sorted(rows)


def new_record(store, oid, kind, **fields):
    need(isinstance(oid, str) and bool(oid), 'identity required')
    need(oid not in store, 'duplicate identity: ' + oid)
    store[oid] = {'id': oid, 'kind': kind, 'revision': 1, 'versions': {},
                  'identity_origin': 'researcher_created', **deepcopy(fields)}


def snapshot_record(store, oid):
    return deepcopy({key: value for key, value in store[oid].items() if key != 'versions'})


def bump(store, oid, **edits):
    obj = store[oid]
    obj['versions'][str(obj['revision'])] = snapshot_record(store, oid)
    obj['revision'] += 1
    obj.update(deepcopy(edits))
    return obj


def at(store, oid, revision):
    need(oid in store, 'unknown identity: ' + oid)
    exact_revision(revision, 'revision for ' + oid)
    obj = store[oid]
    if obj['revision'] == revision:
        return snapshot_record(store, oid)
    key = str(revision)
    need(key in obj['versions'], 'revision not retained: %s@%s' % (oid, revision))
    return deepcopy(obj['versions'][key])


class World:
    group = ''
    mode = ''

    def __init__(self):
        self.head = 0
        self.log = []
        self.store = {}
        self.change_statements = {}
        self.refs = {}
        self.tokens = {}

    def snapshot(self):
        return deepcopy({'head': self.head, 'store': self.store,
                         'change_statements': self.change_statements,
                         'refs': self.refs, 'tokens': self.tokens})

    def commit(self, label, fn):
        before = self.snapshot()
        need(self.head == len(self.log), 'changes are append-only')
        result = fn(self)
        need(isinstance(result, dict), 'step must return observations')
        actions = result.pop('actions', [])
        observations = result.pop('observations', result.pop('queries', {}))
        self.head += 1
        self.log.append({'number': self.head, 'label': label})
        after = self.snapshot()
        return {'label': label, 'change': self.head, 'accepted': True,
                'actions': actions, 'observations': observations,
                'before': before, 'after': after,
                'changed_paths': differences(before, after)}

    def expect_reject(self, fn, prepare=None):
        probe = deepcopy(self)
        if prepare is not None:
            prepare(probe)
        before = probe.snapshot()
        try:
            fn(probe)
        except Reject as error:
            need(probe.snapshot() == before, 'rejection left partial state')
            return {'accepted': False, 'error': str(error)}
        raise AssertionError('expected the action to be rejected')

    def resolve_locator(self, locator):
        need(isinstance(locator, dict) and bool(locator), 'locator required')
        if 'change' in locator:
            return self.statement(locator)['findings']
        if 'goal' in locator:
            return at(self.store, locator['goal'], locator['revision'])['scope']
        if 'key' in locator:
            return self.attempt_entry(locator['key'])['status']
        if 'work' in locator:
            return self.goal_at(locator['revision'])['scope']
        if 'product' in locator:
            return at(self.store, locator['product'], locator['revision'])['dimensions']
        if 'slot' in locator:
            return self.slot(locator['revision'], locator['slot'])['dimensions']
        if 'attempt' in locator:
            return self.plan_text(locator['revision'], locator['section'])
        if 'id' in locator:
            obj = at(self.store, locator['id'], locator['revision'])
            if obj['kind'] == 'goal':
                return obj['scope']
            if obj['kind'] == 'attempt':
                return obj['status']
            if obj['kind'] == 'product':
                return obj['dimensions']
            if obj['kind'] == 'evidence':
                return obj['findings']
            if obj['kind'] == 'plan':
                return obj['sections']
            return None
        raise Reject('unresolved locator: ' + repr(locator))

    def chain(self):
        rows = []
        for label in CHAIN_LABELS:
            rows.append(self.commit(label, lambda world, name=label: getattr(world, name.split('-')[0].lower())()))
        return rows

    def end(self, aid, remaining='retained_unresolved'):
        need(aid in self.store and self.store[aid]['kind'] == 'attempt', 'attempt required')
        need(self.store[aid]['status'] == 'active', 'active attempt required')
        need(remaining in {None, 'retained_unresolved'},
             'ending holder must disclose remaining responsibility as retained_unresolved')
        held = sorted(token for token, holders in self.tokens.items() if aid in holders)
        need(not held or remaining == 'retained_unresolved',
             'ending holder must disclose remaining assigned responsibility')
        bump(self.store, aid, status='ended', outcome='synthetic stop',
             remaining_responsibility=remaining, held_at_end=held)

    def cost(self, chain):
        per_step = [touched_identifiers(step['changed_paths']) for step in chain]
        return {'identity_records': self.identity_count(),
                'max_records_changed_in_one_change': max(len(row) for row in per_step),
                'records_changed_per_step': per_step,
                'revision_sequences': self.revision_sequences(),
                'query_entry_points': self.query_entry_points(),
                'extra_conventions': self.conventions(),
                'failure_modes': self.failure_modes()}

    def historical_references(self):
        rows = []
        for name, locator in sorted(self.refs.items()):
            rows.append({'name': name, 'locator': deepcopy(locator),
                         'resolves_to': self.resolve_locator(locator)})
        return rows


class PlanS0:
    """S0 Plan: an independent record with revisions and per-section adoption."""

    def plan_text(self, revision, section):
        plan = at(self.store, 'P', revision)
        need(section in plan['sections'], 'unknown plan section: ' + section)
        return plan['sections'][section]['description']

    def edit_plan(self, edits, remove=()):
        plan = self.store['P']
        remove = list(remove)
        need(isinstance(edits, dict), 'plan update shape')
        need(bool(edits) or bool(remove), 'empty plan update')
        need(not set(edits) & set(remove) and len(set(remove)) == len(remove), 'plan update overlap')
        unknown = (set(edits) | set(remove)) - set(plan['sections'])
        need(not unknown, 'unknown plan section: ' + ','.join(sorted(unknown)))
        updated = deepcopy(plan['sections'])
        for key in remove:
            updated[key] = {'status': 'superseded', 'description': updated[key]['description']}
        for key, value in edits.items():
            need(isinstance(value, dict) and set(value) == {'status', 'description'},
                 'section structure required')
            updated[key] = deepcopy(value)
        bump(self.store, 'P', sections=updated)

    def adopt(self, aid, revision, scope, basis):
        need(aid in self.store and self.store[aid]['kind'] == 'attempt', 'attempt required')
        need(self.store[aid]['status'] == 'active', 'adoption requires an active attempt')
        plan = at(self.store, 'P', revision)
        need(isinstance(scope, list) and bool(scope) and len(set(scope)) == len(scope),
             'unique nonempty adoption scope required')
        need(set(scope) <= set(plan['sections']), 'adoption scope must name sections of that revision')
        need(isinstance(basis, list) and bool(basis)
             and all(isinstance(x, str) and x.startswith('SYN:') for x in basis),
             'synthetic adoption basis required')
        decisions = deepcopy(self.store[aid]['decisions'])
        decisions.append({'plan': {'id': 'P', 'revision': revision}, 'scope': list(scope),
                          'basis': list(basis), 'change': self.head + 1})
        bump(self.store, aid, decisions=decisions)

    def effective(self, aid, section):
        found = None
        for record in self.store[aid]['decisions']:
            if section in record['scope']:
                found = deepcopy(record['plan'])
        need(found is not None, 'plan scope was not adopted: ' + section)
        return found

    def plan_projection(self):
        return {'plan_revision': self.store['P']['revision'],
                'texts': {key: self.plan_text(self.store['P']['revision'], key)
                          for key in sorted(self.store['P']['sections'])}}


class ProductOps:
    def advance(self, pid, dimensions, actor=None):
        product = self.store[pid]
        need(product['kind'] == 'product', 'product required')
        merged = deepcopy(product['dimensions'])
        for key, value in dimensions.items():
            need(key in DIMENSION_VALUES, 'unknown dimension: ' + str(key))
            need(value in DIMENSION_VALUES[key], 'controlled dimension value required: ' + key)
            merged[key] = value
        fields = {'dimensions': merged}
        if actor is not None:
            fields['advanced_by'] = actor
        bump(self.store, pid, **fields)

    def withdraw(self, pid, parts):
        product = self.store[pid]
        need(isinstance(parts, list) and bool(parts), 'known nonempty withdrawal range required')
        unknown = sorted(set(parts) - set(product['parts']))
        need(not unknown, 'unknown product part: ' + ','.join(unknown))
        updated = deepcopy(product['parts'])
        for part in parts:
            updated[part] = 'withdrawn'
        bump(self.store, pid, parts=updated)


class PlanProductWorld(World, PlanS0, ProductOps):
    def produce(self, aid, pid, parts, section, dimensions):
        need(self.store[aid]['status'] == 'active', 'producing a new result requires an active attempt')
        basis = self.effective(aid, section)
        new_record(self.store, pid, 'product', attempt=aid,
                   parts={part: 'present' for part in parts},
                   dimensions=deepcopy(dimensions), plan_usage={section: basis})


# ---------------------------------------------------------------- C1 Plan


class C1A(PlanProductWorld):
    group, mode = 'C1', 'A'

    def l0(self):
        new_record(self.store, 'G', 'goal', scope=FEATURES, acceptance='pending')
        new_record(self.store, 'P', 'plan', sections=deepcopy(PLAN_V1), links=[])
        new_record(self.store, 'A', 'attempt', goal='G', status='active',
                   scope=['turnstep draft'], decisions=[])
        new_record(self.store, 'R', 'product', attempt='A',
                   parts={'draft_status': 'present', 'draft_notifications': 'present'},
                   dimensions=deepcopy(DRAFT),
                   plan_usage={'turnstep': {'id': 'P', 'revision': 1}})
        self.tokens = {'whole_turn_status': ['A']}
        self.refs = {'old_result_plan': {'id': 'P', 'revision': 1}}
        return {'actions': ['goal G', 'plan P@1', 'attempt A', 'product R with P@1'],
                'observations': {'R_plan': deepcopy(self.refs['old_result_plan'])}}

    def l1(self):
        self.edit_plan({'turnstep': deepcopy(PLAN_V2_TURNSTEP)})
        return {'actions': ['edit only P.turnstep'],
                'observations': {'plan_revision': self.store['P']['revision'],
                                 'attempt_revision': self.store['A']['revision'],
                                 'R_plan': deepcopy(self.store['R']['plan_usage']),
                                 'channel_text': self.plan_text(2, 'channel')}}

    def l2(self):
        self.adopt('A', 2, ['turnstep'], ['SYN:chain-adopt'])
        return {'actions': ['A adopts P@2 for turnstep'],
                'observations': {'adoptions': deepcopy(self.store['A']['decisions']),
                                 'attempt_revision': self.store['A']['revision'],
                                 'R_plan': deepcopy(self.store['R']['plan_usage'])}}

    def l3(self):
        self.produce('A', 'Q', ['draft_status', 'draft_notifications'], 'turnstep', CODE_WRITTEN)
        self.refs['new_result_plan'] = deepcopy(self.store['Q']['plan_usage']['turnstep'])
        return {'actions': ['produce Q under the adopted scope'],
                'observations': {'Q_plan': deepcopy(self.store['Q']['plan_usage']),
                                 'R_plan': deepcopy(self.store['R']['plan_usage'])}}

    def l4(self):
        old = self.plan_text(1, 'turnstep')
        new = self.plan_text(2, 'turnstep')
        new_record(self.store, 'E', 'evidence', goal='G',
                   subject={'id': 'Q', 'revision': 1},
                   scope='turnstep plan usage', nature='synthetic',
                   findings=['old result used: ' + old, 'new result used: ' + new])
        self.refs['check'] = {'id': 'E', 'revision': 1}
        return {'actions': ['record exact plan-version check as Evidence E'],
                'observations': {'findings': deepcopy(self.store['E']['findings']),
                                 'subject': deepcopy(self.store['E']['subject'])},
                'queries': {}}

    def l5(self):
        self.end('A')
        return {'actions': ['end A with retained responsibility'],
                'observations': {'attempt_status': self.store['A']['status'],
                                 'remaining': self.store['A']['remaining_responsibility'],
                                 'goal_acceptance': self.store['G']['acceptance'],
                                 'old_result_readable': deepcopy(self.store['R']['parts'])}}

    def l6(self):
        status_at_write = self.store['A']['status']
        self.advance('Q', {'completion': 'in_progress'}, actor='A')
        bump(self.store, 'A', status='active', outcome='unknown',
             reopen_history=[{'change': self.head + 1, 'prior_status': 'ended'}])
        return {'actions': ['regress Q completion', 'reopen A'],
                'observations': {'status_at_write': status_at_write,
                                 'attempt_status': self.store['A']['status'],
                                 'old_result_dimensions': at(self.store, 'Q', 1)['dimensions'],
                                 'current_dimensions': self.store['Q']['dimensions']}}

    def begin_second_attempt(self):
        new_record(self.store, 'A2', 'attempt', goal='G', status='active',
                   scope=['turnstep draft'], decisions=[])
        self.adopt('A2', 2, ['turnstep'], ['SYN:shared-plan'])
        first = [row['plan'] for row in self.store['A']['decisions'] if 'turnstep' in row['scope']][-1]
        second = [row['plan'] for row in self.store['A2']['decisions'] if 'turnstep' in row['scope']][-1]
        return {'actions': ['begin A2 and adopt the same plan revision'],
                'observations': {'A_plan': deepcopy(first), 'A2_plan': deepcopy(second),
                                 'shared_locator': first == second}}

    def final_state(self):
        return {
            'content': {
                'old_plan_text': self.plan_text(1, 'turnstep'),
                'new_plan_text': self.plan_text(2, 'turnstep'),
                'old_check_findings': deepcopy(self.store['E']['findings']),
                'old_result_dimensions': at(self.store, 'Q', 1)['dimensions'],
                'current_result_dimensions': self.store['Q']['dimensions'],
                'goal_acceptance': self.store['G']['acceptance'],
                'attempt_status': self.store['A']['status']},
            'capabilities': {
                'independent_plan_record': 'P' in self.store,
                'old_plan_text_resolvable': bool(self.plan_text(1, 'turnstep')),
                'partial_section_adoption': self.plan_text(2, 'channel') == PLAN_V1['channel']['description'],
                'shared_plan_version_across_attempts':
                    self.store['A']['decisions'][-1]['plan'] == self.store['A2']['decisions'][-1]['plan']},
            'locators': {
                'old_result_plan': deepcopy(self.store['R']['plan_usage']),
                'new_result_plan': deepcopy(self.store['Q']['plan_usage']),
                'old_check_subject': deepcopy(self.store['E']['subject'])},
        }

    def identity_count(self):
        return {'plan_identities': 1, 'plan_revisions_retained': len(self.store['P']['versions']) + 1}

    def revision_sequences(self):
        return [{'sequence': 'P.revision', 'current': self.store['P']['revision']},
                {'sequence': 'A.revision', 'current': self.store['A']['revision']}]

    def query_entry_points(self):
        return ['plan_text(revision, section)', 'effective(attempt, section)',
                'at(store, id, revision)', 'product.plan_usage']

    def conventions(self):
        return ['Plan ID、revision 与历史版本',
                '采用记录写在 Attempt 的 decisions 上，按 section 覆盖',
                'Product 必须为每个 section 记录 exact {id, revision}']

    def failure_modes(self):
        return ['Plan 版本与 Attempt 采用记录是两处更新，同一批次需要一起回滚',
                '删除旧 Plan revision 会让旧成果的计划引用悬空']

    def native(self):
        return {'storage': 'store["P"] independent plan record',
                'varied_identity': 'plan id P',
                'locator': '{id, revision} plus section in the consumer',
                'sample': deepcopy(self.store['P'])}


class C1B(PlanProductWorld):
    group, mode = 'C1', 'B'

    def host_revision(self):
        return self.store['A']['content'][-1]['revision']

    def plan_text(self, revision, section):
        exact_revision(revision, 'attempt content revision')
        for item in self.store['A']['content']:
            if item['revision'] == revision:
                need(section in item['sections'], 'unknown plan section: ' + section)
                return item['sections'][section]['description']
        raise Reject('attempt content revision not retained: %s' % revision)

    def edit_plan(self, edits, remove=()):
        host = self.store['A']
        current = deepcopy(host['content'][-1]['sections'])
        remove = list(remove)
        need(isinstance(edits, dict), 'plan update shape')
        need(bool(edits) or bool(remove), 'empty plan update')
        need(not set(edits) & set(remove) and len(set(remove)) == len(remove), 'plan update overlap')
        unknown = (set(edits) | set(remove)) - set(current)
        need(not unknown, 'unknown plan section: ' + ','.join(sorted(unknown)))
        for key in remove:
            current[key] = {'status': 'superseded', 'description': current[key]['description']}
        for key, value in edits.items():
            need(isinstance(value, dict) and set(value) == {'status', 'description'},
                 'section structure required')
            current[key] = deepcopy(value)
        host['content'].append({'revision': host['content'][-1]['revision'] + 1,
                                'label': 'local plan edit', 'sections': current})

    def adopt(self, aid, revision, scope, basis):
        need(aid in self.store and self.store[aid]['kind'] == 'attempt', 'attempt required')
        need(self.store[aid]['status'] == 'active', 'adoption requires an active attempt')
        exact_revision(revision, 'adoption content revision')
        need(any(item['revision'] == revision for item in self.store[aid]['content']),
             'attempt content revision not retained: %s' % revision)
        sections = next(item['sections'] for item in self.store[aid]['content']
                        if item['revision'] == revision)
        need(isinstance(scope, list) and bool(scope) and len(set(scope)) == len(scope),
             'unique nonempty adoption scope required')
        need(set(scope) <= set(sections), 'adoption scope must name sections of that revision')
        need(isinstance(basis, list) and bool(basis)
             and all(isinstance(x, str) and x.startswith('SYN:') for x in basis),
             'synthetic adoption basis required')
        self.store[aid]['decisions'].append({'sections': list(scope), 'content_revision': revision,
                                             'basis': list(basis), 'change': self.head + 1})

    def effective(self, aid, section):
        found = None
        for record in self.store[aid]['decisions']:
            if section in record['sections']:
                found = record['content_revision']
        need(found is not None, 'plan scope was not adopted: ' + section)
        return {'attempt': aid, 'revision': found, 'section': section}

    def l0(self):
        new_record(self.store, 'G', 'goal', scope=FEATURES, acceptance='pending')
        new_record(self.store, 'A', 'attempt', goal='G', status='active',
                   scope=['turnstep draft'], decisions=[],
                   content=[{'revision': 1, 'label': 'embedded plan v1',
                             'sections': deepcopy(PLAN_V1)}])
        new_record(self.store, 'R', 'product', attempt='A',
                   parts={'draft_status': 'present', 'draft_notifications': 'present'},
                   dimensions=deepcopy(DRAFT),
                   plan_basis={'turnstep': {'attempt': 'A', 'revision': 1, 'section': 'turnstep'}})
        self.tokens = {'whole_turn_status': ['A']}
        self.refs = {'old_result_plan': {'attempt': 'A', 'revision': 1, 'section': 'turnstep'}}
        return {'actions': ['goal G', 'attempt A with embedded plan revision 1', 'product R'],
                'observations': {'R_plan': deepcopy(self.refs['old_result_plan']),
                                 'plan_record_present': 'P' in self.store}}

    def l1(self):
        self.edit_plan({'turnstep': deepcopy(PLAN_V2_TURNSTEP)})
        return {'actions': ['edit only turnstep inside the attempt content'],
                'observations': {'attempt_content_revision': self.host_revision(),
                                 'R_plan': deepcopy(self.store['R']['plan_basis']),
                                 'channel_text': self.plan_text(self.host_revision(), 'channel')}}

    def l2(self):
        self.adopt('A', self.host_revision(), ['turnstep'], ['SYN:chain-adopt'])
        return {'actions': ['A declares the adopted content revision for turnstep'],
                'observations': {'decisions': deepcopy(self.store['A']['decisions']),
                                 'attempt_content_revision': self.host_revision(),
                                 'R_plan': deepcopy(self.store['R']['plan_basis'])}}

    def l3(self):
        self.produce('A', 'Q', ['draft_status', 'draft_notifications'], 'turnstep', CODE_WRITTEN)
        self.refs['new_result_plan'] = deepcopy(self.store['Q']['plan_basis']['turnstep'])
        return {'actions': ['produce Q under the declared revision'],
                'observations': {'Q_plan': deepcopy(self.store['Q']['plan_basis']),
                                 'R_plan': deepcopy(self.store['R']['plan_basis'])}}

    def produce(self, aid, pid, parts, section, dimensions):
        need(self.store[aid]['status'] == 'active', 'producing a new result requires an active attempt')
        basis = self.effective(aid, section)
        new_record(self.store, pid, 'product', attempt=aid,
                   parts={part: 'present' for part in parts},
                   dimensions=deepcopy(dimensions), plan_basis={section: basis})

    def l4(self):
        old = self.plan_text(1, 'turnstep')
        new = self.plan_text(self.host_revision(), 'turnstep')
        new_record(self.store, 'E', 'evidence', goal='G',
                   subject={'id': 'Q', 'revision': 1},
                   scope='turnstep plan usage', nature='synthetic',
                   findings=['old result used: ' + old, 'new result used: ' + new])
        self.refs['check'] = {'id': 'E', 'revision': 1}
        return {'actions': ['record exact plan-version check as Evidence E'],
                'observations': {'findings': deepcopy(self.store['E']['findings']),
                                 'subject': deepcopy(self.store['E']['subject'])}}

    def l5(self):
        self.end('A')
        return {'actions': ['end A with retained responsibility'],
                'observations': {'attempt_status': self.store['A']['status'],
                                 'remaining': self.store['A']['remaining_responsibility'],
                                 'goal_acceptance': self.store['G']['acceptance'],
                                 'old_result_readable': deepcopy(self.store['R']['parts'])}}

    def l6(self):
        status_at_write = self.store['A']['status']
        self.advance('Q', {'completion': 'in_progress'}, actor='A')
        bump(self.store, 'A', status='active', outcome='unknown',
             reopen_history=[{'change': self.head + 1, 'prior_status': 'ended'}])
        return {'actions': ['regress Q completion', 'reopen A'],
                'observations': {'status_at_write': status_at_write,
                                 'attempt_status': self.store['A']['status'],
                                 'old_result_dimensions': at(self.store, 'Q', 1)['dimensions'],
                                 'current_dimensions': self.store['Q']['dimensions']}}

    def begin_second_attempt(self):
        source = self.host_revision()
        sections = deepcopy(self.store['A']['content'][-1]['sections'])
        new_record(self.store, 'A2', 'attempt', goal='G', status='active',
                   scope=['turnstep draft'], decisions=[],
                   content=[{'revision': 1, 'label': 'copied from A rev %s' % source,
                             'sections': sections}])
        first = {'attempt': 'A', 'revision': source, 'section': 'turnstep'}
        second = {'attempt': 'A2', 'revision': 1, 'section': 'turnstep'}
        return {'actions': ['begin A2 by copying the current plan content'],
                'observations': {'A_plan': first, 'A2_plan': second,
                                 'shared_locator': first == second,
                                 'content_equal': self.store['A2']['content'][-1]['sections']
                                                  == self.store['A']['content'][-1]['sections']}}

    def final_state(self):
        return {
            'content': {
                'old_plan_text': self.plan_text(1, 'turnstep'),
                'new_plan_text': self.plan_text(self.host_revision(), 'turnstep'),
                'old_check_findings': deepcopy(self.store['E']['findings']),
                'old_result_dimensions': at(self.store, 'Q', 1)['dimensions'],
                'current_result_dimensions': self.store['Q']['dimensions'],
                'goal_acceptance': self.store['G']['acceptance'],
                'attempt_status': self.store['A']['status']},
            'capabilities': {
                'independent_plan_record': 'P' in self.store,
                'old_plan_text_resolvable': bool(self.plan_text(1, 'turnstep')),
                'partial_section_adoption': self.plan_text(self.host_revision(), 'channel')
                                            == PLAN_V1['channel']['description'],
                'shared_plan_version_across_attempts': False},
            'locators': {
                'old_result_plan': deepcopy(self.store['R']['plan_basis']),
                'new_result_plan': deepcopy(self.store['Q']['plan_basis']),
                'old_check_subject': deepcopy(self.store['E']['subject'])},
        }

    def identity_count(self):
        return {'plan_identities': 0,
                'attempt_content_revisions_retained': len(self.store['A']['content'])}

    def revision_sequences(self):
        return [{'sequence': 'A.content revisions',
                 'current': self.host_revision(),
                 'retained': [item['revision'] for item in self.store['A']['content']]}]

    def query_entry_points(self):
        return ['plan_text(attempt revision, section)', 'effective(attempt, section)',
                'content revision list on the host']

    def conventions(self):
        return ['宿主内容修订必须逐版保留',
                '定位必须携带 (attempt, revision, section)，不能只给 attempt',
                '采用记录指向内容修订号，写在 Attempt 的 decisions 上',
                '跨尝试共享只能复制内容；共享同一宿主不在本表示内']

    def failure_modes(self):
        return ['改计划推进宿主内容修订，非计划消费者也会看到宿主版本变化',
                '删掉旧内容修订会让旧成果的 section 定位悬空',
                '两个尝试的"同一计划版本"只能表现为内容相等，不能表现为同一身份']

    def native(self):
        return {'storage': 'store["A"].content revisions',
                'varied_identity': 'none for Plan',
                'locator': '{attempt, revision, section}',
                'sample': deepcopy(self.store['A']['content'][-1])}


# ------------------------------------------------------------- C2 Product


class C2A(PlanProductWorld):
    group, mode = 'C2', 'A'

    def l0(self):
        new_record(self.store, 'G', 'goal', scope=FEATURES, acceptance='pending')
        new_record(self.store, 'P', 'plan', sections=deepcopy(PLAN_V1), links=[])
        new_record(self.store, 'A', 'attempt', goal='G', status='active',
                   scope=['turnstep draft'], decisions=[])
        new_record(self.store, 'R', 'product', attempt='A',
                   parts={'draft_status': 'present', 'draft_notifications': 'present'},
                   dimensions=deepcopy(DRAFT),
                   plan_usage={'turnstep': {'id': 'P', 'revision': 1}})
        self.tokens = {'whole_turn_status': ['A']}
        self.refs = {'old_result': {'product': 'R', 'revision': 1}}
        return {'actions': ['goal G', 'plan P@1', 'attempt A', 'product R'],
                'observations': {'R_parts': deepcopy(self.store['R']['parts'])}}

    def l1(self):
        self.edit_plan({'turnstep': deepcopy(PLAN_V2_TURNSTEP)})
        return {'actions': ['edit only P.turnstep'],
                'observations': {'plan_revision': self.store['P']['revision'],
                                 'R_dimensions': at(self.store, 'R', 1)['dimensions']}}

    def l2(self):
        self.adopt('A', 2, ['turnstep'], ['SYN:chain-adopt'])
        return {'actions': ['A adopts P@2 for turnstep'],
                'observations': {'adoptions': deepcopy(self.store['A']['decisions'])}}

    def l3(self):
        self.produce('A', 'Q', ['draft_status', 'draft_notifications'], 'turnstep', CODE_WRITTEN)
        self.refs['new_result'] = {'product': 'Q', 'revision': 1}
        return {'actions': ['produce Q under P@2'],
                'observations': {'Q_plan': deepcopy(self.store['Q']['plan_usage']),
                                 'R_plan': deepcopy(self.store['R']['plan_usage'])}}

    def l4(self):
        dims = at(self.store, 'Q', 1)['dimensions']
        new_record(self.store, 'E', 'evidence', goal='G',
                   subject={'id': 'Q', 'revision': 1}, scope='result dimensions',
                   nature='synthetic',
                   findings=['draft_status at check: %s; acceptance %s'
                             % (dims['implementation'], dims['acceptance'])])
        self.refs['check'] = {'id': 'E', 'revision': 1}
        return {'actions': ['record exact result check as Evidence E'],
                'observations': {'findings': deepcopy(self.store['E']['findings']),
                                 'subject': deepcopy(self.store['E']['subject'])}}

    def l5(self):
        self.end('A')
        return {'actions': ['end A with retained responsibility'],
                'observations': {'attempt_status': self.store['A']['status'],
                                 'old_result_dimensions': at(self.store, 'R', 1)['dimensions'],
                                 'old_result_parts': deepcopy(self.store['R']['parts']),
                                 'goal_acceptance': self.store['G']['acceptance']}}

    def l6(self):
        status_at_write = self.store['A']['status']
        self.advance('Q', {'completion': 'in_progress'}, actor='A')
        bump(self.store, 'A', status='active', outcome='unknown',
             reopen_history=[{'change': self.head + 1, 'prior_status': 'ended'}])
        return {'actions': ['regress Q completion while A is ended', 'reopen A'],
                'observations': {'status_at_write': status_at_write,
                                 'attempt_status': self.store['A']['status'],
                                 'old_result_dimensions': at(self.store, 'Q', 1)['dimensions'],
                                 'current_dimensions': self.store['Q']['dimensions']}}

    def continue_in_second_attempt(self):
        new_record(self.store, 'A2', 'attempt', goal='G', status='active',
                   scope=['turnstep draft'], decisions=[])
        before = self.store['Q']['revision']
        self.advance('Q', {'completion': 'reported_complete'}, actor='A2')
        return {'actions': ['begin A2 and advance Q further'],
                'observations': {'product': 'Q', 'revision_before': before,
                                 'revision_after': self.store['Q']['revision'],
                                 'advanced_by': self.store['Q']['advanced_by'],
                                 'same_identity': self.store['Q']['id'] == 'Q'}}

    def withdraw_current(self):
        self.withdraw('Q', ['draft_status'])
        return {'actions': ['withdraw only Q.draft_status'],
                'observations': {'parts': deepcopy(self.store['Q']['parts'])},
                'queries': {}}

    def final_state(self):
        return {
            'content': {
                'old_result_states': deepcopy(self.store['R']['parts']),
                'new_result_states_after_withdraw': deepcopy(self.store['Q']['parts']),
                'old_result_dimensions': at(self.store, 'R', 1)['dimensions'],
                'old_check_findings': deepcopy(self.store['E']['findings']),
                'goal_acceptance': self.store['G']['acceptance'],
                'old_check_still_resolves': at(self.store, 'Q', 1)['revision'] == 1},
            'capabilities': {
                'independent_product_record': 'Q' in self.store and self.store['Q']['kind'] == 'product',
                'old_result_resolvable_after_end': at(self.store, 'R', 1)['parts']
                                                   == {'draft_status': 'present',
                                                       'draft_notifications': 'present'},
                'partial_withdraw_single_slot': self.store['Q']['parts']['draft_status'] == 'withdrawn'
                                                and self.store['Q']['parts']['draft_notifications'] == 'present',
                'same_result_identity_across_attempts': self.store['Q'].get('advanced_by') == 'A2',
                'slot_local_identity_required': False},
            'locators': {
                'old_result': deepcopy(self.refs['old_result']),
                'new_result': deepcopy(self.refs['new_result']),
                'old_check_subject': deepcopy(self.store['E']['subject'])},
        }

    def identity_count(self):
        return {'product_identities': 2,
                'product_revisions_retained': len(self.store['Q']['versions']) + 1}

    def revision_sequences(self):
        return [{'sequence': 'Q.revision', 'current': self.store['Q']['revision']}]

    def query_entry_points(self):
        return ['at(store, product, revision)', 'product.parts', 'product.dimensions']

    def conventions(self):
        return ['Product ID、revision、parts 与四维状态',
                'Evidence 使用 product 的 exact {id, revision}',
                'part 撤回答复在 parts 上，不删除旧 revision']

    def failure_modes(self):
        return ['成果与尝试生命周期分离后，需要单独记录 advanced_by 才能说明是谁推进']

    def native(self):
        return {'storage': 'store["Q"] independent product record',
                'varied_identity': 'product id',
                'locator': '{product, revision}',
                'sample': deepcopy(self.store['Q'])}


class C2B(PlanProductWorld):
    group, mode = 'C2', 'B'

    def slot(self, revision, name):
        exact_revision(revision, 'result revision')
        for item in self.store['A']['content']:
            if item['revision'] == revision:
                need(name in item['slots'], 'unknown result slot: ' + name)
                return deepcopy(item['slots'][name])
        raise Reject('result revision not retained: %s' % revision)

    def latest_revision(self):
        return self.store['A']['content'][-1]['revision']

    def write_slots(self, values, label):
        host = self.store['A']
        current = deepcopy(host['content'][-1])
        merged = deepcopy(current['slots'])
        for name, value in values.items():
            merged[name] = deepcopy(value)
        host['content'].append({'revision': current['revision'] + 1, 'label': label,
                                'slots': merged, 'written': sorted(values)})
        return host['content'][-1]['revision']

    def l0(self):
        new_record(self.store, 'G', 'goal', scope=FEATURES, acceptance='pending')
        new_record(self.store, 'P', 'plan', sections=deepcopy(PLAN_V1), links=[])
        new_record(self.store, 'A', 'attempt', goal='G', status='active',
                   scope=['turnstep draft'], decisions=[],
                   content=[{'revision': 1, 'label': 'first results',
                             'written': ['draft_notifications', 'draft_status'],
                             'slots': {'draft_status': {'state': 'present', 'dimensions': deepcopy(DRAFT)},
                                       'draft_notifications': {'state': 'present', 'dimensions': deepcopy(DRAFT)}}}])
        self.tokens = {'whole_turn_status': ['A']}
        self.refs = {'old_result': {'attempt': 'A', 'revision': 1, 'slot': 'draft_status'}}
        return {'actions': ['goal G', 'plan P@1', 'attempt A', 'result slot in attempt revision 1'],
                'observations': {'R_locator': deepcopy(self.refs['old_result']),
                                 'product_record_present': 'R' in self.store}}

    def l1(self):
        self.edit_plan({'turnstep': deepcopy(PLAN_V2_TURNSTEP)})
        return {'actions': ['edit only P.turnstep'],
                'observations': {'plan_revision': self.store['P']['revision'],
                                 'result_revision': self.latest_revision(),
                                 'R_state': self.slot(1, 'draft_status')['state']}}

    def l2(self):
        self.adopt('A', 2, ['turnstep'], ['SYN:chain-adopt'])
        return {'actions': ['A adopts P@2 for turnstep'],
                'observations': {'adoptions': deepcopy(self.store['A']['decisions'])}}

    def l3(self):
        revision = self.write_slots({'draft_status': {'state': 'present',
                                                      'dimensions': deepcopy(CODE_WRITTEN)}},
                                    'new result under P@2')
        self.refs['new_result'] = {'attempt': 'A', 'revision': revision, 'slot': 'draft_status'}
        return {'actions': ['write draft_status in a new result revision'],
                'observations': {'Q_locator': deepcopy(self.refs['new_result']),
                                 'R_still': self.slot(1, 'draft_status')['dimensions'],
                                 'written': ['draft_status']}}

    def l4(self):
        revision = self.refs['new_result']['revision']
        dims = self.slot(revision, 'draft_status')['dimensions']
        new_record(self.store, 'E', 'evidence', goal='G',
                   subject=deepcopy(self.refs['new_result']), scope='result dimensions',
                   nature='synthetic',
                   findings=['draft_status at check: %s; acceptance %s'
                             % (dims['implementation'], dims['acceptance'])])
        self.refs['check'] = {'id': 'E', 'revision': 1}
        return {'actions': ['record exact result check as Evidence E'],
                'observations': {'findings': deepcopy(self.store['E']['findings']),
                                 'subject': deepcopy(self.store['E']['subject'])}}

    def l5(self):
        self.end('A')
        return {'actions': ['end A with retained responsibility'],
                'observations': {'attempt_status': self.store['A']['status'],
                                 'old_result_dimensions': self.slot(1, 'draft_status')['dimensions'],
                                 'old_result_state': self.slot(1, 'draft_status')['state'],
                                 'goal_acceptance': self.store['G']['acceptance']}}

    def l6(self):
        status_at_write = self.store['A']['status']
        first = self.write_slots({'draft_status': {
            'state': 'present',
            'dimensions': {'completion': 'in_progress',
                           'implementation': 'reported_code_written',
                           'git': 'unstaged', 'acceptance': 'pending'}}},
            'correct draft_status while the attempt is ended')
        checked = self.slot(self.refs['new_result']['revision'], 'draft_status')['dimensions']
        bump(self.store, 'A', status='active', outcome='unknown',
             reopen_history=[{'change': self.head + 1, 'prior_status': 'ended'}])
        return {'actions': ['correct the result while A is ended', 'reopen A'],
                'observations': {'status_at_write': status_at_write,
                                 'correction_revision': first,
                                 'old_result_dimensions': checked,
                                 'current_dimensions': self.slot(first, 'draft_status')['dimensions'],
                                 'attempt_status': self.store['A']['status']}}

    def produce(self, aid, pid, parts, section, dimensions):  # pragma: no cover - not used
        raise Reject('C2 B has no independent product identity')

    def continue_in_second_attempt(self):
        source = self.latest_revision()
        content = deepcopy(self.slot(source, 'draft_status'))
        content['copied_from'] = {'attempt': 'A', 'revision': source, 'slot': 'draft_status'}
        content['dimensions'] = {'completion': 'reported_complete',
                                 'implementation': 'reported_code_written',
                                 'git': 'unstaged', 'acceptance': 'pending'}
        new_record(self.store, 'A2', 'attempt', goal='G', status='active',
                   scope=['turnstep draft'], decisions=[],
                   content=[{'revision': 1, 'label': 'copied continuing result',
                             'written': ['draft_status'], 'slots': {'draft_status': content}}])
        before = {'attempt': 'A', 'revision': source, 'slot': 'draft_status'}
        after = {'attempt': 'A2', 'revision': 1, 'slot': 'draft_status'}
        return {'actions': ['begin A2 by copying the result slot and advancing it'],
                'observations': {'before_locator': before, 'after_locator': after,
                                 'same_locator': before == after,
                                 'old_slot_unchanged': self.slot(source, 'draft_status')['dimensions'],
                                 'advanced_by': 'A2'}}

    def withdraw_current(self):
        revision = self.write_slots({'draft_status': {
            'state': 'withdrawn',
            'dimensions': self.slot(self.latest_revision(), 'draft_status')['dimensions']}},
            'withdraw only draft_status')
        return {'actions': ['withdraw only draft_status'],
                'observations': {'revision': revision,
                                 'states': {name: self.slot(revision, name)['state']
                                            for name in ('draft_status', 'draft_notifications')}}}

    def final_state(self):
        latest = self.latest_revision()
        states = {name: self.slot(latest, name)['state']
                  for name in ('draft_status', 'draft_notifications')}
        return {
            'content': {
                'old_result_states': {name: self.slot(1, name)['state']
                                      for name in ('draft_status', 'draft_notifications')},
                'new_result_states_after_withdraw': states,
                'old_result_dimensions': self.slot(1, 'draft_status')['dimensions'],
                'old_check_findings': deepcopy(self.store['E']['findings']),
                'goal_acceptance': self.store['G']['acceptance'],
                'old_check_still_resolves':
                    self.slot(self.store['E']['subject']['revision'],
                              self.store['E']['subject']['slot'])['state'] == 'present'},
            'capabilities': {
                'independent_product_record': False,
                'old_result_resolvable_after_end': self.slot(1, 'draft_status')['state'] == 'present',
                'partial_withdraw_single_slot': states['draft_status'] == 'withdrawn'
                                                and states['draft_notifications'] == 'present',
                'same_result_identity_across_attempts': False,
                'slot_local_identity_required': True},
            'locators': {
                'old_result': deepcopy(self.refs['old_result']),
                'new_result': deepcopy(self.refs['new_result']),
                'old_check_subject': deepcopy(self.store['E']['subject'])},
        }

    def identity_count(self):
        return {'product_identities': 0,
                'result_slots': len(self.store['A']['content'][-1]['slots']),
                'attempt_content_revisions_retained': len(self.store['A']['content'])}

    def revision_sequences(self):
        return [{'sequence': 'A.content revisions',
                 'current': self.latest_revision(),
                 'retained': [item['revision'] for item in self.store['A']['content']]}]

    def query_entry_points(self):
        return ['slot(attempt revision, name)', 'content revision list on the host',
                'written slots per revision']

    def conventions(self):
        return ['attempt 内容修订必须逐版保留',
                '定位必须携带 (attempt, revision, slot)，slot 名是局部身份',
                '每次写入必须记录 written 列表，否则无法区分哪些 slot 被这次修订推进',
                '生命周期状态与内容修订分离，ended 时仍可追加成果修正',
                '跨尝试延续只能复制 slot，旧 locator 保持不变']

    def failure_modes(self):
        return ['slot 名成为必须维护的局部身份，改名会破坏旧定位',
                '删掉旧内容修订会让旧证据的成果引用悬空',
                '同一 slot 在不同尝试中不能保持同一身份']

    def native(self):
        return {'storage': 'store["A"].content revisions with slots',
                'varied_identity': 'none for Product',
                'locator': '{attempt, revision, slot}',
                'sample': deepcopy(self.store['A']['content'][-1])}


# ------------------------------------------------------------ C3 Evidence


class C3A(PlanProductWorld):
    group, mode = 'C3', 'A'

    def l0(self):
        new_record(self.store, 'G', 'goal', scope=FEATURES, acceptance='pending')
        new_record(self.store, 'P', 'plan', sections=deepcopy(PLAN_V1), links=[])
        new_record(self.store, 'A', 'attempt', goal='G', status='active',
                   scope=['turnstep draft'], decisions=[])
        new_record(self.store, 'Q', 'product', attempt='A',
                   parts={'draft_status': 'present'},
                   dimensions=deepcopy(DRAFT),
                   plan_usage={'turnstep': {'id': 'P', 'revision': 1}})
        self.tokens = {'whole_turn_status': ['A']}
        self.refs = {'result': {'id': 'Q', 'revision': 1}}
        return {'actions': ['goal G', 'plan P@1', 'attempt A', 'product Q'],
                'observations': {'Q': deepcopy(self.refs['result'])}}

    def l1(self):
        self.edit_plan({'turnstep': deepcopy(PLAN_V2_TURNSTEP)})
        return {'actions': ['edit only P.turnstep'],
                'observations': {'plan_revision': self.store['P']['revision']}}

    def l2(self):
        self.adopt('A', 2, ['turnstep'], ['SYN:chain-adopt'])
        return {'actions': ['A adopts P@2 for turnstep'],
                'observations': {'adoptions': deepcopy(self.store['A']['decisions'])}}

    def l3(self):
        self.produce('A', 'Q2', ['draft_status'], 'turnstep', CODE_WRITTEN)
        self.refs['new_result'] = {'id': 'Q2', 'revision': 1}
        return {'actions': ['produce Q2 under P@2'],
                'observations': {'Q2_plan': deepcopy(self.store['Q2']['plan_usage'])}}

    def l4(self):
        new_record(self.store, 'E1', 'evidence', goal='G',
                   subject={'id': 'Q2', 'revision': 1}, scope='draft_status completion',
                   nature='synthetic',
                   findings=['completion reported; acceptance pending'])
        self.refs['report'] = {'id': 'E1', 'revision': 1}
        return {'actions': ['record report E1'],
                'observations': {'subject': deepcopy(self.store['E1']['subject']),
                                 'findings': deepcopy(self.store['E1']['findings'])}}

    def l5(self):
        self.end('A')
        return {'actions': ['end A with retained responsibility'],
                'observations': {'attempt_status': self.store['A']['status'],
                                 'goal_acceptance': self.store['G']['acceptance']}}

    def l6(self):
        self.advance('Q2', {'completion': 'in_progress'})
        bump(self.store, 'A', status='active', outcome='unknown',
             reopen_history=[{'change': self.head + 1, 'prior_status': 'ended'}])
        return {'actions': ['regress Q2', 'reopen A'],
                'observations': {'old_subject_revision': self.store['E1']['subject']['revision'],
                                 'old_findings': deepcopy(self.store['E1']['findings']),
                                 'current_dimensions': self.store['Q2']['dimensions']}}

    def add_correction(self):
        new_record(self.store, 'E2', 'evidence', goal='G',
                   subject={'id': 'Q2', 'revision': 2}, scope='draft_status completion',
                   nature='synthetic',
                   findings=['correction: completion regressed to in_progress',
                             'previous statement retained'],
                   supersedes={'id': 'E1', 'revision': 1})
        self.refs['correction'] = {'id': 'E2', 'revision': 1}
        return {'actions': ['register a correcting report E2'],
                'observations': {'supersedes': deepcopy(self.store['E2']['supersedes']),
                                 'old_still': deepcopy(self.store['E1']['findings'])}}

    def two_scopes(self):
        new_record(self.store, 'E3', 'evidence', goal='G',
                   subject={'id': 'Q2', 'revision': 2}, scope='presentation only',
                   nature='synthetic', findings=['presentation scope unaffected'])
        new_record(self.store, 'E4', 'evidence', goal='G',
                   subject={'id': 'Q2', 'revision': 2}, scope='turnstep worktree only',
                   nature='synthetic', findings=['turnstep scope regressed'])
        return {'actions': ['register two reports with different scopes in one change'],
                'observations': {'scopes': [self.store['E3']['scope'], self.store['E4']['scope']]}}

    def accept(self):
        locator = deepcopy(self.refs['report'])
        bump(self.store, 'G', acceptance='accepted',
             decision={'actor': 'synthetic-reviewer',
                       'criteria': ['exact evidence present', 'scope named'],
                       'evidence': [deepcopy(locator), deepcopy(locator)]})
        return {'actions': ['accept G citing the same report twice'],
                'observations': {'evidence': deepcopy(self.store['G']['decision']['evidence']),
                                 'citations': len(self.store['G']['decision']['evidence'])}}

    def add_second_report(self):
        new_record(self.store, 'E2', 'evidence', goal='G',
                   subject={'id': 'Q2', 'revision': 2}, scope='draft_status completion',
                   nature='synthetic',
                   findings=['correction: completion regressed to in_progress',
                             'previous statement retained'],
                   supersedes={'id': 'E1', 'revision': 1})
        self.refs['correction'] = {'id': 'E2', 'revision': 1}
        return {'actions': ['register a correcting report E2'],
                'observations': {'supersedes': deepcopy(self.store['E2']['supersedes']),
                                 'old_still': deepcopy(self.store['E1']['findings'])}}

    def two_scopes(self):
        new_record(self.store, 'E3', 'evidence', goal='G',
                   subject={'id': 'Q2', 'revision': 2}, scope='presentation only',
                   nature='synthetic', findings=['presentation scope unaffected'])
        new_record(self.store, 'E4', 'evidence', goal='G',
                   subject={'id': 'Q2', 'revision': 2}, scope='turnstep worktree only',
                   nature='synthetic', findings=['turnstep scope regressed'])
        return {'actions': ['register two reports with different scopes in one change'],
                'observations': {'scopes': [self.store['E3']['scope'], self.store['E4']['scope']]}}

    def accept(self):
        locator = deepcopy(self.refs['report'])
        bump(self.store, 'G', acceptance='accepted',
             decision={'actor': 'synthetic-reviewer',
                       'criteria': ['exact evidence present', 'scope named'],
                       'evidence': [deepcopy(locator), deepcopy(locator)]})
        return {'actions': ['accept G citing the same report twice'],
                'observations': {'evidence': deepcopy(self.store['G']['decision']['evidence']),
                                 'citations': len(self.store['G']['decision']['evidence'])}}

    def final_state(self):
        subject = self.store['E1']['subject']
        rows = self.statements_for('Q2')
        return {
            'content': {
                'original_findings': deepcopy(self.store['E1']['findings']),
                'correction_findings': deepcopy(self.store['E2']['findings']),
                'report_scope_after_subject_update': self.store['E1']['scope'],
                'subject_revision_at_report': subject['revision'],
                'current_subject_revision': self.store['Q2']['revision'],
                'subject_statement_count': len(rows),
                'goal_acceptance': self.store['G']['acceptance']},
            'capabilities': {
                'independent_evidence_record': 'E1' in self.store,
                'report_locator_survives_subject_update':
                    at(self.store, 'Q2', subject['revision'])['revision'] == 1,
                'correction_retains_old_statement': 'E1' in self.store and 'E2' in self.store,
                'same_report_referenced_twice': len(self.store['G']['decision']['evidence']) == 2
                                                and self.store['G']['decision']['evidence'][0]
                                                == self.store['G']['decision']['evidence'][1],
                'subject_query_returns_all_statements': len(rows) >= 2,
                'reference_needs_change_number': False},
            'recorded_failures': [],
            'locators': {
                'report': deepcopy(self.refs['report']),
                'correction': deepcopy(self.refs['correction']),
                'subject': deepcopy(self.store['E1']['subject'])},
        }

    def statements_for(self, subject_id):
        return [key for key, obj in sorted(self.store.items())
                if obj['kind'] == 'evidence' and obj['subject']['id'] == subject_id]

    def identity_count(self):
        evidence = [key for key, obj in self.store.items() if obj['kind'] == 'evidence']
        return {'evidence_identities': len(evidence), 'evidence_revisions': len(evidence)}

    def revision_sequences(self):
        evidence = [key for key, obj in self.store.items() if obj['kind'] == 'evidence']
        return [{'sequence': 'Evidence revisions', 'current': 1, 'records': evidence}]

    def query_entry_points(self):
        return ['at(store, evidence, revision)', 'statements_for(subject id)',
                'goal.decision.evidence']

    def conventions(self):
        return ['Evidence ID、revision、subject 的 exact 版本与 nature',
                '更正作为新 Evidence，旧 Evidence 保留',
                '验收引用 Evidence 的 exact {id, revision}']

    def failure_modes(self):
        return ['Evidence 与 Change 各自编号，两个序列需要协调',
                'subject 身份相同但 revision 不同，按 subject 查询必须自己决定是否合并']

    def native(self):
        return {'storage': 'store["E1"] independent evidence record',
                'varied_identity': 'evidence id',
                'locator': '{id, revision}',
                'sample': deepcopy(self.store['E1'])}


class C3B(PlanProductWorld):
    group, mode = 'C3', 'B'

    def statements(self, subject_id=None):
        rows = []
        for number in sorted(self.change_statements, key=int):
            for index, stmt in enumerate(self.change_statements[number]):
                if subject_id is None or stmt['subject']['id'] == subject_id:
                    rows.append({'locator': {'change': int(number), 'statement': index},
                                 'statement': deepcopy(stmt)})
        return rows

    def add_statement(self, subject, scope, findings, supersedes=None):
        number = self.head + 1
        statement = {'subject': deepcopy(subject), 'scope': scope,
                     'findings': list(findings), 'nature': 'synthetic'}
        if supersedes is not None:
            statement['supersedes'] = deepcopy(supersedes)
        self.change_statements.setdefault(number, []).append(statement)
        return {'change': number, 'statement': len(self.change_statements[number]) - 1}

    def statement(self, locator):
        need(isinstance(locator, dict) and set(locator) == {'change', 'statement'},
             'statement locator must be {change, statement}')
        need(type(locator['change']) is int and locator['change'] > 0,
             'positive change number required')
        need(locator['change'] in self.change_statements,
             'change has no statements: %s' % locator['change'])
        rows = self.change_statements[locator['change']]
        need(type(locator['statement']) is int and 0 <= locator['statement'] < len(rows),
             'statement index out of range')
        return deepcopy(rows[locator['statement']])

    def latest_for_subject(self, subject_id):
        found = self.statements(subject_id)
        need(bool(found), 'no statements for subject: ' + subject_id)
        return found[-1]

    def l0(self):
        new_record(self.store, 'G', 'goal', scope=FEATURES, acceptance='pending')
        new_record(self.store, 'P', 'plan', sections=deepcopy(PLAN_V1), links=[])
        new_record(self.store, 'A', 'attempt', goal='G', status='active',
                   scope=['turnstep draft'], decisions=[])
        new_record(self.store, 'Q', 'product', attempt='A',
                   parts={'draft_status': 'present'}, dimensions=deepcopy(DRAFT),
                   plan_usage={'turnstep': {'id': 'P', 'revision': 1}})
        self.tokens = {'whole_turn_status': ['A']}
        self.refs = {'result': {'id': 'Q', 'revision': 1}}
        return {'actions': ['goal G', 'plan P@1', 'attempt A', 'product Q'],
                'observations': {'Q': deepcopy(self.refs['result']),
                                 'evidence_records': 0}}

    def l1(self):
        self.edit_plan({'turnstep': deepcopy(PLAN_V2_TURNSTEP)})
        return {'actions': ['edit only P.turnstep'],
                'observations': {'plan_revision': self.store['P']['revision']}}

    def l2(self):
        self.adopt('A', 2, ['turnstep'], ['SYN:chain-adopt'])
        return {'actions': ['A adopts P@2 for turnstep'],
                'observations': {'adoptions': deepcopy(self.store['A']['decisions'])}}

    def l3(self):
        self.produce('A', 'Q2', ['draft_status'], 'turnstep', CODE_WRITTEN)
        self.refs['new_result'] = {'id': 'Q2', 'revision': 1}
        return {'actions': ['produce Q2 under P@2'],
                'observations': {'Q2_plan': deepcopy(self.store['Q2']['plan_usage'])}}

    def l4(self):
        locator = self.add_statement({'id': 'Q2', 'revision': 1}, 'draft_status completion',
                                     ['completion reported; acceptance pending'])
        self.refs['report'] = locator
        return {'actions': ['append report statement inside this Change'],
                'observations': {'locator': deepcopy(locator),
                                 'statement': self.statement(locator),
                                 'evidence_records': sum(1 for obj in self.store.values()
                                                         if obj['kind'] == 'evidence')}}

    def l5(self):
        self.end('A')
        return {'actions': ['end A with retained responsibility'],
                'observations': {'attempt_status': self.store['A']['status'],
                                 'goal_acceptance': self.store['G']['acceptance']}}

    def l6(self):
        self.advance('Q2', {'completion': 'in_progress'})
        bump(self.store, 'A', status='active', outcome='unknown',
             reopen_history=[{'change': self.head + 1, 'prior_status': 'ended'}])
        return {'actions': ['regress Q2', 'reopen A'],
                'observations': {'report_statement': self.statement(self.refs['report']),
                                 'current_dimensions': self.store['Q2']['dimensions']}}

    def add_correction(self):
        locator = self.add_statement({'id': 'Q2', 'revision': 2}, 'draft_status completion',
                                     ['correction: completion regressed to in_progress',
                                      'previous statement retained'],
                                     supersedes=deepcopy(self.refs['report']))
        self.refs['correction'] = locator
        return {'actions': ['append a correcting statement in a new Change'],
                'observations': {'correction': deepcopy(locator),
                                 'old_statement': self.statement(self.refs['report']),
                                 'supersedes': self.statement(locator).get('supersedes')}}

    def two_scopes(self):
        first = self.add_statement({'id': 'Q2', 'revision': 2}, 'presentation only',
                                   ['presentation scope unaffected'])
        second = self.add_statement({'id': 'Q2', 'revision': 2}, 'turnstep worktree only',
                                    ['turnstep scope regressed'])
        return {'actions': ['append two statements with different scopes in one Change'],
                'observations': {'first': deepcopy(first), 'second': deepcopy(second),
                                 'same_change': first['change'] == second['change'],
                                 'scopes': [self.statement(first)['scope'], self.statement(second)['scope']]}}

    def accept(self):
        locator = deepcopy(self.refs['report'])
        need(self.statement(locator)['subject']['id'] == 'Q2', 'statement subject must resolve')
        bump(self.store, 'G', acceptance='accepted',
             decision={'actor': 'synthetic-reviewer',
                       'criteria': ['locator resolves', 'scope named'],
                       'evidence': [deepcopy(locator), deepcopy(locator)]})
        return {'actions': ['accept G citing the same statement locator twice'],
                'observations': {'evidence': deepcopy(self.store['G']['decision']['evidence']),
                                 'citations': len(self.store['G']['decision']['evidence'])}}

    def final_state(self):
        report = self.statement(self.refs['report'])
        correction = self.statement(self.refs['correction'])
        rows = self.statements('Q2')
        naive = self.latest_for_subject('Q2')
        failures = [] if naive['locator'] == self.refs['report'] else [
            {'kind': 'wrong_answer',
             'query': '只按 subject 取最新一条陈述',
             'returned': naive['statement']['findings'],
             'expected': report['findings']}]
        return {
            'content': {
                'original_findings': report['findings'],
                'correction_findings': correction['findings'],
                'report_scope_after_subject_update': report['scope'],
                'subject_revision_at_report': report['subject']['revision'],
                'current_subject_revision': self.store['Q2']['revision'],
                'subject_statement_count': len(rows),
                'goal_acceptance': self.store['G']['acceptance']},
            'capabilities': {
                'independent_evidence_record': any(obj['kind'] == 'evidence'
                                                   for obj in self.store.values()),
                'report_locator_survives_subject_update':
                    self.statement(self.refs['report'])['subject']['revision'] == 1,
                'correction_retains_old_statement':
                    bool(self.statement(self.refs['report'])['findings'])
                    and bool(self.statement(self.refs['correction'])['findings']),
                'same_report_referenced_twice': len(self.store['G']['decision']['evidence']) == 2
                                                and self.store['G']['decision']['evidence'][0]
                                                == self.store['G']['decision']['evidence'][1],
                'subject_query_returns_all_statements': len(rows) >= 2,
                'reference_needs_change_number': True},
            'recorded_failures': failures,
            'locators': {
                'report': deepcopy(self.refs['report']),
                'correction': deepcopy(self.refs['correction']),
                'subject': deepcopy(report['subject'])},
        }

    def identity_count(self):
        total = sum(len(rows) for rows in self.change_statements.values())
        return {'evidence_identities': 0, 'statement_locators': total,
                'changes_with_statements': len(self.change_statements)}

    def revision_sequences(self):
        return [{'sequence': 'Change numbers', 'current': self.head,
                 'with_statements': sorted(self.change_statements, key=int)}]

    def query_entry_points(self):
        return ['statement({change, statement})', 'statements(subject id)',
                'latest_for_subject(subject id)']

    def conventions(self):
        return ['Change 编号 append-only，语句序号在同一 Change 内固定',
                '定位必须携带 (change, statement)，只按 subject 取最新会漂移',
                '更正需要新 Change 与新语句，旧语句不修改',
                '验收引用同一 locator 两次，locator 宽度为两项']

    def failure_modes(self):
        return ['只按 subject 取最新会返回修正后的结论，丢失原报告',
                'Change 编号若被压缩或语句被重排，locator 静默指向别的陈述',
                '没有 evidence kind 检查，验收时才能发现 subject 不可追踪']

    def native(self):
        return {'storage': 'change_statements[change][index]',
                'varied_identity': 'none for Evidence',
                'locator': '{change, statement}',
                'sample': deepcopy(self.change_statements[self.refs['report']['change']])}


# --------------------------------------------------------- C4 Goal/Attempt


class C4A(PlanProductWorld):
    group, mode = 'C4', 'A'

    def l0(self):
        new_record(self.store, 'G', 'goal', scope=FEATURES, acceptance='pending')
        new_record(self.store, 'P', 'plan', sections=deepcopy(PLAN_V1), links=[])
        new_record(self.store, 'a1', 'attempt', goal='G', goal_revision=1, status='active',
                   scope=['turnstep draft'], decisions=[])
        new_record(self.store, 'Q', 'product', attempt='a1',
                   parts={'draft_status': 'present'}, dimensions=deepcopy(DRAFT),
                   plan_usage={'turnstep': {'id': 'P', 'revision': 1}})
        self.tokens = {'whole_turn_status': ['a1']}
        self.refs = {'goal': {'id': 'G', 'revision': 1}, 'attempt': {'id': 'a1', 'revision': 1}}
        return {'actions': ['goal G@1', 'plan P@1', 'attempt a1', 'product Q'],
                'observations': {'goal': deepcopy(self.refs['goal'])}}

    def l1(self):
        self.edit_plan({'turnstep': deepcopy(PLAN_V2_TURNSTEP)})
        return {'actions': ['edit only P.turnstep'],
                'observations': {'plan_revision': self.store['P']['revision']}}

    def l2(self):
        self.adopt('a1', 2, ['turnstep'], ['SYN:chain-adopt'])
        return {'actions': ['a1 adopts P@2 for turnstep'],
                'observations': {'adoptions': deepcopy(self.store['a1']['decisions'])}}

    def l3(self):
        self.produce('a1', 'Q2', ['draft_status'], 'turnstep', CODE_WRITTEN)
        self.refs['new_result'] = {'id': 'Q2', 'revision': 1}
        return {'actions': ['produce Q2 under P@2'],
                'observations': {'Q2_plan': deepcopy(self.store['Q2']['plan_usage'])}}

    def l4(self):
        new_record(self.store, 'E', 'evidence', goal='G',
                   subject={'id': 'Q2', 'revision': 1}, scope='attempt a1 scope',
                   nature='synthetic', findings=['attempt a1 scope: turnstep draft'])
        self.refs['check'] = {'id': 'E', 'revision': 1}
        return {'actions': ['record checks against a1'],
                'observations': {'findings': deepcopy(self.store['E']['findings'])}}

    def l5(self):
        self.end('a1')
        return {'actions': ['end a1 with retained responsibility'],
                'observations': {'attempt_status': self.store['a1']['status'],
                                 'goal_acceptance': self.store['G']['acceptance']}}

    def begin_attempt(self, key, scope):
        need(isinstance(scope, list) and bool(scope), 'attempt scope required')
        new_record(self.store, key, 'attempt', goal='G',
                   goal_revision=self.store['G']['revision'], status='active',
                   scope=list(scope), decisions=[])

    def revise_goal(self, scope):
        need(isinstance(scope, list) and bool(scope), 'nonempty goal scope required')
        bump(self.store, 'G', scope=list(scope))

    def l6(self):
        self.begin_attempt('a2', ['second attempt on the same goal'])
        self.begin_attempt('a3', ['parallel attempt on the same goal'])
        self.revise_goal(REVISED_SCOPE)
        self.advance('Q2', {'completion': 'in_progress'})
        return {'actions': ['begin a2 and a3', 'revise G scope', 'regress Q2'],
                'observations': {'attempts': self.attempt_ids(),
                                 'statuses': self.attempt_statuses(),
                                 'a1_goal_revision': self.store['a1']['goal_revision'],
                                 'goal_revision': self.store['G']['revision']}}

    def attempt_ids(self):
        return sorted(key for key, obj in self.store.items() if obj['kind'] == 'attempt')

    def attempt_statuses(self):
        return {key: self.store[key]['status'] for key in self.attempt_ids()}

    def final_state(self):
        return {
            'content': {
                'attempt_keys': self.attempt_ids(),
                'attempt_status': self.attempt_statuses(),
                'a1_scope_basis': at(self.store, 'G', 1)['scope'],
                'current_goal_scope': self.store['G']['scope'],
                'goal_acceptance': self.store['G']['acceptance'],
                'old_check_findings': deepcopy(self.store['E']['findings'])},
            'capabilities': {
                'independent_goal_record': 'G' in self.store and self.store['G']['kind'] == 'goal',
                'attempt_ended_goal_continues': self.store['a1']['status'] == 'ended'
                                                and self.store['G']['acceptance'] == 'pending',
                'two_attempts_same_goal': len(self.attempt_ids()) >= 2,
                'parallel_attempts': self.store['a2']['status'] == 'active'
                                     and self.store['a3']['status'] == 'active',
                'old_attempt_keeps_old_goal_scope':
                    self.store['a1']['goal_revision'] == 1
                    and at(self.store, 'G', 1)['scope'] == FEATURES,
                'attempt_key_reintroduced': False},
            'locators': {
                'goal': {'id': 'G', 'revision': self.store['G']['revision']},
                'attempt': {'id': 'a1', 'revision': at(self.store, 'a1', 1)['revision']}},
        }

    def identity_count(self):
        return {'goal_identities': 1, 'attempt_identities': len(self.attempt_ids()),
                'goal_revisions_retained': len(self.store['G']['versions']) + 1}

    def revision_sequences(self):
        return [{'sequence': 'G.revision', 'current': self.store['G']['revision']},
                {'sequence': 'attempt revisions',
                 'current': {key: self.store[key]['revision'] for key in self.attempt_ids()}}]

    def query_entry_points(self):
        return ['at(store, goal, revision)', 'attempt.goal', 'attempt.goal_revision']

    def conventions(self):
        return ['Goal ID、revision、范围与验收状态',
                '每条 Attempt 记录 goal 与 goal_revision',
                '验收决定引用 exact evidence']

    def failure_modes(self):
        return ['目标与尝试是两个生命周期，结束/验收需要分别检查']

    def native(self):
        return {'storage': 'store["G"] goal + store["a1"] attempt',
                'varied_identity': 'goal id + attempt id',
                'locator': '{id, revision} for each',
                'sample': deepcopy(self.store['G'])}


class C4B(PlanProductWorld):
    group, mode = 'C4', 'B'

    def goal_revision(self):
        return self.store['W']['goal_revisions'][-1]['revision']

    def goal_current(self):
        return deepcopy(self.store['W']['goal_revisions'][-1])

    def goal_at(self, revision):
        exact_revision(revision, 'goal revision')
        for item in self.store['W']['goal_revisions']:
            if item['revision'] == revision:
                return deepcopy(item)
        raise Reject('goal revision not retained: %s' % revision)

    def attempt_entry(self, key):
        for entry in self.store['W']['attempts']:
            if entry['key'] == key:
                return entry
        raise Reject('unknown attempt key: ' + key)

    def begin_attempt(self, key, scope):
        need(all(entry['key'] != key for entry in self.store['W']['attempts']),
             'duplicate attempt key: ' + key)
        self.store['W']['attempts'].append({'key': key, 'goal_revision': self.goal_revision(),
                                            'status': 'active', 'scope': scope, 'decisions': []})

    def adopt(self, aid, revision, scope, basis):
        entry = self.attempt_entry(aid)
        need(entry['status'] == 'active', 'adoption requires an active attempt')
        plan = at(self.store, 'P', revision)
        need(isinstance(scope, list) and bool(scope) and len(set(scope)) == len(scope),
             'unique nonempty adoption scope required')
        need(set(scope) <= set(plan['sections']), 'adoption scope must name sections of that revision')
        need(isinstance(basis, list) and bool(basis)
             and all(isinstance(x, str) and x.startswith('SYN:') for x in basis),
             'synthetic adoption basis required')
        entry['decisions'].append({'plan': {'id': 'P', 'revision': revision},
                                   'scope': list(scope), 'basis': list(basis),
                                   'change': self.head + 1})

    def effective(self, aid, section):
        found = None
        for record in self.attempt_entry(aid)['decisions']:
            if section in record['scope']:
                found = deepcopy(record['plan'])
        need(found is not None, 'plan scope was not adopted: ' + section)
        return found

    def produce(self, aid, pid, parts, section, dimensions):
        entry = self.attempt_entry(aid)
        need(entry['status'] == 'active', 'producing a new result requires an active attempt')
        basis = self.effective(aid, section)
        new_record(self.store, pid, 'product', attempt=aid,
                   parts={part: 'present' for part in parts},
                   dimensions=deepcopy(dimensions), plan_usage={section: basis})

    def revise_goal(self, scope):
        need(isinstance(scope, list) and bool(scope), 'nonempty goal scope required')
        self.store['W']['goal_revisions'].append(
            {'revision': self.goal_revision() + 1, 'scope': list(scope), 'acceptance': 'pending'})

    def end(self, aid, remaining='retained_unresolved'):
        entry = self.attempt_entry(aid)
        need(entry['status'] == 'active', 'active attempt required')
        need(remaining in {None, 'retained_unresolved'},
             'ending holder must disclose remaining responsibility as retained_unresolved')
        held = sorted(token for token, holders in self.tokens.items() if aid in holders)
        need(not held or remaining == 'retained_unresolved',
             'ending holder must disclose remaining assigned responsibility')
        entry.update({'status': 'ended', 'outcome': 'synthetic stop',
                      'remaining_responsibility': remaining, 'held_at_end': held})

    def l0(self):
        new_record(self.store, 'W', 'work',
                   goal_revisions=[{'revision': 1, 'scope': deepcopy(FEATURES),
                                    'acceptance': 'pending'}],
                   attempts=[])
        new_record(self.store, 'P', 'plan', sections=deepcopy(PLAN_V1), links=[])
        self.begin_attempt('a1', ['turnstep draft'])
        new_record(self.store, 'Q', 'product', attempt='a1',
                   parts={'draft_status': 'present'}, dimensions=deepcopy(DRAFT),
                   plan_usage={'turnstep': {'id': 'P', 'revision': 1}})
        self.tokens = {'whole_turn_status': ['a1']}
        self.refs = {'goal': {'work': 'W', 'revision': 1}, 'attempt': {'work': 'W', 'key': 'a1'}}
        return {'actions': ['work W with goal revision 1', 'attempt entry a1', 'product Q'],
                'observations': {'goal': self.goal_current(), 'attempts': ['a1']}}

    def l1(self):
        self.edit_plan({'turnstep': deepcopy(PLAN_V2_TURNSTEP)})
        return {'actions': ['edit only P.turnstep'],
                'observations': {'plan_revision': self.store['P']['revision']}}

    def l2(self):
        self.adopt('a1', 2, ['turnstep'], ['SYN:chain-adopt'])
        return {'actions': ['a1 adopts P@2'],
                'observations': {'decisions': deepcopy(self.attempt_entry('a1')['decisions'])}}

    def l3(self):
        self.produce('a1', 'Q2', ['draft_status'], 'turnstep', CODE_WRITTEN)
        self.refs['new_result'] = {'id': 'Q2', 'revision': 1}
        return {'actions': ['produce Q2 under P@2'],
                'observations': {'Q2_plan': deepcopy(self.store['Q2']['plan_usage'])}}

    def l4(self):
        new_record(self.store, 'E', 'evidence', goal='W',
                   subject={'id': 'Q2', 'revision': 1}, scope='attempt a1 scope',
                   nature='synthetic', findings=['attempt a1 scope: turnstep draft'])
        self.refs['check'] = {'id': 'E', 'revision': 1}
        return {'actions': ['record checks against a1'],
                'observations': {'findings': deepcopy(self.store['E']['findings'])}}

    def l5(self):
        self.end('a1')
        return {'actions': ['end a1 with retained responsibility'],
                'observations': {'attempt_status': self.attempt_entry('a1')['status'],
                                 'goal_acceptance': self.goal_current()['acceptance']}}

    def l6(self):
        self.begin_attempt('a2', ['second attempt on the same goal'])
        self.begin_attempt('a3', ['parallel attempt on the same goal'])
        self.revise_goal(REVISED_SCOPE)
        self.advance('Q2', {'completion': 'in_progress'})
        return {'actions': ['append a2 and a3', 'append goal revision 2', 'regress Q2'],
                'observations': {'attempts': [entry['key'] for entry in self.store['W']['attempts']],
                                 'statuses': {entry['key']: entry['status']
                                              for entry in self.store['W']['attempts']},
                                 'a1_goal_revision': self.attempt_entry('a1')['goal_revision'],
                                 'goal_revision': self.goal_revision()}}

    def attempt_ids(self):
        return [entry['key'] for entry in self.store['W']['attempts']]

    def final_state(self):
        return {
            'content': {
                'attempt_keys': self.attempt_ids(),
                'attempt_status': {entry['key']: entry['status']
                                   for entry in self.store['W']['attempts']},
                'a1_scope_basis': self.goal_at(1)['scope'],
                'current_goal_scope': self.goal_current()['scope'],
                'goal_acceptance': self.goal_current()['acceptance'],
                'old_check_findings': deepcopy(self.store['E']['findings'])},
            'capabilities': {
                'independent_goal_record': any(obj['kind'] == 'goal' for obj in self.store.values()),
                'attempt_ended_goal_continues': self.attempt_entry('a1')['status'] == 'ended'
                                                and self.goal_current()['acceptance'] == 'pending',
                'two_attempts_same_goal': len(self.attempt_ids()) >= 2,
                'parallel_attempts': self.attempt_entry('a2')['status'] == 'active'
                                     and self.attempt_entry('a3')['status'] == 'active',
                'old_attempt_keeps_old_goal_scope':
                    self.attempt_entry('a1')['goal_revision'] == 1
                    and self.goal_at(1)['scope'] == FEATURES,
                'attempt_key_reintroduced': True},
            'locators': {
                'goal': {'work': 'W', 'revision': self.goal_revision()},
                'attempt': {'work': 'W', 'key': 'a1'}},
        }

    def identity_count(self):
        return {'work_identities': 1, 'attempt_keys': len(self.attempt_ids()),
                'goal_revisions_retained': len(self.store['W']['goal_revisions'])}

    def revision_sequences(self):
        return [{'sequence': 'W.goal revisions', 'current': self.goal_revision()},
                {'sequence': 'attempt entries', 'current': self.attempt_ids()}]

    def query_entry_points(self):
        return ['goal_at(revision)', 'attempt_entry(key)', 'goal_current()']

    def conventions(self):
        return ['Work 身份 + 目标 revision 列表',
                '每次尝试必须有稳定 key/index，并有独立 status/scope/goal_revision',
                '目标范围修订追加新 revision，旧尝试保留自己的 goal_revision']

    def failure_modes(self):
        return ['attempt key/index 与独立状态就是重新引入的尝试身份，合并只是名义上的',
                'Work 记录同时承载目标与尝试，任何目标修订都要与尝试列表一起写入']

    def native(self):
        return {'storage': 'store["W"] work record',
                'varied_identity': 'work id + attempt key',
                'locator': '{work, revision} for goal; {work, key} for attempt',
                'sample': deepcopy(self.store['W'])}


# --------------------------------------------------------------- builders


def _legal(world, case_id, intent, fn):
    row = world.commit('probe-' + case_id, fn)
    return {'id': case_id, 'intent': intent, 'change': row['change'],
            'actions': row['actions'], 'observations': row['observations'],
            'changed_paths': row['changed_paths'], 'accepted': row['accepted']}


def _illegal(world, case_id, intent, fn, prepare=None):
    outcome = world.expect_reject(fn, prepare=prepare)
    return {'id': case_id, 'intent': intent, 'accepted': outcome['accepted'],
            'error': outcome['error'], 'unchanged_on_rejection': True}


def _removal(world, removed, still, lost, conventions):
    return {'removed': removed, 'still_readable': still, 'lost': lost,
            'conventions_counted': conventions,
            'note': '探针在 world 的副本上执行；lost 中的错误/错误值是实际读出的结果'}


def build_c1(mode):
    world = C1A() if mode == 'A' else C1B()
    chain = world.chain()
    share = _legal(world, 'shared-plan-version',
                   '第二个尝试采用同一计划版本（或说明为何不能）',
                   lambda w: w.begin_second_attempt())
    legal = [share]
    illegal = [
        _illegal(world, 'empty-plan-update', '空更新必须拒绝',
                 lambda w: w.edit_plan({}, [])),
        _illegal(world, 'overlap-update', 'edit 与 remove 重叠必须拒绝',
                 lambda w: w.edit_plan({'turnstep': deepcopy(PLAN_V2_TURNSTEP)}, ['turnstep'])),
        _illegal(world, 'unknown-section', '未知 section 必须拒绝',
                 lambda w: w.edit_plan({'missing': {'status': 'x', 'description': 'y'}}, [])),
        _illegal(world, 'adopt-while-ended', '已结束尝试未 reopen 不能采用新版',
                 lambda w: w.adopt('A', 2, ['turnstep'], ['SYN:ended']),
                 prepare=lambda w: w.end('A')),
        _illegal(world, 'non-exact-revision', 'revision=None 不能当精确版本',
                 lambda w: w.plan_text(None, 'turnstep')),
    ]
    state = world.final_state()
    state['capabilities']['plan_edit_advances_attempt_version'] = any(
        path.startswith('/store/A/') for path in chain[1]['changed_paths'])
    state['capabilities']['shared_plan_version_across_attempts'] = \
        share['observations']['shared_locator']
    probe = deepcopy(world)
    if probe.mode == 'B':
        probe.store['A']['content'] = [probe.store['A']['content'][-1]]
        removed = '只保留宿主 Attempt 的当前内容修订'
        conventions = ['逐版保留宿主内容修订', '定位携带 attempt + revision + section']
    else:
        probe.store['P']['versions'] = {}
        removed = '只保留 Plan 的当前 revision'
        conventions = ['逐版保留 Plan revision', '消费者记录 exact {id, revision}']
    lost = []
    try:
        probe.plan_text(1, 'turnstep')
    except Reject as error:
        lost.append({'query': '旧成果所用 turnstep 文本 @修订1', 'failure': str(error)})
    still = {'current_text': probe.plan_text(probe.host_revision() if probe.mode == 'B' else 2,
                                             'turnstep')}
    return {'alternative': SPEC['C1']['alt_a' if mode == 'A' else 'alt_b'],
            'native': world.native(), 'chain': chain, 'final_state': state,
            'legal': legal, 'illegal': illegal,
            'removal_probe': _removal(probe, removed, still, lost, conventions),
            'identity_cost': world.cost(chain),
            'historical_references': world.historical_references()}


def build_c2(mode):
    world = C2A() if mode == 'A' else C2B()
    chain = world.chain()
    legal = [
        _legal(world, 'second-attempt-continuation', '第二个尝试继续推进同一成果',
               lambda w: w.continue_in_second_attempt()),
        _legal(world, 'withdraw-single-part', '只撤回列明部分，其余保留',
               lambda w: w.withdraw_current()),
    ]
    illegal = []
    if mode == 'A':
        illegal.append(_illegal(world, 'withdraw-unknown-part', '未知部分不能撤回',
                                lambda w: w.withdraw('Q', ['missing'])))
        illegal.append(_illegal(world, 'produce-into-ended', '已结束尝试不能产生新成果',
                                lambda w: w.produce('A', 'X', ['p'], 'turnstep', deepcopy(DRAFT)),
                                prepare=lambda w: w.end('A')))
    else:
        illegal.append(_illegal(world, 'unknown-slot', '未知 slot 不能定位',
                                lambda w: w.slot(1, 'missing')))
        illegal.append(_illegal(world, 'non-exact-result-revision', 'revision=None 不能当结果版本',
                                lambda w: w.slot(None, 'draft_status')))
    state = world.final_state()
    state['capabilities']['result_correction_while_attempt_ended'] = \
        chain[6]['observations']['status_at_write'] == 'ended'
    probe = deepcopy(world)
    if probe.mode == 'B':
        probe.store['A']['content'] = [probe.store['A']['content'][-1]]
        removed = '只保留结果的最新内容修订'
        conventions = ['逐版保留 attempt 内容修订', '定位携带 attempt + revision + slot']
    else:
        probe.store['Q']['versions'] = {}
        removed = '只保留 Product 的当前 revision'
        conventions = ['逐版保留 Product revision', '证据引用 exact {product, revision}']
    lost = []
    try:
        ref = probe.refs['new_result']
        if probe.mode == 'B':
            probe.slot(ref['revision'], ref['slot'])
        else:
            at(probe.store, ref['product'], ref['revision'])
    except Reject as error:
        lost.append({'query': '旧证据指向的成果版本', 'failure': str(error)})
    still = {'current_dimensions': (probe.store['Q']['dimensions'] if probe.mode == 'A'
                                    else probe.slot(probe.latest_revision(), 'draft_status')['dimensions'])}
    return {'alternative': SPEC['C2']['alt_a' if mode == 'A' else 'alt_b'],
            'native': world.native(), 'chain': chain, 'final_state': state,
            'legal': legal, 'illegal': illegal,
            'removal_probe': _removal(probe, removed, still, lost, conventions),
            'identity_cost': world.cost(chain),
            'historical_references': world.historical_references()}


def build_c3(mode):
    world = C3A() if mode == 'A' else C3B()
    chain = world.chain()
    legal = [
        _legal(world, 'correction-retains-old', '新解释纠正旧结论并保留旧陈述',
               lambda w: w.add_correction()),
        _legal(world, 'two-scopes-one-change', '同一 Change 内两条不同范围的陈述',
               lambda w: w.two_scopes()),
        _legal(world, 'same-report-twice', '同一报告被两处引用',
               lambda w: w.accept()),
    ]
    illegal = [
        _illegal(world, 'non-exact-subject', 'subject 的 revision=None 必须拒绝',
                 lambda w: at(w.store, 'Q2', None)),
    ]
    if mode == 'B':
        illegal.append(_illegal(world, 'statement-out-of-range', '语句序号越界必须拒绝',
                                lambda w: w.statement({'change': w.refs['report']['change'],
                                                       'statement': 99})))
        illegal.append(_illegal(world, 'unknown-change', '不存在的 Change 不能定位',
                                lambda w: w.statement({'change': 999, 'statement': 0})))
    else:
        illegal.append(_illegal(world, 'unknown-evidence', '不存在的 Evidence 不能引用',
                                lambda w: at(w.store, 'E999', 1)))
    state = world.final_state()
    probe = deepcopy(world)
    if probe.mode == 'B':
        probe.change_statements[probe.refs['report']['change']].pop(probe.refs['report']['statement'])
        removed = '删除原报告所在的语句序号（保留 Change 与更正）'
        conventions = ['Change 编号与语句序号不可重排', '引用必须使用 (change, statement)']
    else:
        probe.store.pop('E1', None)
        removed = '删除原 Evidence 记录（保留更正记录）'
        conventions = ['Evidence ID 不可复用', '引用使用 exact {id, revision}']
    lost = []
    try:
        if probe.mode == 'B':
            probe.statement(probe.refs['report'])
        else:
            at(probe.store, 'E1', 1)
    except (Reject, KeyError) as error:
        lost.append({'query': '原报告的内容', 'failure': str(error)})
    still = {'correction_findings': (probe.statement(probe.refs['correction'])['findings']
                                     if probe.mode == 'B'
                                     else probe.store['E2']['findings'])}
    return {'alternative': SPEC['C3']['alt_a' if mode == 'A' else 'alt_b'],
            'native': world.native(), 'chain': chain, 'final_state': state,
            'legal': legal, 'illegal': illegal,
            'removal_probe': _removal(probe, removed, still, lost, conventions),
            'identity_cost': world.cost(chain),
            'historical_references': world.historical_references()}


def _third_attempt(world):
    world.begin_attempt('a4', ['third attempt'])
    return {'actions': ['begin a4'], 'observations': {'attempts': world.attempt_ids()}}


def build_c4(mode):
    world = C4A() if mode == 'A' else C4B()
    chain = world.chain()
    legal = [_legal(world, 'third-attempt', '同一目标可以再开一个尝试', _third_attempt)]
    illegal = [
        _illegal(world, 'end-ended-attempt', '已结束尝试不能再次结束',
                 lambda w: w.end('a1')),
        _illegal(world, 'empty-goal-scope', '空目标范围必须拒绝',
                 lambda w: w.revise_goal([])),
    ]
    if mode == 'B':
        illegal.append(_illegal(world, 'unknown-attempt-key', '未知 attempt key 不能定位',
                                lambda w: w.attempt_entry('missing')))
        legal.append(_legal(world, 'attempt-entry-query', '按 key 读回尝试条目',
                            lambda w: {'actions': ['read a1'],
                                       'observations': {'a1': deepcopy(w.attempt_entry('a1')),
                                                        'goal_at_1': w.goal_at(1)}}))
    else:
        illegal.append(_illegal(world, 'unknown-goal-version', '未知 goal revision 不能解析',
                                lambda w: at(w.store, 'G', 99)))
        legal.append(_legal(world, 'attempt-query', '按 ID 读回尝试',
                            lambda w: {'actions': ['read a1'],
                                       'observations': {'a1': deepcopy(at(w.store, 'a1', 1)),
                                                        'goal_at_1': at(w.store, 'G', 1)}}))
    state = world.final_state()
    probe = deepcopy(world)
    if probe.mode == 'B':
        probe.store['W']['attempts'] = probe.store['W']['attempts'][-1:]
        removed = '只保留最近一个 attempt 条目（删除 key/index 历史）'
        conventions = ['attempt key/index 必须逐条保留', '每条尝试独立保存 status/goal_revision']
    else:
        for key in ['a2', 'a3', 'a4']:
            probe.store.pop(key, None)
        removed = '只保留第一条 Attempt（删除后续尝试身份）'
        conventions = ['每条尝试保留 Goal 引用与 goal revision']
    lost = []
    try:
        if probe.mode == 'B':
            probe.attempt_entry('a1')
        else:
            at(probe.store, 'a3', 1)
    except (Reject, KeyError) as error:
        lost.append({'query': '并行尝试 a1-a3 各自的范围与结束状态', 'failure': str(error)})
    still = {'latest_attempt': (probe.store['W']['attempts'][-1]['key'] if probe.mode == 'B'
                                else probe.attempt_ids()[-1])}
    return {'alternative': SPEC['C4']['alt_a' if mode == 'A' else 'alt_b'],
            'native': world.native(), 'chain': chain, 'final_state': state,
            'legal': legal, 'illegal': illegal,
            'removal_probe': _removal(probe, removed, still, lost, conventions),
            'identity_cost': world.cost(chain),
            'historical_references': world.historical_references()}


BUILDERS = {'C1': build_c1, 'C2': build_c2, 'C3': build_c3, 'C4': build_c4}

TAUTOLOGICAL = {
    'independent_plan_record', 'independent_product_record', 'independent_evidence_record',
    'independent_goal_record', 'attempt_key_reintroduced', 'slot_local_identity_required',
    'reference_needs_change_number'}


def compare(gid, a, b):
    spec = SPEC[gid]
    content = []
    for key in a['final_state']['content']:
        av = a['final_state']['content'][key]
        bv = b['final_state']['content'][key]
        content.append({'query': key, 'A': deepcopy(av), 'B': deepcopy(bv), 'same': av == bv})
    capabilities = []
    for key in a['final_state']['capabilities']:
        av = a['final_state']['capabilities'][key]
        bv = b['final_state']['capabilities'][key]
        capabilities.append({'probe': key, 'meaning': CAP_MEANING[key],
                             'A': av, 'B': bv, 'same': av == bv})
    differences = [row for row in capabilities if not row['same']]
    substantive = [row for row in differences if row['probe'] not in TAUTOLOGICAL]
    mismatches = [row for row in content if not row['same']]
    failures = [{'kind': 'content_mismatch', 'query': row['query'],
                 'observed': {'A': row['A'], 'B': row['B']}} for row in mismatches]
    for label, report in (('A', a), ('B', b)):
        for row in report['final_state'].get('recorded_failures', []):
            failures.append({'kind': row['kind'], 'mode': label, 'query': row['query'],
                             'observed': row.get('returned'), 'expected': row.get('expected')})
        for row in report['removal_probe']['lost']:
            failures.append({'kind': 'removal_probe', 'mode': label,
                             'query': row['query'], 'observed': row['failure']})
    same_successes = [{'kind': 'content', 'probe': row['query'], 'result': deepcopy(row['A'])}
                      for row in content if row['same']]
    same_successes += [{'kind': 'capability', 'probe': row['probe'], 'meaning': row['meaning']}
                       for row in capabilities if row['A'] is True and row['B'] is True]
    return {'group': gid,
            'changed_choice': spec['changed'],
            'fixed': spec['fixed'],
            'alternatives': {'A': a['alternative'], 'B': b['alternative']},
            'native_store': {'A': a['native'], 'B': b['native']},
            'content_queries': content,
            'capability_queries': capabilities,
            'same_successes': same_successes,
            'differences': differences,
            'substantive_differences': substantive,
            'substantive_difference': bool(substantive) or bool(mismatches),
            'limits_and_failures': failures,
            'identity_cost': {'A': a['identity_cost'], 'B': b['identity_cost']},
            'open_questions': spec['open'],
            'A': a, 'B': b}


def assumptions(groups):
    c1 = groups['C1']['B']['final_state']['capabilities']
    c2 = groups['C2']['B']['chain'][6]['observations']
    c3 = groups['C3']['B']['final_state']['capabilities']
    c4 = groups['C4']['B']['final_state']['capabilities']
    rows = [
        {'id': 'A1',
         'before': '内嵌 Plan 必然需要一个新的业务身份，否则无法表达部分采用和旧版引用',
         'group': 'C1',
         'observed': 'B 没有 Plan 记录；部分采用与旧版精确读取都成功，只有“跨尝试共享同一版本身份”失败',
         'refuted': c1['old_plan_text_resolvable'] and c1['partial_section_adoption']
                    and not c1['shared_plan_version_across_attempts']},
        {'id': 'A2',
         'before': '内嵌 Product 在尝试结束后无法记录成果修正，除非虚假重开',
         'group': 'C2',
         'observed': 'B 在 status=ended 时追加了结果修订，attempt 状态保持 ended',
         'refuted': c2['status_at_write'] == 'ended' and c2['correction_revision'] > 0},
        {'id': 'A3',
         'before': 'Change 内陈述不能被后续验收稳定引用',
         'group': 'C3',
         'observed': '同一 (change, statement) 被引用两次；subject 更新后旧 locator 仍返回原陈述',
         'refuted': c3['same_report_referenced_twice']
                    and c3['report_locator_survives_subject_update']},
        {'id': 'A4',
         'before': 'Goal 与 Attempt 合并后不再需要独立的尝试身份',
         'group': 'C4',
         'observed': 'B 使用 attempt key/index 与逐条 status；多次尝试和并行尝试都依赖这些键',
         'refuted': c4['attempt_key_reintroduced']},
    ]
    for row in rows:
        row['status'] = 'refuted' if row['refuted'] else 'not_refuted'
        del row['refuted']
    return rows


def self_check(results):
    for gid, group in results['groups'].items():
        for mode in ('A', 'B'):
            report = group[mode]
            need([step['label'] for step in report['chain']] == CHAIN_LABELS,
                 gid + ' chain labels differ in ' + mode)
            need(all(step['accepted'] for step in report['chain']),
                 gid + ' chain step not accepted in ' + mode)
            need(len(report['illegal']) >= 2, gid + ' illegal probes missing in ' + mode)
            need(all(not row['accepted'] for row in report['illegal']),
                 gid + ' illegal probe was accepted in ' + mode)
            need(bool(report['removal_probe']['lost']),
                 gid + ' removal probe lost nothing in ' + mode)
            need(bool(report['historical_references']),
                 gid + ' historical references missing in ' + mode)
            for key in report['final_state']['capabilities']:
                need(key in CAP_MEANING, 'capability without meaning: ' + key)
        need(set(group['A']['final_state']['content'])
             == set(group['B']['final_state']['content']), gid + ' content keys differ')
        need(set(group['A']['final_state']['capabilities'])
             == set(group['B']['final_state']['capabilities']), gid + ' capability keys differ')
        for row in group['content_queries']:
            need(row['same'], '%s content query differs: %s (A=%r B=%r)'
                 % (gid, row['query'], row['A'], row['B']))


def build_results():
    groups = {}
    for gid in ('C1', 'C2', 'C3', 'C4'):
        groups[gid] = compare(gid, BUILDERS[gid]('A'), BUILDERS[gid]('B'))
    results = {
        'schema': 1,
        'case': 'T12',
        'slice': SLICE,
        'batch': BATCH,
        'generated_by': 't12_identity_trials.build_results',
        'study_baseline': STUDY_BASELINE,
        'control': 'S0 = Goal/Plan/Attempt/Product/Evidence 独立 + Change append-only；每组只改一个选择',
        'common_chain': CHAIN_LABELS,
        'groups': groups,
        'assumptions': assumptions(groups),
        'boundary': {
            'synthetic': '所有比较步骤为本地合成；basis 前缀 SYN:，nature=synthetic，不是 DSH 事件，没有事件时间',
            'no_model_calls': '本模块不调用模型、不运行 Git、不访问网络',
            'no_final_recommendation': True,
            'scope': '只比较四个身份选择；不含其余 15 段，不写最终文档',
            'identity_origin': '所有对象 ID 与 Change 编号都是研究者编码，不是来源原有身份',
        }}
    self_check(results)
    return results


def _fmt_counts(counts):
    return '，'.join('%s=%s' % (key, value) for key, value in sorted(counts.items()))


def build_review(results):
    groups = results['groups']
    lines = []
    add = lines.append
    add('# T12 第2b阶段：四组对象身份的单项比较（identity-v1）')
    add('')
    add('- status: 执行结果；只做单变量比较，不做最终推荐')
    add('- date: 2026-10-29')
    add('- study baseline: `%s`' % results['study_baseline'])
    add('- 生成：`t12_identity_trials.build_results()`；本文件与 `results.json` 由同一次执行产生')
    add('- 共同链：%s' % ' → '.join(label.split('-')[0] for label in results['common_chain']))
    add('')
    add('## 1. 方法与边界')
    add('')
    add('每组只改一个身份选择，其余四项固定在 S0。A 与 B 是两套独立的内存存储，B 中不存在被替代对象的记录。'
        '每步先校验再写入，失败批次不留下部分状态；`before`/`after` 是执行快照，`changed_paths` 是实际差异。'
        '`content_queries` 只记录两侧应等价的语义内容，`capability_queries` 记录表示能力，二者分开比较。')
    add('')
    add('所有新行为使用 `SYN:` basis 与 `synthetic` nature；它们不是 DSH 事件，没有事件时间。'
        '成本只计数可执行的结构：身份记录、修订序列、单次变化的更新位置、查询入口与新约定；'
        '不估计人工时间或模型费用。')
    add('')
    add('## 2. 四组对照总表')
    add('')
    add('| 组 | 只改的选择 | 实质差异 | 差异点 |')
    add('|---|---|---|---|')
    for gid, group in groups.items():
        names = '、'.join(row['probe'] for row in group['substantive_differences']) or '无'
        add('| %s | %s | %s | %s |' % (gid, group['changed_choice'],
                                       '有' if group['substantive_difference'] else '未发现', names))
    add('')
    add('“未发现”只表示在本轮共同链、合法/非法探针和删除探针下没有测到行为差异；'
        '它不表示两种表示等价，也不裁定是否需要独立身份。')
    add('')
    add('## 3. 逐组结果')
    for gid, group in groups.items():
        add('')
        add('### %s：%s' % (gid, group['changed_choice']))
        add('')
        add('- A 表示：%s' % group['alternatives']['A'])
        add('- B 表示：%s' % group['alternatives']['B'])
        add('- 固定：%s' % '、'.join(group['fixed']))
        add('- 原生存储：A `%s`；B `%s`' % (group['native_store']['A']['storage'],
                                          group['native_store']['B']['storage']))
        add('- 定位：A `%s`；B `%s`' % (group['native_store']['A']['locator'],
                                       group['native_store']['B']['locator']))
        add('')
        add('**相同成功**（两侧都执行成功）：' + '；'.join(row['probe'] for row in group['same_successes']))
        add('')
        if group['differences']:
            add('**能力差异**：')
            for row in group['differences']:
                add('- `%s`：A=%s，B=%s。%s' % (row['probe'], row['A'], row['B'], row['meaning']))
        else:
            add('**能力差异**：无。')
        add('')
        if group['limits_and_failures']:
            add('**受限与真实失败**：')
            for row in group['limits_and_failures']:
                add('- [%s/%s] %s → %s' % (row['kind'], row.get('mode', 'both'),
                                           row['query'], row.get('observed')))
        else:
            add('**受限与真实失败**：无。')
        add('')
        probe = group['B']['removal_probe']
        add('**删除/弱化探针（B）**：移除“%s”后，仍可读 `%s`；丢失：' %
            (probe['removed'], probe['still_readable']))
        for row in probe['lost']:
            add('- %s → `%s`' % (row['query'], row['failure']))
        add('- 必须新加的约定：%s' % '；'.join(probe['conventions_counted']))
        add('')
        cost = group['identity_cost']['B']
        add('**B 的成本（实测）**：%s；单次变化最多触及 %s 个记录；修订序列 %s。'
            % (_fmt_counts(cost['identity_records']), cost['max_records_changed_in_one_change'],
               cost['revision_sequences']))
        add('**B 的新约定**：%s。' % '；'.join(cost['extra_conventions']))
        add('**B 的失败模式**：%s。' % '；'.join(cost['failure_modes']))
    add('')
    add('## 4. 被反例改变的假设')
    add('')
    for row in results['assumptions']:
        add('- **%s**（%s，%s）：%s。观察：%s。' %
            (row['id'], row['group'], row['status'], row['before'], row['observed']))
    add('')
    add('## 5. 适用条件')
    add('')
    add('- 结论只对共同链 L0—L6 与列出的合法/非法/删除探针成立；没有测试跨目标共享、批量迁移、并发写入或权限。')
    add('- B 的“成功”依赖它自己的新约定：Plan 需要逐版宿主内容修订与 section 定位；'
        'Product 需要稳定 slot 名与 written 列表；Evidence 需要稳定的 Change 编号与语句序号；'
        'Goal/Attempt 合并需要 attempt key/index 与逐条状态。去掉这些约定，删除探针已经显示不可恢复的内容。')
    add('- A 的成本同样计入：独立对象的 ID/版本/生命周期，以及采用、证据引用、验收决定的第二条更新路径。'
        '本轮没有测人工时间，也没有把 changed paths 当作维护成本。')
    add('- 本轮的“实质差异”来自可执行查询，不来自函数或字段数量；同一查询在两侧返回不同内容才算差异。')
    add('')
    add('## 6. 未决问题')
    add('')
    for gid, group in groups.items():
        add('- %s：%s' % (gid, '；'.join(group['open_questions'])))
    add('')
    add('## 7. 不做最终推荐')
    add('')
    add('本文只给出四组单变量比较的执行结果、成本计数与删除探针。它不选择哪种身份边界应被采用，'
        '也不把“某个方案在本轮的探针下成功”当作最终裁定；调度与裁定由 Astra 负责。')
    add('')
    return '\n'.join(lines) + '\n'


def documents():
    results = build_results()
    return {'results.json': results, 'review.md': build_review(results)}


def _serialize(document):
    if isinstance(document, str):
        return document if document.endswith('\n') else document + '\n'
    return json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + '\n'


def export_identity(directory):
    """Create identity-v1 once.  An existing directory is never overwritten."""
    out = Path(directory)
    documents_to_write = documents()
    out.mkdir(parents=True, exist_ok=False)
    for name, document in documents_to_write.items():
        (out / name).write_text(_serialize(document), encoding='utf-8')
    return str(out.resolve())


def verify_identity(directory):
    """Compare saved evidence with an in-memory rebuild; never writes."""
    out = Path(directory)
    for name, document in documents().items():
        expected = _serialize(document)
        actual = (out / name).read_text(encoding='utf-8')
        if actual != expected:
            raise AssertionError('saved evidence differs from the current build: ' + name)
    return True

