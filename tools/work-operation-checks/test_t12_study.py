from copy import deepcopy
import unittest
import t12_study as s


class ObjectStudyTests(unittest.TestCase):
    def update(self, state, *actions):
        result = s.apply(state, list(actions), state['head'], ['SYN:test'])
        self.assertEqual('applied', result['status'], result['error'])
        return result['state']

    def test_real_facts_have_precise_semantic_landing_and_separate_dimensions(self):
        for placement in ['independent', 'embedded']:
            state = s.real_path(plans=placement)
            self.assertEqual([x['id'] for x in s.FIXTURE['facts']], [c['basis'][0] for c in state['changes'][:6]])
            self.assertEqual('author_reported_reverted', s.version(state, 'batch')['outcome'])
            self.assertEqual('reported_committed', s.version(state,'independent-code')['dimensions']['git'])
            self.assertEqual('unstaged', s.version(state,'draft-code')['dimensions']['git'])
            self.assertEqual('pending', s.version(state,'goal')['acceptance'])
            self.assertEqual('unknown', s.version(state,'group-foundation')['dimensions']['acceptance'])
            self.assertIn('not turnstep', s.version(state,'channel-checks')['scope'])
            self.assertIsNone(s.version(state,'grouping')['plan'])

    def test_partial_architecture_replacement_keeps_rationale_and_old_version(self):
        for placement in ['independent', 'embedded']:
            state = s.real_path(plans=placement)
            old,new=s.version(state,'architecture',1),s.current_plan(state,'architecture')
            self.assertEqual('recorded_arrangement', old['sections']['grouping']['status'])
            self.assertEqual('superseded', new['sections']['grouping']['status'])
            self.assertEqual(old['sections']['presentation'],new['sections']['presentation'])
            self.assertNotIn('foundation',old['sections'])

    def test_plan_change_preserves_prior_implementation_reference(self):
        for placement in ['independent','embedded']:
            state=s.real_path(plans=placement)
            product=s.version(state,'independent-code')
            state=self.update(state,{'op':'change_plan','id':'migration-plan','edits':{'next':{'status':'planned','description':'next test'}}})
            self.assertEqual(2,s.current_plan(state,'migration-plan')['revision'])
            self.assertEqual(product,s.version(state,'independent-code'))
            self.assertEqual(1,product['plan']['revision'])
            self.assertNotIn('next',s.version(state,'migration-plan',1)['sections'])

    def test_close_attempt_retains_goal_products_and_other_work(self):
        state=s.real_path();before=deepcopy(state)
        state=self.update(state,{'op':'end','id':'independent','outcome':'stopped for synthetic test'})
        for oid in ['goal','independent-code','turnstep','draft-code']:
            self.assertEqual(s.version(before,oid),s.version(state,oid))
        self.assertEqual('ended',s.version(state,'independent')['status'])

    def test_partial_withdrawal_changes_only_named_part(self):
        state=s.real_path();old=s.version(state,'independent-code')
        state=self.update(state,{'op':'withdraw_parts','id':'independent-code','parts':['visual']})
        new=s.version(state,'independent-code')
        self.assertEqual('withdrawn',new['parts']['visual'])
        self.assertEqual('present',new['parts']['summary'])
        self.assertEqual(old,s.version(state,'independent-code',1))

    def test_report_does_not_accept_goal_but_explicit_acceptance_can(self):
        state=s.real_path()
        state=self.update(state,{'op':'report','id':'new-check','subject':s.actual_ref(state,'independent-code'),
           'scope':'synthetic extra check','findings':['pass'],'nature':'synthetic'})
        self.assertEqual('pending',s.version(state,'goal')['acceptance'])
        state=self.update(state,{'op':'accept_goal','id':'goal','actor_role':'acceptor','actor':'synthetic-user',
           'criteria':['synthetic scope accepted'],'decision':'accept','evidence':[s.actual_ref(state,'new-check')]})
        self.assertEqual('accepted',s.version(state,'goal')['acceptance'])

    def test_stale_predecessor_and_partial_failure_leave_exact_original(self):
        state=s.real_path();before=deepcopy(state)
        action={'op':'end','id':'independent','outcome':'test'}
        result=s.apply(state,[action],state['head']-1,['SYN:test'])
        self.assertEqual('rejected',result['status']);self.assertEqual(before,result['state'])
        result=s.apply(state,[action,{'op':'withdraw_parts','id':'missing','parts':['x']}],state['head'],['SYN:test'])
        self.assertEqual('rejected',result['status']);self.assertEqual(before,result['state']);self.assertEqual(before,state)

    def test_no_patch_path_and_no_promoting_product_acceptance(self):
        state=s.real_path()
        for action in [{'op':'revise','id':'goal','delta':{'acceptance':'accepted'}},
                       {'op':'accept_goal','id':'goal','decision':'accept'},
                       {'op':'produce','id':'bad-product','attempt':'independent','parts':['x'],
                        'dimensions':{'implementation':'written','git':'committed','acceptance':'accepted'},'location':'test','nature':'synthetic'}]:
            result=s.apply(state,[action],state['head'],['SYN:test'])
            self.assertEqual('rejected',result['status']);self.assertEqual(state,result['state'])

    def test_history_and_queries_are_detached_and_do_not_see_future(self):
        state=s.real_path();past=s.at(state,3)
        self.assertNotIn('draft-code',past['objects'])
        self.assertNotIn('architecture',past['objects'])
        self.assertEqual('active',s.version(past,'migration')['status'])
        view=s.readback(state);view['objects']['goal']['acceptance']='fake'
        self.assertEqual('pending',s.version(state,'goal')['acceptance'])

    def test_source_and_synthetic_labels_cannot_be_confused(self):
        state=s.fresh()
        r=s.apply(state,[{'op':'goal','id':'g','scope':['x']}],0,['SYN:test'],'source_record')
        self.assertEqual('rejected',r['status'])


if __name__=='__main__':
    unittest.main()
