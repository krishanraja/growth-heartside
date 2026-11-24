"""The insight desk's sheet, checked here with the standard library only, and Heartside's adapter to the desk.

The method is the ai-harness insight-desk skill (read live with get_skill; until it is admitted, a local ai-harness
checkout's candidates/insight-desk). Its output is an insight sheet (insight-sheet/1): the insight, up to three ideas
and how each was screened. This file holds the same rules as the skill's references/insight-sheet.schema.json and
scripts/validate_sheet.py, so this engine can check a sheet without the harness on the machine:

    python3 factory/insight_sheet.py check SHEET.json [--methods FILE]   valid or not, every reason printed (exit 0, 1, 2)
    python3 factory/insight_sheet.py sha   SHEET.json                    the sheet_sha256 the sheet should carry
    python3 factory/insight_sheet.py adapter                             config/insight-desk.json parses and names real commands

A sheet feeds the joke lab only through `python3 factory/jokelab.py brief TOPIC --insight SHEET.json`, which puts the
chosen insight and the lead idea in front of the brief and changes nothing else. Sheets live in local/insight-desk/ and
are never committed (rule 9). Approving an idea is plan approval only; nothing here posts, sends or spends.

The two offline checks the bench uses (factory/insight_bench.py) live here too:
  - insight_format: the line reads "[audience] wants X but Y because Z";
  - specificity: with the brand's own name taken out, the idea still needs something only Heartside sells, or a rival
    pet gift shop could run it unchanged.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ADAPTER = os.path.join(ROOT, 'config', 'insight-desk.json')
SCHEMA = 'insight-sheet/1'

TOP_KEYS = ('schema', 'venture', 'repo', 'harness_skill_sha', 'made_at', 'north_star', 'stall_check',
            'insights', 'chosen_insight', 'discarded_obvious', 'ideas', 'consults', 'lead',
            'blind_passes', 'sheet_sha256')
DIAGNOSES = ('idea', 'distribution', 'offer', 'attribution', 'measurement')
LEVELS = ('execution', 'campaign', 'platform', 'business', 'measurement')
TEST_KEYS = ('specificity', 'share', 'analogue', 'floor', 'kill_the_favourite')
RESULTS = ('pass', 'fail', 'unavailable')
CONSULT_RESULTS = ('pass', 'flagged', 'unavailable')
ENGINES = ('divergent-thinker', 'humour-engine')
IDEA_KEYS = ('id', 'claim', 'mechanic', 'idea_level', 'method', 'channel_role', 'conversion_path',
             'kill_condition', 'tests')
INSIGHT_KEYS = ('audience', 'wants', 'but', 'because', 'source', 'read_at', 'assumption')
ID_RE = re.compile(r'^[a-z0-9][a-z0-9-]{0,39}$')
REPO_RE = re.compile(r'^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$')
SHA1_RE = re.compile(r'^[0-9a-f]{40}$')
SHA256_RE = re.compile(r'^[0-9a-f]{64}$')
EM_DASH = chr(0x2014)
SCORE_KEY = re.compile(r'(?i)^(score|scores|rating|points|weight|weighted_total|total)$')
METHOD_HEAD = re.compile(r'(?m)^### `([a-z0-9-]+)`')
INSIGHT_LINE = re.compile(r'^\s*(?P<audience>\S.*?)\s+wants?\s+(?P<wants>\S.*?)\s+but\s+(?P<but>\S.*?)\s+because\s+(?P<because>\S.*?)\s*\.?\s*$',
                          re.I | re.S)


# ---------------------------------------------------------------- helpers

def _filled(value):
    return isinstance(value, str) and value.strip() != ''


def _is_date(value):
    if not isinstance(value, str):
        return False
    try:
        datetime.date.fromisoformat(value)
        return True
    except ValueError:
        return False


def _is_datetime(value):
    if not isinstance(value, str) or 'T' not in value:
        return False
    try:
        datetime.datetime.fromisoformat(value.replace('Z', '+00:00'))
        return True
    except ValueError:
        return False


def _is_int(value):
    return isinstance(value, int) and not isinstance(value, bool)


def canonical(sheet):
    body = {k: v for k, v in sheet.items() if k != 'sheet_sha256'}
    return json.dumps(body, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')


def sheet_sha(sheet):
    return hashlib.sha256(canonical(sheet)).hexdigest()


def load_adapter(path=ADAPTER):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def methods_file(explicit=None):
    """The skill's method list, when a harness checkout is on this machine. None means the method check is skipped."""
    candidates = [explicit, os.environ.get('HEARTSIDE_INSIGHT_METHODS')]
    for harness in (os.environ.get('HEARTSIDE_HARNESS_DIR'), os.path.join(os.path.dirname(ROOT), 'ai-harness')):
        if harness:
            for where in ('skills', 'candidates'):
                candidates.append(os.path.join(harness, where, 'insight-desk', 'references', 'methods-by-category.md'))
    for path in candidates:
        if path and os.path.isfile(path):
            return path
    return None


def known_methods(path):
    with open(path, encoding='utf-8') as f:
        return set(METHOD_HEAD.findall(f.read()))


# ---------------------------------------------------------------- the sheet

def _walk(node, where, errors):
    if isinstance(node, dict):
        for key, value in node.items():
            if SCORE_KEY.match(str(key)):
                errors.append(f'{where}.{key}: no scores; the sheet carries results and reasons only')
            _walk(value, f'{where}.{key}', errors)
    elif isinstance(node, list):
        for i, value in enumerate(node):
            _walk(value, f'{where}[{i}]', errors)
    elif isinstance(node, str) and EM_DASH in node:
        errors.append(f'{where}: carries an em dash')


def _check_test(label, test, errors, analogue=False):
    if not isinstance(test, dict):
        errors.append(f'{label}: missing')
        return
    allowed = {'result', 'reason'} | ({'url', 'read_at'} if analogue else set())
    extra = set(test) - allowed
    if extra:
        errors.append(f'{label}: unexpected fields {", ".join(sorted(extra))}')
    if test.get('result') not in RESULTS:
        errors.append(f'{label}: result must be pass, fail or unavailable (got {test.get("result")!r})')
    if not _filled(test.get('reason')):
        errors.append(f'{label}: needs a reason')
    if analogue:
        for key in ('url', 'read_at'):
            if key not in test:
                errors.append(f'{label}: needs {key} (null when none was found)')
        if test.get('url') is not None and not isinstance(test.get('url'), str):
            errors.append(f'{label}: url is a string or null')
        if test.get('read_at') is not None and not _is_date(test.get('read_at')):
            errors.append(f'{label}: read_at is a date or null')
        if test.get('result') == 'pass':
            if not _filled(test.get('url')):
                errors.append(f'{label}: a passing analogue is linked')
            if not _is_date(test.get('read_at')):
                errors.append(f'{label}: a passing analogue records the date it was read')


def _check_idea(i, idea, methods, errors):
    label = f'ideas[{i}]'
    if not isinstance(idea, dict):
        errors.append(f'{label}: not an object')
        return
    missing = [k for k in IDEA_KEYS if k not in idea]
    if missing:
        errors.append(f'{label}: missing {", ".join(missing)}')
    extra = set(idea) - set(IDEA_KEYS)
    if extra:
        errors.append(f'{label}: unexpected fields {", ".join(sorted(extra))}')
    if not (isinstance(idea.get('id'), str) and ID_RE.match(idea['id'])):
        errors.append(f'{label}: id must be lower-case letters, digits and hyphens')
    for key in ('claim', 'mechanic', 'method', 'channel_role', 'kill_condition'):
        if key in idea and not _filled(idea[key]):
            errors.append(f'{label}: {key} is empty')
    if idea.get('idea_level') not in LEVELS:
        errors.append(f'{label}: idea_level must be one of {", ".join(LEVELS)}')
    if methods is not None and _filled(idea.get('method')) and idea['method'] not in methods:
        errors.append(f'{label}: method {idea["method"]!r} is not in the skill\'s methods-by-category.md')
    path = idea.get('conversion_path')
    if not isinstance(path, dict) or not all(_filled(path.get(k)) for k in ('offer', 'link', 'why_act')):
        errors.append(f'{label}: an idea with no full conversion path (offer, link, why_act) is held off the sheet')
    elif set(path) - {'offer', 'link', 'why_act'}:
        errors.append(f'{label}: conversion_path has unexpected fields')
    tests = idea.get('tests')
    if not isinstance(tests, dict):
        errors.append(f'{label}: tests missing')
        return
    extra = set(tests) - set(TEST_KEYS)
    if extra:
        errors.append(f'{label}: unexpected tests {", ".join(sorted(extra))}')
    for key in TEST_KEYS:
        _check_test(f'{label}.tests.{key}', tests.get(key), errors, analogue=(key == 'analogue'))


def _check_insight(i, insight, errors):
    label = f'insights[{i}]'
    if not isinstance(insight, dict):
        errors.append(f'{label}: not an object')
        return
    for key in ('audience', 'wants', 'but', 'because'):
        if not _filled(insight.get(key)):
            errors.append(f'{label}: {key} is empty')
    extra = set(insight) - set(INSIGHT_KEYS)
    if extra:
        errors.append(f'{label}: unexpected fields {", ".join(sorted(extra))}')
    sourced = 'source' in insight or 'read_at' in insight
    if sourced and 'assumption' in insight:
        errors.append(f'{label}: either a source and read_at, or assumption: true, never both')
    elif 'assumption' in insight:
        if insight['assumption'] is not True:
            errors.append(f'{label}: assumption must be true when present')
    elif not (_filled(insight.get('source')) and _is_date(insight.get('read_at'))):
        errors.append(f'{label}: needs a source and the date it was read, or assumption: true')


def validate(sheet, methods=None):
    """Every reason the sheet is not a valid insight-sheet/1, or [] when it is. methods=None skips the method list."""
    errors = []
    if not isinstance(sheet, dict):
        return ['the sheet is not a JSON object']
    missing = [k for k in TOP_KEYS if k not in sheet]
    if missing:
        errors.append(f'missing {", ".join(missing)}')
    extra = set(sheet) - set(TOP_KEYS)
    if extra:
        errors.append(f'unexpected fields {", ".join(sorted(extra))}')
    if sheet.get('schema') != SCHEMA:
        errors.append(f'schema must be {SCHEMA}')
    if not _filled(sheet.get('venture')):
        errors.append('venture is empty')
    if not (isinstance(sheet.get('repo'), str) and REPO_RE.match(sheet['repo'])):
        errors.append('repo must be owner/name')
    if not (isinstance(sheet.get('harness_skill_sha'), str) and SHA1_RE.match(sheet['harness_skill_sha'])):
        errors.append('harness_skill_sha must be the 40-character commit the skill was read at')
    if not _is_datetime(sheet.get('made_at')):
        errors.append('made_at must be an ISO date-time')

    ns = sheet.get('north_star')
    urgency = current = None
    if not isinstance(ns, dict) or set(ns) != {'metric', 'urgency', 'current', 'as_of'}:
        errors.append('north_star needs exactly metric, urgency, current and as_of')
    else:
        urgency, current = ns.get('urgency'), ns.get('current')
        if not _filled(ns.get('metric')):
            errors.append('north_star.metric is empty')
        if not (_is_int(urgency) and 1 <= urgency <= 5):
            errors.append('north_star.urgency must be 1 to 5')
        if current is not None and (isinstance(current, bool) or not isinstance(current, (int, float))):
            errors.append('north_star.current must be a number or null')
        if ns.get('as_of') is not None and not _is_date(ns.get('as_of')):
            errors.append('north_star.as_of must be a date or null')

    stall = sheet.get('stall_check')
    diagnosis = None
    if not isinstance(stall, dict) or set(stall) != {'diagnosis', 'evidence'}:
        errors.append('stall_check needs exactly diagnosis and evidence')
    else:
        diagnosis = stall.get('diagnosis')
        if diagnosis not in DIAGNOSES:
            errors.append(f'stall_check.diagnosis must be one of {", ".join(DIAGNOSES)}')
        elif diagnosis not in ('idea', 'measurement'):
            errors.append(f'the stall is {diagnosis}, not the idea; the desk stops and makes no sheet')
        if not _filled(stall.get('evidence')):
            errors.append('stall_check.evidence is empty')

    insights = sheet.get('insights')
    if not isinstance(insights, list) or not 1 <= len(insights) <= 3:
        errors.append('insights must hold one to three lines')
        insights = insights if isinstance(insights, list) else []
    for i, insight in enumerate(insights):
        _check_insight(i, insight, errors)
    chosen = sheet.get('chosen_insight')
    if not (_is_int(chosen) and 0 <= chosen < len(insights)):
        errors.append('chosen_insight must point at one of the insights')

    obvious = sheet.get('discarded_obvious')
    if not (isinstance(obvious, list) and len(obvious) == 3 and all(_filled(o) for o in obvious)):
        errors.append('discarded_obvious must hold exactly three ideas')
        obvious = []

    ideas = sheet.get('ideas')
    if not isinstance(ideas, list) or not 1 <= len(ideas) <= 3:
        errors.append('ideas must hold one to three ideas')
        ideas = ideas if isinstance(ideas, list) else []
    for i, idea in enumerate(ideas):
        _check_idea(i, idea, methods, errors)
    by_id = {idea.get('id'): idea for idea in ideas if isinstance(idea, dict)}
    if len(by_id) != len(ideas):
        errors.append('idea ids must be unique')
    plain = {' '.join(str(o).lower().split()) for o in obvious}
    for idea in by_id.values():
        if ' '.join(str(idea.get('claim', '')).lower().split()) in plain:
            errors.append(f'idea {idea.get("id")}: restates a discarded obvious idea')
    if diagnosis == 'measurement' or (urgency == 4 and current is None):
        for idea in by_id.values():
            if idea.get('idea_level') != 'measurement':
                errors.append(f'idea {idea.get("id")}: nothing is measured, so every idea is a measurement idea')

    consults = sheet.get('consults')
    if not isinstance(consults, list):
        errors.append('consults must be a list (empty when no engine was called)')
        consults = []
    for i, consult in enumerate(consults):
        if not isinstance(consult, dict) or set(consult) != {'engine', 'op', 'result', 'ref'}:
            errors.append(f'consults[{i}]: needs exactly engine, op, result and ref')
            continue
        if consult['engine'] not in ENGINES:
            errors.append(f'consults[{i}]: engine must be one of {", ".join(ENGINES)}')
        if consult['result'] not in CONSULT_RESULTS:
            errors.append(f'consults[{i}]: result must be pass, flagged or unavailable; exit 2 is unavailable, never pass')
        if not _filled(consult['op']) or not _filled(consult['ref']):
            errors.append(f'consults[{i}]: op and ref are filled')

    passes = sheet.get('blind_passes')
    if not isinstance(passes, list) or len(passes) != 2:
        errors.append('blind_passes must hold exactly two passes')
        passes = []
    ids = sorted(k for k in by_id if isinstance(k, str))
    for i, blind in enumerate(passes):
        if not isinstance(blind, dict) or set(blind) != {'reader', 'order', 'lead'}:
            errors.append(f'blind_passes[{i}]: needs exactly reader, order and lead')
            continue
        if not _filled(blind['reader']):
            errors.append(f'blind_passes[{i}]: name the reader')
        if not isinstance(blind['order'], list) or sorted(map(str, blind['order'])) != ids:
            errors.append(f'blind_passes[{i}]: order must list every idea id once')
        if blind['lead'] is not None and blind['lead'] not in by_id:
            errors.append(f'blind_passes[{i}]: lead is not an idea on the sheet')
    if len(passes) == 2 and all(isinstance(p, dict) for p in passes):
        if len(ids) > 1 and passes[0].get('order') == passes[1].get('order'):
            errors.append('blind_passes: the two orders must be shuffled differently')
        if any(p.get('reader') in ('writer', 'author') for p in passes):
            errors.append('blind_passes: the reader is never the writer of the ideas')

    lead = sheet.get('lead')
    if lead is not None:
        if lead not in by_id:
            errors.append('lead is not an idea on the sheet')
        else:
            if not passes or any(isinstance(p, dict) and p.get('lead') != lead for p in passes):
                errors.append('lead: both blind passes must pick the same lead; otherwise lead is null')
            tests = by_id[lead].get('tests') or {}
            for key in TEST_KEYS:
                result = (tests.get(key) or {}).get('result') if isinstance(tests.get(key), dict) else None
                if result != 'pass':
                    errors.append(f'lead {lead}: {key} is {result}; an idea leads only when every test passed')

    _walk(sheet, 'sheet', errors)

    claimed = sheet.get('sheet_sha256')
    if not (isinstance(claimed, str) and SHA256_RE.match(claimed)):
        errors.append('sheet_sha256 must be 64 lower-case hex characters')
    elif claimed != sheet_sha(sheet):
        errors.append('sheet_sha256 does not match the sheet; recompute it with: python3 factory/insight_sheet.py sha')
    return errors


def for_this_engine(sheet, adapter):
    """The adapter's own conditions on a valid sheet: this venture, this repository, the idea cap."""
    errors = []
    if sheet.get('venture') != adapter.get('venture'):
        errors.append(f'venture is {sheet.get("venture")!r}; this engine takes {adapter.get("venture")!r} sheets only')
    if sheet.get('repo') != adapter.get('repo'):
        errors.append(f'repo is {sheet.get("repo")!r}; this engine is {adapter.get("repo")!r}')
    if isinstance(sheet.get('ideas'), list) and len(sheet['ideas']) > adapter.get('max_ideas', 3):
        errors.append(f'more than {adapter.get("max_ideas", 3)} ideas')
    return errors


def read_sheet(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def usable(path, adapter=None, methods_path=None):
    """(sheet, errors) for a sheet about to feed this engine: valid, for this venture, and with a lead."""
    adapter = adapter if adapter is not None else load_adapter()
    try:
        sheet = read_sheet(path)
    except (OSError, ValueError) as error:
        return None, [f'cannot read the sheet: {error}']
    mpath = methods_file(methods_path)
    errors = validate(sheet, known_methods(mpath) if mpath else None)
    if isinstance(sheet, dict):
        errors += for_this_engine(sheet, adapter)
        if not errors and sheet.get('lead') is None:
            errors.append('the sheet has no lead (the two blind passes did not agree); it feeds no brief until one leads')
    return sheet, errors


def preamble(sheet):
    """The block jokelab.py brief --insight puts in front of the brief: the chosen insight and the lead idea, nothing else."""
    insight = sheet['insights'][sheet['chosen_insight']]
    idea = next(i for i in sheet['ideas'] if i['id'] == sheet['lead'])
    path = idea['conversion_path']
    where = insight.get('source', 'an assumption, not yet read anywhere')
    when = f', read {insight["read_at"]}' if insight.get('read_at') else ''
    lines = [
        f'Insight desk sheet {sheet["sheet_sha256"][:12]} (skill at {sheet["harness_skill_sha"][:12]}). Write every '
        'candidate from this insight and this idea. The idea is the brief\'s direction, not its words; everything below '
        'the line still binds.',
        '',
        f'The insight: {insight["audience"]} wants {insight["wants"]} but {insight["but"]} because {insight["because"]}.',
        f'Where it comes from: {where}{when}.',
        '',
        f'The lead idea ({idea["id"]}, {idea["idea_level"]} level, method {idea["method"]}): {idea["claim"]}',
        f'How it works: {idea["mechanic"]}',
        f'Its job on the channel: {idea["channel_role"]}',
        f'Why a viewer acts: {path["why_act"]} (offer: {path["offer"]}; link: {path["link"]})',
        f'What kills it: {idea["kill_condition"]}',
        '',
        '----',
    ]
    return '\n'.join(lines)


# ---------------------------------------------------------------- the two offline checks

def insight_format(text):
    """(passed, reason): does the line read "[audience] wants X but Y because Z"."""
    m = INSIGHT_LINE.match(text or '')
    if not m:
        return False, 'not in the form "[audience] wants X but Y because Z"'
    return True, f'audience: {m.group("audience")[:60]}'


def specificity(text, adapter):
    """(passed, reason): with the brand's own names removed, does the idea still need something only Heartside sells."""
    plain = (text or '').lower()
    for word in sorted(adapter.get('brand_words', []), key=len, reverse=True):
        plain = plain.replace(word.lower(), 'a rival pet gift shop')
    hits = [a for a in adapter.get('specificity_anchors', [])
            if re.search(r'(?<![a-z0-9])' + re.escape(a.lower()) + r'(?![a-z0-9])', plain)]
    if not hits:
        return False, 'with the brand swapped for a rival pet gift shop, nothing in it breaks'
    return True, f'still needs: {", ".join(hits[:3])}'


# ---------------------------------------------------------------- the adapter

def _subcommand_exists(script_path, sub, root):
    if os.path.basename(script_path) == 'growth.py':
        sys.path.insert(0, root)
        try:
            from engine import cli
            if sub in cli.COMMANDS:
                return True
        finally:
            sys.path.remove(root)
    with open(script_path, encoding='utf-8') as f:
        return f"add_parser('{sub}'" in f.read()


def adapter_problems(root=ROOT, adapter=None):
    """Every way config/insight-desk.json fails to parse or names a command, file or flag this engine does not have."""
    path = os.path.join(root, 'config', 'insight-desk.json')
    if adapter is None:
        try:
            adapter = load_adapter(path)
        except (OSError, ValueError) as error:
            return [f'config/insight-desk.json does not parse: {error}']
    problems = []
    for key in ('venture', 'repo', 'skill', 'sheet_schema', 'sheets_dir', 'max_ideas', 'humour', 'divergent', 'hook',
                'commands', 'specificity_anchors', 'brand_words', 'bench'):
        if key not in adapter:
            problems.append(f'config/insight-desk.json: missing {key}')
    if problems:
        return problems
    if adapter['sheet_schema'] != SCHEMA:
        problems.append(f'sheet_schema is {adapter["sheet_schema"]!r}, not {SCHEMA}')
    if not str(adapter['sheets_dir']).startswith('local/'):
        problems.append('sheets_dir must sit under local/ (never committed)')
    if not (_is_int(adapter['max_ideas']) and 1 <= adapter['max_ideas'] <= 3):
        problems.append('max_ideas is 1 to 3')
    if adapter['divergent'].get('namespace') != f'growth-heartside:{adapter["divergent"].get("lane")}':
        problems.append('divergent.namespace must be growth-heartside:<lane>, the namespace --lane files under')
    for rel in [adapter.get('floor'), (adapter.get('humour') or {}).get('doctrine')]:
        if rel and not os.path.isfile(os.path.join(root, rel)):
            problems.append(f'{rel} does not exist')
    commands = list(adapter['commands']) + [f'{adapter["hook"]["command"]} {adapter["hook"]["flag"]}',
                                            adapter['divergent']['command'], adapter['humour'].get('check', ''),
                                            adapter.get('claims', '')]
    for command in commands:
        if not command:
            continue
        parts = command.split()
        if len(parts) < 2 or parts[0] != 'python3':
            problems.append(f'{command!r}: expected "python3 <script> [sub] [--flag]"')
            continue
        script = os.path.join(root, parts[1])
        if not os.path.isfile(script):
            problems.append(f'{command!r}: {parts[1]} does not exist')
            continue
        with open(script, encoding='utf-8') as f:
            source = f.read()
        rest = parts[2:]
        subs = [p for p in rest if not p.startswith('-')]
        flags = [p for p in rest if p.startswith('--')]
        if subs and not _subcommand_exists(script, subs[0], root):
            problems.append(f'{command!r}: {parts[1]} has no {subs[0]} command')
        for flag in flags:
            owner = source
            if os.path.basename(script) == 'growth.py':
                with open(os.path.join(root, 'engine', 'cli.py'), encoding='utf-8') as f:
                    owner += f.read()
            if f"'{flag}'" not in owner:
                problems.append(f'{command!r}: {parts[1]} has no {flag} option')
    return problems


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest='cmd', required=True)
    c = sub.add_parser('check'); c.add_argument('sheet'); c.add_argument('--methods')
    s = sub.add_parser('sha'); s.add_argument('sheet')
    sub.add_parser('adapter')
    a = p.parse_args(argv)
    if a.cmd == 'adapter':
        problems = adapter_problems()
        for problem in problems:
            print(f'ADAPTER  {problem}')
        if not problems:
            print('config/insight-desk.json parses and every command it names exists')
        return 1 if problems else 0
    try:
        sheet = read_sheet(a.sheet)
    except (OSError, ValueError) as error:
        print(f'cannot read the sheet: {error}', file=sys.stderr)
        return 2
    if a.cmd == 'sha':
        print(sheet_sha(sheet) if isinstance(sheet, dict) else '')
        return 0
    mpath = methods_file(a.methods)
    errors = validate(sheet, known_methods(mpath) if mpath else None)
    if isinstance(sheet, dict):
        errors += for_this_engine(sheet, load_adapter())
    for error in errors:
        print(f'INVALID  {error}')
    if not mpath:
        print('note: the skill\'s method list is not on this machine, so method names were not checked '
              '(set HEARTSIDE_HARNESS_DIR or pass --methods)', file=sys.stderr)
    if errors:
        return 1
    print(f'VALID {SCHEMA}: {len(sheet["ideas"])} idea(s), lead {sheet["lead"] or "none"}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
