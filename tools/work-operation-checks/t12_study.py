"""T12 controlled object study. Additive offline experiment, Python stdlib only."""
from copy import deepcopy
from pathlib import Path
import argparse
import json

HERE = Path(__file__).resolve().parent
FIXTURE = json.loads((HERE / 't12_experiment_fixture.json').read_text(encoding='utf-8'))
KNOWN_BASIS = {x['id'] for x in FIXTURE['facts'] + FIXTURE['supplements']}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def fresh(layout='parent', plans='independent'):
    require(layout in {'parent', 'relation', 'child'}, 'unknown responsibility layout')
    require(plans in {'independent', 'embedded'}, 'unknown plan placement')
    return {'head': 0, 'layout': layout, 'plans': plans, 'objects': {}, 'versions': {}, 'changes': [], 'responsibility': None}


def snapshot(state):
    return deepcopy({k: v for k, v in state.items() if k != 'changes'})


def current_plan(state, pid):
    if state['plans'] == 'independent':
        obj = state['objects'].get(pid)
    else:
        found = [p for o in state['objects'].values() for key, p in o.get('plan_records', {}).items() if key == pid]
        require(len(found) <= 1, 'duplicate embedded plan identity')
        obj = found[0] if found else None
    require(obj is not None and obj['kind'] == 'plan', 'plan missing: ' + pid)
    return deepcopy(obj)


def version(state, oid, revision=None):
    require(revision is None or type(revision) is int and revision > 0, 'invalid version')
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


def ref(state, value):
    require(isinstance(value, dict) and set(value) == {'id', 'revision'}, 'exact reference required')
    version(state, value['id'], value['revision'])
    return deepcopy(value)


def new_object(state, oid, kind, **fields):
    require(isinstance(oid, str) and oid, 'identity required')
    try:
        version(state, oid)
    except ValueError:
        pass
    else:
        raise ValueError('identity already exists')
    state['objects'][oid] = {'id': oid, 'kind': kind, 'revision': 1, 'identity_origin': 'researcher_created', **deepcopy(fields)}


def touch(state, oid, kind):
    obj = state['objects'].get(oid)
    require(obj is not None and obj['kind'] == kind, 'wrong or missing object type')
    state['versions'].setdefault(oid, {})[str(obj['revision'])] = deepcopy(obj)
    obj['revision'] += 1
    return obj


def save_plan(state, plan, owner):
    try:
        previous = current_plan(state, plan['id'])
    except ValueError:
        previous = None
    if previous:
        state['versions'].setdefault(plan['id'], {})[str(previous['revision'])] = previous
    if state['plans'] == 'independent':
        state['objects'][plan['id']] = deepcopy(plan)
    else:
        host = touch(state, owner, 'attempt')
        host.setdefault('plan_records', {})[plan['id']] = deepcopy(plan)


def execute(state, action):
    """All public updates use this dispatcher; no generic patch is accepted."""
    op = action['op']
    if op == 'goal':
        new_object(state, action['id'], 'goal', scope=action['scope'], acceptance='pending', origin='researcher_created')
    elif op == 'begin':
        goal = state['objects'].get(action['goal'])
        require(goal is not None and goal['kind'] == 'goal', 'goal required')
        plan = None if action.get('plan') is None else ref(state, action['plan'])
        if plan:
            require(version(state, plan['id'], plan['revision'])['kind'] == 'plan', 'attempt requires plan')
        new_object(state, action['id'], 'attempt', goal=action['goal'], scope=action['scope'], plan=plan,
                   status='active', outcome='unknown', location=action.get('location', 'unknown'))
    elif op == 'plan':
        require(action['id'] not in state['objects'], 'plan identity exists')
        try:
            current_plan(state, action['id'])
        except ValueError:
            pass
        else:
            raise ValueError('plan identity exists')
        owner = state['objects'].get(action['owner'])
        require(owner is not None and owner['kind'] == 'attempt', 'plan owner required')
        require(isinstance(action['sections'], dict) and action['sections'], 'structured plan sections required')
        plan = {'id': action['id'], 'kind': 'plan', 'revision': 1, 'identity_origin': 'researcher_created', 'owner': action['owner'],
                'sections': deepcopy(action['sections']), 'links': deepcopy(action.get('links', []))}
        for link in plan['links']:
            require(link['kind'] in {'historical_reference', 'depends_on'}, 'typed plan link required')
            ref(state, link['target'])
        save_plan(state, plan, action['owner'])
    elif op == 'change_plan':
        plan = current_plan(state, action['id'])
        edits, removals = action.get('edits', {}), action.get('remove', [])
        require(isinstance(edits, dict) and isinstance(removals, list), 'plan update type')
        require(edits or removals, 'empty plan update')
        require(not set(edits) & set(removals) and len(set(removals)) == len(removals), 'plan update overlap')
        require(set(removals) <= set(plan['sections']), 'unknown plan section')
        for key in removals:
            plan['sections'][key] = {'status': 'superseded', 'description': plan['sections'][key]['description']}
        for key, value in edits.items():
            require(isinstance(value, dict) and set(value) == {'status', 'description'}, 'section structure required')
            plan['sections'][key] = deepcopy(value)
        plan['revision'] += 1
        save_plan(state, plan, plan['owner'])
    elif op == 'produce':
        attempt = state['objects'].get(action['attempt'])
        require(attempt is not None and attempt['kind'] == 'attempt' and attempt['status'] == 'active', 'active attempt required')
        dimensions = action['dimensions']
        require(set(dimensions) == {'implementation', 'git', 'acceptance'}, 'three separate product dimensions required')
        require(dimensions['acceptance'] in {'pending', 'unknown'}, 'implementation cannot accept product')
        new_object(state, action['id'], 'product', attempt=action['attempt'], plan=deepcopy(attempt['plan']),
                   parts={p: 'present' for p in action['parts']}, dimensions=dimensions,
                   location=action['location'], nature=action['nature'])
    elif op == 'end':
        old = state['objects'].get(action['id'])
        require(old is not None and old['kind'] == 'attempt' and old['status'] == 'active', 'active attempt required')
        obj = touch(state, action['id'], 'attempt')
        obj['status'], obj['outcome'] = 'ended', action['outcome']
    elif op == 'withdraw_parts':
        old = state['objects'].get(action['id'])
        require(old is not None and old['kind'] == 'product', 'product required')
        require(bool(action['parts']) and set(action['parts']) <= set(old['parts']), 'known nonempty withdrawal range required')
        obj = touch(state, action['id'], 'product')
        for part in action['parts']:
            obj['parts'][part] = 'withdrawn'
    elif op == 'report':
        subject = ref(state, action['subject'])
        require(action['nature'] in {'author_report', 'documented', 'synthetic'}, 'report nature required')
        new_object(state, action['id'], 'evidence', subject=subject, scope=action['scope'],
                   findings=action['findings'], nature=action['nature'])
    elif op == 'accept_goal':
        require(action.get('actor_role') == 'acceptor' and action.get('criteria') and action.get('decision') == 'accept', 'explicit acceptance authority and criteria required')
        require(action.get('evidence'), 'acceptance evidence required')
        for item in action['evidence']:
            ref(state, item)
        obj = touch(state, action['id'], 'goal')
        obj['acceptance'] = 'accepted'
        obj['decision'] = {'actor': action['actor'], 'criteria': action['criteria'], 'evidence': deepcopy(action['evidence'])}
    elif op in {'responsibility_init', 'assign', 'transfer', 'share', 'unassign', 'unknown'}:
        import t12_responsibility as responsibility
        if op == 'responsibility_init':
            require(state['responsibility'] is None, 'responsibility already initialized')
            state['responsibility'] = responsibility.new(state['layout'], action['tokens'], action['holders'], unknown=action.get('unknown', True))
        else:
            require(state['responsibility'] is not None, 'responsibility missing')
            result = responsibility.apply(state['responsibility'], action, state['responsibility']['revision'])
            require(result['status'] == 'applied', result.get('error', 'responsibility rejected'))
            state['responsibility'] = result['state']
    else:
        raise ValueError('unsupported update: ' + str(op))


def differences(before, after, prefix=''):
    if isinstance(before, dict) and isinstance(after, dict):
        result = []
        for key in sorted(set(before) | set(after)):
            name = prefix + '/' + key
            if key not in before or key not in after:
                result.append(name)
            else:
                result.extend(differences(before[key], after[key], name))
        return result
    return [] if before == after else [prefix]


def apply(state, actions, expected, basis, nature='synthetic'):
    """A batch either commits all effects and provenance, or returns its original input."""
    original, work = deepcopy(state), deepcopy(state)
    try:
        require(type(expected) is int and expected == state['head'], 'stale predecessor')
        require(isinstance(actions, list) and actions, 'nonempty actions required')
        require(isinstance(basis, list) and basis and all(x in KNOWN_BASIS or x.startswith('SYN:') for x in basis), 'known evidence or synthetic label required')
        require(nature in {'source_record', 'synthetic'}, 'change nature')
        require(nature != 'source_record' or all(x in KNOWN_BASIS for x in basis), 'synthetic basis is not history')
        for action in actions:
            require(isinstance(action, dict), 'action structure')
            execute(work, action)
        before = snapshot(state)
        work['head'] += 1
        after = snapshot(work)
        paths = differences(before, after)
        change = {'number': work['head'], 'basis': deepcopy(basis), 'nature': nature,
                  'actions': deepcopy(actions), 'before': before, 'after': after, 'changed_paths': paths}
        work['changes'].append(change)
        return {'status': 'applied', 'state': work, 'changed_paths': paths, 'error': None}
    except (ValueError, KeyError, TypeError) as error:
        return {'status': 'rejected', 'state': original, 'changed_paths': [], 'error': str(error)}


def at(state, number):
    require(type(number) is int and 0 <= number <= state['head'], 'history position')
    if not number:
        return fresh(state['layout'], state['plans'])
    result = deepcopy(state['changes'][number - 1]['after'])
    result['changes'] = deepcopy(state['changes'][:number])
    return result


def actual_ref(state, oid):
    obj = version(state, oid)
    return {'id': oid, 'revision': obj['revision']}


def real_path(layout='parent', plans='independent'):
    s = fresh(layout, plans)
    def step(fact, actions):
        nonlocal s
        result = apply(s, actions, s['head'], [fact], 'source_record')
        require(result['status'] == 'applied', result['error'])
        s = result['state']
    sections = lambda **items: {k: {'status': 'recorded_arrangement', 'description': v} for k,v in items.items()}
    step('T12.01', [
        {'op':'goal','id':'goal','scope': FIXTURE['feature_families']},
        {'op':'begin','id':'batch','goal':'goal','scope':FIXTURE['feature_families'],'location':'PR #4565'}])
    step('T12.02', [
        {'op':'report','id':'regression','subject':actual_ref(s,'batch'),'scope':'original batch',
         'findings':['author reports reverted eight minutes after merge','six benchmarks miss new streaming hot paths'],'nature':'author_report'},
        {'op':'end','id':'batch','outcome':'author_reported_reverted'},
        {'op':'begin','id':'migration','goal':'goal','scope':FIXTURE['feature_families'],'location':'recorded follow-up arrangement'}])
    step('T12.03', [
        {'op':'plan','id':'migration-plan','owner':'migration','sections':sections(
            channel='completed independent features stay in presentation channel',
            turnstep='unfinished code continues in turnstep worktree',
            reference='original PR retained as reference; experiments not automatically transferred'),
         'links':[{'kind':'historical_reference','target':actual_ref(s,'batch')}] }])
    planref = actual_ref(s, 'migration-plan')
    step('T12.04', [
        {'op':'begin','id':'independent','goal':'goal','scope':['independent visuals','summary','filter'],'plan':planref,'location':'presentation channel'},
        {'op':'produce','id':'independent-code','attempt':'independent','parts':['visual','summary','filter'],
         'dimensions':{'implementation':'reported_code_written','git':'reported_committed','acceptance':'pending'},'location':'presentation channel','nature':'documented'},
        {'op':'begin','id':'turnstep','goal':'goal','scope':['whole-Turn status','notifications','other behaviors not fully enumerated'],'plan':planref,'location':'turnstep worktree'},
        {'op':'produce','id':'draft-code','attempt':'turnstep','parts':['whole-Turn status','notifications','other unspecified behavior'],
         'dimensions':{'implementation':'reported_draft_written','git':'unstaged','acceptance':'pending'},'location':'turnstep worktree','nature':'documented'}])
    step('T12.05', [
        {'op':'begin','id':'grouping','goal':'goal','scope':['grouping foundation and remaining product integration'],'location':'source documents; exact worktree unknown'},
        {'op':'produce','id':'group-foundation','attempt':'grouping','parts':['Definition-owned grouping foundation'],
         'dimensions':{'implementation':'reported_implemented','git':'unknown','acceptance':'unknown'},'location':'S022 implemented note','nature':'documented'},
        {'op':'report','id':'grouping-pending','subject':{'id':'grouping','revision':1},'scope':'product grouping behavior and performance','findings':['still incomplete'],'nature':'documented'}])
    step('T12.06', [
        {'op':'report','id':'channel-checks','subject':actual_ref(s,'independent'),'scope':'presentation channel; not turnstep worktree',
         'findings':['build/lint/coverage author-reported pass','real-model GUI demo and performance pending'],'nature':'author_report'}])
    step('S028.partial_replacement', [
        {'op':'plan','id':'architecture','owner':'migration','sections':sections(
            presentation='presentation policy and per-Turn eligibility rationale retained',
            grouping='event fold, builder materialization, Step ranges and changedLocationData route'), 'links':[]},
        {'op':'change_plan','id':'architecture','remove':['grouping'],
         'edits':{'foundation':{'status':'reported_implemented_route','description':'Definition-owned grouping foundation supersedes old grouping route'}}}])
    return s


def readback(state):
    objects = deepcopy(state['objects'])
    plans = {pid: current_plan(state, pid) for pid in ['migration-plan','architecture']}
    if state['plans'] == 'embedded':
        for obj in objects.values():
            obj.pop('plan_records', None)
    return {'objects': objects, 'plan_records': plans, 'history': [
        {'number': c['number'], 'basis': c['basis'], 'nature': c['nature'], 'actions': c['actions']}
        for c in state['changes']], 'unknowns': FIXTURE['unknowns'],
        'identity_origin': 'researcher-created identities; recorded content attributed by basis'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=False)
    for layout in ['parent', 'relation', 'child']:
        state = real_path(layout)
        (out / (layout + '-real.json')).write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')
    (out / 'readback.json').write_text(json.dumps(readback(real_path()), ensure_ascii=False, indent=2), encoding='utf-8')
    print(str(out.resolve()))
