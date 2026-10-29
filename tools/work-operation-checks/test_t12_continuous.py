"""Continuous control chain for T12: references, plan adoption, lifecycle, acceptance."""
from copy import deepcopy
import unittest
import t12_responsibility as responsibility
import t12_study as s


DRAFT = {'completion': 'in_progress', 'implementation': 'reported_draft_written',
         'git': 'unstaged', 'acceptance': 'pending'}


def update(state, actions, basis=('SYN:test',)):
    result = s.apply(state, list(actions), state['head'], list(basis))
    if result['status'] != 'applied':
        raise AssertionError(result['error'])
    return result['state']


def chain(plans='independent'):
    """G/A on P1 produce R; P2 then edits one section.  Explicit synthetic sequence."""
    state = s.fresh('parent', plans)
    sections = {'alpha': {'status': 'planned', 'description': 'alpha v1'},
                'beta': {'status': 'planned', 'description': 'beta v1'}}
    state = update(state, [
        {'op': 'goal', 'id': 'g', 'scope': ['alpha', 'beta']},
        {'op': 'begin', 'id': 'owner', 'goal': 'g', 'scope': ['alpha', 'beta']},
        {'op': 'plan', 'id': 'p', 'owner': 'owner', 'sections': sections},
        {'op': 'begin', 'id': 'a', 'goal': 'g', 'scope': ['alpha', 'beta'],
         'plan': {'id': 'p', 'revision': 1}},
        {'op': 'begin', 'id': 'b', 'goal': 'g', 'scope': ['alpha', 'beta']}])
    return update(state, [
        {'op': 'produce', 'id': 'r', 'attempt': 'a', 'parts': ['alpha-part'],
         'dimensions': dict(DRAFT), 'location': 'synthetic workspace', 'nature': 'synthetic'},
        {'op': 'report', 'id': 'r-report', 'subject': {'id': 'r', 'revision': 1},
         'scope': 'alpha and beta as first drafted', 'findings': ['draft only'], 'nature': 'synthetic'},
        {'op': 'responsibility_init', 'owner': 'owner', 'tokens': ['alpha', 'beta'], 'holders': ['a', 'b']},
        {'op': 'assign', 'token': 'beta', 'to': 'a'}])


def acceptance(evidence, goal='g'):
    return {'op': 'accept_goal', 'id': goal, 'actor_role': 'acceptor', 'actor': 'synthetic-reviewer',
            'criteria': ['declared scope checked'], 'decision': 'accept', 'evidence': list(evidence)}


class PlanAdoptionTests(unittest.TestCase):
    def test_chain_adopts_one_scope_and_never_upgrades_silently(self):
        for placement in ['independent', 'embedded']:
            state = chain(placement)
            r_before, report_before = s.version(state, 'r'), s.version(state, 'r-report')
            begin_adoption = s.version(state, 'a')['plan_adoptions']
            self.assertEqual(1, len(begin_adoption))
            self.assertEqual({'plan': {'id': 'p', 'revision': 1}, 'scope': ['alpha', 'beta'],
                              'basis': ['SYN:test'], 'change': 1, 'origin': 'begin'}, begin_adoption[0])

            state = update(state, [{'op': 'change_plan', 'id': 'p',
                                    'edits': {'beta': {'status': 'planned', 'description': 'beta v2'}}}])
            self.assertEqual(2, s.current_plan(state, 'p')['revision'])
            self.assertEqual(begin_adoption, s.version(state, 'a')['plan_adoptions'])
            self.assertEqual({'id': 'p', 'revision': 1},
                             s.version(state, 'r')['plan_usage']['sections']['beta']['plan'])

            state = update(state, [{'op': 'adopt_plan', 'id': 'a', 'plan': {'id': 'p', 'revision': 2},
                                    'scope': ['beta'], 'basis': ['SYN:beta-rework']}],
                           basis=['SYN:adopt-beta'])
            adopted = s.version(state, 'a')['plan_adoptions'][-1]
            self.assertEqual({'id': 'p', 'revision': 2}, adopted['plan'])
            self.assertEqual(['beta'], adopted['scope'])
            self.assertEqual(['SYN:beta-rework'], adopted['basis'])
            self.assertEqual(state['head'], adopted['change'])
            self.assertEqual({'id': 'p', 'revision': 1}, s.version(state, 'a')['plan'])
            sections = s.plan_sections(state, 'a')
            self.assertEqual(2, sections['beta']['plan']['revision'])
            self.assertEqual(1, sections['alpha']['plan']['revision'])

            state = update(state, [
                {'op': 'produce', 'id': 'q', 'attempt': 'a', 'parts': ['beta-part'],
                 'dimensions': dict(DRAFT), 'location': 'synthetic workspace',
                 'nature': 'synthetic', 'plan_scope': ['beta']},
                {'op': 'produce', 'id': 'q-alpha', 'attempt': 'a', 'parts': ['alpha-part'],
                 'dimensions': dict(DRAFT), 'location': 'synthetic workspace',
                 'nature': 'synthetic', 'plan_scope': ['alpha']},
                {'op': 'produce', 'id': 'q-mixed', 'attempt': 'a', 'parts': ['both-parts'],
                 'dimensions': dict(DRAFT), 'location': 'synthetic workspace',
                 'nature': 'synthetic', 'plan_scope': ['alpha', 'beta']}])
            self.assertEqual({'id': 'p', 'revision': 2},
                             s.version(state, 'q')['plan_usage']['sections']['beta']['plan'])
            self.assertEqual('explicit_scope', s.version(state, 'q')['plan_usage']['mode'])
            self.assertNotIn('plan', s.version(state, 'q'))
            self.assertEqual({'id': 'p', 'revision': 1}, s.version(state, 'q')['initial_plan'])
            self.assertEqual(1, s.version(state, 'q-alpha')['plan_usage']['sections']['alpha']['plan']['revision'])
            mixed = s.version(state, 'q-mixed')['plan_usage']['sections']
            self.assertEqual(1, mixed['alpha']['plan']['revision'])
            self.assertEqual(2, mixed['beta']['plan']['revision'])

            omitted = s.apply(state, [
                {'op': 'produce', 'id': 'q-legacy', 'attempt': 'a', 'parts': ['legacy-part'],
                 'dimensions': dict(DRAFT), 'location': 'synthetic workspace', 'nature': 'synthetic'}],
                state['head'], ['SYN:test'])
            self.assertEqual('rejected', omitted['status'])
            self.assertEqual(state, omitted['state'])
            self.assertIn('explicit plan scope required after explicit adoption', omitted['error'])

            state = update(state, [
                {'op': 'adopt_plan', 'id': 'a', 'plan': {'id': 'p', 'revision': 1},
                 'scope': ['beta'], 'basis': ['SYN:continue-p1']},
                {'op': 'produce', 'id': 'q-old', 'attempt': 'a', 'parts': ['old-part'],
                 'dimensions': dict(DRAFT), 'location': 'synthetic workspace',
                 'nature': 'synthetic', 'plan_scope': ['beta']}])
            old = s.version(state, 'q-old')
            self.assertEqual('explicit_scope', old['plan_usage']['mode'])
            self.assertEqual(1, old['plan_usage']['sections']['beta']['plan']['revision'])
            self.assertEqual({'id': 'p', 'revision': 1}, old['initial_plan'])
            self.assertNotIn('plan', old)
            self.assertEqual({'id': 'p', 'revision': 1}, s.plan_sections(state, 'a')['beta']['plan'])

            self.assertEqual(r_before, s.version(state, 'r'))
            self.assertEqual(report_before, s.version(state, 'r-report'))
            self.assertEqual(1, s.version(state, 'r')['revision'])
            self.assertEqual(begin_adoption, s.version(state, 'a', 1)['plan_adoptions'])

    def test_adoption_rejects_unadopted_scope_and_other_goal_plan(self):
        state = chain()
        state = update(state, [
            {'op': 'change_plan', 'id': 'p', 'edits': {'beta': {'status': 'planned', 'description': 'beta v2'}}},
            {'op': 'goal', 'id': 'other', 'scope': ['gamma']},
            {'op': 'begin', 'id': 'other-owner', 'goal': 'other', 'scope': ['gamma']},
            {'op': 'plan', 'id': 'other-plan', 'owner': 'other-owner',
             'sections': {'gamma': {'status': 'planned', 'description': 'gamma v1'}}}])
        before = deepcopy(state)
        for action in [
            {'op': 'adopt_plan', 'id': 'a', 'plan': {'id': 'p', 'revision': 2},
             'scope': ['missing'], 'basis': ['SYN:x']},
            {'op': 'adopt_plan', 'id': 'a', 'plan': {'id': 'other-plan', 'revision': 1},
             'scope': ['gamma'], 'basis': ['SYN:x']},
            {'op': 'adopt_plan', 'id': 'a', 'plan': {'id': 'p', 'revision': 1},
             'scope': ['beta'], 'basis': []},
            {'op': 'produce', 'id': 'bad', 'attempt': 'a', 'parts': ['x'], 'dimensions': dict(DRAFT),
             'location': 'x', 'nature': 'synthetic', 'plan_scope': ['missing']}]:
            result = s.apply(state, [action], state['head'], ['SYN:test'])
            self.assertEqual('rejected', result['status'])
            self.assertEqual(before, result['state'])
        self.assertEqual(1, len(s.version(state, 'a')['plan_adoptions']))

    def test_batch_rolls_back_adoption_and_product_together(self):
        state = chain()
        state = update(state, [{'op': 'change_plan', 'id': 'p',
                                'edits': {'beta': {'status': 'planned', 'description': 'beta v2'}}}])
        before = deepcopy(state)
        result = s.apply(state, [
            {'op': 'adopt_plan', 'id': 'a', 'plan': {'id': 'p', 'revision': 2},
             'scope': ['beta'], 'basis': ['SYN:x']},
            {'op': 'produce', 'id': 'q', 'attempt': 'a', 'parts': ['x'], 'dimensions': dict(DRAFT),
             'location': 'x', 'nature': 'synthetic', 'plan_scope': ['alpha', 'missing']}],
            state['head'], ['SYN:test'])
        self.assertEqual('rejected', result['status'])
        self.assertEqual(before, result['state'])
        self.assertEqual(before, state)
        self.assertEqual(state['head'], len(state['changes']))
        self.assertEqual(1, len(s.version(state, 'a')['plan_adoptions']))
        self.assertNotIn('q', state['objects'])


class ReferenceTests(unittest.TestCase):
    def test_exact_revision_rejects_none_bool_zero_and_missing_but_query_keeps_current(self):
        state = chain()
        self.assertEqual(1, s.version(state, 'p')['revision'])
        self.assertEqual(1, s.version(state, 'p', 1)['revision'])
        for bad in (None, True, False, 0, -1, 99, '1', 1.0):
            with self.assertRaises(ValueError):
                s.ref(state, {'id': 'p', 'revision': bad})
        for action in [
            {'op': 'adopt_plan', 'id': 'a', 'plan': {'id': 'p', 'revision': None},
             'scope': ['alpha'], 'basis': ['SYN:x']},
            {'op': 'report', 'id': 'bad-report', 'subject': {'id': 'p', 'revision': True},
             'scope': 'x', 'findings': ['x'], 'nature': 'synthetic'},
            {'op': 'begin', 'id': 'bad-attempt', 'goal': 'g', 'scope': ['x'],
             'plan': {'id': 'p', 'revision': 0}}]:
            result = s.apply(state, [action], state['head'], ['SYN:test'])
            self.assertEqual('rejected', result['status'])
            self.assertEqual(state, result['state'])


class LifecycleTests(unittest.TestCase):
    def test_end_requires_disclosure_then_reopen_is_explicit(self):
        for placement in ['independent', 'embedded']:
            state = chain(placement)
            result = s.apply(state, [{'op': 'end', 'id': 'a', 'outcome': 'synthetic stop'}],
                             state['head'], ['SYN:test'])
            self.assertEqual('rejected', result['status'])
            result = s.apply(state, [{'op': 'end', 'id': 'a', 'outcome': 'synthetic stop',
                                      'remaining': 'silently_done'}], state['head'], ['SYN:test'])
            self.assertEqual('rejected', result['status'])
            state = update(state, [{'op': 'end', 'id': 'a', 'outcome': 'synthetic stop',
                                    'remaining': 'retained_unresolved'}])
            self.assertEqual('retained_unresolved', s.version(state, 'a')['remaining_responsibility'])
            for action in [
                {'op': 'produce', 'id': 'blocked', 'attempt': 'a', 'parts': ['x'],
                 'dimensions': dict(DRAFT), 'location': 'x', 'nature': 'synthetic'},
                {'op': 'adopt_plan', 'id': 'a', 'plan': {'id': 'p', 'revision': 1},
                 'scope': ['alpha'], 'basis': ['SYN:x']},
                {'op': 'assign', 'token': 'alpha', 'to': 'a'}]:
                result = s.apply(state, [action], state['head'], ['SYN:test'])
                self.assertEqual('rejected', result['status'], action['op'])
                self.assertEqual(state, result['state'])
            state = update(state, [{'op': 'transfer', 'token': 'beta', 'from': 'a', 'to': 'b'}])
            self.assertEqual({'state': 'assigned', 'holders': ['b']},
                             responsibility.project(state['responsibility'])['beta'])
            ended_ref = s.actual_ref(state, 'a')
            state = update(state, [{'op': 'reopen', 'id': 'a'}])
            reopened = s.version(state, 'a')
            self.assertEqual('active', reopened['status'])
            self.assertEqual('unknown', reopened['outcome'])
            self.assertEqual('synthetic stop', reopened['reopen_history'][0]['prior_outcome'])
            self.assertEqual('retained_unresolved', reopened['reopen_history'][0]['remaining'])
            self.assertEqual(state['head'], reopened['reopen_history'][0]['change'])
            self.assertEqual('ended', s.version(state, 'a', ended_ref['revision'])['status'])
            state = update(state, [{'op': 'assign', 'token': 'alpha', 'to': 'a'}])
            self.assertEqual({'state': 'assigned', 'holders': ['a']},
                             responsibility.project(state['responsibility'])['alpha'])
            result = s.apply(state, [{'op': 'reopen', 'id': 'a'}], state['head'], ['SYN:test'])
            self.assertEqual('rejected', result['status'])

    def test_new_holders_must_be_active_in_all_three_layouts(self):
        for layout in ['parent', 'relation', 'child']:
            state = s.fresh(layout)
            state = update(state, [
                {'op': 'goal', 'id': 'g', 'scope': ['X', 'Y', 'Z']},
                {'op': 'begin', 'id': 'p', 'goal': 'g', 'scope': ['X', 'Y', 'Z']},
                {'op': 'begin', 'id': 'c1', 'goal': 'g', 'scope': ['X', 'Y']},
                {'op': 'begin', 'id': 'c2', 'goal': 'g', 'scope': ['X']},
                {'op': 'responsibility_init', 'owner': 'p', 'tokens': ['X', 'Y', 'Z'],
                 'holders': ['c1', 'c2']},
                {'op': 'assign', 'token': 'X', 'to': 'c1'},
                {'op': 'assign', 'token': 'Y', 'to': 'c2'}])
            state = update(state, [{'op': 'end', 'id': 'c1', 'outcome': 'stop',
                                    'remaining': 'retained_unresolved'}])
            state = update(state, [{'op': 'share', 'token': 'X', 'holders': ['c1', 'c2']}])
            self.assertEqual({'state': 'shared', 'holders': ['c1', 'c2']},
                             responsibility.project(state['responsibility'])['X'])
            for action in [
                {'op': 'assign', 'token': 'Z', 'to': 'c1'},
                {'op': 'share', 'token': 'Y', 'holders': ['c2', 'c1']},
                {'op': 'transfer', 'token': 'Y', 'from': 'c2', 'to': 'c1'}]:
                result = s.apply(state, [action], state['head'], ['SYN:test'])
                self.assertEqual('rejected', result['status'], (layout, action['op']))
                self.assertEqual(state, result['state'])
            state = update(state, [{'op': 'reopen', 'id': 'c1'},
                                   {'op': 'assign', 'token': 'Z', 'to': 'c1'}])
            self.assertEqual({'state': 'assigned', 'holders': ['c1']},
                             responsibility.project(state['responsibility'])['Z'])

    def test_ended_attempt_cannot_join_initial_responsibility(self):
        state = s.fresh()
        state = update(state, [
            {'op': 'goal', 'id': 'g', 'scope': ['X']},
            {'op': 'begin', 'id': 'p', 'goal': 'g', 'scope': ['X']},
            {'op': 'begin', 'id': 'c', 'goal': 'g', 'scope': ['X']},
            {'op': 'end', 'id': 'c', 'outcome': 'done'}])
        result = s.apply(state, [{'op': 'responsibility_init', 'owner': 'p', 'tokens': ['X'],
                                  'holders': ['c']}], state['head'], ['SYN:test'])
        self.assertEqual('rejected', result['status'])
        self.assertIsNone(state['responsibility'])


class ProductAndAcceptanceTests(unittest.TestCase):
    def test_advance_product_values_are_controlled_and_regression_is_legal(self):
        state = chain()
        state = update(state, [
            {'op': 'advance_product', 'id': 'r', 'dimensions': {'git': 'reported_committed'}},
            {'op': 'advance_product', 'id': 'r', 'dimensions': {'git': 'unstaged'}}])
        self.assertEqual('unstaged', s.version(state, 'r')['dimensions']['git'])
        self.assertEqual('reported_draft_written', s.version(state, 'r')['dimensions']['implementation'])
        for bad in ({'git': ['unstaged']}, {'git': {'state': 'unstaged'}}, {'completion': 3},
                    {'implementation': 'made up'}, {'acceptance': 'accepted'}, {}):
            result = s.apply(state, [{'op': 'advance_product', 'id': 'r', 'dimensions': bad}],
                             state['head'], ['SYN:test'])
            self.assertEqual('rejected', result['status'], bad)
            self.assertEqual(state, result['state'])
        self.assertEqual(1, s.version(state, 'r', 1)['revision'])

    def test_acceptance_needs_evidence_traceable_to_the_same_goal(self):
        state = chain()
        state = update(state, [
            {'op': 'report', 'id': 'goal-report', 'subject': {'id': 'g', 'revision': 1},
             'scope': 'goal describes itself', 'findings': ['self description'], 'nature': 'synthetic'}])
        for evidence in ([s.actual_ref(state, 'g')],
                         [s.actual_ref(state, 'r')],
                         [s.actual_ref(state, 'goal-report')]):
            result = s.apply(state, [acceptance(evidence)], state['head'], ['SYN:test'])
            self.assertEqual('rejected', result['status'])
            self.assertEqual(state, result['state'])
        result = s.apply(state, [{'op': 'report', 'id': 'blank-scope',
                                  'subject': s.actual_ref(state, 'r'), 'scope': '   ',
                                  'findings': ['x'], 'nature': 'synthetic'}],
                         state['head'], ['SYN:test'])
        self.assertEqual('rejected', result['status'])
        state = update(state, [
            {'op': 'goal', 'id': 'other', 'scope': ['gamma']},
            {'op': 'begin', 'id': 'other-attempt', 'goal': 'other', 'scope': ['gamma']},
            {'op': 'produce', 'id': 'other-product', 'attempt': 'other-attempt', 'parts': ['gamma-part'],
             'dimensions': dict(DRAFT), 'location': 'other workspace', 'nature': 'synthetic'},
            {'op': 'report', 'id': 'other-report', 'subject': {'id': 'other-product', 'revision': 1},
             'scope': 'gamma only', 'findings': ['other goal'], 'nature': 'synthetic'}])
        result = s.apply(state, [acceptance([s.actual_ref(state, 'other-report')])],
                         state['head'], ['SYN:test'])
        self.assertEqual('rejected', result['status'])
        state = update(state, [{'op': 'advance_product', 'id': 'r',
                                'dimensions': {'completion': 'reported_migration_complete'}}])
        state = update(state, [acceptance([s.actual_ref(state, 'r-report')])])
        goal = s.version(state, 'g')
        self.assertEqual('accepted', goal['acceptance'])
        self.assertEqual([{'id': 'r-report', 'revision': 1}], goal['decision']['evidence'])
        self.assertEqual('draft only', s.version(state, 'r-report')['findings'][0])
        self.assertEqual(1, s.version(state, 'r-report')['revision'])


class PlanAuthorityTests(unittest.TestCase):
    def test_plan_usage_is_single_authority_and_initial_plan_is_separate(self):
        state = chain()
        state = update(state, [
            {'op': 'change_plan', 'id': 'p', 'edits': {'beta': {'status': 'planned',
                                                                'description': 'beta v2'}}},
            {'op': 'adopt_plan', 'id': 'a', 'plan': {'id': 'p', 'revision': 2},
             'scope': ['beta'], 'basis': ['SYN:beta-rework']},
            {'op': 'produce', 'id': 'x', 'attempt': 'a', 'parts': ['beta-part'],
             'dimensions': dict(DRAFT), 'location': 'synthetic workspace',
             'nature': 'synthetic', 'plan_scope': ['beta']}])
        product = s.version(state, 'x')
        self.assertEqual({'id': 'p', 'revision': 2},
                         product['plan_usage']['sections']['beta']['plan'])
        self.assertEqual({'id': 'p', 'revision': 1}, product['initial_plan'])
        self.assertNotIn('plan', product)
        legacy_product = s.version(state, 'r')
        self.assertEqual(legacy_product['initial_plan'], legacy_product['plan'])
        self.assertEqual('legacy_initial_plan', legacy_product['plan_usage']['mode'])
        view = s.readback(state)
        self.assertEqual({'id': 'p', 'revision': 2},
                         view['product_plan_usage']['x']['sections']['beta']['plan'])
        self.assertEqual({'id': 'p', 'revision': 1}, view['product_initial_plan']['x'])
        self.assertNotIn('x', view['product_legacy_plan_projection'])
        self.assertIn('r', view['product_legacy_plan_projection'])

    def test_initial_plan_projection_alone_does_not_authorize_an_explicit_result(self):
        state = chain()
        state = update(state, [
            {'op': 'change_plan', 'id': 'p', 'edits': {'beta': {'status': 'planned',
                                                                'description': 'beta v2'}}},
            {'op': 'adopt_plan', 'id': 'a', 'plan': {'id': 'p', 'revision': 2},
             'scope': ['beta'], 'basis': ['SYN:beta-rework']}])
        before = deepcopy(state)
        result = s.apply(state, [
            {'op': 'produce', 'id': 'x', 'attempt': 'a', 'parts': ['beta-part'],
             'dimensions': dict(DRAFT), 'location': 'synthetic workspace',
             'nature': 'synthetic'}], state['head'], ['SYN:test'])
        self.assertEqual('rejected', result['status'])
        self.assertEqual(before, result['state'])
        self.assertIn('explicit plan scope required', result['error'])


class S029MappingTests(unittest.TestCase):
    def test_item_status_scope_and_partial_reuse_are_queryable(self):
        state = s.real_path()
        view = s.s029_items(state)['items']
        committed = ['1', '2', '3', '4A', '4B', '5', '9permission']
        drafts = ['6', '7', '8', '9context', '10', '11']
        for item_id in committed:
            item = view[item_id]
            self.assertEqual('independent-code', item['product'])
            self.assertEqual('reported_committed', item['status']['git'])
            self.assertEqual('reported_committed', item['current']['dimensions']['git'])
            self.assertTrue(item['current']['matches_source_status'])
            self.assertTrue(item['scope'])
        for item_id in drafts:
            item = view[item_id]
            self.assertEqual('draft-code', item['product'])
            self.assertEqual('unstaged', item['status']['git'])
            self.assertEqual('incomplete', item['current']['dimensions']['completion'])
            self.assertTrue(item['current']['matches_source_status'])
        self.assertEqual('9_permission_system_hiding', view['9permission']['part'])
        self.assertEqual('9_context_hiding', view['9context']['part'])
        self.assertNotEqual(view['4A']['part'], view['4B']['part'])
        self.assertEqual('latestCompletedParagraphFirstLine', view['5']['reuse']['symbol'])
        self.assertEqual('S029.reuse', view['5']['reuse']['basis'])
        self.assertEqual('documented_status', view['5']['nature'])

    def test_context_dependency_is_typed_bidirectional_and_not_completion(self):
        state = s.real_path()
        context = s.relations_for_item(state, '9context')
        self.assertEqual([{'object': 'draft-code', 'scope': '9_context_hiding'}], [context['endpoint']])
        self.assertEqual([('S029.dep.9context-on-8', 'outgoing')],
                         [(row['relation'], row['direction']) for row in context['relations']])
        notifications = s.relations_for_item(state, '8')
        self.assertEqual(
            [('S029.dep.8-on-turn-inputs', 'outgoing'),
             ('S029.dep.9context-on-8', 'incoming')],
            [(row['relation'], row['direction']) for row in notifications['relations']])
        turn_inputs = s.relations_for(state, 'turnstep', 'Turn starts and Inbox claims')
        self.assertEqual([('S029.dep.8-on-turn-inputs', 'incoming')],
                         [(row['relation'], row['direction']) for row in turn_inputs])
        relation = state['relations']['S029.dep.9context-on-8']
        self.assertEqual({'object': 'draft-code', 'scope': '9_context_hiding'}, relation['from'])
        self.assertEqual({'object': 'draft-code', 'scope': '8_trigger_notifications'}, relation['to'])
        self.assertEqual(['S029.dependency'], relation['basis'])
        self.assertEqual('documented_requirement', relation['nature'])
        self.assertEqual('incomplete', s.s029_items(state)['items']['8']['status']['completion'])
        self.assertEqual('incomplete', s.s029_items(state)['items']['9context']['status']['completion'])
        self.assertEqual('pending', s.version(state, 'goal')['acceptance'])
        self.assertEqual('present', s.version(state, 'draft-code')['parts']['8_trigger_notifications'])
        self.assertEqual('present', s.version(state, 'draft-code')['parts']['9_context_hiding'])


if __name__ == '__main__':
    unittest.main()
