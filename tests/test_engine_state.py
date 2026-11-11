"""Protocol 1.20.0: Krish's instruction and the engine's state, proved against synthetic fixtures only.

Ruling (Krish, 2026-11-11): every growth engine's priorities, obsessions, next
steps and outstanding items feed live across Control Centre, and Krish
instructs each engine with his next best action, which starts it.
"""
from contextlib import redirect_stderr, redirect_stdout
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest

from engine import control_center, engine_state, ledger, protocol
from engine.control_center import canonical, report_digest
from tests.test_protocol import (DIRECTIVE, NOW, SCHEMA, STATE, TOKEN, FakeGrowth, StandIn, recommendations,
                                 validate)

ROOT = Path(__file__).resolve().parent.parent
DIRECTIVE_SCHEMA = json.loads((ROOT / 'docs/control-center/engine-directive.schema.json').read_text())
IID = 'ki_' + '0123456789abcdef01234567'
# Synthetic words with a marker that must never leave the engine: not in a report, an ack, stdout or a file.
WORDS = 'Synthetic instruction words MARKER-7f3a: lead with the dog chat format this week.'
HELD_RULE = ('Krish has held this engine until it is ready. Propose nothing and ask him nothing. '
             'Report one hold that names what stops you being ready and what would clear it.')

NORTH_STAR = '''# North Star

> By 31 December 2026, organic posts sell more Heartside gifts than paid ads ever have, and every winning format was found by this engine and approved by Krish in one press.

```yaml north-star-metric
metric: "Synthetic organic net sales, trailing 4 weeks"
unit: USD
direction: up
target: 50000
deadline: 2026-12-28
ladder:
  - [2026-10-12, 200]
  - [2026-10-19, 728]
  - [2026-10-26, 1417]
```
'''
GET_GOING = '''# Get going

## The build

- [x] **Step 0.** Done already.
- [ ] **Step 1.** The synthetic loop, proved against the stand-in: every case covered.
- [ ] **Step 2.** A later step.

## Checks
'''
NOW_MD = '''# Synthetic engine

## What is next and what is waiting on Krish

- Next (2026-10-19): Krish posts the synthetic reel at 13:00 London.
- **Waiting on Krish:** set the synthetic channel times. Then a second sentence.
- **Still to rewrite:** the synthetic playbook.
- Rule on the synthetic brief before it is proposed.
- Write to someone@example.invalid about the synthetic thing.
- North Star check (2026-10-19): holds.

## Read next
'''
AGENTS = '''# Synthetic agents

Krish, 2026-10-14: "I want to build an autonomous browser based growth
engine that can be run from anywhere (codex or cowork), solely focused on
getting this business to 10k a month with minimal paid CAC", then "Ensure
the growth engine is always across what the main heartside repository is
doing at any point in time".
'''


def directive(instruction=True, features=True, held=False):
    value = copy.deepcopy(DIRECTIVE)
    body = value['directive']
    body['schema_version'] = '1.20.0'
    body['constraints'].update(autonomy='autonomous', autonomy_rule='synthetic autonomy rule')
    body['objectives'] = [{'key': 'organic_net_sales_usd', 'label': 'Organic net sales', 'target': 50000, 'unit': 'USD',
                           'window': '28d', 'timezone': 'Europe/London', 'latest': 0, 'availability': 'measured'}]
    body['north_star'] = {'parent': None, 'own': {'repo': 'krishanraja/growth-heartside', 'metric': 'Synthetic', 'unit': 'USD',
                                                  'aim_by': '2026-12-28', 'week_of': '2026-10-19', 'week_target': 728, 'current': 0,
                                                  'urgency': 4, 'urgency_reason': 'synthetic', 'read_on': '2026-10-19'},
                          'intensity': {'urgency': 4, 'drafts_multiplier': 2, 'rule': 'synthetic'}}
    if features:
        body['features'] = {'engine_state': True, 'krish_instruction': True}
        body['krish_instruction'] = ({'id': IID, 'words': WORDS, 'given_at': '2026-10-19T07:30:00Z', 'given_by': 'krish',
                                      'supersedes': None} if instruction and not held else None)
    elif instruction:
        body['krish_instruction'] = {'id': IID, 'words': WORDS, 'given_at': '2026-10-19T07:30:00Z', 'given_by': 'krish',
                                     'supersedes': None}
    if held:
        body['next_action'] = {'proposal_id': None, 'instruction': HELD_RULE, 'why': 'Krish held it: it is not ready yet.',
                               'close_condition': None}
    return value


def write_docs(root):
    (root / 'docs').mkdir(parents=True, exist_ok=True)
    (root / 'docs/NORTH_STAR.md').write_text(NORTH_STAR)
    (root / 'docs/GET-GOING.md').write_text(GET_GOING)
    (root / 'NOW.md').write_text(NOW_MD)
    (root / 'AGENTS.md').write_text(AGENTS)


class StateTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        write_docs(self.root)
        self.db = ledger.connect(self.root / 'local/engine.sqlite3')

    def tearDown(self):
        self.db.close()
        self.temporary.cleanup()

    def build(self, value, seen=False):
        return protocol.build_report(root=self.root, state=copy.deepcopy(STATE), db=self.db, now=NOW,
                                     run_id='heartside:2026-10-19:synthetic-directive-42', mode='synthetic',
                                     directive=value, recommendations=recommendations(), instruction_seen=seen)

    def test_the_directive_fixture_matches_the_schema(self):
        self.assertEqual(validate(DIRECTIVE_SCHEMA, directive()['directive']), [])

    def test_an_instruction_is_received_first_by_id_and_its_words_never_leave(self):
        report = self.build(directive())
        self.assertEqual(validate(SCHEMA, report), [])
        self.assertEqual(report['payload_sha256'], report_digest(report))
        self.assertEqual(report['schema_version'], '1.20.0')
        self.assertTrue(report['activity'][0]['line'].startswith(f"Received Krish's instruction {IID}"))
        ack, = report['instruction_acks']
        self.assertEqual((ack['instruction_id'], ack['state'], ack['evidence_url'], ack['at']),
                         (IID, 'received', None, '2026-10-19T08:00:00Z'))
        self.assertLessEqual(len(ack['line']), 280)
        wire = canonical(report)
        self.assertNotIn('MARKER-7f3a', wire)
        self.assertNotIn(WORDS, wire)
        # An ack never goes in holds, so it never changes the report's status.
        self.assertFalse(any(IID in (h['detail'] or '') + h['reason'] for h in report['holds']))
        self.assertEqual(report['status'], self.build(directive(instruction=False))['status'])

    def test_an_instruction_received_before_is_not_received_again(self):
        report = self.build(directive(), seen=True)
        self.assertNotIn('instruction_acks', report)
        self.assertIn('still open', report['activity'][0]['line'])
        self.assertEqual(validate(SCHEMA, report), [])

    def test_no_instruction_sends_no_ack_and_no_instruction_line(self):
        report = self.build(directive(instruction=False))
        self.assertNotIn('instruction_acks', report)
        self.assertFalse(any('instruction' in a['line'].lower() for a in report['activity'][:1]))
        self.assertEqual(report['schema_version'], '1.20.0')  # the state fields still go
        self.assertEqual(validate(SCHEMA, report), [])

    def test_a_held_engine_gets_no_instruction_and_acks_nothing(self):
        report = self.build(directive(held=True))
        self.assertNotIn('instruction_acks', report)
        self.assertFalse(any(IID in a['line'] for a in report['activity']))
        self.assertEqual(validate(SCHEMA, report), [])

    def test_an_instruction_reaching_a_held_engine_is_received_then_blocked(self):
        value = directive(held=True)
        value['directive']['krish_instruction'] = directive()['directive']['krish_instruction']
        report = self.build(value)
        self.assertEqual([a['state'] for a in report['instruction_acks']], ['received', 'blocked'])
        self.assertIn('Engine held', report['instruction_acks'][1]['line'])
        self.assertEqual(validate(SCHEMA, report), [])

    def test_before_control_center_serves_1_20_0_nothing_new_is_sent(self):
        report = self.build(directive(features=False))
        for key in ('priorities', 'obsessions', 'next_steps', 'instruction_acks'):
            self.assertNotIn(key, report)
        self.assertEqual(report['schema_version'], '1.0.0')
        self.assertNotIn('MARKER-7f3a', canonical(report))
        self.assertIn('does not take acks yet', report['activity'][0]['line'])
        self.assertEqual(validate(SCHEMA, report), [])
        old = copy.deepcopy(DIRECTIVE)  # a 1.0.0 directive with no instruction at all
        self.assertEqual(self.build(old)['schema_version'], '1.0.0')

    def test_priorities_come_from_the_north_star_then_the_constraint_then_the_recommendations(self):
        report = self.build(directive(instruction=False))
        lines = [(p['rank'], p['line'], p['objective_key']) for p in report['priorities']]
        self.assertEqual(lines[0], (1, 'Synthetic organic net sales, trailing 4 weeks: $50,000 by 2026-12-28. '
                                       "This week's rung is $728; read $0 (U4).", 'organic_net_sales_usd'))
        self.assertEqual(lines[1][1], 'Purchase claims held until the public catalog matches the canonical gifts')
        self.assertEqual([l[1] for l in lines[2:]], [r['title'] for r in recommendations()])
        self.assertEqual([l[2] for l in lines[2:]], [r['objective_key'] for r in recommendations()])
        # Without Control Center's reading, the rung comes from the repository's own ladder and no reading is claimed.
        bare = directive(instruction=False)
        del bare['directive']['north_star']
        first = self.build(bare)['priorities'][0]['line']
        self.assertTrue(first.endswith("This week's rung is $728."), first)

    def test_obsessions_are_only_his_quoted_words_still_in_their_files(self):
        found = engine_state.obsessions(self.root)
        self.assertEqual([o['since'] for o in found], ['2026-10-18', '2026-10-14', '2026-10-14'])
        for item in found:
            self.assertTrue(item['line'].startswith('"') and item['line'].endswith('"'))
            self.assertLessEqual(len(item['line']), 200)
        (self.root / 'AGENTS.md').write_text('# Nothing quoted here any more.\n')
        self.assertEqual(len(engine_state.obsessions(self.root)), 1)
        (self.root / 'docs/NORTH_STAR.md').unlink()
        self.assertEqual(engine_state.obsessions(self.root), [])
        self.assertNotIn('obsessions', self.build(directive(instruction=False)))

    def test_next_steps_come_from_get_going_then_now_md_and_drop_an_address(self):
        steps = engine_state.next_steps(self.root)
        self.assertEqual(steps, [
            {'line': 'Build step 1 (docs/GET-GOING.md): The synthetic loop, proved against the stand-in.', 'waits_on': 'engine', 'when': None},
            {'line': 'Krish posts the synthetic reel at 13:00 London.', 'waits_on': 'krish', 'when': '2026-10-19'},
            {'line': 'Waiting on Krish: set the synthetic channel times. Then a second sentence.', 'waits_on': 'krish', 'when': None},
            {'line': 'Still to rewrite: the synthetic playbook.', 'waits_on': 'engine', 'when': None},
            {'line': 'Rule on the synthetic brief before it is proposed.', 'waits_on': 'krish', 'when': None},
        ])
        (self.root / 'docs/GET-GOING.md').unlink()
        (self.root / 'NOW.md').unlink()
        self.assertEqual(engine_state.next_steps(self.root), [])

    def test_lines_never_carry_an_address_or_a_phone_number_and_wrap_whole(self):
        self.assertIsNone(engine_state.line('Write to someone@example.invalid today'))
        self.assertIsNone(engine_state.line('Call +1 (555) 010-0199 today'))
        self.assertEqual(engine_state.line('Due 2026-12-28 at 13:00'), 'Due 2026-12-28 at 13:00')
        long = 'A short first sentence. ' + 'word ' * 60
        self.assertEqual(engine_state.line(long), 'A short first sentence.')
        self.assertLessEqual(len(engine_state.line('word ' * 80)), 200)

    def test_a_malformed_instruction_is_ignored(self):
        for bad in ({'id': 'ki_short', 'words': WORDS}, {'id': IID, 'words': ''}, 'text', None):
            value = directive()
            value['directive']['krish_instruction'] = bad
            report = self.build(value)
            self.assertNotIn('instruction_acks', report)
            self.assertEqual(validate(SCHEMA, report), [])


class WakeTests(unittest.TestCase):
    """The loop, end to end against the local stand-in: a second wake the same day, and the words never printed."""

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        write_docs(self.root)
        self.stand = StandIn()
        self.stand.directive = directive()
        self.env = {'CONTROL_CENTER_ENGINE_TOKEN': TOKEN, 'CONTROL_CENTER_URL': self.stand.base,
                    'GITHUB_EVENT_NAME': 'repository_dispatch', 'GITHUB_RUN_ID': '42', 'GITHUB_RUN_ATTEMPT': '1',
                    'CC_DIRECTIVE_ID': 'heartside:2026-10-19'}

    def tearDown(self):
        self.stand.close()
        self.temporary.cleanup()

    def run_once(self, run_id, mode='live'):
        out, err = io.StringIO(), io.StringIO()
        client = control_center.Client(self.stand.base, TOKEN)
        env = {**self.env, 'GITHUB_RUN_ID': run_id}
        with redirect_stdout(out), redirect_stderr(err):
            summary = protocol.run(self.root, FakeGrowth(), client, mode, env, recommendations(), NOW)
        everything = out.getvalue() + err.getvalue() + json.dumps(summary) + '\n'.join(self.stand.logs)
        for path in self.root.rglob('*'):
            if path.is_file():
                everything += path.read_text(errors='ignore')
        self.assertNotIn('MARKER-7f3a', everything)
        return summary

    def test_a_second_wake_the_same_day_is_its_own_report_and_receives_once(self):
        first = self.run_once('42')
        self.assertEqual((first['run_id'], first['attempt']['status'], first['acks']),
                         ('heartside:2026-10-19:directive-42', 'succeeded', ['received']))
        self.assertEqual(first['instruction']['id'], IID)
        self.assertRegex(first['instruction']['words_sha256'], r'^[0-9a-f]{64}$')
        # Control Center wakes it again the same day (his instruction): a new GitHub run, so a new run id.
        second = self.run_once('43')
        self.assertEqual((second['run_id'], second['attempt']['status']), ('heartside:2026-10-19:directive-43', 'succeeded'))
        self.assertEqual(second['acks'], [])  # an earlier live report already received it
        self.assertEqual(set(self.stand.reports), {'heartside:2026-10-19:directive-42', 'heartside:2026-10-19:directive-43'})
        stored = self.stand.reports['heartside:2026-10-19:directive-43']
        self.assertIn('still open', stored['activity'][0]['line'])
        for report in self.stand.reports.values():
            self.assertEqual(validate(SCHEMA, report), [])
            self.assertNotIn('MARKER-7f3a', canonical(report))
        self.assertEqual(len(self.stand.routes('GET', 'reports')), 2)

    def test_no_instruction_makes_no_extra_call(self):
        self.stand.directive = directive(instruction=False)
        summary = self.run_once('44')
        self.assertEqual(summary['attempt']['status'], 'succeeded')
        self.assertNotIn('instruction', summary)
        self.assertFalse(self.stand.routes('GET', 'reports'))


if __name__ == '__main__':
    unittest.main()
