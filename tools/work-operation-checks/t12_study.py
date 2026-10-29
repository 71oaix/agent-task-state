"""T12 controlled object study. Additive offline experiment, Python stdlib only."""
from copy import deepcopy
from pathlib import Path
import argparse
import json

HERE = Path(__file__).resolve().parent
FIXTURE = json.loads((HERE / 't12_experiment_fixture.json').read_text(encoding='utf-8'))
KNOWN_BASIS = {x['id'] for x in FIXTURE['facts'] + FIXTURE['supplements']}
ACTION_KEYS = {
    'goal': {'op','id','scope'}, 'begin': {'op','id','goal','scope','plan','location'},
    'plan': {'op','id','owner','sections','links'}, 'change_plan': {'op','id','edits','remove'},
    'produce': {'op','id','attempt','parts','dimensions','location','nature','plan_scope'},
    'adopt_plan': {'op','id','plan','scope','basis'},
    'end': {'op','id','outcome','remaining'}, 'reopen': {'op','id'},
    'advance_product': {'op','id','dimensions'},
    'withdraw_parts': {'op','id','parts'}, 'report': {'op','id','subject','scope','findings','nature'},
    'accept_goal': {'op','id','actor_role','actor','criteria','decision','evidence'},
    'responsibility_init': {'op','tokens','holders','unknown','owner'},
    'assign': {'op','token','to'}, 'transfer': {'op','token','from','to'},
    'share': {'op','token','holders'}, 'unassign': {'op','token','from'}, 'unknown': {'op','token'},
    'relate': {'op','id','kind','from','to','basis','nature','meaning'},
    'register_items': {'op','items'}
}
DIMENSION_VALUES = {
    'completion': {'unknown','not_started','incomplete','in_progress',
                   'reported_migration_complete','reported_complete','complete'},
    'implementation': {'unknown','not_started','reported_draft_written','reported_code_written',
                       'reported_implemented','implemented'},
    'git': {'unknown','not_started','unstaged','staged','reported_committed','committed'}
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def fresh(layout='parent', plans='independent'):
    require(layout in {'parent', 'relation', 'child'}, 'unknown responsibility layout')
    require(plans in {'independent', 'embedded'}, 'unknown plan placement')
    return {'head': 0, 'layout': layout, 'plans': plans, 'objects': {}, 'versions': {}, 'changes': [],
            'relations': {}, 'items': {}, 'responsibility': None}


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
    """A public reference must name one existing revision; None/bool/0 are not revisions."""
    require(isinstance(value, dict) and set(value) == {'id', 'revision'}, 'exact reference required')
    require(isinstance(value['id'], str) and bool(value['id']), 'exact reference identity required')
    require(type(value['revision']) is int and value['revision'] > 0, 'exact positive revision required')
    version(state, value['id'], value['revision'])
    return deepcopy(value)


def _known_basis(values, label):
    require(isinstance(values, list) and values and all(
        isinstance(x, str) and (x in KNOWN_BASIS or x.startswith('SYN:')) for x in values), label)


def goal_of(state, obj):
    """Resolve the goal an object belongs to; evidence carries its goal from report time."""
    if obj['kind'] == 'goal':
        return obj['id']
    if obj['kind'] == 'attempt':
        return obj.get('goal')
    if obj['kind'] == 'product':
        attempt = state['objects'].get(obj.get('attempt'))
        require(attempt is not None and attempt['kind'] == 'attempt', 'product attempt missing')
        return attempt.get('goal')
    if obj['kind'] == 'evidence':
        return obj.get('goal')
    return None


def active_attempt(state, aid, label='attempt'):
    obj = state['objects'].get(aid)
    require(obj is not None and obj['kind'] == 'attempt', label + ' must reference an attempt')
    require(obj['status'] == 'active', label + ' must be active')
    return obj


def plan_sections(state, attempt_id):
    """Return the effective plan reference per section; later explicit adoption wins."""
    attempt = state['objects'].get(attempt_id)
    require(attempt is not None and attempt['kind'] == 'attempt', 'attempt required')
    result = {}
    for record in attempt.get('plan_adoptions', []):
        for name in record['scope']:
            result[name] = {'plan': deepcopy(record['plan']), 'change': record['change']}
    return result


def _plan_usage(state, attempt, requested):
    """Resolve which plan revision each produced section used.

    ``plan_usage`` is the only authority for actually used plan revisions.
    Without ``plan_scope`` the legacy convention is the begin-time plan revision
    for exactly its own sections, but only while the attempt has never explicitly
    adopted another version.  Once an explicit adoption exists, omitting the
    field would silently hide the choice and is rejected.
    """
    if requested is None:
        explicit = [r for r in attempt.get('plan_adoptions', []) if r.get('origin') != 'begin']
        require(not explicit, 'explicit plan scope required after explicit adoption')
        begin = next((r for r in attempt.get('plan_adoptions', []) if r.get('origin') == 'begin'), None)
        if begin is None:
            return {'mode': 'legacy_initial_plan', 'scope': [], 'sections': {}}
        sections = {name: {'plan': deepcopy(begin['plan']), 'change': begin['change']} for name in begin['scope']}
        return {'mode': 'legacy_initial_plan', 'scope': list(begin['scope']), 'sections': sections}
    require(isinstance(requested, list) and requested
            and all(isinstance(x, str) and bool(x) for x in requested)
            and len(set(requested)) == len(requested), 'explicit unique plan scope required')
    effective = plan_sections(state, attempt['id'])
    missing = [x for x in requested if x not in effective]
    require(not missing, 'plan scope was not adopted: ' + ','.join(missing))
    return {'mode': 'explicit_scope', 'scope': list(requested),
            'sections': {name: deepcopy(effective[name]) for name in requested}}


def _relation_endpoint(state, value, label):
    """A relation endpoint is an existing object plus a precise scope inside it."""
    require(isinstance(value, dict) and set(value) == {'object', 'scope'},
            label + ' must be an object+scope endpoint')
    require(isinstance(value['object'], str) and value['object'] in state['objects'],
            label + ' object must exist')
    require(isinstance(value['scope'], str) and value['scope'].strip(),
            label + ' scope is required')
    obj = state['objects'][value['object']]
    if obj['kind'] == 'product':
        require(value['scope'] in obj['parts'], label + ' scope must name a product part')
    elif obj['kind'] == 'attempt':
        require(value['scope'] in obj.get('scope', []), label + ' scope must be in the attempt scope')
    else:
        require(False, label + ' must be a product or attempt')
    return deepcopy(value)


def relations_for(state, oid, scope=None):
    """Return typed relations touching one object(+scope), from either end."""
    require(oid in state['objects'], 'unknown relation endpoint object')
    require(scope is None or isinstance(scope, str) and bool(scope), 'relation scope filter')
    rows = []
    for rid, relation in sorted(state['relations'].items()):
        for direction, near, far in (('outgoing', relation['from'], relation['to']),
                                     ('incoming', relation['to'], relation['from'])):
            if near['object'] == oid and (scope is None or near['scope'] == scope):
                rows.append({'relation': rid, 'direction': direction, 'kind': relation['kind'],
                             'from': deepcopy(relation['from']), 'to': deepcopy(relation['to']),
                             'basis': deepcopy(relation['basis']), 'nature': relation['nature'],
                             'other': deepcopy(far)})
    return rows


def relations_for_item(state, item_id):
    """Resolve an S029 item to its product part and query both relation ends."""
    require(item_id in state['items'], 'unknown item: ' + str(item_id))
    item = state['items'][item_id]
    endpoint = {'object': item['product'], 'scope': item['part']}
    return {'item': item_id, 'endpoint': deepcopy(endpoint),
            'relations': relations_for(state, endpoint['object'], endpoint['scope'])}


def s029_items(state):
    """Read the S029 item records together with their current product projection."""
    rows = {}
    for item_id, item in sorted(state['items'].items()):
        product = state['objects'].get(item['product'])
        require(product is not None and product['kind'] == 'product', 'item product missing: ' + item_id)
        require(item['part'] in product['parts'], 'item part missing: ' + item_id)
        row = deepcopy(item)
        row['current'] = {
            'product_revision': product['revision'],
            'part_state': product['parts'][item['part']],
            'dimensions': deepcopy(product['dimensions']),
            'matches_source_status': all(product['dimensions'][name] == item['status'][name]
                                         for name in ('completion', 'implementation', 'git', 'acceptance'))
        }
        rows[item_id] = row
    return {'items': rows,
            'note': 'item statuses are S029 records copied into this controlled study; current is the state projection, not independent verification'}


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


def _execute(state, action, basis):
    """All public updates use this dispatcher; no generic patch is accepted."""
    op = action['op']
    require(op in ACTION_KEYS and set(action) <= ACTION_KEYS[op], 'unsupported operation or unexpected update fields')
    if op == 'goal':
        new_object(state, action['id'], 'goal', scope=action['scope'], acceptance='pending', origin='researcher_created')
    elif op == 'begin':
        goal = state['objects'].get(action['goal'])
        require(goal is not None and goal['kind'] == 'goal', 'goal required')
        plan = None if action.get('plan') is None else ref(state, action['plan'])
        adoptions = []
        if plan:
            plan_obj = version(state, plan['id'], plan['revision'])
            require(plan_obj['kind'] == 'plan', 'attempt requires plan')
            require(state['objects'][plan_obj['owner']]['goal'] == action['goal'], 'plan belongs to a different goal; explicit adaptation required')
            adoptions = [{'plan': deepcopy(plan), 'scope': sorted(plan_obj['sections']),
                          'basis': deepcopy(basis), 'change': state['head'] + 1, 'origin': 'begin'}]
        new_object(state, action['id'], 'attempt', goal=action['goal'], scope=action['scope'], plan=plan,
                   plan_adoptions=adoptions, status='active', outcome='unknown',
                   location=action.get('location', 'unknown'))
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
    elif op == 'adopt_plan':
        attempt = active_attempt(state, action['id'])
        plan = ref(state, action['plan'])
        plan_obj = version(state, plan['id'], plan['revision'])
        require(plan_obj['kind'] == 'plan', 'plan required')
        require(state['objects'][plan_obj['owner']]['goal'] == attempt['goal'],
                'plan belongs to a different goal; explicit adaptation required')
        scope = action['scope']
        require(isinstance(scope, list) and scope and all(isinstance(x, str) and bool(x) for x in scope)
                and len(set(scope)) == len(scope), 'explicit unique adoption scope required')
        require(set(scope) <= set(plan_obj['sections']), 'adoption scope must name sections of that plan revision')
        _known_basis(action['basis'], 'known adoption basis required')
        record = {'plan': plan, 'scope': sorted(scope), 'basis': deepcopy(action['basis']),
                  'change': state['head'] + 1, 'origin': 'adopt_plan'}
        obj = touch(state, action['id'], 'attempt')
        obj.setdefault('plan_adoptions', []).append(record)
    elif op == 'produce':
        attempt = active_attempt(state, action['attempt'])
        dimensions = action['dimensions']
        require(isinstance(dimensions, dict) and set(dimensions) == {'completion', 'implementation', 'git', 'acceptance'},
                'four separate product dimensions required')
        require(dimensions['acceptance'] in {'pending', 'unknown'}, 'implementation cannot accept product')
        for name in ('completion', 'implementation', 'git'):
            require(isinstance(dimensions[name], str) and dimensions[name] in DIMENSION_VALUES[name],
                    'controlled dimension value required: ' + name)
        usage = _plan_usage(state, attempt, action.get('plan_scope'))
        initial_plan = deepcopy(attempt['plan'])
        fields = {'attempt': action['attempt'], 'initial_plan': initial_plan, 'plan_usage': usage,
                  'parts': {p: 'present' for p in action['parts']}, 'dimensions': dimensions,
                  'location': action['location'], 'nature': action['nature']}
        if action.get('plan_scope') is None:
            # Compatibility projection for old callers that never name a scope.
            # It is only written when it is equal to the actual (legacy) usage and
            # is never an authority for an explicit partial adoption.
            fields['plan'] = deepcopy(initial_plan)
        new_object(state, action['id'], 'product', **fields)
    elif op == 'end':
        old = state['objects'].get(action['id'])
        require(old is not None and old['kind'] == 'attempt' and old['status'] == 'active', 'active attempt required')
        require(action.get('remaining') in {None, 'retained_unresolved'}, 'remaining must be retained_unresolved when disclosed')
        if state['responsibility'] is not None:
            import t12_responsibility as responsibility
            outstanding = [t for t,v in responsibility.project(state['responsibility']).items() if action['id'] in v['holders']]
            if state['responsibility'].get('owner') == action['id']:
                outstanding += [t for t,v in responsibility.project(state['responsibility']).items() if v['state'] in {'unknown','unassigned'}]
            require(not outstanding or action.get('remaining') == 'retained_unresolved', 'ending holder must disclose remaining assigned responsibility')
        obj = touch(state, action['id'], 'attempt')
        obj['status'], obj['outcome'] = 'ended', action['outcome']
        if action.get('remaining'):
            obj['remaining_responsibility'] = action['remaining']
    elif op == 'reopen':
        old = state['objects'].get(action['id'])
        require(old is not None and old['kind'] == 'attempt' and old['status'] == 'ended', 'ended attempt required')
        obj = touch(state, action['id'], 'attempt')
        obj.setdefault('reopen_history', []).append(
            {'change': state['head'] + 1, 'prior_outcome': obj['outcome'],
             'remaining': obj.get('remaining_responsibility')})
        obj['status'], obj['outcome'] = 'active', 'unknown'
    elif op == 'advance_product':
        dimensions = action['dimensions']
        require(isinstance(dimensions, dict) and dimensions and set(dimensions) <= set(DIMENSION_VALUES), 'only explicit migration/implementation/git progress can advance product')
        for name, value in dimensions.items():
            require(isinstance(value, str) and value in DIMENSION_VALUES[name],
                    'controlled dimension value required: ' + name)
        old = state['objects'].get(action['id'])
        require(old is not None and old['kind']=='product', 'product required')
        obj = touch(state, action['id'], 'product')
        obj['dimensions'].update(deepcopy(dimensions))
    elif op == 'withdraw_parts':
        old = state['objects'].get(action['id'])
        require(old is not None and old['kind'] == 'product', 'product required')
        require(bool(action['parts']) and set(action['parts']) <= set(old['parts']), 'known nonempty withdrawal range required')
        obj = touch(state, action['id'], 'product')
        for part in action['parts']:
            obj['parts'][part] = 'withdrawn'
    elif op == 'report':
        subject = ref(state, action['subject'])
        subject_obj = version(state, subject['id'], subject['revision'])
        goal_id = goal_of(state, subject_obj)
        require(goal_id in state['objects'] and state['objects'][goal_id]['kind'] == 'goal',
                'report subject is not traceable to a goal')
        require(isinstance(action['scope'], str) and action['scope'].strip(), 'report scope required')
        require(action['nature'] in {'author_report', 'documented', 'synthetic'}, 'report nature required')
        new_object(state, action['id'], 'evidence', subject=subject, goal=goal_id, scope=action['scope'],
                   findings=action['findings'], nature=action['nature'])
    elif op == 'accept_goal':
        require(action.get('actor_role') == 'acceptor' and action.get('criteria') and action.get('decision') == 'accept', 'explicit acceptance authority and criteria required')
        require(action.get('evidence'), 'acceptance evidence required')
        require(state['objects'].get(action['id'], {}).get('kind') == 'goal', 'goal required')
        for item in action['evidence']:
            item = ref(state, item)
            evidence = version(state, item['id'], item['revision'])
            require(evidence['kind'] == 'evidence', 'acceptance evidence must be an evidence object')
            require(evidence.get('goal') == action['id'], 'acceptance evidence belongs to a different goal')
            require(isinstance(evidence.get('scope'), str) and evidence['scope'].strip(),
                    'acceptance evidence scope required')
            subject = evidence['subject']
            subject_obj = version(state, subject['id'], subject['revision'])
            require(subject_obj['kind'] in {'attempt', 'product'}, 'acceptance subject must be an attempt or product')
            require(goal_of(state, subject_obj) == action['id'],
                    'acceptance subject is not traceable to this goal')
        obj = touch(state, action['id'], 'goal')
        obj['acceptance'] = 'accepted'
        obj['decision'] = {'actor': action['actor'], 'criteria': action['criteria'], 'evidence': deepcopy(action['evidence'])}
    elif op == 'relate':
        require(action['id'] not in state['relations'], 'relation identity exists')
        require(action['kind'] == 'product_requirement', 'only a documented product requirement is supported')
        source = _relation_endpoint(state, action['from'], 'from')
        target = _relation_endpoint(state, action['to'], 'to')
        require(source != target, 'relation endpoints must differ')
        _known_basis(action['basis'], 'known relation basis required')
        require(action['nature'] == 'documented_requirement', 'relation nature must retain documented_requirement')
        require('meaning' not in action or isinstance(action['meaning'], str) and action['meaning'].strip(),
                'relation meaning must be text when supplied')
        record = {'id': action['id'], 'kind': action['kind'], 'from': source, 'to': target,
                  'basis': deepcopy(action['basis']), 'nature': action['nature']}
        if 'meaning' in action:
            record['meaning'] = action['meaning']
        state['relations'][action['id']] = record
    elif op == 'register_items':
        require(not state['items'], 'item records already registered')
        require(isinstance(action['items'], list) and action['items'], 'nonempty item records required')
        registered = {}
        for item in action['items']:
            require(isinstance(item, dict), 'item structure')
            required = {'id', 'label', 'source', 'nature', 'product', 'part', 'scope', 'source_status', 'status'}
            require(required <= set(item) and set(item) <= required | {'reuse'}, 'item fields')
            item_id = item['id']
            require(isinstance(item_id, str) and bool(item_id) and item_id not in registered,
                    'unique item identity required')
            require(item['source'] in FIXTURE['sources'], 'known item source required')
            require(isinstance(item['label'], str) and item['label'].strip(), 'item label required')
            require(isinstance(item['scope'], str) and item['scope'].strip(), 'item scope required')
            require(isinstance(item['nature'], str) and item['nature'].strip(), 'item nature required')
            require(isinstance(item['source_status'], str) and item['source_status'].strip(),
                    'source status text required')
            product = state['objects'].get(item['product'])
            require(product is not None and product['kind'] == 'product', 'item product required')
            require(item['part'] in product['parts'], 'item part must exist on its product')
            status = item['status']
            require(isinstance(status, dict) and set(status) == {'completion', 'implementation', 'git', 'acceptance'},
                    'item status must keep four separate dimensions')
            for name in ('completion', 'implementation', 'git', 'acceptance'):
                require(status[name] == product['dimensions'][name],
                        'item status must agree with the current product dimension: ' + name)
            if 'reuse' in item:
                reuse = item['reuse']
                require(isinstance(reuse, dict) and set(reuse) == {'kind', 'symbol', 'source', 'basis', 'nature'},
                        'reuse record fields')
                require(isinstance(reuse['symbol'], str) and reuse['symbol'].strip(), 'reuse symbol required')
                require(isinstance(reuse['kind'], str) and reuse['kind'].strip(), 'reuse kind required')
                require(isinstance(reuse['source'], str) and reuse['source'].strip(), 'reuse source required')
                require(isinstance(reuse['nature'], str) and reuse['nature'].strip(), 'reuse nature required')
                _known_basis([reuse['basis']], 'known reuse basis required')
            registered[item_id] = deepcopy(item)
        state['items'] = registered
    elif op in {'responsibility_init', 'assign', 'transfer', 'share', 'unassign', 'unknown'}:
        import t12_responsibility as responsibility
        if op == 'responsibility_init':
            require(state['responsibility'] is None, 'responsibility already initialized')
            require(action['owner'] in state['objects'] and state['objects'][action['owner']]['kind']=='attempt', 'parent responsibility owner required')
            for holder in action['holders']:
                active_attempt(state, holder, 'responsibility holder')
            state['responsibility'] = responsibility.new(state['layout'], action['tokens'], action['holders'], unknown=action.get('unknown', True))
            state['responsibility']['owner'] = action['owner']
        else:
            require(state['responsibility'] is not None, 'responsibility missing')
            if op in {'assign', 'transfer'}:
                active_attempt(state, action['to'], 'new responsibility holder')
            elif op == 'share':
                current = responsibility.project(state['responsibility'])[action['token']]['holders']
                for holder in action['holders']:
                    if holder not in current:
                        active_attempt(state, holder, 'new responsibility holder')
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
        require(isinstance(basis, list) and basis and all(isinstance(x, str) and (x in KNOWN_BASIS or x.startswith('SYN:')) for x in basis), 'known evidence or synthetic label required')
        require(nature in {'source_record', 'synthetic'}, 'change nature')
        require(nature != 'source_record' or all(x in KNOWN_BASIS for x in basis), 'synthetic basis is not history')
        for action in actions:
            require(isinstance(action, dict), 'action structure')
            _execute(work, action, basis)
        before = snapshot(state)
        work['head'] += 1
        after = snapshot(work)
        paths = differences(before, after)
        change = {'number': work['head'], 'basis': deepcopy(basis), 'nature': nature,
                  'actor': 'source_author_unspecified' if nature == 'source_record' else 'synthetic_operator',
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
         'links':[{'kind':'historical_reference','target':actual_ref(s,'batch')}] },
        {'op':'begin','id':'independent','goal':'goal','scope':['completed independent feature scope; exact original feature allocation unknown'],'plan':{'id':'migration-plan','revision':1},'location':'presentation channel'},
        {'op':'begin','id':'turnstep','goal':'goal','scope':['remaining unfinished scope; exact original feature allocation unknown','Turn starts and Inbox claims'],'plan':{'id':'migration-plan','revision':1},'location':'turnstep worktree'},
        {'op':'responsibility_init','owner':'migration','tokens':FIXTURE['feature_families'],'holders':['independent','turnstep'],'unknown':True}])
    step('T12.04', [
        {'op':'produce','id':'independent-code','attempt':'independent',
         'parts':['visual','summary','filter','1_chinese_tool_titles','2_tool_row_visuals',
                  '3_bash_stopped_sr_text','4A_text_shimmer','4B_memoization_reference_stability',
                  '5_streaming_reasoning_summary','9_permission_system_hiding'],
         'dimensions':{'completion':'reported_migration_complete','implementation':'reported_code_written','git':'reported_committed','acceptance':'pending'},'location':'presentation channel','nature':'documented'},
        {'op':'produce','id':'draft-code','attempt':'turnstep',
         'parts':['whole-Turn status','notifications','other unspecified behavior',
                  '6_keep_open_after_cancel_failure','7_whole_turn_status_duration',
                  '8_trigger_notifications','9_context_hiding',
                  '10_turn_action_bar_position','11_action_bar_persistent_visibility'],
         'dimensions':{'completion':'incomplete','implementation':'reported_draft_written','git':'unstaged','acceptance':'pending'},'location':'turnstep worktree','nature':'documented'},
        {'op':'register_items','items':FIXTURE['s029_items']}])
    step('T12.05', [
        {'op':'begin','id':'grouping','goal':'goal','scope':['grouping foundation and remaining product integration'],'location':'source documents; exact worktree unknown'},
        {'op':'produce','id':'group-foundation','attempt':'grouping','parts':['Definition-owned grouping foundation'],
         'dimensions':{'completion':'unknown','implementation':'reported_implemented','git':'unknown','acceptance':'unknown'},'location':'S022 implemented note','nature':'documented'},
        {'op':'report','id':'grouping-pending','subject':{'id':'grouping','revision':1},'scope':'product grouping behavior and performance','findings':['still incomplete'],'nature':'documented'}])
    step('T12.06', [
        {'op':'report','id':'channel-checks','subject':actual_ref(s,'independent'),'scope':'presentation channel; not turnstep worktree',
         'findings':['build/lint/coverage author-reported pass','real-model GUI demo and performance pending'],'nature':'author_report'}])
    step('S029.dependency', [
        {**relation, 'op':'relate'} for relation in FIXTURE['s029_dependencies']])
    step('S028.partial_replacement', [
        {'op':'plan','id':'architecture','owner':'migration','sections':sections(
            presentation='presentation policy and per-Turn eligibility rationale retained',
            grouping='event fold, builder materialization, Step ranges and changedLocationData route'), 'links':[]},
        {'op':'change_plan','id':'architecture','remove':['grouping'],
         'edits':{'foundation':{'status':'reported_implemented_route','description':'Definition-owned grouping foundation supersedes old grouping route'}}}])
    return s


def readback(state):
    objects = deepcopy(state['objects'])
    plan_ids = sorted({oid for oid, obj in state['objects'].items() if obj['kind'] == 'plan'} |
                      {pid for obj in state['objects'].values() for pid in obj.get('plan_records', {})})
    plans = {pid: current_plan(state, pid) for pid in plan_ids}
    if state['plans'] == 'embedded':
        for obj in objects.values():
            obj.pop('plan_records', None)
    import t12_responsibility as responsibility
    relation_index = {}
    for rid, relation in sorted(state['relations'].items()):
        for side, direction in (('from', 'outgoing'), ('to', 'incoming')):
            endpoint = relation[side]
            key = endpoint['object'] + '::' + endpoint['scope']
            other = relation['to' if side == 'from' else 'from']
            relation_index.setdefault(key, []).append(
                {'relation': rid, 'direction': direction, 'other': deepcopy(other)})
    item_view = s029_items(state) if state['items'] else {
        'items': {}, 'note': 'no S029 item records registered in this state'}
    return {'objects': objects, 'plan_records': plans, 'responsibility_view': responsibility.project(state['responsibility']), 'history': [
        {'number': c['number'], 'basis': c['basis'], 'nature': c['nature'], 'actions': c['actions']}
        for c in state['changes']], 'unknowns': FIXTURE['unknowns'],
        'identity_origin': 'researcher-created identities; record revisions are not upstream releases',
        'source_index': deepcopy(FIXTURE['sources']),
        'fact_index': {f['id']:[sid for sid in FIXTURE['sources'] if sid in f['source']] for f in FIXTURE['facts'] + FIXTURE['supplements']},
        'plan_usage': {oid: deepcopy(obj['plan']) for oid,obj in objects.items() if obj['kind']=='attempt'},
        'attempt_initial_plan': {oid: deepcopy(obj['plan']) for oid,obj in objects.items() if obj['kind']=='attempt'},
        'plan_adoptions': {oid: deepcopy(obj.get('plan_adoptions', [])) for oid,obj in objects.items() if obj['kind']=='attempt'},
        'adopted_plan_sections': {oid: plan_sections(state, oid) for oid,obj in state['objects'].items() if obj['kind']=='attempt'},
        'product_plan_usage': {oid: deepcopy(obj.get('plan_usage')) for oid,obj in objects.items() if obj['kind']=='product'},
        'product_initial_plan': {oid: deepcopy(obj.get('initial_plan')) for oid,obj in objects.items() if obj['kind']=='product'},
        'product_legacy_plan_projection': {oid: deepcopy(obj['plan']) for oid,obj in objects.items() if obj['kind']=='product' and 'plan' in obj},
        'historical_plans': {oid+'@'+rev: deepcopy(obj) for oid,versions in state['versions'].items() for rev,obj in versions.items() if obj['kind']=='plan'},
        'items': item_view, 'relations': deepcopy(state['relations']), 'relation_index': relation_index,
        'reading_rules': ['unknown ownership may become known after new supporting evidence; it is not permanently forbidden',
                          'real-model GUI is not synonymous with real-device GUI',
                          'basis identifiers provide traceability, not automatic proof of semantic support',
                          'product_plan_usage is the only authority for plan revisions actually used; product_initial_plan is the begin-time reference',
                          'a legacy product plan field appears only when no explicit plan scope was used; it is a compatibility projection, not an adoption authority',
                          'after an explicit adoption, a product must name plan_scope; continue an older revision by explicitly adopting it again',
                          'a typed relation is a product requirement; it does not mean either endpoint is complete, handed over, or accepted',
                          'S029 item statuses are source records; current product dimensions are a state projection, not independent verification',
                          'same-goal evidence, nonempty scope and explicit criteria make an acceptance structurally reviewable; the checker does not judge natural-language truth or semantic sufficiency']}


def synthetic_path(layout):
    """A fixed legal sequence and rejected alternatives, explicitly not DSH events."""
    import t12_responsibility as responsibility
    state = fresh(layout)
    initial = [{'op':'goal','id':'goal','scope':['X','Y']},
               {'op':'begin','id':'parent','goal':'goal','scope':['X','Y']},
               {'op':'begin','id':'a','goal':'goal','scope':['synthetic child a']},
               {'op':'begin','id':'b','goal':'goal','scope':['synthetic child b']},
               {'op':'responsibility_init','owner':'parent','tokens':['X','Y'],'holders':['a','b']}]
    state = apply(state, initial, 0, ['SYN:initial'])['state']
    steps = [({'op':'assign','token':'X','to':'a'}, 'X to a'),
             ({'op':'assign','token':'Y','to':'b'}, 'only Y to b; X remains a'),
             ({'op':'transfer','token':'X','from':'a','to':'b'}, 'explicit transfer X'),
             ({'op':'share','token':'X','holders':['a','b']}, 'explicit shared responsibility'),
             ({'op':'unassign','token':'X','from':['a','b']}, 'explicit unassignment'),
             ({'op':'unknown','token':'X'}, 'unknown is not unassigned')]
    rows = []
    for action, intent in steps:
        before = responsibility.project(state['responsibility'])
        result = apply(state, [action], state['head'], ['SYN:sequence'])
        require(result['status'] == 'applied', result['error'])
        state = result['state']
        rows.append({'intent':intent,'action':action,'before':before,'after':responsibility.project(state['responsibility']),
                     'native_changed_paths':[p for p in result['changed_paths'] if p.startswith('/responsibility/') and p!='/responsibility/revision']})
    bad = [{'op':'transfer','token':'Y','from':'a','to':'b'},
           {'op':'assign','token':'Y','to':'a'},
           {'op':'revise','id':'goal','delta':{'acceptance':'accepted'}},
           {'op':'end','id':'b','outcome':'silently done'}]
    rejected = []
    for action in bad:
        result = apply(state,[action],state['head'],['SYN:negative'])
        require(result['status']=='rejected' and result['state']==state, 'negative probe unexpectedly changed state')
        rejected.append({'action':action,'error':result['error']})
    return {'state':state,'steps':rows,'rejected':rejected}


def comparison():
    profiles = {}
    for layout in ['parent','relation','child']:
        real,synthetic=real_path(layout),synthetic_path(layout)
        profiles[layout]={'real':readback(real),'synthetic':synthetic,
                          'responsibility_snapshot':deepcopy(real['responsibility'])}
    expected = [r['after'] for r in profiles['parent']['synthetic']['steps']]
    for profile in profiles.values():
        require([r['after'] for r in profile['synthetic']['steps']]==expected,'semantic difference across layouts')
    plans={}
    for placement in ['independent','embedded']:
        initial=real_path(plans=placement)
        result=apply(initial,[{'op':'change_plan','id':'migration-plan','edits':{'later':{'status':'planned','description':'synthetic later phase'}}}],initial['head'],['SYN:plan-change'])
        require(result['status']=='applied',result['error'])
        plans[placement]={'old_product':version(initial,'independent-code'),'product_after_plan_change':version(result['state'],'independent-code'),
                          'old_plan':version(result['state'],'migration-plan',1),'new_plan':current_plan(result['state'],'migration-plan'),
                          'changed_paths':result['changed_paths']}
        require(plans[placement]['old_product']==plans[placement]['product_after_plan_change'],'plan changed old implementation')
    return {'profiles':profiles,'plan_placement':plans,
            'interpretation':'same explicit semantics; changed paths describe this implementation, not human time or model cost'}


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
    (out / 'comparison.json').write_text(json.dumps(comparison(), ensure_ascii=False, indent=2), encoding='utf-8')
    print(str(out.resolve()))
