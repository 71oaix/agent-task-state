"""Boundary checks for T12 part progress, T03 plans, T13 correction, T15 dependencies."""
import json
import unittest

import t12_boundary_checks as b
import t12_study as s


def setUpModule():
    if not b.BOUNDARY_DIR.exists():
        b.export_boundary(b.BOUNDARY_DIR)


def _walk_keys(value):
    if isinstance(value, dict):
        for key, child in value.items():
            yield key
            yield from _walk_keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_keys(child)


class EvidenceTests(unittest.TestCase):
    def test_boundary_v1_was_written_by_the_export_and_is_not_overwritten(self):
        for name in ('results.json', 'readback.json', 'rules.md'):
            self.assertTrue((b.BOUNDARY_DIR / name).is_file(), name)
        self.assertTrue(b.verify_boundary(b.BOUNDARY_DIR))
        before = sorted(path.name for path in b.BOUNDARY_DIR.iterdir())
        with self.assertRaises(FileExistsError):
            b.export_boundary(b.BOUNDARY_DIR)
        self.assertEqual(before, sorted(path.name for path in b.BOUNDARY_DIR.iterdir()))

    def test_results_record_every_check_without_unexpected_failures(self):
        results = b.build_results()
        self.assertTrue(results['summary']['ok'], results['summary']['failed'])
        self.assertEqual([], results['summary']['failed'])
        self.assertEqual(4, len(results['cases']))
        for case in results['cases']:
            self.assertTrue(case['checks'], case['id'])
            self.assertIn('raw_failure', case)
            self.assertIn('records', case)
            for check in case['checks']:
                self.assertTrue(check['ok'], (case['id'], check['id'], check['observed']))

    def test_readback_contains_no_answers_scores_or_pass_labels(self):
        saved = json.loads((b.BOUNDARY_DIR / 'readback.json').read_text(encoding='utf-8'))
        forbidden = {'answer', 'answers', 'expected_answer', 'truth', 'verdict',
                     'pass', 'passed', 'fail', 'failed', 'score', 'expected'}
        keys = {key.lower() for key in _walk_keys(saved)}
        self.assertFalse(keys & forbidden, str(keys & forbidden))
        for key in ('operations', 'records', 'evidence', 'questions', 'synthetic_boundary'):
            self.assertIn(key, saved)
        self.assertIn('no expected answers', saved['representation_note'])
        self.assertTrue(any(row['kind'] == 'raw_failure' for row in saved['records']))
        self.assertTrue(any(row.get('label') == 'notification-part-progress'
                            for row in saved['records']))

    def test_source_fixture_keeps_only_real_facts_and_urls(self):
        ids = [fact['id'] for fact in b.FIXTURE['facts']]
        self.assertEqual(sorted(ids), sorted(set(ids)))
        for fact in b.FIXTURE['facts']:
            self.assertIn(fact['id'].split('.')[0], {'T03', 'T13', 'T15'})
            self.assertTrue(fact['meaning'])
        self.assertEqual({'T13.01', 'T13.02', 'T13.03', 'T13.04', 'T13.05'},
                         {fact['id'] for fact in b.FIXTURE['facts']
                          if fact['id'].startswith('T13.')})
        for sid, source in b.FIXTURE['sources'].items():
            self.assertIn(source['revision'], source['url'])
        self.assertNotIn('synthetic', json.dumps(b.FIXTURE['facts']).lower())

    def test_real_and_synthetic_changes_are_labelled_separately(self):
        results = b.build_results()
        for case in results['cases']:
            for record in case['records']:
                self.assertIn(record['input']['nature'], {'source_record', 'synthetic'})
                if record['input']['nature'] == 'synthetic':
                    self.assertTrue(record['input']['basis'][0].startswith('SYN:'))
                else:
                    self.assertFalse(record['input']['basis'][0].startswith('SYN:'))


class CorePreservationTests(unittest.TestCase):
    def test_old_core_state_has_no_part_authority_and_old_projection_shape(self):
        state = s.real_path()
        self.assertNotIn('part_states', s.version(state, 'draft-code'))
        row = s.s029_items(state)['items']['9context']['current']
        self.assertEqual({'product_revision', 'part_state', 'dimensions', 'matches_source_status'}, set(row))
        self.assertEqual('present', row['part_state'])
        self.assertEqual(set(s.readback(state)), {
            'objects', 'plan_records', 'responsibility_view', 'history', 'unknowns',
            'identity_origin', 'source_index', 'fact_index', 'plan_usage',
            'attempt_initial_plan', 'plan_adoptions', 'adopted_plan_sections',
            'product_plan_usage', 'product_initial_plan', 'product_legacy_plan_projection',
            'historical_plans', 'items', 'relations', 'relation_index', 'reading_rules'})

    def test_old_product_advance_still_updates_shared_dimensions(self):
        state = s.real_path()
        result = s.apply(state, [{'op': 'advance_product', 'id': 'draft-code',
                                  'dimensions': {'git': 'reported_committed'}}],
                         state['head'], ['SYN:test'])
        self.assertEqual('applied', result['status'], result['error'])
        updated = s.version(result['state'], 'draft-code')
        self.assertEqual('reported_committed', updated['dimensions']['git'])
        self.assertNotIn('part_states', updated)
        self.assertEqual('reported_committed', s.s029_items(result['state'])['items']['9context']['current']['dimensions']['git'])

    def test_part_update_leaves_old_report_other_product_and_goal_exact(self):
        state = s.real_path()
        report = s.version(state, 'channel-checks')
        other = s.version(state, 'independent-code')
        goal = s.version(state, 'goal')
        result = s.apply(state, [{'op': 'advance_parts', 'id': 'draft-code',
                                  'parts': ['8_trigger_notifications'],
                                  'dimensions': {'git': 'reported_committed'}}],
                         state['head'], ['SYN:test'])
        self.assertEqual('applied', result['status'], result['error'])
        self.assertEqual(report, s.version(result['state'], 'channel-checks'))
        self.assertEqual(other, s.version(result['state'], 'independent-code'))
        self.assertEqual(goal, s.version(result['state'], 'goal'))
        self.assertEqual(1, s.version(result['state'], 'channel-checks')['revision'])


class PartProgressTests(unittest.TestCase):
    def test_only_named_part_moves_and_old_revision_stays(self):
        state = s.real_path()
        old = s.version(state, 'draft-code')
        result = s.apply(state, [{'op': 'advance_parts', 'id': 'draft-code',
                                  'parts': ['8_trigger_notifications'],
                                  'dimensions': {'completion': 'reported_migration_complete',
                                                 'implementation': 'reported_code_written',
                                                 'git': 'reported_committed'}}],
                         state['head'], ['SYN:test'])
        self.assertEqual('applied', result['status'], result['error'])
        state = result['state']
        self.assertEqual(old, s.version(state, 'draft-code', 1))
        self.assertEqual('reported_migration_complete',
                         s.s029_items(state)['items']['8']['current']['dimensions']['completion'])
        self.assertEqual('incomplete',
                         s.s029_items(state)['items']['9context']['current']['dimensions']['completion'])
        self.assertEqual('unknown', s.version(state, 'draft-code')['dimensions']['completion'])
        progress = s.part_progress(state, 'draft-code')
        self.assertTrue(progress['subdivided'])
        self.assertEqual('unknown', progress['overall']['completion'])
        self.assertEqual('pending', s.version(state, 'goal')['acceptance'])

    def test_global_entry_rejects_ambiguous_range_and_accepts_full_range(self):
        state = s.real_path()
        state = s.apply(state, [{'op': 'advance_parts', 'id': 'draft-code',
                                 'parts': ['8_trigger_notifications'],
                                 'dimensions': {'git': 'reported_committed'}}],
                        state['head'], ['SYN:test'])['state']
        for action in ({'op': 'advance_product', 'id': 'draft-code',
                        'dimensions': {'git': 'reported_committed'}},
                       {'op': 'advance_product', 'id': 'draft-code', 'parts': ['9_context_hiding'],
                        'dimensions': {'git': 'reported_committed'}}):
            result = s.apply(state, [action], state['head'], ['SYN:test'])
            self.assertEqual('rejected', result['status'])
            self.assertEqual(state, result['state'])
        parts = sorted(s.version(state, 'draft-code')['part_states'])
        result = s.apply(state, [{'op': 'advance_product', 'id': 'draft-code', 'parts': parts,
                                  'dimensions': {'git': 'reported_committed'}}],
                         state['head'], ['SYN:test'])
        self.assertEqual('applied', result['status'], result['error'])
        self.assertEqual('reported_committed',
                         s.part_progress(result['state'], 'draft-code')['overall']['git'])


class PlanOwnerTests(unittest.TestCase):
    def test_goal_owned_plan_report_subject_does_not_accept(self):
        state = s.fresh()
        sections = {'stage1': {'status': 'draft_work_complete', 'description': 'one'}}
        result = s.apply(state, [
            {'op': 'goal', 'id': 'g', 'scope': ['rebuild']},
            {'op': 'plan', 'id': 'p', 'owner': 'g', 'sections': sections},
            {'op': 'report', 'id': 'plan-report', 'subject': {'id': 'p', 'revision': 1},
             'scope': 'stage status', 'findings': ['stage one draft'], 'nature': 'synthetic'}],
            state['head'], ['SYN:test'])
        self.assertEqual('applied', result['status'], result['error'])
        state = result['state']
        self.assertEqual('g', s.goal_of(state, s.version(state, 'p')))
        self.assertEqual('p', s.version(state, 'plan-report')['subject']['id'])
        self.assertEqual('pending', s.version(state, 'g')['acceptance'])
        rejected = s.apply(state, [{'op': 'accept_goal', 'id': 'g', 'actor_role': 'acceptor',
                                    'actor': 'reviewer', 'criteria': ['plan only'],
                                    'decision': 'accept', 'evidence': [s.actual_ref(state, 'plan-report')]}],
                           state['head'], ['SYN:test'])
        self.assertEqual('rejected', rejected['status'])

    def test_attempt_owned_plan_path_still_works(self):
        state = s.fresh()
        state = s.apply(state, [{'op': 'goal', 'id': 'g', 'scope': ['x']},
                                {'op': 'begin', 'id': 'a', 'goal': 'g', 'scope': ['x']}],
                        state['head'], ['SYN:test'])['state']
        result = s.apply(state, [{'op': 'plan', 'id': 'p', 'owner': 'a',
                                  'sections': {'s': {'status': 'planned', 'description': 'x'}}}],
                         state['head'], ['SYN:test'])
        self.assertEqual('applied', result['status'], result['error'])
        self.assertEqual('g', s.goal_of(result['state'], s.current_plan(result['state'], 'p')))

    def test_goal_owned_plan_also_works_with_embedded_placement(self):
        state = s.fresh('parent', 'embedded')
        sections = {'s': {'status': 'planned', 'description': 'x'}}
        result = s.apply(state, [
            {'op': 'goal', 'id': 'g', 'scope': ['x']},
            {'op': 'plan', 'id': 'p', 'owner': 'g', 'sections': sections},
            {'op': 'begin', 'id': 'a', 'goal': 'g', 'scope': ['x'],
             'plan': {'id': 'p', 'revision': 1}}],
            state['head'], ['SYN:test'])
        self.assertEqual('applied', result['status'], result['error'])
        state = result['state']
        self.assertEqual(sections, s.current_plan(state, 'p')['sections'])
        self.assertEqual('g', s.goal_of(state, s.version(state, 'a')))
        self.assertEqual({'id': 'p', 'revision': 1}, s.plan_sections(state, 'a')['s']['plan'])


class InterpretationTests(unittest.TestCase):
    def test_scope_correction_and_undetermined_outside(self):
        state, _ = b._t13_state()
        covered = s.interpretations(state, b.T13_SCOPES['correction'][0])
        outside = s.interpretations(state, b.T13_SCOPES['outside_correction'][0])
        broader = s.interpretations(state, b.T13_SCOPES['broader_not_supported'][0])
        self.assertEqual('corrected', covered['status'])
        self.assertEqual('t13-console-rewrite', covered['current']['evidence']['id'])
        self.assertEqual('t13-tail-delay', covered['history'][0]['evidence']['id'])
        self.assertEqual(['T13.02', 'T13.03'], covered['corrections'][0]['basis'])
        self.assertEqual('undetermined', outside['status'])
        self.assertIsNone(outside['current'])
        self.assertEqual('undetermined', broader['status'])
        self.assertEqual([], broader['history'])
        self.assertEqual(1, s.version(state, 't13-tail-delay')['revision'])

    def test_widening_and_report_correction_are_rejected(self):
        state, _ = b._t13_state()
        for action in (
                {'op': 'correct_interpretation', 'id': 'bad1',
                 'prior': s.actual_ref(state, 't13-tail-delay'), 'scope': 'all',
                 'scope_ids': b.T13_SCOPES['broader_not_supported'], 'findings': ['x'],
                 'basis': ['T13.02'], 'nature': 'synthetic'},
                {'op': 'correct_interpretation', 'id': 'bad2',
                 'prior': s.actual_ref(state, 't13-measurement'), 'scope': 'x',
                 'scope_ids': [b.T13_SCOPES['correction'][0]], 'findings': ['x'],
                 'basis': ['T13.02'], 'nature': 'synthetic'}):
            result = s.apply(state, [action], state['head'], ['SYN:test'])
            self.assertEqual('rejected', result['status'])
            self.assertEqual(state, result['state'])

    def test_widening_scope_is_rejected_before_any_correction_exists(self):
        state, _ = b._t13_state()
        before = s.at(state, 3)  # old interpretation and measurements exist; no correction yet
        result = s.apply(before, [{'op': 'correct_interpretation', 'id': 'bad-expand',
                                   'prior': s.actual_ref(before, 't13-tail-delay'),
                                   'scope': 'all delayed failures',
                                   'scope_ids': b.T13_SCOPES['broader_not_supported'],
                                   'findings': ['x'], 'basis': ['T13.02'],
                                   'nature': 'synthetic'}],
                         before['head'], ['SYN:test'])
        self.assertEqual('rejected', result['status'])
        self.assertIn('correction scope must stay inside', result['error'])
        self.assertEqual(before, result['state'])


class DeliveryDependencyTests(unittest.TestCase):
    def test_exact_relation_does_not_drift_and_never_declares_incompatibility(self):
        state, _ = b._t15_state()
        relation = state['relations']['T15.dep.harness-kit']
        self.assertEqual({'object': 't15-harness', 'revision': 1, 'scope': 'adapter'},
                         relation['from'])
        self.assertEqual({'name': 'libreoffice-kit-npm', 'version': 'unknown', 'digest': 'unknown'},
                         relation['external'])
        self.assertEqual('current', s.relation_status(state, 'T15.dep.harness-kit')['status'])
        result = s.apply(state, [{'op': 'advance_product', 'id': 't15-harness',
                                  'dimensions': {'implementation': 'reported_implemented'}}],
                         state['head'], ['SYN:test'])
        self.assertEqual('applied', result['status'], result['error'])
        state = result['state']
        self.assertEqual(relation, state['relations']['T15.dep.harness-kit'])
        status = s.relation_status(state, 'T15.dep.harness-kit')
        self.assertEqual('needs_recheck', status['status'])
        self.assertIsNone(status['automatic_compatibility_conclusion'])
        self.assertEqual('current', s.relation_status(state, 'T15.dep.desktop-kit')['status'])

    def test_old_product_requirement_relation_is_preserved(self):
        state = s.real_path()
        old = json.loads(json.dumps(state['relations']['S029.dep.9context-on-8']))
        result = s.apply(state, [{'op': 'advance_parts', 'id': 'draft-code',
                                  'parts': ['8_trigger_notifications'],
                                  'dimensions': {'git': 'reported_committed'}}],
                         state['head'], ['SYN:test'])
        self.assertEqual('applied', result['status'], result['error'])
        self.assertEqual(old, result['state']['relations']['S029.dep.9context-on-8'])
        self.assertEqual('needs_explicit_recheck',
                         s.relation_status(result['state'], 'S029.dep.9context-on-8')['status'])


if __name__ == '__main__':
    unittest.main()
