"""Checks for identity-v2: the corrected strong-B comparison for C1/C2."""
import json
import unittest

import t12_identity_trials as v1
import t12_identity_trials_v2 as t

_RESULTS = None


def results():
    global _RESULTS
    if _RESULTS is None:
        _RESULTS = t.build_results()
    return _RESULTS


def setUpModule():
    if not t.IDENTITY_DIR.exists():
        t.export_identity(t.IDENTITY_DIR)


class EvidenceTests(unittest.TestCase):
    def test_identity_v2_was_written_by_the_export_function_and_is_not_overwritten(self):
        for name in ('results.json', 'review.md'):
            self.assertTrue((t.IDENTITY_DIR / name).is_file(), name)
        self.assertTrue(t.verify_identity(t.IDENTITY_DIR))
        before = sorted(path.name for path in t.IDENTITY_DIR.iterdir())
        with self.assertRaises(FileExistsError):
            t.export_identity(t.IDENTITY_DIR)
        self.assertEqual(before, sorted(path.name for path in t.IDENTITY_DIR.iterdir()))

    def test_results_file_is_the_executed_document(self):
        saved = json.loads((t.IDENTITY_DIR / 'results.json').read_text(encoding='utf-8'))
        self.assertEqual(['C1', 'C2', 'C3', 'C4'], sorted(saved['groups']))
        self.assertTrue(saved['boundary']['no_final_recommendation'])
        self.assertEqual(t.C1_CHAIN, saved['common_chain']['C1'])
        self.assertEqual(t.C2_CHAIN, saved['common_chain']['C2'])
        self.assertIn('d9e78236', saved['v1_status']['note'])


class ChainTests(unittest.TestCase):
    def test_every_group_runs_its_whole_chain_in_both_storages(self):
        for gid, group in results()['groups'].items():
            expected = t.EXPECTED_CHAINS[gid]
            for mode in ('A', 'B'):
                chain = group[mode]['chain']
                self.assertEqual(expected, [step['label'] for step in chain], (gid, mode))
                for step in chain:
                    self.assertTrue(step['accepted'], (gid, mode, step['label']))
                    self.assertTrue(step['changed_paths'], (gid, mode, step['label']))
                    self.assertIn('observations', step)
                    self.assertTrue(step['before'] and step['after'])

    def test_c1_strong_b_keeps_shared_version_and_reads_old_plan_text(self):
        group = results()['groups']['C1']
        old_text = v1.PLAN_V1['turnstep']['description']
        new_text = v1.PLAN_V2_TURNSTEP['description']
        for mode in ('A', 'B'):
            report = group[mode]
            content = report['final_state']['content']
            self.assertEqual(old_text, content['old_plan_text'], mode)
            self.assertEqual(new_text, content['new_plan_text'], mode)
            self.assertEqual(old_text, content['pre_adoption_plan_text'], mode)
            self.assertEqual(old_text, content['second_attempt_plan_text'], mode)
            locators = report['final_state']['locators']
            self.assertEqual(locators['old_result_plan'], locators['second_attempt_plan'],
                             'the second attempt must reference the exact old version')
            self.assertTrue(report['final_state']['capabilities']
                            ['shared_plan_version_across_attempts'], mode)
            self.assertFalse(report['chain'][-1]['observations']['copied_plan_content'], mode)
        self.assertNotEqual(group['A']['final_state']['locators']['old_result_plan'],
                            group['B']['final_state']['locators']['old_result_plan'])
        self.assertFalse(group['B']['chain'][-1]['observations']['copied_plan_content'])

    def test_c1_reports_extra_version_coupling_without_failing(self):
        group = results()['groups']['C1']
        self.assertFalse(group['A']['final_state']['capabilities']
                         ['plan_edit_advances_attempt_version'])
        self.assertTrue(group['B']['final_state']['capabilities']
                        ['plan_edit_advances_attempt_version'])
        self.assertFalse(group['A']['final_state']['capabilities']
                         ['lifecycle_change_creates_new_plan_version'])
        self.assertTrue(group['B']['final_state']['capabilities']
                        ['lifecycle_change_creates_new_plan_version'])
        self.assertTrue(group['A']['final_state']['capabilities']
                        ['old_plan_locator_readable_after_lifecycle_change'])
        self.assertTrue(group['B']['final_state']['capabilities']
                        ['old_plan_locator_readable_after_lifecycle_change'])
        coupling = group['B']['final_state']['version_coupling']
        self.assertGreater(coupling['lifecycle_end']['plan_version_after'],
                           coupling['lifecycle_end']['plan_version_before'])
        self.assertIn('不作为失败判据', coupling['note'])
        for mode in ('A', 'B'):
            self.assertEqual('ended', group[mode]['final_state']['content']['attempt_status'])

    def test_c2_strong_b_keeps_slot_identity_across_attempts(self):
        group = results()['groups']['C2']
        for mode in ('A', 'B'):
            report = group[mode]
            l7 = report['chain'][-1]['observations']
            self.assertTrue(l7['same_identity'], mode)
            self.assertEqual('A2', l7['producer'], mode)
            self.assertEqual('ended', l7['host_attempt_status'], mode)
            self.assertGreater(l7['revision_after'], l7['revision_before'])
            self.assertEqual(v1.DRAFT, l7['historical_result']['dimensions'])
            self.assertEqual('in_progress',
                             l7['correction_result']['dimensions']['completion'])
            self.assertTrue(report['final_state']['capabilities']
                            ['same_result_identity_across_attempts'], mode)
            self.assertTrue(report['final_state']['capabilities']
                            ['host_attempt_remains_ended'], mode)
            self.assertTrue(report['final_state']['capabilities']
                            ['cross_attempt_write_preserves_history'], mode)
        self.assertEqual({'attempt': 'A', 'slot': 'draft_status'},
                         group['B']['chain'][-1]['observations']['logical_locator_after'])
        self.assertEqual({'product': 'Q'},
                         group['A']['chain'][-1]['observations']['logical_locator_after'])

    def test_c2_b_keeps_the_legal_write_path(self):
        group = results()['groups']['C2']
        for mode in ('A', 'B'):
            report = group[mode]
            self.assertTrue(any(row['id'] == 'withdraw-single-part' and row['accepted']
                                for row in report['legal']), mode)
            self.assertTrue(any(row['id'] == 'current-read' and row['accepted']
                                for row in report['legal']), mode)
            self.assertEqual('reported_complete',
                             report['final_state']['content']
                             ['new_result_dimensions']['completion'], mode)
        slot_paths = [path for path in group['B']['chain'][3]['changed_paths']
                      if path.startswith('/store/A/slots')]
        self.assertTrue(slot_paths, group['B']['chain'][3]['changed_paths'])
        for row in group['B']['illegal']:
            self.assertNotIn('no independent product identity', row['error'])
        self.assertEqual([], group['differences'])

    def test_rejections_are_real_and_atomic(self):
        for gid in ('C1', 'C2'):
            group = results()['groups'][gid]
            for mode in ('A', 'B'):
                rows = group[mode]['illegal']
                self.assertGreaterEqual(len(rows), 4, (gid, mode))
                kinds = {row['kind'] for row in rows}
                self.assertLessEqual({'stale', 'invalid_locator', 'atomicity'}, kinds,
                                     (gid, mode))
                for row in rows:
                    self.assertFalse(row['accepted'], (gid, mode, row['id']))
                    self.assertTrue(row['error'])
                    self.assertTrue(row['state_unchanged'])
                    self.assertTrue(row['head_unchanged'])
                atomic = [row for row in rows if row['kind'] == 'atomicity'][0]
                self.assertTrue(atomic['mutated_before_failure'])
                self.assertIn('synthetic mid-step failure', atomic['error'])

    def test_comparison_drops_preset_false_capabilities(self):
        for gid in ('C1', 'C2'):
            group = results()['groups'][gid]
            probes = [row['probe'] for row in group['capability_queries']]
            for name in ('independent_plan_record', 'independent_product_record',
                         'slot_local_identity_required'):
                self.assertNotIn(name, probes, gid)
            for row in group['content_queries']:
                self.assertTrue(row['same'], (gid, row['query']))
            for row in group['differences']:
                self.assertNotEqual(row['A'], row['B'], (gid, row['probe']))

    def test_placement_probe_shows_where_each_identity_lives(self):
        for gid in ('C1', 'C2'):
            row = results()['groups'][gid]['placement_queries'][0]
            self.assertTrue(row['A'], gid)
            self.assertFalse(row['B'], gid)
            self.assertFalse(row['same'], gid)

    def test_c3_and_c4_are_reused_from_v1(self):
        for gid in ('C3', 'C4'):
            group = results()['groups'][gid]
            self.assertIn('reused_from', group)
            for mode in ('A', 'B'):
                self.assertEqual(v1.CHAIN_LABELS,
                                 [step['label'] for step in group[mode]['chain']])
                for key in group[mode]['final_state']['capabilities']:
                    self.assertIn(key, v1.CAP_MEANING)

    def test_v1_module_is_not_modified_by_the_correction(self):
        self.assertFalse(v1.build_c1('B')['final_state']['capabilities']
                         ['shared_plan_version_across_attempts'])
        self.assertFalse(v1.build_c2('B')['final_state']['capabilities']
                         ['same_result_identity_across_attempts'])

    def test_boundary_and_interface_coverage_are_explicit(self):
        data = results()
        self.assertTrue(data['boundary']['no_final_recommendation'])
        self.assertIn('合成', data['boundary']['synthetic'])
        self.assertIn('不声称', data['interface_coverage']['claim'])
        self.assertTrue(data['interface_coverage']['covered'])
        self.assertTrue(data['interface_coverage']['not_covered'])
        self.assertTrue(data['v1_status']['unchanged_by_this_run'])
        self.assertIn('d9e78236', data['v1_status']['note'])


class ReviewTests(unittest.TestCase):
    def test_review_reports_corrections_cost_and_rejections(self):
        data = results()
        text = t.build_review(data)
        for heading in ('## 1. 这一版修正了什么', '## 2. 方法与边界',
                        '## 4. C1/C2 逐组结果', '## 6. 被反例改变的假设',
                        '## 7. 适用条件与 v2 接口覆盖', '## 8. v1 现存结果的状态',
                        '## 9. 不做最终推荐'):
            self.assertIn(heading, text)
        self.assertIn('identity-v1', text)
        self.assertIn('d9e78236', text)
        self.assertIn('不声称', text)
        self.assertIn('未发现', text)
        self.assertIn('拒绝证据', text)
        self.assertIn('不作为失败判据', text)
        self.assertNotIn('建议采用', text)
        for gid in ('C1', 'C2'):
            self.assertIn('### %s' % gid, text)


if __name__ == '__main__':
    unittest.main()
