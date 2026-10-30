"""Regression for coexisting interpretations and the single-branch T12 handoff export."""
import hashlib
import json
import unittest

import t12_handoff as h
import t12_study as s

SCOPE = 'SYN:coexist-scope'
SCOPE_B = 'SYN:coexist-scope-b'
FORBIDDEN = {'answer', 'answers', 'expected_answer', 'truth', 'verdict',
             'pass', 'passed', 'fail', 'failed', 'score', 'expected', 'checks'}


def setUpModule():
    h.export_handoff(h.HANDOFF_DIR)
    h.export_handoff_v2(h.HANDOFF_DIR_V2)


def _walk_keys(value):
    if isinstance(value, dict):
        for key, child in value.items():
            yield key
            yield from _walk_keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_keys(child)


def _legacy_unique_root_rule(evidence, scope_id, prior_id):
    """Frozen reproduction of the pre-change predicate; failure evidence only."""
    return s._scope_roots(evidence, scope_id) == [prior_id]


def _probe_state():
    state = s.fresh()
    result = s.apply(state, [
        {'op': 'goal', 'id': 'coexist-goal', 'scope': ['synthetic coexistence probe']},
        {'op': 'begin', 'id': 'coexist-work', 'goal': 'coexist-goal',
         'scope': ['synthetic coexistence probe']}],
        state['head'], ['SYN:coexist'])
    assert result['status'] == 'applied', result['error']
    return result['state']


def _report(state, oid, scope_ids):
    result = s.apply(state, [
        {'op': 'report', 'id': oid, 'subject': s.actual_ref(state, 'coexist-work'),
         'scope': 'synthetic interpretation ' + oid,
         'findings': ['synthetic interpretation ' + oid],
         'nature': 'synthetic', 'content_kind': 'interpretation',
         'scope_ids': list(scope_ids)}],
        state['head'], ['SYN:coexist'])
    assert result['status'] == 'applied', result['error']
    return result['state']


def _correct(state, new_id, prior_id, scope_ids):
    return s.apply(state, [
        {'op': 'correct_interpretation', 'id': new_id,
         'prior': s.actual_ref(state, prior_id),
         'scope': 'synthetic correction ' + new_id,
         'scope_ids': list(scope_ids),
         'findings': ['synthetic correction ' + new_id],
         'basis': ['SYN:coexist'], 'nature': 'synthetic'}],
        state['head'], ['SYN:coexist'])


def _coexisting():
    return _report(_report(_probe_state(), 'coexist-h1', [SCOPE]), 'coexist-h2', [SCOPE])


class CoexistingInterpretationTests(unittest.TestCase):
    def test_two_independent_hypotheses_can_be_corrected_one_at_a_time(self):
        state = _coexisting()
        before = s.interpretations(state, SCOPE)
        self.assertEqual('multiple_unresolved', before['status'])
        self.assertIsNone(before['current'])
        self.assertEqual(['coexist-h1', 'coexist-h2'],
                         [row['evidence']['id'] for row in before['history']])
        evidence = s._interpretation_evidence(state)
        self.assertFalse(_legacy_unique_root_rule(evidence, SCOPE, 'coexist-h1'))
        self.assertFalse(_legacy_unique_root_rule(evidence, SCOPE, 'coexist-h2'))

        h2_before = s.version(state, 'coexist-h2')
        result = _correct(state, 'coexist-h1-fix', 'coexist-h1', [SCOPE])
        self.assertEqual('applied', result['status'], result['error'])
        state = result['state']

        after = s.interpretations(state, SCOPE)
        self.assertEqual('multiple_unresolved', after['status'])
        self.assertIsNone(after['current'])
        self.assertEqual(['coexist-h1-fix', 'coexist-h2'],
                         s._scope_roots(s._interpretation_evidence(state), SCOPE))
        self.assertEqual(['coexist-h1', 'coexist-h2', 'coexist-h1-fix'],
                         [row['evidence']['id'] for row in after['history']])
        self.assertEqual(h2_before, s.version(state, 'coexist-h2'))
        self.assertEqual(['coexist-h1-fix'],
                         [row['evidence']['id'] for row in after['corrections']])
        self.assertEqual({'id': 'coexist-h1', 'revision': 1},
                         after['corrections'][0]['corrects'])

    def test_superseded_hypothesis_is_rejected_and_the_other_stays_correctable(self):
        state = _correct(_coexisting(), 'coexist-h1-fix', 'coexist-h1', [SCOPE])['state']
        again = _correct(state, 'coexist-h1-again', 'coexist-h1', [SCOPE])
        self.assertEqual('rejected', again['status'])
        self.assertEqual(state, again['state'])
        self.assertIn('current interpretation', again['error'])

        second = _correct(state, 'coexist-h2-fix', 'coexist-h2', [SCOPE])
        self.assertEqual('applied', second['status'], second['error'])
        state = second['state']
        view = s.interpretations(state, SCOPE)
        self.assertEqual('multiple_unresolved', view['status'])
        self.assertEqual(['coexist-h1-fix', 'coexist-h2-fix'],
                         s._scope_roots(s._interpretation_evidence(state), SCOPE))
        self.assertEqual(['coexist-h1', 'coexist-h2', 'coexist-h1-fix', 'coexist-h2-fix'],
                         [row['evidence']['id'] for row in view['history']])

    def test_chain_disjoint_and_partial_scope_rules_are_unchanged(self):
        state = _report(_probe_state(), 'chain-old', [SCOPE, SCOPE_B])
        state = _correct(state, 'chain-fix-1', 'chain-old', [SCOPE])['state']
        state = _correct(state, 'chain-fix-2', 'chain-fix-1', [SCOPE])['state']
        view = s.interpretations(state, SCOPE)
        self.assertEqual('corrected', view['status'])
        self.assertEqual('chain-fix-2', view['current']['evidence']['id'])
        self.assertEqual(['chain-old', 'chain-fix-1', 'chain-fix-2'],
                         [row['evidence']['id'] for row in view['history']])

        other = s.interpretations(state, SCOPE_B)
        self.assertEqual('recorded', other['status'])
        self.assertEqual('chain-old', other['current']['evidence']['id'])
        state = _correct(state, 'chain-b-fix', 'chain-old', [SCOPE_B])['state']
        other = s.interpretations(state, SCOPE_B)
        self.assertEqual('corrected', other['status'])
        self.assertEqual('chain-b-fix', other['current']['evidence']['id'])

        mixed = _correct(state, 'chain-mixed', 'chain-old', [SCOPE, SCOPE_B])
        self.assertEqual('rejected', mixed['status'])
        self.assertEqual(state, mixed['state'])
        self.assertIn('current interpretation', mixed['error'])


class HandoffExportTests(unittest.TestCase):
    def _readback(self):
        return json.loads((h.HANDOFF_DIR / 'readback.json').read_text(encoding='utf-8'))

    def _checks(self):
        return json.loads((h.HANDOFF_DIR / 'checks.json').read_text(encoding='utf-8'))

    def test_export_writes_once_and_verifies_existing_files(self):
        for name in h.GENERATED:
            self.assertTrue((h.HANDOFF_DIR / name).is_file(), name)
        self.assertTrue(h.verify_handoff(h.HANDOFF_DIR))
        before = {name: (h.HANDOFF_DIR / name).read_bytes() for name in h.GENERATED}
        h.export_handoff(h.HANDOFF_DIR)
        self.assertEqual(before, {name: (h.HANDOFF_DIR / name).read_bytes() for name in h.GENERATED})

    def test_readback_is_one_branch_with_the_complete_snapshot(self):
        readback = self._readback()
        self.assertEqual(h.BRANCH, readback['branch']['id'])
        self.assertFalse(readback['branch']['parallel_probe_states_included'])
        state = readback['state']
        self.assertEqual(readback['head'], state['head'])
        self.assertEqual(readback['branch']['current_head'], state['head'])
        for key in ('head', 'layout', 'plans', 'objects', 'versions',
                    'changes', 'relations', 'items', 'responsibility'):
            self.assertIn(key, state)
        self.assertEqual(list(range(1, state['head'] + 1)),
                         [change['number'] for change in state['changes']])
        self.assertEqual(1 + s.real_path()['head'], readback['branch']['synthetic_start_change'])
        self.assertEqual(readback['branch']['historical_base_head'] + 4, state['head'])
        self.assertEqual(sorted(range(1, state['head'] + 1)),
                         sorted(row['change'] for row in readback['records']))
        self.assertEqual(len(readback['records']), state['head'])
        self.assertEqual(4, len([row for row in readback['records']
                                 if row['origin'] == 'synthetic_continuation']))
        for row in readback['records']:
            self.assertIsInstance(row['exact_references'], dict)
        produced = next(row for row in readback['records']
                        if row['anchor'] == 'handoff-produce-v2')
        self.assertEqual({'id': h.PLAN, 'revision': 2},
                         produced['observation'][0]['plan_usage']['sections']['turnstep']['plan'])
        self.assertEqual({'id': h.PLAN, 'revision': 1},
                         produced['observation'][0]['initial_plan'])
        self.assertFalse(produced['observation'][0]['legacy_plan_present'])

    def test_plan_owner_is_not_the_used_plan_version(self):
        authority = self._readback()['plan_authority']
        self.assertEqual({'id': h.PLAN, 'revision': 2},
                         authority['product_plan_usage'][h.PRODUCT]['sections']['turnstep']['plan'])
        self.assertEqual({'id': h.PLAN, 'revision': 1},
                         authority['product_initial_plan'][h.PRODUCT])
        self.assertEqual({'id': h.PLAN, 'revision': 1}, authority['attempt_begin_plan'][h.ATTEMPT])
        self.assertEqual('migration', authority['plan_owner'][h.PLAN])
        self.assertEqual({'id': h.PLAN, 'revision': 1},
                         authority['product_plan_usage']['draft-code']['sections']['turnstep']['plan'])
        self.assertNotIn(h.PRODUCT, authority['product_legacy_plan_projection'])
        self.assertIn('only authority', authority['rule'])

    def test_report_pointers_are_exact(self):
        readback = self._readback()
        rows = {row['evidence']['id']: row for row in readback['report_pointers']}
        self.assertEqual({'id': h.PRODUCT, 'revision': 1}, rows[h.REPORT]['subject'])
        self.assertEqual('synthetic', rows[h.REPORT]['nature'])
        self.assertEqual({'id': 'independent', 'revision': 1}, rows['channel-checks']['subject'])
        for row in readback['report_pointers']:
            self.assertEqual(row['evidence']['revision'],
                             readback['state']['objects'][row['evidence']['id']]['revision'])

    def test_readback_has_no_expected_results_scores_or_probe_answers(self):
        readback = self._readback()
        text = json.dumps(readback, ensure_ascii=False)
        keys = {key.lower() for key in _walk_keys(readback)}
        self.assertFalse(keys & FORBIDDEN, str(keys & FORBIDDEN))
        self.assertNotIn('"rejected"', text)
        self.assertIn('No expected result', readback['representation_note'])
        self.assertIn('checks.json', readback['branch']['note'])
        checks = self._checks()
        for case in checks['cases']:
            self.assertNotIn(case['id'], text)

    def test_next_step_runs_from_the_exported_snapshot_without_hidden_state(self):
        readback = self._readback()
        contract = readback['write_contract']
        request = readback['next_step_request']
        self.assertEqual(readback['head'], contract['current_head'])
        state = readback['state']
        _, built, _ = h.build_chain()
        self.assertEqual(built, state)
        action = dict(contract['allowed_operation'])
        action['dimensions'] = dict(request['requested_values'])
        self.assertEqual(request['target']['part'], action['parts'][0])

        result = s.apply(state, [action], state['head'], ['SYN:exported-next-step'], 'synthetic')
        self.assertEqual('applied', result['status'], result['error'])
        updated = result['state']
        self.assertEqual(state['head'] + 1, updated['head'])
        progress = s.part_progress(updated, h.PRODUCT)
        self.assertEqual('reported_code_written',
                         progress['parts'][request['target']['part']]['dimensions']['implementation'])
        self.assertEqual(h.DRAFT, progress['parts'][h.NOTES_PART]['dimensions'])
        self.assertEqual('pending', s.version(updated, 'goal')['acceptance'])
        self.assertEqual(s.version(state, 'draft-code'), s.version(updated, 'draft-code'))
        self.assertEqual(s.version(state, 'channel-checks'), s.version(updated, 'channel-checks'))
        self.assertEqual({'id': h.PLAN, 'revision': 2},
                         s.version(updated, h.PRODUCT)['plan_usage']['sections']['turnstep']['plan'])

    def test_checks_keep_scoring_and_probes_off_the_branch(self):
        checks = self._checks()
        self.assertTrue(checks['summary']['ok'], checks['summary']['failed'])
        self.assertEqual([], checks['summary']['failed'])
        self.assertEqual(self._readback()['head'], checks['base_head'])
        for case in checks['cases']:
            self.assertEqual(checks['base_head'], case['input']['head'])
            if case['output']['status'] == 'rejected':
                self.assertTrue(case['output']['error'])
                self.assertTrue(case['unchanged_on_rejection'])
        self.assertEqual(2, len([case for case in checks['cases']
                                 if case['output']['status'] == 'rejected']))


class HandoffV2Tests(unittest.TestCase):
    def _readback(self):
        return json.loads((h.HANDOFF_DIR_V2 / 'readback.json').read_text(encoding='utf-8'))

    def _checks(self):
        return json.loads((h.HANDOFF_DIR_V2 / 'checks.json').read_text(encoding='utf-8'))

    def _resume_bytes(self):
        return (h.HANDOFF_DIR_V2 / h.RESUME_NAME).read_bytes()

    def test_v2_export_is_a_deterministic_rebuild(self):
        for name in h.GENERATED_V2:
            self.assertTrue((h.HANDOFF_DIR_V2 / name).is_file(), name)
        self.assertTrue(h.verify_handoff_v2(h.HANDOFF_DIR_V2))
        before = {name: (h.HANDOFF_DIR_V2 / name).read_bytes() for name in h.GENERATED_V2}
        h.export_handoff_v2(h.HANDOFF_DIR_V2)
        self.assertEqual(before, {name: (h.HANDOFF_DIR_V2 / name).read_bytes()
                                  for name in h.GENERATED_V2})

    def test_v2_contract_states_structure_and_domain_only(self):
        readback = self._readback()
        contract = readback['write_contract']
        contract_text = json.dumps(contract, ensure_ascii=False)
        self.assertNotIn('allowed_operation', json.dumps(readback, ensure_ascii=False))
        operation = contract['operation']
        self.assertEqual('advance_parts', operation['op'])
        self.assertEqual({'id', 'parts', 'dimensions'}, set(operation['fields']))
        fields = operation['fields']
        self.assertEqual(['completion', 'git', 'implementation'],
                         sorted(fields['dimensions']['allowed_keys']))
        for name in ('completion', 'implementation', 'git'):
            self.assertEqual(sorted(s.DIMENSION_VALUES[name]), fields['dimensions']['values'][name])
        self.assertNotIn('value', fields['id'])
        self.assertNotIn('default', contract_text)
        self.assertNotIn(h.PRODUCT, contract_text)
        self.assertNotIn(h.BEHAVIOR_PART, contract_text)
        self.assertEqual(readback['head'], contract['current_head'])
        self.assertEqual('complete state from resume-state.json',
                         contract['apply_arguments']['state'])

        request = readback['next_step_request']
        self.assertEqual({'product': h.PRODUCT, 'part': h.BEHAVIOR_PART}, request['target'])
        self.assertIn(h.PRODUCT, request['text'])
        self.assertIn('reported_code_written', request['text'])

    def test_v2_readback_holds_no_ready_to_submit_action(self):
        readback = self._readback()
        text = json.dumps(readback, ensure_ascii=False)
        ready = []

        def walk(value):
            if isinstance(value, dict):
                if 'op' in value and ({'parts', 'dimensions'} & set(value)):
                    ready.append(value)
                for child in value.values():
                    walk(child)
            elif isinstance(value, list):
                for child in value:
                    walk(child)

        walk(readback)
        self.assertEqual([], ready)
        self.assertNotIn('"rejected"', text)
        keys = {key.lower() for key in _walk_keys(readback)}
        self.assertFalse(keys & FORBIDDEN, str(keys & FORBIDDEN))
        for case in self._checks()['cases']:
            self.assertNotIn(case['id'], text)

    def test_v2_view_keeps_current_data_and_object_history(self):
        readback = self._readback()
        _, state, _ = h.build_chain()
        view = readback['view']
        self.assertEqual(state['head'], view['head'])
        self.assertEqual(state['head'], readback['head'])
        self.assertFalse(view['complete'])
        self.assertNotIn('changes', view)
        self.assertEqual(state['objects'], view['objects'])
        self.assertEqual(state['versions'], view['versions'])
        self.assertEqual(state['items'], view['items'])
        self.assertEqual(state['relations'], view['relations'])
        self.assertEqual(state['responsibility'], view['responsibility'])
        self.assertEqual(s.version(state, h.PLAN, 1), view['versions'][h.PLAN]['1'])
        self.assertNotIn('before', set(_walk_keys(readback)))
        self.assertNotIn('after', set(_walk_keys(readback)))

    def test_v2_records_keep_each_change_action_basis_and_reference(self):
        readback = self._readback()
        _, state, _ = h.build_chain()
        records = readback['records']
        self.assertEqual(list(range(1, state['head'] + 1)), [row['change'] for row in records])
        self.assertEqual(4, len([row for row in records
                                 if row['origin'] == 'synthetic_continuation']))
        for row in records:
            self.assertEqual(['actions', 'anchor', 'basis', 'change', 'changed_paths', 'nature',
                              'origin', 'references'], sorted(row))
            self.assertTrue(row['basis'])
            self.assertTrue(row['actions'])
            self.assertTrue(row['changed_paths'])
        produced = next(row for row in records if row['anchor'] == 'handoff-produce-v2')
        self.assertEqual('produce', produced['actions'][0]['op'])
        self.assertEqual(2, produced['actions'][0]['part_count'])
        self.assertEqual(h.ATTEMPT, produced['actions'][0]['attempt'])
        for path in produced['changed_paths']:
            self.assertLessEqual(path.count('/'), 4, path)

    def test_v2_plan_authority_and_report_links_survive_compression(self):
        readback = self._readback()
        authority = readback['plan_authority']
        self.assertEqual({'id': h.PLAN, 'revision': 2},
                         authority['product_plan_usage'][h.PRODUCT]['sections']['turnstep'])
        self.assertEqual({'id': h.PLAN, 'revision': 1}, authority['product_initial_plan'][h.PRODUCT])
        self.assertEqual({'id': h.PLAN, 'revision': 1},
                         authority['attempt_begin_plan'][h.ATTEMPT])
        self.assertEqual([{'plan': {'id': h.PLAN, 'revision': 1},
                           'scope': ['channel', 'reference', 'turnstep'], 'change': 3},
                          {'plan': {'id': h.PLAN, 'revision': 2},
                           'scope': ['turnstep'], 'change': 10}],
                         authority['attempt_adoptions'][h.ATTEMPT])
        self.assertEqual('migration', authority['plan_owner'][h.PLAN])
        self.assertIn('only authority', authority['rule'])
        self.assertEqual(2, len(readback['view']['relations']))
        self.assertIn(h.REPORT, readback['view']['objects'])
        self.assertIn('S029', readback['source_entry']['sources'])

    def test_v2_readback_stays_under_the_size_budget(self):
        text = (h.HANDOFF_DIR_V2 / 'readback.json').read_text(encoding='utf-8')
        v1_text = (h.HANDOFF_DIR / 'readback.json').read_text(encoding='utf-8')
        self.assertLess(len(text), 45000, len(text))
        self.assertLess(len(text), len(v1_text))

    def test_v2_resume_state_matches_the_pointer_and_executes_the_next_step(self):
        readback = self._readback()
        raw = self._resume_bytes()
        self.assertEqual(h.RESUME_NAME, readback['resume']['path'])
        self.assertEqual(hashlib.sha256(raw).hexdigest(), readback['resume']['sha256'])
        self.assertEqual(len(raw.decode('utf-8')), readback['resume']['characters'])
        state = json.loads(raw.decode('utf-8'))['state']
        _, built, _ = h.build_chain()
        self.assertEqual(built, state)
        self.assertEqual(list(range(1, state['head'] + 1)),
                         [change['number'] for change in state['changes']])

        result = s.apply(state, [dict(h.NEXT_ACTION)], state['head'],
                         ['SYN:exported-next-step'], 'synthetic')
        self.assertEqual('applied', result['status'], result['error'])
        updated = result['state']
        self.assertEqual(state['head'] + 1, updated['head'])
        progress = s.part_progress(updated, h.PRODUCT)
        self.assertEqual('reported_code_written',
                         progress['parts'][h.BEHAVIOR_PART]['dimensions']['implementation'])
        self.assertEqual(h.DRAFT, progress['parts'][h.NOTES_PART]['dimensions'])
        self.assertEqual('pending', s.version(updated, 'goal')['acceptance'])
        self.assertEqual(s.version(state, 'draft-code'), s.version(updated, 'draft-code'))
        self.assertEqual(s.version(state, 'channel-checks'), s.version(updated, 'channel-checks'))
        self.assertEqual({'id': h.PLAN, 'revision': 2},
                         s.version(updated, h.PRODUCT)['plan_usage']['sections']['turnstep']['plan'])
        self.assertEqual(s.version(state, h.PLAN, 1), s.version(updated, h.PLAN, 1))

    def test_v2_checks_hold_the_expected_results(self):
        checks = self._checks()
        self.assertTrue(checks['summary']['ok'], checks['summary']['failed'])
        self.assertEqual([], checks['summary']['failed'])
        self.assertEqual(self._readback()['head'], checks['base_head'])
        self.assertIn('resume-state-executes', [check['id'] for check in checks['checks']])
        self.assertIn('readback-size-budget', [check['id'] for check in checks['checks']])
        self.assertEqual(2, len([case for case in checks['cases']
                                 if case['output']['status'] == 'rejected']))
        for case in checks['cases']:
            self.assertEqual(checks['base_head'], case['input']['head'])
            if case['output']['status'] == 'rejected':
                self.assertTrue(case['output']['error'])
                self.assertTrue(case['unchanged_on_rejection'])


if __name__ == '__main__':
    unittest.main()
