"""Final review for two confirmed T12 defects and the GLM handoff payload.

The tests exercise the real core.  ``_legacy_version`` and
``_legacy_part_progress_overall`` / ``_legacy_advance_product_allowed`` are
frozen copies of the pre-fix predicates; they keep the reproduced wrong answer
as explicit evidence instead of editing old exports or expected results.
"""
import hashlib
import unittest
from copy import deepcopy

import t12_handoff as h
import t12_study as s

GLM_INPUT_SHA256 = 'c885247c1c1af73e8b5a32949b5df605f3c77b6516e4558d0bf310cbf7c8bb32'
GLM_ACTIONS = [{'op': 'advance_parts', 'id': h.PRODUCT, 'parts': [h.BEHAVIOR_PART],
                'dimensions': {'implementation': 'reported_code_written'}}]
GLM_ORIGINAL_BASIS = ['SYN:handoff-produce-v2', 'SYN:handoff-report-v2']
GLM_CORRECTED_BASIS = ['SYN:handoff-next-step-request']
COMPLETE = {'completion': 'complete', 'implementation': 'implemented',
            'git': 'committed', 'acceptance': 'pending'}
UNKNOWN = {'completion': 'unknown', 'implementation': 'unknown',
           'git': 'unknown', 'acceptance': 'pending'}


def _legacy_version(state, oid, revision=None):
    """Frozen pre-fix version(): it always indexes state['changes']."""
    def find(view):
        if oid in view['objects']:
            return view['objects'][oid]
        for obj in view['objects'].values():
            if oid in obj.get('plan_records', {}):
                return obj['plan_records'][oid]

    for view in [state] + [c['after'] for c in reversed(state['changes'])]:
        obj = find(view)
        if obj and (revision is None or obj['revision'] == revision):
            return deepcopy(obj)
        if revision is not None:
            obj = view.get('versions', {}).get(oid, {}).get(str(revision))
            if obj:
                return deepcopy(obj)
    raise ValueError('unknown object version: ' + oid)


def _legacy_part_progress_overall(product):
    """Frozen pre-fix non-subdivided branch: shared dimensions, no presence check."""
    return deepcopy(product['dimensions'])


def _legacy_advance_product_allowed(product):
    """Frozen pre-fix non-subdivided branch: any existing product could advance."""
    return product['kind'] == 'product' and 'part_states' not in product


def _apply(state, actions, basis=('SYN:final-review',)):
    return s.apply(state, list(actions), state['head'], list(basis), 'synthetic')


def _product_state(parts=('only',)):
    state = s.fresh()
    result = s.apply(state, [
        {'op': 'goal', 'id': 'final-goal', 'scope': ['synthetic final review']},
        {'op': 'begin', 'id': 'final-attempt', 'goal': 'final-goal',
         'scope': ['synthetic final review']},
        {'op': 'produce', 'id': 'final-product', 'attempt': 'final-attempt',
         'parts': list(parts), 'dimensions': dict(COMPLETE),
         'location': 'synthetic final review', 'nature': 'synthetic'},
        {'op': 'report', 'id': 'final-report',
         'subject': {'id': 'final-product', 'revision': 1},
         'scope': 'synthetic final review report', 'findings': ['before withdrawal'],
         'nature': 'synthetic'}],
        0, ['SYN:final-review'])
    assert result['status'] == 'applied', result['error']
    return result['state']


class ViewVersionTests(unittest.TestCase):
    def test_frozen_legacy_version_raises_keyerror_on_the_view(self):
        _, state, _ = h.build_chain()
        view = h._view(state)
        self.assertNotIn('changes', view)
        with self.assertRaises(KeyError):
            _legacy_version(view, 'goal')

    def test_view_answers_current_and_archived_object_versions(self):
        _, state, _ = h.build_chain()
        view = h._view(state)
        for oid in ('goal', 'migration-plan', 'draft-code', h.PRODUCT,
                    'continuation-record'):
            self.assertEqual(s.version(state, oid), s.version(view, oid))
        self.assertEqual(2, s.version(view, h.PLAN)['revision'])
        self.assertEqual(1, s.version(view, h.PLAN, 1)['revision'])
        self.assertEqual(s.version(state, h.PLAN, 1), s.version(view, h.PLAN, 1))

    def test_view_answers_embedded_plan_versions(self):
        state = s.real_path(plans='embedded')
        view = h._view(state)
        self.assertNotIn('architecture', view['objects'])
        self.assertIn('architecture', view['versions'])
        self.assertEqual(2, s.version(view, 'architecture')['revision'])
        self.assertEqual(1, s.version(view, 'architecture', 1)['revision'])
        self.assertEqual(s.version(state, 'architecture', 1),
                         s.version(view, 'architecture', 1))

    def test_view_unknown_reference_still_raises_value_error(self):
        _, state, _ = h.build_chain()
        view = h._view(state)
        for call in (lambda: s.version(view, 'missing-object'),
                     lambda: s.version(view, 'goal', 9),
                     lambda: s.version(view, 'goal', 0)):
            with self.assertRaises(ValueError):
                call()

    def test_complete_state_keeps_the_recorded_snapshot_fallback(self):
        state = s.real_path()
        del state['versions']['batch']['1']
        recovered = s.version(state, 'batch', 1)
        self.assertEqual(1, recovered['revision'])
        self.assertEqual('active', recovered['status'])


class EmptyPartProgressTests(unittest.TestCase):
    def test_frozen_legacy_predicates_reproduce_the_reported_defect(self):
        state = _product_state()
        state = _apply(state, [{'op': 'withdraw_parts', 'id': 'final-product',
                                'parts': ['only']}])['state']
        product = s.version(state, 'final-product')
        self.assertNotIn('part_states', product)
        self.assertEqual('complete', _legacy_part_progress_overall(product)['completion'])
        self.assertTrue(_legacy_advance_product_allowed(product))

    def test_non_subdivided_all_withdrawn_reports_unknown(self):
        state = _product_state()
        state = _apply(state, [{'op': 'withdraw_parts', 'id': 'final-product',
                                'parts': ['only']}])['state']
        progress = s.part_progress(state, 'final-product')
        self.assertFalse(progress['subdivided'])
        self.assertEqual('withdrawn', progress['parts']['only']['presence'])
        self.assertEqual(UNKNOWN, progress['overall'])

    def test_non_subdivided_empty_group_advance_is_rejected_atomically(self):
        state = _product_state()
        state = _apply(state, [{'op': 'withdraw_parts', 'id': 'final-product',
                                'parts': ['only']}])['state']
        before = deepcopy(state)
        result = _apply(state, [{'op': 'advance_product', 'id': 'final-product',
                                 'dimensions': {'git': 'reported_committed'}}])
        self.assertEqual('rejected', result['status'])
        self.assertEqual(before, result['state'])
        self.assertIn('present', result['error'])

    def test_non_subdivided_partial_withdrawal_keeps_remaining_progress(self):
        state = _product_state(parts=('kept', 'gone'))
        state = _apply(state, [{'op': 'withdraw_parts', 'id': 'final-product',
                                'parts': ['gone']}])['state']
        self.assertEqual('complete',
                         s.part_progress(state, 'final-product')['overall']['completion'])
        result = _apply(state, [{'op': 'advance_product', 'id': 'final-product',
                                 'dimensions': {'git': 'staged'}}])
        self.assertEqual('applied', result['status'], result['error'])
        updated = s.version(result['state'], 'final-product')
        self.assertEqual({'kept': 'present', 'gone': 'withdrawn'}, updated['parts'])
        self.assertEqual('staged', updated['dimensions']['git'])

    def test_subdivided_all_withdrawn_reports_unknown_and_rejects_empty_advance(self):
        state = _apply(_product_state(parts=('one', 'two')), [
            {'op': 'advance_parts', 'id': 'final-product', 'parts': ['one'],
             'dimensions': {'implementation': 'reported_code_written'}}])['state']
        self.assertIn('part_states', s.version(state, 'final-product'))
        state = _apply(state, [{'op': 'withdraw_parts', 'id': 'final-product',
                                'parts': ['one', 'two']}])['state']
        progress = s.part_progress(state, 'final-product')
        self.assertTrue(progress['subdivided'])
        self.assertEqual(UNKNOWN, progress['overall'])
        before = deepcopy(state)
        for action in (
                {'op': 'advance_product', 'id': 'final-product',
                 'dimensions': {'git': 'staged'}},
                {'op': 'advance_product', 'id': 'final-product', 'parts': [],
                 'dimensions': {'git': 'staged'}},
                {'op': 'advance_product', 'id': 'final-product', 'parts': ['one'],
                 'dimensions': {'git': 'staged'}}):
            result = _apply(state, [action])
            self.assertEqual('rejected', result['status'])
            self.assertEqual(before, result['state'])

    def test_subdivided_partial_withdrawal_keeps_remaining_part_usable(self):
        state = _apply(_product_state(parts=('kept', 'gone')), [
            {'op': 'advance_parts', 'id': 'final-product', 'parts': ['kept'],
             'dimensions': {'git': 'reported_committed'}}])['state']
        state = _apply(state, [{'op': 'withdraw_parts', 'id': 'final-product',
                                'parts': ['gone']}])['state']
        result = _apply(state, [{'op': 'advance_product', 'id': 'final-product',
                                 'parts': ['kept'],
                                 'dimensions': {'implementation': 'reported_implemented'}}])
        self.assertEqual('applied', result['status'], result['error'])
        progress = s.part_progress(result['state'], 'final-product')
        self.assertEqual('reported_implemented',
                         progress['parts']['kept']['dimensions']['implementation'])
        self.assertEqual('withdrawn', progress['parts']['gone']['presence'])
        rejected = _apply(result['state'], [
            {'op': 'advance_parts', 'id': 'final-product', 'parts': ['gone'],
             'dimensions': {'git': 'staged'}}])
        self.assertEqual('rejected', rejected['status'])

    def test_withdrawal_and_advance_preserve_old_product_report_goal_and_history(self):
        state = _product_state(parts=('kept', 'gone'))
        old_product = s.version(state, 'final-product')
        old_report = s.version(state, 'final-report')
        old_goal = s.version(state, 'final-goal')
        state = _apply(state, [{'op': 'withdraw_parts', 'id': 'final-product',
                                'parts': ['gone']}])['state']
        state = _apply(state, [{'op': 'advance_product', 'id': 'final-product',
                                'dimensions': {'git': 'staged'}}])['state']
        self.assertEqual(old_product, s.version(state, 'final-product', 1))
        self.assertEqual(old_report, s.version(state, 'final-report'))
        self.assertEqual(old_goal, s.version(state, 'final-goal'))
        self.assertEqual([1, 2, 3], [change['number'] for change in state['changes']])
        self.assertEqual('pending', s.version(state, 'final-goal')['acceptance'])


class HandoffPackageTests(unittest.TestCase):
    def test_fixed_readback_package_hash_matches(self):
        text = h._serialize_v2(h.build_readback_v2())
        self.assertEqual(GLM_INPUT_SHA256,
                         hashlib.sha256(text.encode('utf-8')).hexdigest())

    def test_readback_records_split_real_and_synthetic_changes(self):
        readback = h.build_readback_v2()
        historical = [row['change'] for row in readback['records']
                      if row['origin'] == 'historical_anchor']
        synthetic = [row['change'] for row in readback['records']
                     if row['origin'] == 'synthetic_continuation']
        self.assertEqual(list(range(1, 9)), historical)
        self.assertEqual([9, 10, 11, 12], synthetic)


class GlmPayloadTests(unittest.TestCase):
    def _run(self, basis):
        state = h.build_resume_state()['state']
        before = deepcopy(state)
        result = s.apply(state, deepcopy(GLM_ACTIONS), 12, list(basis), 'synthetic')
        return before, result

    def test_original_payload_is_structurally_accepted_at_head_12(self):
        before, result = self._run(GLM_ORIGINAL_BASIS)
        self.assertEqual(12, before['head'])
        self.assertEqual('applied', result['status'], result['error'])
        after = result['state']
        self.assertEqual(13, after['head'])
        self.assertEqual(GLM_ORIGINAL_BASIS, after['changes'][-1]['basis'])
        progress = s.part_progress(after, h.PRODUCT)
        self.assertEqual('reported_code_written',
                         progress['parts'][h.BEHAVIOR_PART]['dimensions']['implementation'])
        self.assertEqual(h.DRAFT, progress['parts'][h.NOTES_PART]['dimensions'])
        self.assertEqual('pending', s.version(after, 'goal')['acceptance'])
        self.assertEqual({'id': h.PLAN, 'revision': 2},
                         s.version(after, h.PRODUCT)['plan_usage']['sections']['turnstep']['plan'])
        self.assertEqual(s.version(before, 'draft-code'), s.version(after, 'draft-code'))
        self.assertEqual(s.version(before, 'channel-checks'), s.version(after, 'channel-checks'))
        self.assertEqual(s.version(before, h.PLAN, 1), s.version(after, h.PLAN, 1))
        self.assertEqual(list(range(1, 14)),
                         [change['number'] for change in after['changes']])

    def test_original_basis_names_old_production_and_report_changes(self):
        rows = {row['anchor']: row for row in h.build_readback_v2()['records']}
        self.assertEqual(11, rows['handoff-produce-v2']['change'])
        self.assertEqual(12, rows['handoff-report-v2']['change'])
        self.assertEqual(['SYN:handoff-produce-v2'], rows['handoff-produce-v2']['basis'])
        self.assertEqual(['SYN:handoff-report-v2'], rows['handoff-report-v2']['basis'])

    def test_plan_and_report_facts_match_the_corrected_answer(self):
        state = h.build_resume_state()['state']
        for oid in ('draft-code', 'independent-code'):
            usage = s.version(state, oid)['plan_usage']
            self.assertEqual('legacy_initial_plan', usage['mode'])
            self.assertEqual(['channel', 'reference', 'turnstep'], sorted(usage['sections']))
            for section in usage['sections'].values():
                self.assertEqual({'id': h.PLAN, 'revision': 1}, section['plan'])
        product = s.version(state, h.PRODUCT)
        self.assertEqual('explicit_scope', product['plan_usage']['mode'])
        self.assertEqual(['turnstep'], product['plan_usage']['scope'])
        self.assertEqual({'id': h.PLAN, 'revision': 2},
                         product['plan_usage']['sections']['turnstep']['plan'])
        self.assertEqual('migration', s.current_plan(state, h.PLAN)['owner'])
        report = s.version(state, 'channel-checks')
        self.assertEqual(1, report['revision'])
        self.assertEqual({'id': 'independent', 'revision': 1}, report['subject'])
        self.assertEqual('presentation channel; not turnstep worktree', report['scope'])

    def test_corrected_basis_runs_with_the_same_state_effect(self):
        before_original, original = self._run(GLM_ORIGINAL_BASIS)
        before_corrected, corrected = self._run(GLM_CORRECTED_BASIS)
        self.assertEqual(before_original, before_corrected)
        self.assertEqual('applied', corrected['status'], corrected['error'])
        self.assertEqual(GLM_CORRECTED_BASIS, corrected['state']['changes'][-1]['basis'])
        self.assertEqual(s.snapshot(original['state']), s.snapshot(corrected['state']))
        self.assertEqual(original['changed_paths'], corrected['changed_paths'])
        after = corrected['state']
        self.assertEqual(13, after['head'])
        self.assertEqual(s.version(before_corrected, h.PRODUCT),
                         s.version(after, h.PRODUCT, 1))
        self.assertEqual('pending', s.version(after, 'goal')['acceptance'])
        self.assertEqual({'id': h.PLAN, 'revision': 2},
                         s.version(after, h.PRODUCT)['plan_usage']['sections']['turnstep']['plan'])


if __name__ == '__main__':
    unittest.main()
