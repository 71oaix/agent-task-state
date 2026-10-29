"""Execute the continuous export functions and keep the first core-v1 evidence."""
from pathlib import Path
import tempfile
import unittest
import t12_continuous as c


def setUpModule():
    if not c.CORE_DIR.exists():
        c.export_core(c.CORE_DIR)


def _walk_keys(value):
    if isinstance(value, dict):
        for key, child in value.items():
            yield key
            yield from _walk_keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_keys(child)


class CoreEvidenceTests(unittest.TestCase):
    def test_core_v1_was_written_by_the_export_function_and_is_not_overwritten(self):
        for name in ('trace.json', 'checks.json', 'readback.json', 'operations.md', 'manifest.json'):
            self.assertTrue((c.CORE_DIR / name).is_file(), name)
        self.assertTrue(c.verify_core(c.CORE_DIR))
        before = sorted(path.name for path in c.CORE_DIR.iterdir())
        with self.assertRaises(FileExistsError):
            c.export_core(c.CORE_DIR)
        self.assertEqual(before, sorted(path.name for path in c.CORE_DIR.iterdir()))

    def test_export_refuses_an_existing_directory_in_a_temporary_location(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'already-here'
            target.mkdir()
            with self.assertRaises(FileExistsError):
                c.export_core(target)


class TraceTests(unittest.TestCase):
    def test_trace_shows_real_anchors_and_a_separate_synthetic_chain(self):
        trace = c.build_trace()
        historical = trace['historical']['steps']
        self.assertEqual(
            ['T12.01', 'T12.02', 'T12.03', 'T12.04', 'T12.05', 'T12.06',
             'S029.dependency', 'S028.partial_replacement'],
            [step['basis'][0] for step in historical])
        for step in historical:
            self.assertEqual('source_record', step['nature'])
            for field in ('actions', 'before', 'after', 'changed_paths', 'exact_references', 'observations'):
                self.assertIn(field, step)
        synthetic = trace['synthetic']['steps']
        self.assertEqual(trace['historical']['final_head'], trace['synthetic']['starts_from_change'])
        self.assertEqual(['plan-v2', 'adopt-v2', 'produce-v2', 'report-v2', 'accept-v2',
                          'adopt-p1', 'produce-p1', 'regress-v2', 'assign-responsibility',
                          'end-turnstep', 'reopen-turnstep'],
                         [step['label'] for step in synthetic])
        for step in synthetic:
            self.assertEqual('synthetic', step['nature'])
            self.assertTrue(step['basis'][0].startswith('SYN:'))
            self.assertIn('change', step)
        produce_v2 = next(step for step in synthetic if step['label'] == 'produce-v2')
        observation = produce_v2['observations'][0]
        self.assertEqual({'id': 'migration-plan', 'revision': 2},
                         observation['plan_usage']['sections']['turnstep']['plan'])
        self.assertEqual({'id': 'migration-plan', 'revision': 1}, observation['initial_plan'])
        self.assertFalse(observation['legacy_plan_present'])
        produce_p1 = next(step for step in synthetic if step['label'] == 'produce-p1')
        self.assertEqual({'id': 'migration-plan', 'revision': 1},
                         produce_p1['observations'][-1]['plan_usage']['sections']['turnstep']['plan'])
        self.assertIn('T12.04', [step['basis'][0] for step in historical if step['change'] == 4])

    def test_trace_keeps_exact_old_references_per_step(self):
        trace = c.build_trace()
        report = next(step for step in trace['historical']['steps']
                      if step['actions'][0]['op'] == 'report' and step['actions'][0]['id'] == 'channel-checks')
        self.assertEqual({'id': 'independent', 'revision': 1},
                         report['actions'][0]['subject'])
        self.assertIn('independent@1', report['exact_references'])
        self.assertEqual('active', report['exact_references']['independent@1']['status'])


class ChecksTests(unittest.TestCase):
    def test_checks_store_literal_inputs_outputs_and_errors(self):
        checks = c.build_checks()['cases']
        by_id = {case['id']: case for case in checks}
        for case in checks:
            self.assertIn('input', case)
            self.assertIn('output', case)
            if case['kind'] != 'query':
                self.assertIn('actions', case['input'])
                self.assertIn('status', case['output'])
                self.assertIn('state_after', case['output'])
            if case['output'].get('status') == 'rejected':
                self.assertTrue(case['output']['error'])
                self.assertTrue(case['unchanged_on_rejection'])
        self.assertIn('explicit plan scope required after explicit adoption',
                      by_id['omit-scope-after-adoption']['output']['error'])
        self.assertEqual('rejected', by_id['unadopted-scope']['output']['status'])
        self.assertEqual('rejected', by_id['other-goal-plan']['output']['status'])
        self.assertEqual('rejected', by_id['atomic-batch']['output']['status'])
        self.assertFalse(by_id['atomic-batch']['output']['observation']['has_product'])
        single = by_id['explicit-single-p2']['output']['observation']
        self.assertEqual({'id': 'migration-plan', 'revision': 2},
                         single['plan_usage']['sections']['turnstep']['plan'])
        self.assertEqual({'id': 'migration-plan', 'revision': 1}, single['initial_plan'])
        self.assertFalse(single['legacy_plan_present'])
        mixed = by_id['explicit-mixed-versions']['output']['observation']['plan_usage']['sections']
        self.assertEqual(1, mixed['channel']['plan']['revision'])
        self.assertEqual(2, mixed['turnstep']['plan']['revision'])
        old = by_id['explicit-old-version']['output']['observation']
        self.assertEqual(1, old['plan_usage']['sections']['turnstep']['plan']['revision'])
        self.assertTrue(by_id['legacy-no-explicit-scope']['output']['observation']['legacy_plan_present'])
        relations = by_id['relation-both-ends']['output']
        self.assertEqual('S029.dep.9context-on-8',
                         relations['9context']['relations'][0]['relation'])
        self.assertEqual([('S029.dep.8-on-turn-inputs', 'outgoing'),
                          ('S029.dep.9context-on-8', 'incoming')],
                         [(row['relation'], row['direction']) for row in relations['8']['relations']])
        self.assertEqual('latestCompletedParagraphFirstLine',
                         by_id['s029-items']['output']['items']['5']['reuse']['symbol'])
        self.assertEqual('incomplete',
                         by_id['s029-items']['output']['items']['9context']['status']['completion'])
        self.assertEqual('reported_committed',
                         by_id['s029-items']['output']['items']['9permission']['status']['git'])


class ReadbackTests(unittest.TestCase):
    def test_readback_is_a_representation_without_truth_answers_or_recommendations(self):
        readback = c.build_readback()
        for key in ('historical', 'synthetic', 'operations', 'query_questions'):
            self.assertIn(key, readback)
        forbidden = {'answer', 'answers', 'expected_answer', 'truth', 'recommendation'}
        keys = {key.lower() for key in _walk_keys(readback)}
        self.assertFalse(keys & forbidden, 'unexpected answer keys: ' + str(keys & forbidden))
        historical = readback['historical']
        self.assertEqual('migration-plan',
                         historical['product_plan_usage']['independent-code']['sections']['channel']['plan']['id'])
        self.assertIn('independent-code', historical['product_legacy_plan_projection'])
        self.assertIn('architecture@1', historical['historical_plans'])
        self.assertEqual('latestCompletedParagraphFirstLine',
                         historical['items']['items']['5']['reuse']['symbol'])
        self.assertEqual(['S029.dependency'],
                         historical['relations']['S029.dep.9context-on-8']['basis'])
        self.assertTrue(historical['relation_index'])
        self.assertEqual('pending', historical['objects']['goal']['acceptance'])
        self.assertIn('no expected answers', readback['representation_note'])
        self.assertIn('plan_usage', c.build_operations())
        self.assertIn('不表示任一端已完成', c.build_operations())

    def test_manifest_declares_generation_history_and_synthetic_boundary(self):
        manifest = c.build_manifest()
        self.assertEqual(c.BASELINE_HEAD, manifest['baseline_head'])
        self.assertEqual('test_t12_export.py under unittest discovery',
                         manifest['generated_by']['driver'])
        self.assertFalse(manifest['generated_by']['cli_executed_in_this_slice'])
        self.assertGreaterEqual(manifest['history']['historical_steps'], 7)
        self.assertGreaterEqual(manifest['history']['synthetic_steps'], 9)
        self.assertTrue(manifest['synthetic_boundary']['not_dsh_events'])
        self.assertTrue(manifest['synthetic_boundary']['no_event_times'])
        self.assertIn('unknown', manifest['model_call_note'])
        self.assertIn('No four identity replacements', manifest['scope_limit'])
        self.assertIn('core-v1', manifest['anti_overwrite'])


if __name__ == '__main__':
    unittest.main()
