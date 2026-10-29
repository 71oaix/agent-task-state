"""Execute the four identity trials and keep the first identity-v1 evidence."""
from pathlib import Path
import json
import unittest
import t12_identity_trials as t


def setUpModule():
    if not t.IDENTITY_DIR.exists():
        t.export_identity(t.IDENTITY_DIR)


class EvidenceTests(unittest.TestCase):
    def test_identity_v1_was_written_by_the_export_function_and_is_not_overwritten(self):
        for name in ('results.json', 'review.md'):
            self.assertTrue((t.IDENTITY_DIR / name).is_file(), name)
        self.assertTrue(t.verify_identity(t.IDENTITY_DIR))
        before = sorted(path.name for path in t.IDENTITY_DIR.iterdir())
        with self.assertRaises(FileExistsError):
            t.export_identity(t.IDENTITY_DIR)
        self.assertEqual(before, sorted(path.name for path in t.IDENTITY_DIR.iterdir()))

    def test_results_file_is_the_executed_document(self):
        saved = json.loads((t.IDENTITY_DIR / 'results.json').read_text(encoding='utf-8'))
        self.assertEqual(sorted(saved['groups']), ['C1', 'C2', 'C3', 'C4'])
        self.assertEqual(t.CHAIN_LABELS, saved['common_chain'])
        self.assertTrue(saved['boundary']['no_final_recommendation'])


class ChainTests(unittest.TestCase):
    def setUp(self):
        self.results = t.build_results()

    def test_every_group_runs_the_whole_chain_in_both_storages(self):
        for gid, group in self.results['groups'].items():
            for mode in ('A', 'B'):
                chain = group[mode]['chain']
                self.assertEqual(t.CHAIN_LABELS, [step['label'] for step in chain], (gid, mode))
                for step in chain:
                    self.assertTrue(step['accepted'], (gid, mode, step['label']))
                    self.assertTrue(step['changed_paths'], (gid, mode, step['label']))
                    self.assertIn('observations', step)
                    self.assertIn('before', step)
                    self.assertIn('after', step)
                self.assertGreaterEqual(len(group[mode]['illegal']), 2)
                for probe in group[mode]['illegal']:
                    self.assertFalse(probe['accepted'])
                    self.assertTrue(probe['error'])
                    self.assertTrue(probe['unchanged_on_rejection'])

    def test_b_does_not_keep_the_replaced_independent_record(self):
        store = lambda gid, mode: self.results['groups'][gid][mode]['chain'][-1]['after']['store']
        self.assertIn('P', store('C1', 'A'))
        self.assertNotIn('P', store('C1', 'B'))
        self.assertEqual([], [key for key, obj in store('C1', 'B').items() if obj['kind'] == 'plan'])
        self.assertEqual([], [key for key, obj in store('C2', 'B').items()
                              if obj['kind'] == 'product'])
        self.assertEqual([], [key for key, obj in store('C3', 'B').items()
                              if obj['kind'] == 'evidence'])
        self.assertEqual([], [key for key, obj in store('C4', 'B').items()
                              if obj['kind'] == 'goal'])
        self.assertIn('W', store('C4', 'B'))

    def test_c1_old_plan_text_is_retained_and_sharing_differs(self):
        group = self.results['groups']['C1']
        text = t.PLAN_V1['turnstep']['description']
        self.assertEqual(text, group['A']['final_state']['content']['old_plan_text'])
        self.assertEqual(text, group['B']['final_state']['content']['old_plan_text'])
        self.assertEqual({'id': 'P', 'revision': 1},
                         group['A']['final_state']['locators']['old_result_plan']['turnstep'])
        self.assertEqual({'turnstep': {'attempt': 'A', 'revision': 1, 'section': 'turnstep'}},
                         group['B']['final_state']['locators']['old_result_plan'])
        self.assertFalse(group['A']['final_state']['capabilities']['plan_edit_advances_attempt_version'])
        self.assertTrue(group['B']['final_state']['capabilities']['plan_edit_advances_attempt_version'])
        self.assertEqual(1, group['A']['chain'][1]['observations']['attempt_revision'])
        self.assertEqual(2, group['B']['chain'][1]['observations']['attempt_content_revision'])
        self.assertTrue(group['A']['final_state']['capabilities']['shared_plan_version_across_attempts'])
        self.assertFalse(group['B']['final_state']['capabilities']['shared_plan_version_across_attempts'])
        shared = group['B']['legal'][0]['observations']
        self.assertFalse(shared['shared_locator'])
        self.assertTrue(shared['content_equal'])
        self.assertEqual('attempt content revision not retained: 1',
                         group['B']['removal_probe']['lost'][0]['failure'])
        self.assertIn('逐版保留宿主内容修订', group['B']['removal_probe']['conventions_counted'])

    def test_c2_result_identity_and_post_end_correction(self):
        group = self.results['groups']['C2']
        self.assertEqual('reported_draft_written',
                         group['B']['final_state']['content']['old_result_dimensions']['implementation'])
        self.assertEqual('ended', group['B']['chain'][6]['observations']['status_at_write'])
        self.assertGreater(group['B']['chain'][6]['observations']['correction_revision'], 0)
        self.assertEqual('ended', group['A']['chain'][6]['observations']['status_at_write'])
        self.assertEqual({'draft_status': 'withdrawn', 'draft_notifications': 'present'},
                         group['B']['final_state']['content']['new_result_states_after_withdraw'])
        self.assertEqual({'draft_status': 'withdrawn', 'draft_notifications': 'present'},
                         group['A']['final_state']['content']['new_result_states_after_withdraw'])
        self.assertTrue(group['A']['final_state']['capabilities']['same_result_identity_across_attempts'])
        self.assertFalse(group['B']['final_state']['capabilities']['same_result_identity_across_attempts'])
        self.assertTrue(group['B']['final_state']['capabilities']['slot_local_identity_required'])
        self.assertEqual('result revision not retained: 2',
                         group['B']['removal_probe']['lost'][0]['failure'])
        self.assertEqual('A2', group['B']['legal'][0]['observations']['advanced_by'])
        self.assertFalse(group['B']['legal'][0]['observations']['same_locator'])

    def test_c3_reference_survives_subject_update_and_correction(self):
        group = self.results['groups']['C3']
        self.assertEqual({'change': 5, 'statement': 0},
                         group['B']['final_state']['locators']['report'])
        self.assertEqual({'id': 'E1', 'revision': 1},
                         group['A']['final_state']['locators']['report'])
        self.assertEqual(1, group['B']['final_state']['content']['subject_revision_at_report'])
        self.assertEqual(1, group['A']['final_state']['content']['subject_revision_at_report'])
        self.assertEqual(['completion reported; acceptance pending'],
                         group['B']['final_state']['content']['original_findings'])
        self.assertEqual(4, group['B']['final_state']['content']['subject_statement_count'])
        self.assertEqual(4, group['A']['final_state']['content']['subject_statement_count'])
        self.assertTrue(group['B']['final_state']['capabilities']['same_report_referenced_twice'])
        self.assertEqual(2, group['B']['legal'][2]['observations']['citations'])
        self.assertEqual(['turnstep scope regressed'],
                         group['B']['final_state']['recorded_failures'][0]['returned'])
        self.assertEqual('wrong_answer', group['B']['final_state']['recorded_failures'][0]['kind'])
        self.assertEqual([], group['A']['final_state']['recorded_failures'])

    def test_c4_attempt_history_and_goal_scope(self):
        group = self.results['groups']['C4']
        self.assertEqual(['a1', 'a2', 'a3', 'a4'],
                         group['B']['final_state']['content']['attempt_keys'])
        self.assertEqual(['a1', 'a2', 'a3', 'a4'],
                         group['A']['final_state']['content']['attempt_keys'])
        self.assertEqual({'a1': 'ended', 'a2': 'active', 'a3': 'active', 'a4': 'active'},
                         group['B']['final_state']['content']['attempt_status'])
        self.assertEqual(t.FEATURES, group['B']['final_state']['content']['a1_scope_basis'])
        self.assertEqual(t.REVISED_SCOPE, group['B']['final_state']['content']['current_goal_scope'])
        self.assertEqual('pending', group['B']['final_state']['content']['goal_acceptance'])
        self.assertTrue(group['B']['final_state']['capabilities']['attempt_key_reintroduced'])
        self.assertFalse(group['A']['final_state']['capabilities']['attempt_key_reintroduced'])
        self.assertEqual(1, group['B']['chain'][6]['observations']['a1_goal_revision'])
        self.assertEqual('unknown attempt key: a1',
                         group['B']['removal_probe']['lost'][0]['failure'])

    def test_each_removal_probe_names_what_cannot_be_recovered(self):
        for gid, group in self.results['groups'].items():
            for mode in ('A', 'B'):
                probe = group[mode]['removal_probe']
                self.assertTrue(probe['removed'])
                self.assertEqual(1, len(probe['lost']), (gid, mode))
                self.assertTrue(probe['lost'][0]['failure'])
                self.assertTrue(probe['conventions_counted'])
                self.assertTrue(probe['still_readable'])

    def test_comparison_keeps_common_successes_and_real_differences(self):
        for gid, group in self.results['groups'].items():
            self.assertTrue(group['same_successes'], gid)
            self.assertEqual([], [row for row in group['content_queries'] if not row['same']], gid)
            for row in group['differences']:
                self.assertNotEqual(row['A'], row['B'])
        self.assertTrue(self.results['groups']['C1']['substantive_differences'])
        self.assertTrue(self.results['groups']['C2']['substantive_differences'])
        self.assertEqual([], self.results['groups']['C3']['substantive_differences'])
        self.assertEqual([], self.results['groups']['C4']['substantive_differences'])

    def test_review_reports_conditions_and_no_recommendation(self):
        text = t.build_review(self.results)
        for gid in ('C1', 'C2', 'C3', 'C4'):
            self.assertIn('### %s' % gid, text)
        self.assertIn('不做最终推荐', text)
        self.assertIn('删除/弱化探针', text)
        self.assertIn('未发现', text)
        self.assertIn('被反例改变的假设', text)
        self.assertIn(str(self.results['groups']['C1']['identity_cost']['B']
                          ['max_records_changed_in_one_change']), text)
        self.assertNotIn('建议采用', text)


if __name__ == '__main__':
    unittest.main()
