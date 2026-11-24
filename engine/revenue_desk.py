"""The revenue desk adapter check (config/revenue-desk.json; AGENTS.md, "Revenue desk").

Reads only. It holds the adapter to its shape: the five steps from post to net sales in order, each read from a
function that exists in this engine, bands that carry no figure and bind nothing until Krish's yes, one action per
alarm, offer terms bound to real functions in engine/offers.py, PAID-BOOSTS unchanged, no spend authority and the
store job still off the schedule.
"""
import ast
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA = 'revenue-desk-adapter/1'
STEPS = ('post', 'session', 'add_to_cart', 'order', 'net_sales')
ALARMS = ('blind', 'warning', 'breach')
REQUIRED = ('schema', 'venture', 'repo', 'skill', 'north_star', 'freshness_days', 'steps', 'bands', 'alarms',
            'offer_terms', 'paid_boosts', 'spend_authority', 'store_job', 'asks', 'sheets_dir', 'validator_exits')


def _functions(path):
    with open(path, encoding='utf-8') as f:
        tree = ast.parse(f.read())
    return {node.name for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}


def _function_problems(root, module, names):
    path = os.path.join(root, module)
    if not os.path.isfile(path):
        return [f'{module} does not exist']
    have = _functions(path)
    return [f'{module} has no function {name}' for name in names if name not in have]


def _command_problems(root, command):
    parts = command.split()
    if len(parts) < 3 or parts[:2] != ['python3', 'growth.py']:
        return [f'{command!r}: expected "python3 growth.py <command> [action]"']
    with open(os.path.join(root, 'engine', 'cli.py'), encoding='utf-8') as f:
        cli = f.read()
    return [f'{command!r}: growth.py has no {word} command' for word in parts[2:4]
            if not word.startswith('-') and f"add_parser('{word}'" not in cli]


def adapter_problems(root=ROOT, adapter=None):
    """Every way config/revenue-desk.json fails to parse or names a function, file or command this engine lacks."""
    path = os.path.join(root, 'config', 'revenue-desk.json')
    if adapter is None:
        try:
            with open(path, encoding='utf-8') as f:
                raw = f.read()
            adapter = json.loads(raw)
        except (OSError, ValueError) as error:
            return [f'does not parse: {error}']
    else:
        raw = json.dumps(adapter)
    problems = [f'missing {key}' for key in REQUIRED if key not in adapter]
    if problems:
        return problems
    if '\u2014' in raw or '!' in raw:
        problems.append('no em dashes or exclamation marks')
    if adapter['schema'] != SCHEMA:
        problems.append(f'schema is {adapter["schema"]!r}, not {SCHEMA}')
    if adapter['venture'] != 'heartside':
        problems.append('venture must be heartside')
    steps = adapter['steps']
    if [s.get('id') for s in steps] != list(STEPS):
        problems.append(f'steps must be {", ".join(STEPS)}, in that order')
    for step in steps:
        sid = step.get('id')
        if step.get('better') not in ('up', 'down'):
            problems.append(f'step {sid}: better must be up or down')
        if not step.get('read'):
            problems.append(f'step {sid}: names no read source')
        for source in step.get('read', []):
            problems += [f'step {sid}: {p}' for p in
                         _function_problems(root, source.get('module', ''), [source.get('function', '')])]
        for command in step.get('commands', []):
            problems += [f'step {sid}: {p}' for p in _command_problems(root, command)]
    if not {s['module'] for step in steps for s in step.get('read', [])} >= {'engine/attribution.py', 'engine/insights.py'}:
        problems.append('the steps must read from engine/attribution.py and engine/insights.py')
    bands = adapter['bands']
    if bands.get('label') != 'assumption' or bands.get('binding') is not False:
        problems.append('bands are labelled assumption and bind nothing until Krish says yes')
    if bands.get('warning') is not None or bands.get('breach') is not None:
        problems.append('bands carry no figure until calibrated from this engine\'s own history and approved')
    if not bands.get('binding_after') or 'yes' not in bands['binding_after']:
        problems.append('bands.binding_after must name Krish\'s yes')
    for name in ALARMS:
        alarm = adapter['alarms'].get(name)
        if not isinstance(alarm, dict) or not isinstance(alarm.get('action'), str) or not alarm['action'].strip():
            problems.append(f'alarm {name}: needs exactly one required action')
    if set(adapter['alarms']) != set(ALARMS):
        problems.append(f'alarms are exactly {", ".join(ALARMS)}')
    offers = adapter['offer_terms']
    problems += [f'offer_terms: {p}' for p in
                 _function_problems(root, offers.get('module', ''), offers.get('functions', []))]
    if offers.get('module') != 'engine/offers.py' or not offers.get('rules'):
        problems.append('offer_terms must bind rules to engine/offers.py')
    boosts = adapter['paid_boosts']
    if boosts.get('change') != 'none' or not os.path.isfile(os.path.join(root, boosts.get('doctrine', ''))):
        problems.append('paid_boosts: docs/PAID-BOOSTS.md must exist and stay unchanged (change: none)')
    if adapter['spend_authority'] != 'none':
        problems.append('spend_authority must be none')
    store = adapter['store_job']
    with open(os.path.join(root, 'automations.json'), encoding='utf-8') as f:
        automations = json.load(f)
    if store.get('schedule') != 'off' or store.get('job') not in [a.get('job') for a in automations.get('off_schedule', [])]:
        problems.append('store_job must stay off the schedule (automations.json off_schedule)')
    if store.get('job') in [a.get('job') for a in automations.get('automations', [])]:
        problems.append('the store job is on the schedule in automations.json')
    if not str(adapter['sheets_dir']).startswith('local/'):
        problems.append('sheets_dir must sit under local/ (never committed)')
    if set(adapter['validator_exits']) != {'0', '1', '2'} or 'never a pass' not in adapter['validator_exits']['2']:
        problems.append('validator_exits: 0 pass, 1 held, 2 unavailable and never a pass')
    if not isinstance(adapter['freshness_days'], int) or adapter['freshness_days'] < 1:
        problems.append('freshness_days must be a whole number of days')
    for name, doc in (('north_star', adapter['north_star'].get('doctrine', '')),):
        if not os.path.isfile(os.path.join(root, doc)):
            problems.append(f'{name}: {doc} does not exist')
    if adapter['north_star'].get('step') not in STEPS:
        problems.append('north_star.step must name one of the steps')
    # No figures: the adapter holds no money amount.
    if re.search(r'\$\s?\d', raw):
        problems.append('the adapter holds no money figure')
    return problems
