"""T12 identity-v2: bounded correction of the two embedded-identity comparisons.

identity-v1 (imported unchanged) let the embedded alternatives be limited by
their own storage helper.  Its C1 B plan lived in "attempt content revisions"
that were not the host attempt's revisions, and its C2 B made a second attempt
copy the slot into itself, so "shared version" and "same result identity" were
false by construction.  This module keeps the same single-variable question and
the same chain inputs, but requires B to support the full legal behaviour:

* C1: the plan is stored in the host attempt's complete revision history.  A
  second attempt may adopt ``(host, revision, section)`` exactly, without a
  copy.  A plan edit and an unrelated lifecycle change only add revisions; old
  references stay readable.  A new plan revision reaches a consumer's new
  result only through an explicit adoption.
* C2: a result slot keeps the logical locator ``(host attempt, slot)`` when a
  second attempt advances it.  The host stays ended, every revision records its
  producer, and history is append-only.

v2 adds a transactional commit over v1's non-atomic ``World.commit`` (v1 itself
is not modified), exact expected-revision guards, and explicit stale/atomic
probes.  C3/C4 are rebuilt with v1's unchanged builders and compared with v1's
``compare``.  The module does not run the DSH, call models, use Git or judge
natural-language truth.
"""
from copy import deepcopy
from pathlib import Path
import json

import t12_identity_trials as v1

BATCH = v1.BATCH
SLICE = 'identity-v2'
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
IDENTITY_DIR = ROOT / 'artifacts/agent-task-state/maintenance' / BATCH / SLICE
V1_DIR = ROOT / 'artifacts/agent-task-state/maintenance' / BATCH / 'identity-v1'

FEATURES = v1.FEATURES
PLAN_V1 = v1.PLAN_V1
PLAN_V2_TURNSTEP = v1.PLAN_V2_TURNSTEP
DRAFT = v1.DRAFT
CODE_WRITTEN = v1.CODE_WRITTEN
DIMENSION_VALUES = v1.DIMENSION_VALUES

Reject = v1.Reject
need = v1.need
exact_revision = v1.exact_revision
new_record = v1.new_record
at = v1.at
bump = v1.bump
differences = v1.differences
touched_identifiers = v1.touched_identifiers

C1_CHAIN = ['L0-establish', 'L1-local-plan-edit', 'L1b-produce-before-adoption',
            'L2-adopt-new-version', 'L3-new-result', 'L4-exact-check',
            'L5-end-with-responsibility', 'L6-rework-while-ended',
            'L7-second-attempt-exact-version']
C2_CHAIN = ['L0-establish', 'L1-local-plan-edit', 'L2-adopt-new-version',
            'L3-new-result', 'L4-exact-check', 'L5-end-with-responsibility',
            'L6-rework-while-ended', 'L7-second-attempt-advances-result']
EXPECTED_CHAINS = {'C1': C1_CHAIN, 'C2': C2_CHAIN,
                   'C3': v1.CHAIN_LABELS, 'C4': v1.CHAIN_LABELS}

CAP_MEANING = {
    'old_plan_text_resolvable': '旧成果所用的计划文本仍可按精确版本读出',
    'partial_section_adoption': '只采用计划中的一个 section，其余 section 不受影响',
    'plan_edit_advances_attempt_version': '局部修改计划同时推进承载它的 Attempt revision',
    'lifecycle_change_creates_new_plan_version':
        '无关的 Attempt 生命周期变化（结束）也推进承载计划的 version 序列',
    'produce_uses_only_adopted_version':
        '计划已有新版本但消费者未显式采用时，新成果仍使用旧的已采用版本',
    'new_plan_version_does_not_change_old_result': '计划新版本不改写旧成果所记的计划文本',
    'shared_plan_version_across_attempts':
        '两个尝试引用同一计划版本（同一 locator，而不是内容相等）',
    'old_plan_locator_readable_after_lifecycle_change':
        '宿主生命周期变化后旧成果的计划定位仍可读',
    'old_result_resolvable_after_end': '尝试结束后旧成果仍按精确版本可读',
    'partial_withdraw_single_slot': '只撤回列明的成果部分，其余部分保留',
    'result_correction_while_attempt_ended': '尝试保持 ended 时记录成果修正，不虚假 reopen',
    'same_result_identity_across_attempts': '另一个尝试推进同一成果时逻辑定位不变',
    'advance_producer_recorded': '跨尝试推进成果时记录实际推进者',
    'cross_attempt_write_preserves_history': '跨尝试推进不覆盖更早的成果修订',
    'host_attempt_remains_ended': '成果被另一个尝试推进时宿主 Attempt 仍保持 ended',
}

SPEC = {
    'C1': {
        'changed': 'Plan 的身份：独立 Plan 对象 vs 宿主 Attempt 的完整 revision 历史内嵌计划',
        'fixed': ['Product 独立', 'Evidence 独立', 'Goal 与 Attempt 分离', 'Change append-only'],
        'alt_a': '独立 Plan 记录 P，带 revision 与历史；采用记录写在消费者 Attempt 上',
        'alt_b': '没有 Plan 记录；计划随宿主 Attempt 的完整 revision 历史保存，定位为 (attempt, revision, section)',
        'open': ['宿主 revision 同时承载计划、采用与生命周期时，无关变化造成的版本推进如何归档',
                 'section 定位是否需要额外的跨 section 顺序约束'],
        'placement_probe': '删除宿主 Attempt 后旧成果的计划文本仍可读',
    },
    'C2': {
        'changed': 'Product 的身份：独立 Product 对象 vs 宿主 Attempt 内的结果 slot',
        'fixed': ['Plan 独立', 'Evidence 独立', 'Goal 与 Attempt 分离', 'Change append-only'],
        'alt_a': '独立 Product 记录 Q，带 revision、parts 与四维；推进者写在 Product 上',
        'alt_b': '没有 Product 记录；结果 slot 留在宿主 Attempt 内，逻辑定位为 (attempt, slot)，精确读取再加 slot revision',
        'open': ['slot 的逐 revision 历史与生产者记录是否已等价于一个嵌套的 Product 版本序列',
                 '宿主被归档或删除时，内嵌成果的身份如何保留'],
        'placement_probe': '删除宿主 Attempt 后结果仍可读',
    },
}


# --------------------------------------------------------------- v2 world


class V2World(v1.World):
    """v1 state shape with a transactional commit and exact-locator helpers."""

    chain_labels = ()

    def chain(self):
        return [self.commit(label,
                            (lambda world, name=label: getattr(world, name.split('-')[0].lower())()))
                for label in self.chain_labels]

    def _restore(self, snapshot):
        self.head = snapshot['head']
        self.store = snapshot['store']
        self.change_statements = snapshot['change_statements']
        self.refs = snapshot['refs']
        self.tokens = snapshot['tokens']

    def commit(self, label, fn):
        before = self.snapshot()
        need(self.head == len(self.log), 'changes are append-only')
        try:
            result = fn(self)
            need(isinstance(result, dict), 'step must return observations')
        except Exception:
            self._restore(before)
            raise
        actions = list(result.get('actions', []))
        observations = deepcopy(result.get('observations', result.get('queries', {})))
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
            probe.commit('probe-prepare', prepare)
        before = probe.snapshot()
        try:
            probe.commit('probe-reject', fn)
        except Reject as error:
            need(probe.snapshot() == before, 'rejection left partial state')
            return {'accepted': False, 'error': str(error)}
        raise AssertionError('expected the action to be rejected')


class ProductWrite:
    """Product operations that always require the exact current revision."""

    def advance(self, pid, dimensions, actor=None, expected_revision=None):
        product = self.store.get(pid)
        need(product is not None and product['kind'] == 'product', 'product required: ' + str(pid))
        need(type(expected_revision) is int and expected_revision == product['revision'],
             'stale product update: expected %s, current %s'
             % (expected_revision, product['revision']))
        merged = deepcopy(product['dimensions'])
        for key, value in dimensions.items():
            need(key in DIMENSION_VALUES, 'unknown dimension: ' + str(key))
            need(value in DIMENSION_VALUES[key], 'controlled dimension value required: ' + key)
            merged[key] = value
        fields = {'dimensions': merged}
        if actor is not None:
            fields['advanced_by'] = actor
        bump(self.store, pid, **fields)

    def withdraw(self, pid, parts, expected_revision=None):
        product = self.store.get(pid)
        need(product is not None and product['kind'] == 'product', 'product required: ' + str(pid))
        need(type(expected_revision) is int and expected_revision == product['revision'],
             'stale product update: expected %s, current %s'
             % (expected_revision, product['revision']))
        need(isinstance(parts, list) and bool(parts), 'known nonempty withdrawal range required')
        unknown = sorted(set(parts) - set(product['parts']))
        need(not unknown, 'unknown product part: ' + ','.join(unknown))
        updated = deepcopy(product['parts'])
        for part in parts:
            updated[part] = 'withdrawn'
        bump(self.store, pid, parts=updated)


# ---------------------------------------------------------------- C1 Plan


class C1Base(V2World, ProductWrite):
    """The same chain and inputs for both C1 storages."""

    group = 'C1'
    chain_labels = C1_CHAIN

    def create_plan(self):
        raise NotImplementedError

    def attempt_fields(self):
        raise NotImplementedError

    def edit_plan(self, edits, expected_revision):
        raise NotImplementedError

    def plan_version(self):
        raise NotImplementedError

    def adopt_exact(self, aid, revision, scope, basis):
        raise NotImplementedError

    def effective(self, aid, section):
        raise NotImplementedError

    def text_of(self, section, locator):
        raise NotImplementedError

    def latest_plan_text(self, section):
        raise NotImplementedError

    def begin_second_attempt(self):
        raise NotImplementedError

    def second_attempt_has_own_plan(self):
        raise NotImplementedError

    def mark_ended(self, aid, held, remaining):
        raise NotImplementedError

    def plan_basis(self, pid, section):
        return deepcopy(self.store[pid]['plan_usage'][section])

    def attempt_revision(self, aid):
        return self.store[aid]['revision']

    def produce_result(self, aid, pid, parts, section, dimensions):
        need(self.store[aid]['status'] == 'active',
             'producing a new result requires an active attempt')
        basis = self.effective(aid, section)
        new_record(self.store, pid, 'product', attempt=aid,
                   parts={part: 'present' for part in parts},
                   dimensions=deepcopy(dimensions), plan_usage={section: basis})

    def end(self, aid, remaining='retained_unresolved'):
        need(aid in self.store and self.store[aid]['kind'] == 'attempt', 'attempt required')
        need(self.store[aid]['status'] == 'active', 'active attempt required')
        need(remaining in {None, 'retained_unresolved'},
             'ending holder must disclose remaining responsibility as retained_unresolved')
        held = sorted(token for token, holders in self.tokens.items() if aid in holders)
        need(not held or remaining == 'retained_unresolved',
             'ending holder must disclose remaining assigned responsibility')
        self.mark_ended(aid, held, remaining)

    # -- chain -------------------------------------------------------
    def l0(self):
        new_record(self.store, 'G', 'goal', scope=FEATURES, acceptance='pending')
        self.create_plan()
        new_record(self.store, 'A', 'attempt', goal='G', status='active',
                   scope=['turnstep draft'], decisions=[], **self.attempt_fields())
        self.adopt_exact('A', 1, ['turnstep'], ['SYN:initial-plan'])
        self.produce_result('A', 'R', ['draft_status', 'draft_notifications'],
                            'turnstep', DRAFT)
        self.tokens = {'whole_turn_status': ['A']}
        self.refs = {'old_result_plan': self.plan_basis('R', 'turnstep')}
        return {'actions': ['goal G', 'plan version 1', 'attempt A',
                            'explicit adoption of turnstep', 'result R'],
                'observations': {'R_plan': self.plan_basis('R', 'turnstep'),
                                 'old_plan_text': self.text_of('turnstep',
                                                               self.plan_basis('R', 'turnstep')),
                                 'plan_version': self.plan_version(),
                                 'attempt_revision': self.attempt_revision('A')}}

    def l1(self):
        plan_before = self.plan_version()
        attempt_before = self.attempt_revision('A')
        self.edit_plan({'turnstep': deepcopy(PLAN_V2_TURNSTEP)},
                       expected_revision=plan_before)
        return {'actions': ['edit only turnstep with the exact current revision'],
                'observations': {'plan_version_before': plan_before,
                                 'plan_version_after': self.plan_version(),
                                 'attempt_revision_before': attempt_before,
                                 'attempt_revision_after': self.attempt_revision('A'),
                                 'old_result_plan': self.plan_basis('R', 'turnstep'),
                                 'old_plan_text': self.text_of('turnstep',
                                                               self.plan_basis('R', 'turnstep')),
                                 'channel_text': self.latest_plan_text('channel')}}

    def l1b(self):
        self.produce_result('A', 'Q0', ['draft_status', 'draft_notifications'],
                            'turnstep', CODE_WRITTEN)
        basis = self.plan_basis('Q0', 'turnstep')
        return {'actions': ['produce Q0 after the plan edit, before any new adoption'],
                'observations': {'Q0_plan': basis,
                                 'Q0_plan_text': self.text_of('turnstep', basis),
                                 'plan_version_now': self.plan_version(),
                                 'used_previous_version':
                                     basis == self.plan_basis('R', 'turnstep'),
                                 'old_result_plan': self.plan_basis('R', 'turnstep')}}

    def l2(self):
        before = self.attempt_revision('A')
        self.adopt_exact('A', self.plan_version(), ['turnstep'], ['SYN:chain-adopt'])
        return {'actions': ['A explicitly adopts the current plan version for turnstep'],
                'observations': {'decision': deepcopy(self.store['A']['decisions'][-1]),
                                 'attempt_revision_before': before,
                                 'attempt_revision_after': self.attempt_revision('A'),
                                 'adopted_plan': self.effective('A', 'turnstep')}}

    def l3(self):
        self.produce_result('A', 'Q', ['draft_status', 'draft_notifications'],
                            'turnstep', CODE_WRITTEN)
        self.refs['new_result_plan'] = self.plan_basis('Q', 'turnstep')
        basis = self.plan_basis('Q', 'turnstep')
        return {'actions': ['produce Q under the explicitly adopted version'],
                'observations': {'Q_plan': basis,
                                 'Q_plan_text': self.text_of('turnstep', basis),
                                 'R_plan': self.plan_basis('R', 'turnstep'),
                                 'used_adopted_version':
                                     basis == self.effective('A', 'turnstep')}}

    def l4(self):
        old = self.text_of('turnstep', self.plan_basis('R', 'turnstep'))
        new = self.text_of('turnstep', self.plan_basis('Q', 'turnstep'))
        new_record(self.store, 'E', 'evidence', goal='G',
                   subject={'id': 'Q', 'revision': 1},
                   scope='turnstep plan usage', nature='synthetic',
                   findings=['old result used: ' + old, 'new result used: ' + new])
        self.refs['check'] = {'id': 'E', 'revision': 1}
        return {'actions': ['record the exact plan-version check as Evidence E'],
                'observations': {'findings': deepcopy(self.store['E']['findings']),
                                 'subject': deepcopy(self.store['E']['subject'])}}

    def l5(self):
        plan_before = self.plan_version()
        attempt_before = self.attempt_revision('A')
        self.end('A')
        old = self.plan_basis('R', 'turnstep')
        new = self.plan_basis('Q', 'turnstep')
        return {'actions': ['end A with retained responsibility'],
                'observations': {'attempt_status': self.store['A']['status'],
                                 'plan_version_before': plan_before,
                                 'plan_version_after': self.plan_version(),
                                 'attempt_revision_before': attempt_before,
                                 'attempt_revision_after': self.attempt_revision('A'),
                                 'old_result_plan_text': self.text_of('turnstep', old),
                                 'consumer_plan_text': self.text_of('turnstep', new),
                                 'latest_plan_text': self.latest_plan_text('turnstep'),
                                 'goal_acceptance': self.store['G']['acceptance']}}

    def l6(self):
        status_at_write = self.store['A']['status']
        self.advance('Q', {'completion': 'in_progress'}, actor='A',
                     expected_revision=self.store['Q']['revision'])
        return {'actions': ['regress Q completion while A is ended'],
                'observations': {'status_at_write': status_at_write,
                                 'attempt_status': self.store['A']['status'],
                                 'old_result_dimensions': at(self.store, 'Q', 1)['dimensions'],
                                 'current_dimensions': self.store['Q']['dimensions']}}

    def l7(self):
        self.begin_second_attempt()
        self.adopt_exact('A2', 1, ['turnstep'], ['SYN:second-attempt-old-version'])
        self.produce_result('A2', 'Q2', ['draft_status', 'draft_notifications'],
                            'turnstep', CODE_WRITTEN)
        old = self.plan_basis('R', 'turnstep')
        second = self.plan_basis('Q2', 'turnstep')
        return {'actions': ['begin A2 without a plan copy',
                            'A2 adopts the exact old version 1',
                            'A2 produces Q2 under it'],
                'observations': {'A2_decision': deepcopy(self.store['A2']['decisions'][-1]),
                                 'R_plan': old, 'Q2_plan': second,
                                 'same_locator': old == second,
                                 'copied_plan_content': self.second_attempt_has_own_plan(),
                                 'Q2_plan_text': self.text_of('turnstep', second),
                                 'host_attempt_status': self.store['A']['status']}}

    # -- probes ------------------------------------------------------
    def readback_references(self):
        old = self.plan_basis('R', 'turnstep')
        new = self.plan_basis('Q', 'turnstep')
        second = self.plan_basis('Q2', 'turnstep')
        adopted = self.effective('A', 'turnstep')
        return {'old_result_plan': old,
                'old_plan_text': self.text_of('turnstep', old),
                'current_adopted_plan': adopted,
                'current_adopted_text': self.text_of('turnstep', adopted),
                'second_attempt_plan': second,
                'second_attempt_text': self.text_of('turnstep', second),
                'same_old_and_second_locator': old == second,
                'latest_plan_text': self.latest_plan_text('turnstep')}

    def edit_with_current_revision(self):
        self.edit_plan({'turnstep': deepcopy(PLAN_V2_TURNSTEP)},
                       expected_revision=self.plan_version())
        return {'actions': ['edit turnstep with the exact current revision'],
                'observations': {'plan_version': self.plan_version(),
                                 'text': self.latest_plan_text('turnstep')}}

    def atomic_failure_probe(self):
        self.edit_plan({'turnstep': deepcopy(PLAN_V2_TURNSTEP)},
                       expected_revision=self.plan_version())
        need(False, 'synthetic mid-step failure after a legal plan edit')

    # -- state -------------------------------------------------------
    def final_state(self, chain):
        steps = {row['label']: row['observations'] for row in chain}
        l1 = steps['L1-local-plan-edit']
        l3 = steps['L3-new-result']
        l5 = steps['L5-end-with-responsibility']
        l6 = steps['L6-rework-while-ended']
        l7 = steps['L7-second-attempt-exact-version']
        old = self.plan_basis('R', 'turnstep')
        new = self.plan_basis('Q', 'turnstep')
        second = self.plan_basis('Q2', 'turnstep')
        return {
            'content': {
                'old_plan_text': self.text_of('turnstep', old),
                'new_plan_text': self.text_of('turnstep', new),
                'pre_adoption_plan_text': self.text_of('turnstep',
                                                       self.plan_basis('Q0', 'turnstep')),
                'second_attempt_plan_text': self.text_of('turnstep', second),
                'old_check_findings': deepcopy(self.store['E']['findings']),
                'old_result_dimensions': at(self.store, 'Q', 1)['dimensions'],
                'current_result_dimensions': self.store['Q']['dimensions'],
                'goal_acceptance': self.store['G']['acceptance'],
                'attempt_status': self.store['A']['status']},
            'capabilities': {
                'old_plan_text_resolvable': bool(self.text_of('turnstep', old)),
                'partial_section_adoption':
                    self.latest_plan_text('channel') == PLAN_V1['channel']['description'],
                'plan_edit_advances_attempt_version':
                    l1['attempt_revision_after'] > l1['attempt_revision_before'],
                'lifecycle_change_creates_new_plan_version':
                    l5['plan_version_after'] > l5['plan_version_before'],
                'produce_uses_only_adopted_version':
                    steps['L1b-produce-before-adoption']['used_previous_version']
                    and l3['used_adopted_version'],
                'new_plan_version_does_not_change_old_result':
                    self.text_of('turnstep', old) == steps['L0-establish']['old_plan_text'],
                'shared_plan_version_across_attempts': l7['same_locator'],
                'old_plan_locator_readable_after_lifecycle_change':
                    bool(self.text_of('turnstep', old)) and l6['status_at_write'] == 'ended'},
            'locators': {
                'old_result_plan': old,
                'new_result_plan': new,
                'pre_adoption_plan': self.plan_basis('Q0', 'turnstep'),
                'second_attempt_plan': second,
                'old_check_subject': deepcopy(self.store['E']['subject']),
                'attempt_revision_now': self.attempt_revision('A')},
            'version_coupling': {
                'plan_edit': {'plan_version_before': l1['plan_version_before'],
                              'plan_version_after': l1['plan_version_after'],
                              'attempt_revision_before': l1['attempt_revision_before'],
                              'attempt_revision_after': l1['attempt_revision_after']},
                'lifecycle_end': {'plan_version_before': l5['plan_version_before'],
                                  'plan_version_after': l5['plan_version_after'],
                                  'attempt_revision_before': l5['attempt_revision_before'],
                                  'attempt_revision_after': l5['attempt_revision_after']},
                'note': 'B 的“计划版本”就是宿主 Attempt 的 revision 序列，'
                        '计划修改与无关生命周期变化都会推进它；A 的 Plan revision 与 Attempt revision 独立。'
                        '额外耦合在此记录，不作为失败判据。'}}


class C1A(C1Base):
    group, mode = 'C1', 'A'

    def create_plan(self):
        new_record(self.store, 'P', 'plan', sections=deepcopy(PLAN_V1), links=[])

    def attempt_fields(self):
        return {}

    def edit_plan(self, edits, expected_revision):
        plan = self.store['P']
        need(type(expected_revision) is int and expected_revision == plan['revision'],
             'stale plan update: expected %s, current %s'
             % (expected_revision, plan['revision']))
        need(isinstance(edits, dict), 'plan update shape')
        need(bool(edits), 'empty plan update')
        current = deepcopy(plan['sections'])
        unknown = set(edits) - set(current)
        need(not unknown, 'unknown plan section: ' + ','.join(sorted(unknown)))
        for key, value in edits.items():
            need(isinstance(value, dict) and set(value) == {'status', 'description'},
                 'section structure required')
            current[key] = deepcopy(value)
        bump(self.store, 'P', sections=current)

    def plan_version(self):
        return self.store['P']['revision']

    def adopt_exact(self, aid, revision, scope, basis):
        need(aid in self.store and self.store[aid]['kind'] == 'attempt', 'attempt required')
        need(self.store[aid]['status'] == 'active', 'adoption requires an active attempt')
        plan = at(self.store, 'P', revision)
        need(isinstance(scope, list) and bool(scope) and len(set(scope)) == len(scope),
             'unique nonempty adoption scope required')
        need(set(scope) <= set(plan['sections']),
             'adoption scope must name sections of that revision')
        need(isinstance(basis, list) and bool(basis)
             and all(isinstance(x, str) and x.startswith('SYN:') for x in basis),
             'synthetic adoption basis required')
        decisions = deepcopy(self.store[aid]['decisions'])
        decisions.append({'plan': {'id': 'P', 'revision': revision},
                          'scope': list(scope), 'basis': list(basis),
                          'change': self.head + 1})
        bump(self.store, aid, decisions=decisions)

    def effective(self, aid, section):
        found = None
        for record in self.store[aid]['decisions']:
            if section in record['scope']:
                found = deepcopy(record['plan'])
        need(found is not None, 'plan scope was not adopted: ' + section)
        return found

    def plan_text(self, revision, section):
        plan = at(self.store, 'P', revision)
        need(section in plan['sections'], 'unknown plan section: ' + section)
        return plan['sections'][section]['description']

    def text_of(self, section, locator):
        need(isinstance(locator, dict) and locator.get('id') == 'P', 'plan locator required')
        return self.plan_text(locator['revision'], section)

    def latest_plan_text(self, section):
        return self.plan_text(self.store['P']['revision'], section)

    def begin_second_attempt(self):
        new_record(self.store, 'A2', 'attempt', goal='G', status='active',
                   scope=['turnstep draft'], decisions=[])

    def second_attempt_has_own_plan(self):
        return False

    def mark_ended(self, aid, held, remaining):
        bump(self.store, aid, status='ended', outcome='synthetic stop',
             remaining_responsibility=remaining, held_at_end=held)

    def text_at_none(self):
        return self.plan_text(None, 'turnstep')

    def identity_shape(self):
        return {'logical_identity': 'Plan P',
                'storage': 'store["P"] independent record with versions',
                'locator': '{id, revision}; section lives in the consumer',
                'version_sequence': 'P.revision, independent of attempt revisions'}

    def caller_requirements(self):
        return ['Plan must exist and the exact revision must be retained',
                'adoption requires an active consumer attempt',
                'every consumer records {id, revision} per adopted section',
                'plan edit requires the exact current plan revision']

    def identity_count(self):
        products = [key for key, obj in self.store.items() if obj['kind'] == 'product']
        return {'plan_identities': 1,
                'plan_revisions_retained': len(self.store['P']['versions']) + 1,
                'product_identities': len(products)}

    def revision_sequences(self):
        return [{'sequence': 'P.revision', 'current': self.store['P']['revision']},
                {'sequence': 'A.revision', 'current': self.store['A']['revision'],
                 'note': 'adoption and end advance it; plan edits do not'}]

    def query_entry_points(self):
        return ['plan_text(revision, section)', 'effective(attempt, section)',
                'at(store, id, revision)', 'product.plan_usage']

    def conventions(self):
        return ['Plan ID、revision 与历史版本',
                '采用记录写在消费者 Attempt 的 decisions 上，按 section 覆盖',
                '每个 Product 为 section 记录 exact plan locator',
                'Plan revision 与 Attempt revision 是两条独立序列']

    def failure_modes(self):
        return ['Plan 版本与采用记录分两处更新，同一批次需要一起回滚',
                '删除旧 Plan revision 会让旧成果的计划引用悬空']

    def native(self):
        return {'storage': 'store["P"] independent plan record',
                'varied_identity': 'plan id P',
                'locator': '{id, revision} plus section in the consumer',
                'sample': deepcopy(self.store['P'])}


class C1B(C1Base):
    group, mode = 'C1', 'B'
    plan_host = 'A'

    def create_plan(self):
        return None

    def attempt_fields(self):
        return {'revision': 1,
                'sections': deepcopy(PLAN_V1),
                'history': [{'revision': 1, 'label': 'initial plan', 'status': 'active',
                             'sections': deepcopy(PLAN_V1), 'decisions': []}]}

    def history_entry(self, aid, revision):
        need(aid in self.store and self.store[aid]['kind'] == 'attempt',
             'unknown attempt host: ' + str(aid))
        exact_revision(revision, 'attempt revision')
        for item in self.store[aid]['history']:
            if item['revision'] == revision:
                return item
        raise Reject('attempt revision not retained: %s@%s' % (aid, revision))

    def append_revision(self, aid, label, status=None, sections=None, decisions=None):
        host = self.store[aid]
        entry = {'revision': host['revision'] + 1, 'label': label,
                 'status': host['status'] if status is None else status,
                 'sections': deepcopy(host['sections'] if sections is None else sections),
                 'decisions': deepcopy(host['decisions'] if decisions is None else decisions)}
        host['history'].append(entry)
        host['revision'] = entry['revision']
        host['status'] = entry['status']
        host['sections'] = entry['sections']
        host['decisions'] = entry['decisions']
        return entry

    def edit_plan(self, edits, expected_revision):
        host = self.store['A']
        need(type(expected_revision) is int and expected_revision == host['revision'],
             'stale plan update: expected %s, current %s'
             % (expected_revision, host['revision']))
        current = deepcopy(host['sections'])
        need(isinstance(edits, dict), 'plan update shape')
        need(bool(edits), 'empty plan update')
        unknown = set(edits) - set(current)
        need(not unknown, 'unknown plan section: ' + ','.join(sorted(unknown)))
        for key, value in edits.items():
            need(isinstance(value, dict) and set(value) == {'status', 'description'},
                 'section structure required')
            current[key] = deepcopy(value)
        self.append_revision('A', 'local plan edit', sections=current)

    def plan_version(self):
        return self.store['A']['revision']

    def adopt_exact(self, aid, revision, scope, basis):
        need(aid in self.store and self.store[aid]['kind'] == 'attempt', 'attempt required')
        need(self.store[aid]['status'] == 'active', 'adoption requires an active attempt')
        entry = self.history_entry(self.plan_host, revision)
        need(isinstance(scope, list) and bool(scope) and len(set(scope)) == len(scope),
             'unique nonempty adoption scope required')
        need(set(scope) <= set(entry['sections']),
             'adoption scope must name sections of that revision')
        need(isinstance(basis, list) and bool(basis)
             and all(isinstance(x, str) and x.startswith('SYN:') for x in basis),
             'synthetic adoption basis required')
        decisions = deepcopy(self.store[aid]['decisions'])
        decisions.append({'attempt': self.plan_host, 'revision': revision,
                          'sections': list(scope), 'basis': list(basis),
                          'change': self.head + 1})
        self.append_revision(aid, 'adopt exact plan revision', decisions=decisions)

    def effective(self, aid, section):
        found = None
        for record in self.store[aid]['decisions']:
            if section in record['sections']:
                found = {'attempt': record['attempt'], 'revision': record['revision'],
                         'section': section}
        need(found is not None, 'plan scope was not adopted: ' + section)
        return found

    def plan_text_at(self, aid, revision, section):
        entry = self.history_entry(aid, revision)
        need(section in entry['sections'], 'unknown plan section: ' + section)
        return entry['sections'][section]['description']

    def text_of(self, section, locator):
        need(isinstance(locator, dict) and 'attempt' in locator and 'revision' in locator,
             'embedded plan locator required')
        need(locator.get('section', section) == section, 'plan section mismatch')
        return self.plan_text_at(locator['attempt'], locator['revision'], section)

    def latest_plan_text(self, section):
        return self.plan_text_at('A', self.store['A']['revision'], section)

    def begin_second_attempt(self):
        new_record(self.store, 'A2', 'attempt', goal='G', status='active',
                   scope=['turnstep draft'], decisions=[], revision=1, sections={},
                   history=[{'revision': 1, 'label': 'begin without a plan copy',
                             'status': 'active', 'sections': {}, 'decisions': []}])

    def second_attempt_has_own_plan(self):
        return bool(self.store['A2'].get('sections'))

    def mark_ended(self, aid, held, remaining):
        self.append_revision(aid, 'end with retained responsibility', status='ended')
        host = self.store[aid]
        host['outcome'] = 'synthetic stop'
        host['remaining_responsibility'] = remaining
        host['held_at_end'] = held

    def text_at_none(self):
        return self.plan_text_at('A', None, 'turnstep')

    def resolve_locator(self, locator):
        if isinstance(locator, dict) and 'attempt' in locator and 'section' in locator:
            return self.plan_text_at(locator['attempt'], locator['revision'],
                                     locator['section'])
        return super().resolve_locator(locator)

    def identity_shape(self):
        return {'logical_identity': '(host attempt A, revision, section)',
                'storage': 'store["A"].history revisions',
                'locator': '{attempt, revision, section}',
                'version_sequence': 'A.revision, shared by plan, adoption and lifecycle'}

    def caller_requirements(self):
        return ['host attempt must exist and retain the exact revision',
                'adoption requires an active consumer attempt and names the host revision',
                'every consumer records (host attempt, revision, section)',
                'plan edit requires the exact current host revision',
                'cross-attempt reference is read-only on the host history']

    def identity_count(self):
        products = [key for key, obj in self.store.items() if obj['kind'] == 'product']
        return {'plan_identities': 0,
                'host_attempt_revisions_retained': len(self.store['A']['history']),
                'second_attempt_revisions_retained': len(self.store['A2']['history']),
                'product_identities': len(products)}

    def revision_sequences(self):
        return [{'sequence': 'A.revisions (host attempt)',
                 'current': self.store['A']['revision'],
                 'retained': [entry['revision'] for entry in self.store['A']['history']]},
                {'sequence': 'A2.revisions', 'current': self.store['A2']['revision'],
                 'retained': [entry['revision'] for entry in self.store['A2']['history']]}]

    def query_entry_points(self):
        return ['plan_text_at(host, revision, section)', 'effective(consumer, section)',
                'history_entry(host, revision)', 'product.plan_usage']

    def conventions(self):
        return ['宿主 Attempt 的完整历史 revision 必须逐版保留（计划、状态、采用记录同版保存）',
                '计划定位是 (host attempt, revision, section)；跨尝试引用直接指向宿主历史，不复制',
                '采用记录写在消费者上，但指向计划宿主与精确 revision',
                '计划修改与无关生命周期变化都会推进同一个宿主 revision 序列']

    def failure_modes(self):
        return ['宿主 revision 同时承载计划、采用与生命周期，无关变化也会推进计划版本',
                '删掉旧宿主 revision 会让旧成果的计划定位与旧采用一起悬空',
                '删除宿主 Attempt 会同时删除计划历史']

    def native(self):
        return {'storage': 'store["A"].history revisions (host attempt)',
                'varied_identity': 'none for Plan',
                'locator': '{attempt, revision, section}',
                'sample': deepcopy(self.store['A']['history'][-1])}


# ------------------------------------------------------------- C2 Product


class C2Base(V2World, v1.PlanS0, ProductWrite):
    """The same chain and inputs for both C2 storages; Plan stays independent."""

    group = 'C2'
    chain_labels = C2_CHAIN

    def attempt_fields(self):
        raise NotImplementedError

    def create_first_result(self):
        raise NotImplementedError

    def create_second_result(self):
        raise NotImplementedError

    def result_locator(self, which):
        raise NotImplementedError

    def result_view(self, which, revision=None):
        raise NotImplementedError

    def advance_result(self, dimensions, producer):
        raise NotImplementedError

    def withdraw_one_part(self):
        raise NotImplementedError

    def old_state(self):
        raise NotImplementedError

    def current_state(self):
        raise NotImplementedError

    def untouched_state(self):
        raise NotImplementedError

    def check_resolves(self):
        raise NotImplementedError

    def atomic_failure_probe(self):
        raise NotImplementedError

    def text_at_none(self):
        raise NotImplementedError

    def identity_shape(self):
        raise NotImplementedError

    def caller_requirements(self):
        raise NotImplementedError

    # -- chain -------------------------------------------------------
    def l0(self):
        new_record(self.store, 'G', 'goal', scope=FEATURES, acceptance='pending')
        new_record(self.store, 'P', 'plan', sections=deepcopy(PLAN_V1), links=[])
        new_record(self.store, 'A', 'attempt', goal='G', status='active',
                   scope=['turnstep draft'], decisions=[], **self.attempt_fields())
        self.adopt('A', 1, ['turnstep'], ['SYN:initial-plan'])
        self.create_first_result()
        self.tokens = {'whole_turn_status': ['A']}
        self.refs = {'old_result': self.result_locator('old')}
        return {'actions': ['goal G', 'plan P@1', 'attempt A',
                            'explicit adoption of turnstep', 'first result'],
                'observations': {'old_result': self.result_view('old', 1)}}

    def l1(self):
        self.edit_plan({'turnstep': deepcopy(PLAN_V2_TURNSTEP)})
        return {'actions': ['edit only P.turnstep'],
                'observations': {'plan_revision': self.store['P']['revision'],
                                 'old_result': self.result_view('old', 1)}}

    def l2(self):
        self.adopt('A', 2, ['turnstep'], ['SYN:chain-adopt'])
        return {'actions': ['A adopts P@2 for turnstep'],
                'observations': {'decisions': deepcopy(self.store['A']['decisions'])}}

    def l3(self):
        self.create_second_result()
        self.refs['new_result'] = self.result_locator('new')
        return {'actions': ['write the second result under the adopted P@2'],
                'observations': {'new_result': self.result_view('new', None),
                                 'old_result': self.result_view('old', 1)}}

    def l4(self):
        subject = self.evidence_subject()
        dims = self.result_view('new', subject['revision'] if 'revision' in subject else None)
        new_record(self.store, 'E', 'evidence', goal='G', subject=deepcopy(subject),
                   scope='result dimensions', nature='synthetic',
                   findings=['draft_status at check: %s; acceptance %s'
                             % (dims['dimensions']['implementation'],
                                dims['dimensions']['acceptance'])])
        self.refs['check'] = {'id': 'E', 'revision': 1}
        return {'actions': ['record the exact result check as Evidence E'],
                'observations': {'findings': deepcopy(self.store['E']['findings']),
                                 'subject': deepcopy(self.store['E']['subject'])}}

    def l5(self):
        self.end('A')
        return {'actions': ['end A with retained responsibility'],
                'observations': {'attempt_status': self.store['A']['status'],
                                 'old_result': self.result_view('old', 1),
                                 'new_result': self.result_view('new', None),
                                 'goal_acceptance': self.store['G']['acceptance']}}

    def l6(self):
        status_at_write = self.store['A']['status']
        self.advance_result({'completion': 'in_progress'}, 'A')
        return {'actions': ['correct the result while A is ended'],
                'observations': {'status_at_write': status_at_write,
                                 'attempt_status': self.store['A']['status'],
                                 'correction_result': self.result_view('new', None),
                                 'current_dimensions': self.result_view('new', None)['dimensions']}}

    def l7(self):
        new_record(self.store, 'A2', 'attempt', goal='G', status='active',
                   scope=['turnstep draft'], decisions=[])
        before = self.result_view('new', None)
        self.advance_result({'completion': 'reported_complete'}, 'A2')
        after = self.result_view('new', None)
        return {'actions': ['begin A2', 'A2 advances the same logical result'],
                'observations': {'logical_locator_before': before['locator'],
                                 'logical_locator_after': after['locator'],
                                 'same_identity': before['locator'] == after['locator'],
                                 'revision_before': before['revision'],
                                 'revision_after': after['revision'],
                                 'producer': after['producer'],
                                 'host_attempt_status': self.store['A']['status'],
                                 'historical_result': self.result_view('old', 1),
                                 'correction_result': self.result_view('new', before['revision']),
                                 'current_dimensions': after['dimensions']}}

    def final_state(self, chain):
        steps = {row['label']: row['observations'] for row in chain}
        l6 = steps['L6-rework-while-ended']
        l7 = steps['L7-second-attempt-advances-result']
        old = self.result_view('old', 1)
        current = self.result_view('new', None)
        return {
            'content': {
                'old_result_dimensions': old['dimensions'],
                'old_result_state': self.old_state(),
                'new_result_dimensions': current['dimensions'],
                'new_result_state_after_withdraw': self.current_state(),
                'untouched_part_state': self.untouched_state(),
                'old_check_findings': deepcopy(self.store['E']['findings']),
                'goal_acceptance': self.store['G']['acceptance'],
                'attempt_status': self.store['A']['status'],
                'advance_producer': l7['producer'],
                'old_check_still_resolves': self.check_resolves()},
            'capabilities': {
                'old_result_resolvable_after_end': bool(old['dimensions']),
                'partial_withdraw_single_slot':
                    self.current_state() == 'withdrawn' and self.untouched_state() == 'present',
                'result_correction_while_attempt_ended': l6['status_at_write'] == 'ended',
                'same_result_identity_across_attempts': l7['same_identity'],
                'advance_producer_recorded': l7['producer'] == 'A2',
                'cross_attempt_write_preserves_history':
                    l7['historical_result']['dimensions'] == old['dimensions']
                    and l7['correction_result']['dimensions'] == l6['current_dimensions'],
                'host_attempt_remains_ended': l7['host_attempt_status'] == 'ended'},
            'locators': {
                'old_result': old['locator'],
                'new_result': current['locator'],
                'old_check_subject': deepcopy(self.store['E']['subject']),
                'current_result_revision': current['revision']}}

    def readback_references(self):
        old = self.result_view('old', 1)
        current = self.result_view('new', None)
        correction = self.result_view('new', current['revision'] - 1)
        return {'old_result': old, 'current_result': current,
                'previous_revision': correction,
                'same_logical_locator': old['locator'] == current['locator'],
                'producer': current['producer']}


class C2A(C2Base):
    group, mode = 'C2', 'A'

    def attempt_fields(self):
        return {}

    def create_first_result(self):
        new_record(self.store, 'R', 'product', attempt='A',
                   parts={'draft_status': 'present', 'draft_notifications': 'present'},
                   dimensions=deepcopy(DRAFT),
                   plan_usage={'turnstep': {'id': 'P', 'revision': 1}})

    def create_second_result(self):
        need(self.effective('A', 'turnstep') == {'id': 'P', 'revision': 2},
             'P@2 must be explicitly adopted before the second result')
        new_record(self.store, 'Q', 'product', attempt='A',
                   parts={'draft_status': 'present', 'draft_notifications': 'present'},
                   dimensions=deepcopy(CODE_WRITTEN),
                   plan_usage={'turnstep': {'id': 'P', 'revision': 2}})

    def result_locator(self, which):
        return {'product': 'R' if which == 'old' else 'Q', 'revision': 1}

    def result_view(self, which, revision=None):
        pid = 'R' if which == 'old' else 'Q'
        product = self.store[pid]
        if revision is None:
            item = {'revision': product['revision'],
                    'dimensions': deepcopy(product['dimensions']),
                    'parts': deepcopy(product['parts']),
                    'advanced_by': product.get('advanced_by')}
        else:
            snapshot = at(self.store, pid, revision)
            item = {'revision': snapshot['revision'],
                    'dimensions': deepcopy(snapshot['dimensions']),
                    'parts': deepcopy(snapshot['parts']),
                    'advanced_by': snapshot.get('advanced_by')}
        return {'locator': {'product': pid}, 'revision': item['revision'],
                'dimensions': item['dimensions'], 'parts': item['parts'],
                'producer': item['advanced_by']}

    def evidence_subject(self):
        return {'id': 'Q', 'revision': 1}

    def advance_result(self, dimensions, producer):
        self.advance('Q', dimensions, actor=producer,
                     expected_revision=self.store['Q']['revision'])

    def withdraw_one_part(self):
        self.withdraw('Q', ['draft_status'], expected_revision=self.store['Q']['revision'])
        return {'actions': ['withdraw only Q.draft_status'],
                'observations': {'parts': deepcopy(self.store['Q']['parts']),
                                 'revision': self.store['Q']['revision']}}

    def old_state(self):
        return self.store['R']['parts']['draft_status']

    def current_state(self):
        return self.store['Q']['parts']['draft_status']

    def untouched_state(self):
        return self.store['Q']['parts']['draft_notifications']

    def check_resolves(self):
        subject = self.store['E']['subject']
        return at(self.store, subject['id'], subject['revision'])['revision'] == 1

    def atomic_failure_probe(self):
        self.advance('Q', {'completion': 'complete'}, actor='A',
                     expected_revision=self.store['Q']['revision'])
        need(False, 'synthetic mid-step failure after a legal result advance')

    def stale_probe(self):
        self.advance('Q', {'completion': 'complete'}, actor='A2', expected_revision=1)

    def unknown_target_probe(self):
        self.advance('MISSING', {'completion': 'complete'}, actor='A2',
                     expected_revision=1)

    def text_at_none(self):
        return at(self.store, 'Q', None)

    def identity_shape(self):
        return {'logical_identity': 'Product Q',
                'storage': 'store["Q"] independent record with versions',
                'locator': '{product, revision}',
                'version_sequence': 'Q.revision, independent of the attempt lifecycle',
                'producer_field': 'advanced_by on the Product'}

    def caller_requirements(self):
        return ['Product must exist and the exact revision must be current for a write',
                'advancing needs no attempt state; the actor is recorded on the Product',
                'withdrawal names known parts and the exact current revision',
                'historical read needs {product, revision}']

    def identity_count(self):
        products = [key for key, obj in self.store.items() if obj['kind'] == 'product']
        return {'product_identities': len(products),
                'product_revisions_retained': len(self.store['Q']['versions']) + 1}

    def revision_sequences(self):
        return [{'sequence': 'Q.revision', 'current': self.store['Q']['revision']}]

    def query_entry_points(self):
        return ['at(store, product, revision)', 'product.parts', 'product.dimensions']

    def conventions(self):
        return ['Product ID、revision、parts 与四维状态',
                'Evidence 使用 product 的 exact {id, revision}',
                '撤回与推进都要求 exact current revision',
                'Product 不依赖 Attempt 记录是否存在']

    def failure_modes(self):
        return ['成果与尝试生命周期分离后，必须单独记录 advanced_by 才能说明推进者']

    def native(self):
        return {'storage': 'store["Q"] independent product record',
                'varied_identity': 'product id',
                'locator': '{product, revision}',
                'sample': deepcopy(self.store['Q'])}


class C2B(C2Base):
    group, mode = 'C2', 'B'

    def attempt_fields(self):
        return {'slots': {}}

    def _slot_record(self, host, name):
        need(host in self.store and self.store[host]['kind'] == 'attempt',
             'unknown attempt host: ' + str(host))
        slots = self.store[host].get('slots', {})
        need(name in slots, 'unknown result slot: ' + str(name))
        return slots[name]

    def _slot_snapshot(self, item):
        return {'state': item['state'],
                'dimensions': deepcopy(item['dimensions']),
                'producer': item['producer'],
                'dimension_producer': item['dimension_producer'],
                'plan_usage': deepcopy(item.get('plan_usage'))}

    def create_slot(self, host, name, dimensions, producer, plan_usage):
        slots = self.store[host]['slots']
        need(name not in slots, 'duplicate result slot: ' + name)
        slots[name] = {'revision': 1, 'state': 'present',
                       'dimensions': deepcopy(dimensions), 'producer': producer,
                       'dimension_producer': producer,
                       'plan_usage': deepcopy(plan_usage), 'versions': {}}

    def slot_current(self, host, name):
        item = self._slot_record(host, name)
        return {'revision': item['revision'], 'state': item['state'],
                'dimensions': deepcopy(item['dimensions']),
                'producer': item['producer'],
                'dimension_producer': item['dimension_producer'],
                'plan_usage': deepcopy(item.get('plan_usage'))}

    def slot_at(self, host, name, revision):
        item = self._slot_record(host, name)
        exact_revision(revision, 'result revision')
        if revision == item['revision']:
            return self.slot_current(host, name)
        key = str(revision)
        need(key in item['versions'],
             'result revision not retained: %s/%s@%s' % (host, name, revision))
        snapshot = item['versions'][key]
        return {'revision': int(key), 'state': snapshot['state'],
                'dimensions': deepcopy(snapshot['dimensions']),
                'producer': snapshot['producer'],
                'dimension_producer': snapshot['dimension_producer'],
                'plan_usage': deepcopy(snapshot.get('plan_usage'))}

    def write_slot(self, host, name, dimensions=None, state=None, producer=None,
                   plan_usage=None, expected_revision=None):
        item = self._slot_record(host, name)
        need(type(expected_revision) is int and expected_revision == item['revision'],
             'stale slot update: expected %s, current %s'
             % (expected_revision, item['revision']))
        need(isinstance(producer, str) and bool(producer), 'producer required')
        merged = deepcopy(item['dimensions'])
        for key, value in (dimensions or {}).items():
            need(key in DIMENSION_VALUES, 'unknown dimension: ' + str(key))
            need(value in DIMENSION_VALUES[key], 'controlled dimension value required: ' + key)
            merged[key] = value
        if state is not None:
            need(state in {'present', 'withdrawn'}, 'known result state required')
        item['versions'][str(item['revision'])] = self._slot_snapshot(item)
        item['revision'] += 1
        item['dimensions'] = merged
        if state is not None:
            item['state'] = state
        item['producer'] = producer
        if dimensions:
            item['dimension_producer'] = producer
        if plan_usage is not None:
            item['plan_usage'] = deepcopy(plan_usage)
        return item['revision']

    def create_first_result(self):
        need(self.effective('A', 'turnstep') == {'id': 'P', 'revision': 1},
             'P@1 must be explicitly adopted before the first result')
        self.create_slot('A', 'draft_status', DRAFT, 'A',
                         {'turnstep': {'id': 'P', 'revision': 1}})
        self.create_slot('A', 'draft_notifications', DRAFT, 'A',
                         {'turnstep': {'id': 'P', 'revision': 1}})

    def create_second_result(self):
        need(self.effective('A', 'turnstep') == {'id': 'P', 'revision': 2},
             'P@2 must be explicitly adopted before the second result')
        self.write_slot('A', 'draft_status', dimensions=CODE_WRITTEN, producer='A',
                        plan_usage={'turnstep': {'id': 'P', 'revision': 2}},
                        expected_revision=1)

    def result_locator(self, which):
        return {'attempt': 'A', 'slot': 'draft_status', 'revision': 1 if which == 'old' else 2}

    def result_view(self, which, revision=None):
        item = (self.slot_at('A', 'draft_status', revision) if revision is not None
                else self.slot_current('A', 'draft_status'))
        return {'locator': {'attempt': 'A', 'slot': 'draft_status'},
                'revision': item['revision'], 'dimensions': item['dimensions'],
                'state': item['state'], 'producer': item['dimension_producer']}

    def evidence_subject(self):
        return deepcopy(self.refs['new_result'])

    def advance_result(self, dimensions, producer):
        item = self.slot_current('A', 'draft_status')
        self.write_slot('A', 'draft_status', dimensions=dimensions, producer=producer,
                        expected_revision=item['revision'])

    def withdraw_one_part(self):
        item = self.slot_current('A', 'draft_status')
        self.write_slot('A', 'draft_status', state='withdrawn', producer='A',
                        expected_revision=item['revision'])
        return {'actions': ['withdraw only the draft_status slot'],
                'observations': {'states': {name: self.slot_current('A', name)['state']
                                            for name in ('draft_status', 'draft_notifications')},
                                 'revision': self.slot_current('A', 'draft_status')['revision']}}

    def old_state(self):
        return self.slot_at('A', 'draft_status', 1)['state']

    def current_state(self):
        return self.slot_current('A', 'draft_status')['state']

    def untouched_state(self):
        return self.slot_current('A', 'draft_notifications')['state']

    def check_resolves(self):
        subject = self.store['E']['subject']
        return bool(self.slot_at(subject['attempt'], subject['slot'], subject['revision']))

    def atomic_failure_probe(self):
        self.write_slot('A', 'draft_status', dimensions={'completion': 'complete'},
                        producer='A',
                        expected_revision=self.slot_current('A', 'draft_status')['revision'])
        need(False, 'synthetic mid-step failure after a legal slot write')

    def stale_probe(self):
        self.write_slot('A', 'draft_status', dimensions={'completion': 'complete'},
                        producer='A2', expected_revision=1)

    def unknown_target_probe(self):
        self.write_slot('A', 'MISSING', dimensions={'completion': 'complete'},
                        producer='A2', expected_revision=1)

    def text_at_none(self):
        return self.slot_at('A', 'draft_status', None)

    def resolve_locator(self, locator):
        if isinstance(locator, dict) and 'attempt' in locator and 'slot' in locator:
            return self.slot_at(locator['attempt'], locator['slot'],
                                locator['revision'])['dimensions']
        return super().resolve_locator(locator)

    def identity_shape(self):
        return {'logical_identity': '(host attempt A, slot draft_status)',
                'storage': 'store["A"].slots["draft_status"] with per-slot versions',
                'locator': '{attempt, slot}; exact history adds the slot revision',
                'version_sequence': 'slot revision inside the host, host status unchanged',
                'producer_field': 'producer and dimension_producer per slot revision'}

    def caller_requirements(self):
        return ['host attempt must exist; the slot name is a stable local identity',
                'a write names the exact current slot revision and a producer',
                'the host may be ended; the write does not change its status',
                'historical read needs {attempt, slot, revision}']

    def identity_count(self):
        slots = self.store['A']['slots']
        revisions = sum(len(item['versions']) + 1 for item in slots.values())
        return {'product_identities': 0, 'result_slots': len(slots),
                'slot_revisions_retained': revisions}

    def revision_sequences(self):
        return [{'sequence': 'A.slots.%s.revision' % name,
                 'current': item['revision'],
                 'retained': sorted(int(key) for key in item['versions']) + [item['revision']]}
                for name, item in sorted(self.store['A']['slots'].items())]

    def query_entry_points(self):
        return ['slot_current(host, slot)', 'slot_at(host, slot, revision)',
                'product.plan_usage on the slot revision']

    def conventions(self):
        return ['宿主 Attempt 内的 slot 必须逐 revision 保留',
                '逻辑定位是 (attempt, slot)；精确历史再带 slot revision',
                '每次写入必须记录 producer；只有推进四维的写入才更新 dimension_producer',
                '宿主 lifecycle 状态与 slot 修订分离，ended 时仍可由另一个尝试推进',
                '跨尝试推进不复制 slot，逻辑定位保持不变']

    def failure_modes(self):
        return ['slot 名成为必须维护的局部身份，改名会破坏旧定位',
                '删掉旧 slot revision 会让旧证据的成果引用悬空',
                '删除宿主 Attempt 会同时删除成果历史']

    def native(self):
        return {'storage': 'store["A"].slots (host attempt)',
                'varied_identity': 'none for Product',
                'locator': '{attempt, slot} + exact revision for history',
                'sample': deepcopy(self.store['A']['slots']['draft_status'])}


# --------------------------------------------------------------- builders


def _legal(world, case_id, intent, fn):
    row = world.commit('probe-' + case_id, fn)
    return {'id': case_id, 'intent': intent, 'change': row['change'],
            'actions': row['actions'], 'observations': row['observations'],
            'changed_paths': row['changed_paths'], 'accepted': row['accepted']}


def _illegal(world, case_id, kind, intent, fn, mutated=False):
    outcome = world.expect_reject(fn)
    return {'id': case_id, 'kind': kind, 'intent': intent, 'accepted': False,
            'error': outcome['error'], 'state_unchanged': True,
            'head_unchanged': True, 'mutated_before_failure': mutated}


def _removal(world, removed, still, lost, conventions):
    return {'removed': removed, 'still_readable': still, 'lost': lost,
            'conventions_counted': conventions,
            'note': '探针在 world 的副本上执行；lost 中的错误是实际读出的结果'}


def _placement(world, reader):
    copy = deepcopy(world)
    copy.store.pop('A', None)
    try:
        value = reader(copy)
    except (Reject, KeyError) as error:
        return {'removed': 'host attempt A（删除探针，不是正常路径）',
                'readable': False, 'observed': str(error)}
    return {'removed': 'host attempt A（删除探针，不是正常路径）',
            'readable': True, 'observed': value}


def build_c1(mode):
    world = C1A() if mode == 'A' else C1B()
    chain = world.chain()
    legal = [
        _legal(world, 'legal-plan-edit-with-current-revision',
               '带当前精确 revision 的计划修改必须被接受（证明 guard 不禁用合法更新）',
               lambda w: w.edit_with_current_revision()),
        _legal(world, 'reference-readback',
               '读回旧成果计划文本、消费者当前采用与第二次尝试采用的版本',
               lambda w: {'actions': ['read back exact plan references'],
                          'observations': w.readback_references()}),
    ]
    illegal = [
        _illegal(world, 'stale-plan-update', 'stale',
                 '过期 revision 的计划更新必须拒绝',
                 lambda w: w.edit_plan({'turnstep': deepcopy(PLAN_V2_TURNSTEP)},
                                       expected_revision=1)),
        _illegal(world, 'unknown-plan-section', 'invalid_locator',
                 '未知 section 必须拒绝',
                 lambda w: w.edit_plan({'missing': {'status': 'x', 'description': 'y'}},
                                       expected_revision=w.plan_version())),
        _illegal(world, 'non-exact-plan-revision', 'invalid_locator',
                 'revision=None 不能当精确版本',
                 lambda w: w.text_at_none()),
        _illegal(world, 'unknown-plan-version', 'invalid_locator',
                 '不存在的计划版本不能采用',
                 lambda w: w.adopt_exact('A2', 99, ['turnstep'], ['SYN:missing'])),
        _illegal(world, 'mid-step-atomic-rollback', 'atomicity',
                 '合法计划修改后中途异常必须整体回退',
                 lambda w: w.atomic_failure_probe(), mutated=True),
    ]
    state = world.final_state(chain)
    old = world.plan_basis('R', 'turnstep')
    probe = deepcopy(world)
    if mode == 'B':
        probe.store['A']['history'] = [probe.store['A']['history'][-1]]
        removed = '只保留宿主 Attempt 的最新 revision'
        conventions = ['逐版保留宿主 Attempt 的完整历史 revision',
                       '定位携带 (host attempt, revision, section)']
    else:
        probe.store['P']['versions'] = {}
        removed = '只保留 Plan 的当前 revision'
        conventions = ['逐版保留 Plan revision', '消费者记录 exact {id, revision}']
    lost = []
    try:
        if mode == 'B':
            probe.plan_text_at('A', 1, 'turnstep')
        else:
            probe.plan_text(1, 'turnstep')
    except Reject as error:
        lost.append({'query': '旧成果所用 turnstep 文本 @rev1', 'failure': str(error)})
    still = {'current_text': probe.latest_plan_text('turnstep')}
    return {'alternative': SPEC['C1']['alt_a' if mode == 'A' else 'alt_b'],
            'native': world.native(), 'identity_shape': world.identity_shape(),
            'caller_requirements': world.caller_requirements(),
            'chain': chain, 'final_state': state, 'legal': legal, 'illegal': illegal,
            'removal_probe': _removal(probe, removed, still, lost, conventions),
            'placement_effect': _placement(world, lambda w: w.text_of('turnstep', old)),
            'identity_cost': world.cost(chain),
            'historical_references': world.historical_references()}


def build_c2(mode):
    world = C2A() if mode == 'A' else C2B()
    chain = world.chain()
    legal = [
        _legal(world, 'historical-read', '按精确版本读回旧成果与刚修正的成果',
               lambda w: {'actions': ['read exact historical results'],
                          'observations': {
                              'old_result': w.result_view('old', 1),
                              'previous_revision': w.result_view(
                                  'new', w.result_view('new', None)['revision'] - 1)}}),
        _legal(world, 'current-read', '读回当前成果与推进者',
               lambda w: {'actions': ['read the current result'],
                          'observations': {'current_result': w.result_view('new', None)}}),
        _legal(world, 'withdraw-single-part', '只撤回列明部分，其余保留',
               lambda w: w.withdraw_one_part()),
    ]
    illegal = [
        _illegal(world, 'stale-result-update', 'stale',
                 '过期 revision 的成果写入必须拒绝',
                 lambda w: w.stale_probe()),
        _illegal(world, 'unknown-result-target', 'invalid_locator',
                 '未知成果目标必须拒绝',
                 lambda w: w.unknown_target_probe()),
        _illegal(world, 'non-exact-result-revision', 'invalid_locator',
                 'revision=None 不能当精确成果版本',
                 lambda w: w.text_at_none()),
        _illegal(world, 'mid-step-atomic-rollback', 'atomicity',
                 '合法成果写入后中途异常必须整体回退',
                 lambda w: w.atomic_failure_probe(), mutated=True),
    ]
    state = world.final_state(chain)
    probe = deepcopy(world)
    if mode == 'B':
        probe.store['A']['slots'].pop('draft_status')
        removed = '删除宿主 Attempt 的成果 slot'
        conventions = ['slot 逐 revision 保留', '逻辑定位 (attempt, slot) 稳定',
                       '每次写入记录 producer']
    else:
        probe.store['Q']['versions'] = {}
        removed = '只保留 Product 的当前 revision'
        conventions = ['逐版保留 Product revision', '证据引用 exact {product, revision}']
    lost = []
    try:
        if mode == 'B':
            probe.slot_at('A', 'draft_status', 1)
        else:
            at(probe.store, 'Q', 1)
    except (Reject, KeyError) as error:
        lost.append({'query': '旧证据指向的成果版本', 'failure': str(error)})
    still = {'current_dimensions': (probe.result_view('new', None)['dimensions']
                                    if mode == 'A'
                                    else probe.slot_current('A', 'draft_notifications')['dimensions'])}
    return {'alternative': SPEC['C2']['alt_a' if mode == 'A' else 'alt_b'],
            'native': world.native(), 'identity_shape': world.identity_shape(),
            'caller_requirements': world.caller_requirements(),
            'chain': chain, 'final_state': state, 'legal': legal, 'illegal': illegal,
            'removal_probe': _removal(probe, removed, still, lost, conventions),
            'placement_effect': _placement(
                world, lambda w: w.result_view('new', None)['dimensions']),
            'identity_cost': world.cost(chain),
            'historical_references': world.historical_references()}


BUILDERS = {'C1': build_c1, 'C2': build_c2}


def compare_v2(gid, a, b):
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
    placement = [{'probe': spec['placement_probe'],
                  'A': a['placement_effect']['readable'],
                  'B': b['placement_effect']['readable'],
                  'same': a['placement_effect']['readable'] == b['placement_effect']['readable'],
                  'observed': {'A': a['placement_effect']['observed'],
                               'B': b['placement_effect']['observed']}}]
    substantive = ([dict(row, kind='capability') for row in differences] +
                   [dict(row, kind='placement') for row in placement if not row['same']])
    mismatches = [row for row in content if not row['same']]
    failures = [{'kind': 'content_mismatch', 'query': row['query'],
                 'observed': {'A': row['A'], 'B': row['B']}} for row in mismatches]
    for label, report in (('A', a), ('B', b)):
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
            'identity_shape': {'A': a['identity_shape'], 'B': b['identity_shape']},
            'caller_requirements': {'A': a['caller_requirements'],
                                    'B': b['caller_requirements']},
            'content_queries': content,
            'capability_queries': capabilities,
            'placement_queries': placement,
            'same_successes': same_successes,
            'differences': differences,
            'substantive_differences': substantive,
            'substantive_difference': bool(substantive) or bool(mismatches),
            'limits_and_failures': failures,
            'identity_cost': {'A': a['identity_cost'], 'B': b['identity_cost']},
            'version_coupling': {'A': a['final_state'].get('version_coupling'),
                                 'B': b['final_state'].get('version_coupling')},
            'open_questions': spec['open'],
            'A': a, 'B': b}


def assumptions(groups):
    c1 = groups['C1']
    c2 = groups['C2']
    c1b = c1['B']['final_state']
    c2b = c2['B']['final_state']
    rows = [
        {'id': 'V1',
         'before': '内嵌 Plan 无法在不复制的情况下被另一个尝试引用同一版本',
         'group': 'C1',
         'observed': 'C1 两种表示中，第二次尝试都以同一 locator 引用旧版本：%s / %s，'
                     '且第二次尝试没有自己的计划副本。'
                     % (c1['A']['chain'][-1]['observations']['R_plan'],
                        c1['A']['chain'][-1]['observations']['Q2_plan']),
         'refuted': c1b['capabilities']['shared_plan_version_across_attempts']
                    and not c1['B']['chain'][-1]['observations']['copied_plan_content']},
        {'id': 'V2',
         'before': '内嵌 Product 跨尝试推进时必然复制到新宿主并丢失原身份',
         'group': 'C2',
         'observed': 'C2 B 由 A2 推进 A 的原 slot，逻辑定位保持 %s，宿主保持 %s。'
                     % (c2b['locators']['new_result'], c2b['content']['attempt_status']),
         'refuted': c2b['capabilities']['same_result_identity_across_attempts']
                    and c2b['capabilities']['host_attempt_remains_ended']},
        {'id': 'V3',
         'before': '无关的 Attempt 生命周期变化会让旧成果的计划引用失效',
         'group': 'C1',
         'observed': '结束时 B 的宿主 revision 从 %s 推进到 %s，但旧成果的 turnstep 文本仍读出原值。'
                     % (c1b['version_coupling']['lifecycle_end']['attempt_revision_before'],
                        c1b['version_coupling']['lifecycle_end']['attempt_revision_after']),
         'refuted': c1b['capabilities']['old_plan_locator_readable_after_lifecycle_change']},
        {'id': 'V4',
         'before': '内嵌表示不需要额外的版本保留约定',
         'group': 'C1/C2',
         'observed': 'C1 B 必须逐版保留宿主 revision；C2 B 必须逐 slot 保留 revision 与 producer。'
                     '删除这些历史的探针分别丢失旧计划文本与旧成果版本。',
         'refuted': bool(c1['B']['removal_probe']['lost']) and bool(c2['B']['removal_probe']['lost'])},
    ]
    for row in rows:
        row['status'] = 'refuted' if row['refuted'] else 'not_refuted'
        del row['refuted']
    return rows


def self_check(results):
    for gid, group in results['groups'].items():
        expected = EXPECTED_CHAINS[gid]
        for mode in ('A', 'B'):
            report = group[mode]
            need([step['label'] for step in report['chain']] == expected,
                 '%s chain labels differ in %s' % (gid, mode))
            need(all(step['accepted'] for step in report['chain']),
                 '%s chain step not accepted in %s' % (gid, mode))
            need(all(step['before'] and step['after'] for step in report['chain']),
                 '%s chain trace missing in %s' % (gid, mode))
            need(all(step['changed_paths'] for step in report['chain']),
                 '%s chain step changed nothing in %s' % (gid, mode))
            need(bool(report['removal_probe']['lost']),
                 '%s removal probe lost nothing in %s' % (gid, mode))
            need(bool(report['historical_references']),
                 '%s historical references missing in %s' % (gid, mode))
            if gid in ('C1', 'C2'):
                need(len(report['illegal']) >= 4, '%s illegal probes missing in %s' % (gid, mode))
                kinds = {row['kind'] for row in report['illegal']}
                need({'stale', 'invalid_locator', 'atomicity'} <= kinds,
                     '%s probe kinds missing in %s' % (gid, mode))
                need(all(not row['accepted'] for row in report['illegal']),
                     '%s illegal probe was accepted in %s' % (gid, mode))
                need(all(row['state_unchanged'] for row in report['illegal']),
                     '%s rejection changed state in %s' % (gid, mode))
                need(all(row['head_unchanged'] for row in report['illegal']),
                     '%s rejection advanced head in %s' % (gid, mode))
                atomic = [row for row in report['illegal'] if row['kind'] == 'atomicity']
                need(atomic and 'synthetic mid-step failure' in atomic[0]['error'],
                     '%s atomic probe did not reach the forced failure in %s' % (gid, mode))
                need(any(row['accepted'] for row in report['legal']),
                     '%s has no accepted legal probe in %s' % (gid, mode))
            for key in report['final_state']['capabilities']:
                meanings = CAP_MEANING if gid in ('C1', 'C2') else v1.CAP_MEANING
                need(key in meanings, 'capability without meaning: ' + key)
        need(set(group['A']['final_state']['content'])
             == set(group['B']['final_state']['content']), gid + ' content keys differ')
        need(set(group['A']['final_state']['capabilities'])
             == set(group['B']['final_state']['capabilities']),
             gid + ' capability keys differ')
        for row in group['content_queries']:
            need(row['same'], '%s content query differs: %s (A=%r B=%r)'
                 % (gid, row['query'], row['A'], row['B']))
    c1 = results['groups']['C1']
    need(c1['A']['final_state']['capabilities']['shared_plan_version_across_attempts']
         and c1['B']['final_state']['capabilities']['shared_plan_version_across_attempts'],
         'C1 shared plan locator is not true on both sides')
    c2 = results['groups']['C2']
    need(c2['A']['final_state']['capabilities']['same_result_identity_across_attempts']
         and c2['B']['final_state']['capabilities']['same_result_identity_across_attempts'],
         'C2 result identity is not stable on both sides')
    need(results['boundary']['no_final_recommendation'], 'boundary lost')


def build_results():
    groups = {}
    for gid in ('C1', 'C2'):
        groups[gid] = compare_v2(gid, BUILDERS[gid]('A'), BUILDERS[gid]('B'))
    for gid, builder in (('C3', v1.build_c3), ('C4', v1.build_c4)):
        group = v1.compare(gid, builder('A'), builder('B'))
        group['reused_from'] = 'identity-v1: t12_identity_trials.build_c%s (unchanged)' % gid[1]
        groups[gid] = group
    results = {
        'schema': 2,
        'case': 'T12',
        'slice': SLICE,
        'batch': BATCH,
        'generated_by': 't12_identity_trials_v2.build_results',
        'corrects': 'identity-v1',
        'study_baseline': v1.STUDY_BASELINE,
        'control': 'S0 + v2 强 B：C1 内嵌计划用宿主完整 revision 历史，C2 内嵌 slot 保持 (host, slot) 逻辑定位',
        'common_chain': {'C1': C1_CHAIN, 'C2': C2_CHAIN,
                         'C3': v1.CHAIN_LABELS, 'C4': v1.CHAIN_LABELS},
        'groups': groups,
        'assumptions': assumptions(groups),
        'v1_status': {
            'directory': 'artifacts/agent-task-state/maintenance/%s/identity-v1' % BATCH,
            'unchanged_by_this_run': True,
            'note': 'v1 现存 results.json 与 review.md 是上一任务重新生成后的文件，本轮只读不写；'
                    'v1 的测试仍对现存文件做内存复算校验。初始工具失败是另一事件（任务 d9e78236），'
                    '因此本记录不声称 v1 的历次输出都未被覆盖，只说明现存文件在本轮固定。'},
        'interface_coverage': {
            'covered': ['plan edit with the exact current revision',
                        'adoption by an active consumer from an exact version '
                        '(including another attempt history)',
                        'produce with the explicitly adopted version',
                        'result advance by a different active attempt with the exact current revision',
                        'result correction while the host attempt is ended',
                        'withdrawal of one result part/slot',
                        'exact historical readback after later writes',
                        'rejection of a stale update',
                        'rejection of an invalid locator',
                        'mid-step exception rollback'],
            'not_covered': ['concurrent writers', 'cross-goal plan sharing', 'authority/permissions',
                            'bulk rename or migration', 'host archival beyond the deletion probe',
                            'natural-language truth of evidence', 'DSH event semantics'],
            'claim': '只证明上列 v2 公开操作在给定输入下的行为；不声称 v2 的所有公开路径安全，'
                     '也不把未覆盖的路径当作已验证。'},
        'boundary': {
            'synthetic': '所有比较步骤为本地合成；basis 前缀 SYN:，nature=synthetic，'
                         '不是 DSH 事件，没有事件时间；T12 事实只作为问题动机，不冒充新的历史记录。',
            'no_model_calls': '本模块不调用模型、不运行 Git、不访问网络',
            'no_final_recommendation': True,
            'scope': '只比较 C1/C2 的强 B 修正与复用 C3/C4；不写最终文档、不更新规范',
            'identity_origin': '所有对象 ID 与 Change 编号都是研究者编码，不是来源原有身份',
        }}
    self_check(results)
    return results


def _compact(value, limit=360):
    text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    return text if len(text) <= limit else text[:limit] + '…'


def _fmt_counts(counts):
    return '，'.join('%s=%s' % (key, value) for key, value in sorted(counts.items()))


def _fmt_step(label, a_step, b_step):
    return '| %s | %s | %s | %s |' % (
        label, a_step['change'], b_step['change'],
        _compact({'A': a_step['observations'], 'B': b_step['observations']}, 520))


def _group_section(gid, group, lines):
    add = lines.append
    add('')
    add('### %s：%s' % (gid, group['changed_choice']))
    add('')
    add('- A 表示：%s' % group['alternatives']['A'])
    add('- B 表示：%s' % group['alternatives']['B'])
    add('- 固定：%s' % '、'.join(group['fixed']))
    add('- 逻辑身份 / 存放位置：')
    for mode in ('A', 'B'):
        shape = group['identity_shape'][mode]
        add('  - %s：`%s`；存放 `%s`；定位 `%s`；版本序列 `%s`%s' % (
            mode, shape['logical_identity'], shape['storage'], shape['locator'],
            shape['version_sequence'],
            ('；生产者 `%s`' % shape['producer_field']) if 'producer_field' in shape else ''))
    add('- 调用者要求：A %s；B %s' % ('；'.join(group['caller_requirements']['A']),
                                     '；'.join(group['caller_requirements']['B'])))
    add('')
    add('**共同链（A/B 同步执行，含实际 change 号与关键读回）**')
    add('')
    add('| 步骤 | A change | B change | 关键观察（A/B） |')
    add('|---|---|---|---|')
    for a_step, b_step in zip(group['A']['chain'], group['B']['chain']):
        add(_fmt_step(a_step['label'], a_step, b_step))
    add('')
    add('**相同成功**：' + '；'.join(row['probe'] for row in group['same_successes']))
    add('')
    if group['differences']:
        add('**能力差异（行为查询）**：')
        for row in group['differences']:
            add('- `%s`：A=%s，B=%s。%s' % (row['probe'], row['A'], row['B'], row['meaning']))
    else:
        add('**能力差异（行为查询）**：未发现。两种表示在共同链与合法/非法探针下返回相同内容；'
            '差别只在存放位置、定位宽度与版本序列（见上表与成本）。')
    add('')
    add('**存放位置差异（删除探针）**：')
    for row in group['placement_queries']:
        add('- `%s`：A=%s，B=%s；读出 A=%s / B=%s' % (
            row['probe'], row['A'], row['B'], _compact(row['observed']['A'], 160),
            _compact(row['observed']['B'], 160)))
    add('')
    add('**合法探针（实际执行并接受）**：')
    for row in group['A']['legal']:
        add('- A `%s`：%s → %s' % (row['id'], row['intent'], _compact(row['observations'])))
    for row in group['B']['legal']:
        add('- B `%s`：%s → %s' % (row['id'], row['intent'], _compact(row['observations'])))
    add('')
    add('**拒绝证据（状态与 head 均未变化）**：')
    for mode in ('A', 'B'):
        for row in group[mode]['illegal']:
            add('- %s `%s`（%s）：%s → `%s`' % (mode, row['id'], row['kind'], row['intent'],
                                               row['error']))
    add('')
    add('**删除/弱化探针（B）**：移除“%s”后，仍可读 `%s`；丢失：' %
        (group['B']['removal_probe']['removed'],
         _compact(group['B']['removal_probe']['still_readable'])))
    for row in group['B']['removal_probe']['lost']:
        add('- %s → `%s`' % (row['query'], row['failure']))
    add('- 必须新加的约定：%s' % '；'.join(group['B']['removal_probe']['conventions_counted']))
    add('')
    if group['version_coupling']['B']:
        add('**B 的额外版本耦合（记录，不自动判失败）**：%s' %
            _compact(group['version_coupling']['B'], 700))
        add('')
    cost = group['identity_cost']['B']
    add('**B 的成本（实测）**：%s；单次变化最多触及 %s 个记录；修订序列 %s。'
        % (_fmt_counts(cost['identity_records']), cost['max_records_changed_in_one_change'],
           _compact(cost['revision_sequences'])))
    add('**B 的新约定**：%s。' % '；'.join(cost['extra_conventions']))
    add('**B 的失败模式**：%s。' % '；'.join(cost['failure_modes']))


def build_review(results):
    groups = results['groups']
    lines = []
    add = lines.append
    add('# T12 第2b阶段修正：强 B 的身份比较（identity-v2）')
    add('')
    add('- status: 执行结果；只做两组内嵌身份的有界纠偏，不做最终推荐')
    add('- date: 2026-10-30')
    add('- study baseline: `%s`' % results['study_baseline'])
    add('- 生成：`t12_identity_trials_v2.build_results()`；本文件与 `results.json` 由同一次执行产生')
    add('- C1 链：%s' % ' → '.join(results['common_chain']['C1']))
    add('- C2 链：%s' % ' → '.join(results['common_chain']['C2']))
    add('- C3/C4：复用 identity-v1 未改动的 builder 与 compare，未改写 v1 文件')
    add('')
    add('## 1. 这一版修正了什么')
    add('')
    add('identity-v1 的 C1 B 把计划放在“attempt content revision”里，这套 revision 不是宿主 Attempt 的 revision。'
        '计划修改只推进内容修订，宿主 revision 不动；第二个尝试无法指向 A 的精确版本，只能复制内容，'
        '于是 `shared_plan_version_across_attempts` 被结构性地判为 False。v1 的 C1 测试还把这一结果当作实质差异，'
        '这是比较设置造成的，不是“独立 Plan”相对“内嵌 Plan”的必然差别。')
    add('')
    add('identity-v1 的 C2 B 要求 A2 把 slot 复制进 A2 自己的内容修订，旧 locator 因此改变，'
        '`same_result_identity_across_attempts` 同样被结构性地判为 False。v1 的 C2 B 还把合法的 produce 路径写成'
        '“C2 B has no independent product identity”并直接拒绝；v2 不再用禁用合法更新换取探针通过。')
    add('')
    add('v2 的 B 满足与 A 相同的合法行为：C1 B 的计划在宿主 Attempt 的完整 revision 历史里，'
        'A2 直接采用 `(A, revision, section)` 而不复制；计划新版本只有被消费者显式采用才进入它的新成果。'
        'C2 B 的成果 slot 保持逻辑定位 `(A, slot)`，A2 推进 A 的原 slot，宿主保持 ended，'
        '每个 revision 记录 producer，历史不被覆盖。')
    add('')
    add('## 2. 方法与边界')
    add('')
    add('每组只改一个身份选择，其余四项固定在 S0；A 与 B 是两套独立的内存存储，B 中不存在被替代对象的记录。'
        '两组的 A 与 B 使用同一组链步骤、同一组合法/非法探针意图与同一组输入，差别只允许来自身份存放位置。')
    add('')
    add('v2 的提交是事务性的：每步先记录快照，任何异常都会整体回退并保持 head 不变（v1 的 `World.commit` 未改，'
        'v2 在本地封装）。每组至少包含过期更新、无效定位、中途异常原子回退三类拒绝探针；'
        '所有拒绝都核对状态与 head 未变化。')
    add('')
    add('所有新行为使用 `SYN:` basis 与 `synthetic` nature；它们不是 DSH 事件，没有事件时间。'
        'T12 的历史事实只用于提出“内嵌计划/内嵌成果能否跨尝试共享”的问题，不冒充新的历史记录。'
        '成本只计数可执行结构：身份记录、修订序列、单次变化的更新位置、查询入口与新约定；'
        '不估计人工时间或模型费用。')
    add('')
    add('能力查询只保留有行为读回的项；`independent_plan_record`、`independent_product_record`、'
        '`slot_local_identity_required` 这类由前提直接决定真假的条目已从比较中剔除。')
    add('')
    add('## 3. 四组对照总表')
    add('')
    add('| 组 | 只改的选择 | 行为差异 | 差异点 |')
    add('|---|---|---|---|')
    for gid, group in groups.items():
        names = '、'.join(row['probe'] for row in group['substantive_differences']) or '未发现'
        add('| %s | %s | %s | %s |' % (gid, group['changed_choice'],
                                       '有' if group['substantive_difference'] else '未发现', names))
    add('')
    add('“未发现”只表示在本轮共同链、合法/非法探针和删除/放置探针下没有测到行为差异；'
        '不表示两种表示等价，也不裁定是否需要独立身份。C3/C4 的“未发现”来自 v1 的既有结果，本轮未改其 builder。')
    add('')
    add('## 4. C1/C2 逐组结果')
    _group_section('C1', groups['C1'], lines)
    _group_section('C2', groups['C2'], lines)
    add('')
    add('## 5. C3/C4 复用结果')
    add('')
    for gid in ('C3', 'C4'):
        group = groups[gid]
        add('- %s：%s；%s。' % (gid, group['changed_choice'],
                               '复用 `identity-v1` 的 builder 与 compare，行为差异为“未发现”'
                               if not group['substantive_difference'] else '复用 v1 并发现差异'))
    add('')
    add('C3/C4 的完整链、删除探针与成本仍在 `results.json` 的对应组内；它们不是本轮新增的执行结论，'
        '而是同一 builder 的再次运行结果，用来保持四组表完整。')
    add('')
    add('## 6. 被反例改变的假设')
    add('')
    for row in results['assumptions']:
        add('- **%s**（%s，%s）：%s。观察：%s。' %
            (row['id'], row['group'], row['status'], row['before'], row['observed']))
    add('')
    add('## 7. 适用条件与 v2 接口覆盖')
    add('')
    add('- 结论只对列出的共同链、合法/非法探针、删除探针与放置探针成立；'
        '没有测试并发写入、跨目标共享、权限、批量迁移或人工维护时间。')
    add('- 强 B 的“成功”依赖它自己的新约定：%s。'
        % '；'.join(groups['C1']['B']['identity_cost']['extra_conventions']))
    add('- 强 B 的“成功”依赖它自己的新约定：%s。'
        % '；'.join(groups['C2']['B']['identity_cost']['extra_conventions']))
    add('- A 的成本同样计入：独立对象的 ID/版本/生命周期，以及采用、证据引用、验收决定的第二条更新路径。'
        '本轮没有把 changed paths 当作人工成本。')
    add('')
    add('**v2 接口覆盖**（只列实际执行过的公开操作）：')
    add('')
    for item in results['interface_coverage']['covered']:
        add('- 已覆盖：%s' % item)
    for item in results['interface_coverage']['not_covered']:
        add('- 未覆盖：%s' % item)
    add('')
    add(results['interface_coverage']['claim'])
    add('')
    add('## 8. v1 现存结果的状态')
    add('')
    add('- %s' % results['v1_status']['note'])
    add('- 因此本文件只固定 v2 的执行结果，不改写 v1 的目录，也不把“现存 v1 文件未变”扩展成“v1 历次输出从未被覆盖”。')
    add('')
    add('## 9. 不做最终推荐')
    add('')
    add('本文只给出 C1/C2 强 B 修正后的执行结果、读回、成本与拒绝证据，并复用 C3/C4 的既有比较。'
        '它不选择哪种身份边界应被采用，也不把“某个方案在本轮探针下成功”当作最终裁定；调度与裁定由 Astra 负责。')
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
    """Create identity-v2 once.  An existing directory is never overwritten."""
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
