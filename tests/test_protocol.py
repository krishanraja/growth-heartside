"""The Control Center growth engine protocol, proved against a local stand-in only."""
from contextlib import redirect_stderr, redirect_stdout
import copy
import datetime as dt
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import io
import json
import logging
from pathlib import Path
import re
import tempfile
import threading
import unittest
import urllib.parse

from engine import assets, control_center, ledger, media, protocol
from engine.engine_state import carries_contact
from engine.control_center import Client, ProtocolError, canonical, report_digest
from tests.ui_fixtures import evidence

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = json.loads((ROOT / 'docs/control-center/engine-report.schema.json').read_text())
EXAMPLE = json.loads((ROOT / 'docs/control-center/engine-report.example.json').read_text())
TOKEN = 'gen1_' + 'synthetic-test-bearer-' + 'z' * 30
NOW = dt.datetime(2026, 10, 19, 8, 0, tzinfo=dt.timezone.utc)
ENGINE_STATE_KEYS = ('priorities', 'obsessions', 'next_steps', 'instruction_acks')
CID = 'IG_EMO_REEL_C01_H03_V1_20261019'
REVISION = 'c' * 64
CAPTION = 'Your dog loves you too. The note on the example portrait is signed Love, Milo.'
STATE = {'sha': 'a' * 40, 'rules_ok': True, 'synced_at': '2026-10-19T07:55:00+00:00',
         'offers': [{'id': 'portrait', 'name': 'portrait', 'kind': 'gift', 'price_cents': 5900, 'prices_cents': [5900, 11900]}],
         'store': [{'title': 'An older print', 'available': True, 'prices': [24.0]}]}
DIRECTIVE = {'ok': True, 'chosen_by': 'rule', 'directive': {
    'schema_version': '1.0.0', 'directive_id': 'heartside:2026-10-19', 'engine_id': 'growth-heartside',
    'for_date': '2026-10-19', 'aim': 'synthetic aim', 'objectives': [],
    'next_action': {'proposal_id': 'heartside:rec:measurement', 'instruction': 'Import the reports', 'why': 'Widest gap',
                    'close_condition': {'event': 'measurement_current', 'reference': None}},
    'decisions_since': [], 'constraints': {'walls': 'synthetic walls', 'spend_cap_usd': 0, 'max_actions': 5}}}


def validate(schema, value, path='$'):
    """Strict subset of JSON Schema: also refuses a field the schema does not name at any depth."""
    errors = []
    kinds = schema.get('type')
    kinds = kinds if isinstance(kinds, list) else [kinds] if kinds else []
    checks = {'object': lambda v: isinstance(v, dict), 'array': lambda v: isinstance(v, list),
              'string': lambda v: isinstance(v, str), 'null': lambda v: v is None,
              'number': lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
              'integer': lambda v: isinstance(v, int) and not isinstance(v, bool),
              'boolean': lambda v: isinstance(v, bool)}
    if kinds and not any(checks[k](value) for k in kinds):
        return [f'{path}: wrong type']
    if 'oneOf' in schema and sum(not validate(branch, value, path) for branch in schema['oneOf']) != 1:
        errors.append(f'{path}: matches no single oneOf branch')
    if 'const' in schema and value != schema['const']:
        errors.append(f'{path}: not {schema["const"]}')
    if 'enum' in schema and value not in schema['enum']:
        errors.append(f'{path}: not in {schema["enum"]}')
    if isinstance(value, dict) and 'properties' in schema:
        errors += [f'{path}.{k}: required' for k in schema.get('required', []) if k not in value]
        for key, item in value.items():
            if key not in schema['properties']:
                errors.append(f'{path}.{key}: unknown field')
            else:
                errors += validate(schema['properties'][key], item, f'{path}.{key}')
    if isinstance(value, list):
        if len(value) > schema.get('maxItems', len(value)):
            errors.append(f'{path}: too many items')
        for i, item in enumerate(value):
            errors += validate(schema.get('items', {}), item, f'{path}[{i}]')
    if isinstance(value, str):
        if len(value) > schema.get('maxLength', len(value)):
            errors.append(f'{path}: too long')
        if 'pattern' in schema and not re.search(schema['pattern'], value):
            errors.append(f'{path}: pattern')
    if isinstance(value, (int, float)) and not isinstance(value, bool) and value < schema.get('minimum', value):
        errors.append(f'{path}: below minimum')
    return errors


class StandIn:
    """An in-process Control Center for one engine. It never leaves 127.0.0.1."""

    def __init__(self, token=TOKEN):
        self.token, self.calls, self.attempts, self.reports = token, [], {}, {}
        self.directive, self.decisions, self.inactive, self.redirect = copy.deepcopy(DIRECTIVE), [], False, False
        self.logs = []
        stand = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, fmt, *args):
                stand.logs.append(fmt % args)

            def reply(self, status, body=None, headers=None):
                data = json.dumps(body).encode() if body is not None else b''
                self.send_response(status)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Cache-Control', 'no-store')
                for k, v in (headers or {}).items():
                    self.send_header(k, v)
                self.send_header('Content-Length', str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def handle_any(self, method):
                url = urllib.parse.urlsplit(self.path)
                prefix = '/api/growth/engines/heartside/'
                route = url.path[len(prefix):] if url.path.startswith(prefix) else None
                body = None
                if method == 'POST':
                    body = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
                stand.calls.append((method, route, body, self.headers.get('Idempotency-Key')))
                if stand.redirect:
                    return self.reply(302, {}, {'Location': 'https://elsewhere.invalid/'})
                if self.headers.get('Authorization') != 'Bearer ' + stand.token or route is None:
                    return self.reply(401, {'error': 'unauthorized'})
                if method == 'GET' and route == 'directive':
                    return self.reply(200, stand.directive)
                if method == 'GET' and route == 'decisions':
                    return self.reply(200, {'ok': True, 'decisions': stand.decisions})
                if method == 'POST' and route == 'attempts':
                    return self.attempt(body)
                if method == 'POST' and route == 'reports':
                    return self.report(body)
                if method == 'GET' and route == 'reports':  # ?recent=<n>: own live reports, newest first
                    n = int(urllib.parse.parse_qs(url.query).get('recent', ['10'])[0])
                    live = [r for r in reversed(list(stand.reports.values())) if r.get('mode') == 'live'][:n]
                    return self.reply(200, {'ok': True, 'reports': [
                        {'run_id': r['run_id'], 'accepted_at': '2026-10-19T08:00:01Z', 'status': r.get('status'),
                         'activity': r.get('activity', [])} for r in live]})
                if method == 'GET' and route.startswith('reports/'):
                    run_id = urllib.parse.unquote(route[len('reports/'):])
                    if run_id not in stand.reports:
                        return self.reply(404, {'error': 'not_found'})
                    stored = stand.reports[run_id]
                    return self.reply(200, {'accepted': True, 'run_id': run_id, 'payload_sha256': stored['payload_sha256'],
                                            'mode': stored['mode'], 'accepted_at': '2026-10-19T08:00:01Z', 'report': stored})
                return self.reply(404, {'error': 'not_found'})

            def attempt(self, record):
                history = stand.attempts.setdefault(record['attempt_id'], [])
                if record['status'] != 'started':
                    terminal = [r for r in history if r['status'] != 'started']
                    if terminal and terminal[0] != record:
                        return self.reply(409, {'error': 'attempt_conflict'})
                    if terminal:
                        return self.reply(200, {'ok': True, 'attempt': record, 'replayed': True})
                history.append(record)
                return self.reply(200, {'ok': True, 'attempt': record})

            def report(self, report):
                # Like Control Center: any 1.x the schema lists, and a field newer than the version sent is refused.
                version = tuple(int(p) for p in str(report.get('schema_version', '0.0.0')).split('.'))
                if report.get('credits_spent') is not None and version < (1, 16, 0):
                    return self.reply(400, {'error': 'schema_version'})
                if any(k in report for k in ENGINE_STATE_KEYS) and version < (1, 20, 0):
                    return self.reply(400, {'error': 'schema_version'})
                if any(carries_contact(x['line']) for k in ENGINE_STATE_KEYS for x in report.get(k, [])):
                    return self.reply(400, {'error': 'bad_request'})
                if validate(SCHEMA, report) or self.headers.get('Idempotency-Key') != report.get('run_id'):
                    return self.reply(400, {'error': 'bad_request'})
                if report_digest(report) != report['payload_sha256']:
                    return self.reply(400, {'error': 'payload_sha256'})
                if stand.inactive and report['mode'] == 'live':
                    return self.reply(409, {'error': 'engine_inactive'})
                old = stand.reports.get(report['run_id'])
                if old and old['payload_sha256'] != report['payload_sha256']:
                    return self.reply(409, {'error': 'conflict'})
                stand.reports[report['run_id']] = report
                return self.reply(200, {'accepted': True, 'run_id': report['run_id'],
                                        'payload_sha256': report['payload_sha256'], 'replayed': bool(old)})

            def do_GET(self):
                self.handle_any('GET')

            def do_POST(self):
                self.handle_any('POST')

        self.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        self.base = f'http://127.0.0.1:{self.server.server_address[1]}'
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def close(self):
        self.server.shutdown()
        self.server.server_close()

    def routes(self, method, route):
        return [c for c in self.calls if c[0] == method and c[1] == route]


class FakeGrowth:
    HERE = str(ROOT)

    def __init__(self, state=STATE, fail=False):
        self.state, self.fail = state, fail

    def sync(self, quiet=False):
        if self.fail:
            raise OSError('network down')
        return copy.deepcopy(self.state)

    def load_state(self):
        return copy.deepcopy(self.state)


# A fixture, not the live file: recommendations.json is empty since 14 Nov (its two advice items were withdrawn).
RECOMMENDATIONS = [
    {
        "id": "heartside:rec:product-readiness",
        "title": "Verify the product before a sales campaign",
        "why": "The approved gift range differs from the public catalog. Product work is already handed over.",
        "target_url": "https://github.com/krishanraja/heartside/pull/13",
        "next_action": "The product owner completes the public gift range and real purchase and print proof, then the engine refreshes readiness. Growth continues with audience materials meanwhile.",
        "closes_when": "The canonical gifts, prices, purchase flow and print proof agree with the public store. Product evidence stays in heartside.",
        "close_event": "catalog_ready",
        "objective_key": "net_sales_usd"
    },
    {
        "id": "heartside:rec:measurement",
        "title": "Keep measurement evidence current",
        "why": "Connected analytics in an authoring session do not grant the scheduled runner the same private access. No performance winner can be declared before real publications and observations.",
        "target_url": "https://github.com/krishanraja/growth-heartside/blob/main/docs/ENGINE.md",
        "next_action": "Import current verified aggregate Shopify reports and native creative observations through the documented schemas. Configure a licensed provider budget separately before enabling paid generation.",
        "closes_when": "Current reporting windows and exact published creative revisions have source-backed observations, with missing attribution still explicit.",
        "close_event": "measurement_current",
        "objective_key": "organic_orders"
    }
]


def recommendations():
    return json.loads(json.dumps(RECOMMENDATIONS))


class DigestTests(unittest.TestCase):
    def test_worked_example_digest_is_reproduced(self):
        self.assertEqual(report_digest(EXAMPLE), 'f4351324e84aa1baf6afd1bc4d2ffadb3039ab6399b2309c2717b89a26a0a517')
        self.assertEqual(report_digest(EXAMPLE), EXAMPLE['payload_sha256'])
        self.assertEqual(validate(SCHEMA, EXAMPLE), [])

    def test_canonical_json_matches_javascript_and_refuses_python_only_numbers(self):
        self.assertEqual(canonical({'b': [1, 'é'], 'a': {'d': None, 'c': 12.5}}), '{"a":{"c":12.5,"d":null},"b":[1,"é"]}')
        with self.assertRaises(ValueError):
            canonical({'value': 1.0})
        self.assertEqual(protocol.money(10.0), 10)
        self.assertEqual(protocol.money(-3.456), -3.46)


class ReportTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.db = ledger.connect(self.root / 'local/engine.sqlite3')
        (self.root / 'config').mkdir(exist_ok=True)
        (self.root / 'config/channels.json').write_text((ROOT / 'config/channels.json').read_text())

    def tearDown(self):
        self.db.close()
        self.temporary.cleanup()

    def build(self, db='self', directive=None, state=STATE):
        return protocol.build_report(root=self.root, state=copy.deepcopy(state), db=self.db if db == 'self' else db, now=NOW,
                                     run_id='heartside:2026-10-19:synthetic-directive', mode='synthetic',
                                     directive=directive, recommendations=recommendations())

    def approve(self, caption=CAPTION):
        item = {'platform': 'instagram', 'creative_id': CID, 'intent': 'audience', 'why': 'test', 'text': caption, 'alt_text': 'A mug.'}
        path = self.root / 'local/media' / CID / 'rev/payload.bin'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b'checked fixture output')
        from tests.ui_fixtures import layout
        layout_path = path.parent / 'layout.json'; layout_path.write_text(json.dumps(layout()))
        manifest = {'version': media.VERSION, 'creative_id': CID, 'revision': REVISION, 'copy_sha256': {CID: media.copy_digest(item)},
                    'files': {role: {'path': str(p.relative_to(self.root)), 'sha256': assets.sha256(p)}
                              for role in media.REQUIRED_ROLES for p in [layout_path if role.endswith('_layout') else path]}}
        (path.parent / 'manifest.json').write_text(json.dumps(manifest))
        ledger.record_render(self.db, CID, REVISION, {'mechanism': 'Recognition opening.'}, manifest)
        ledger.mark(self.db, CID, REVISION, 'approved')
        pack = self.root / 'local/automation/runs/2026-10-19/daily-pack/pack.json'
        pack.parent.mkdir(parents=True, exist_ok=True)
        pack.write_text(json.dumps({'items': [item]}))
        release, review = evidence(self.root, CID, REVISION, caption, path, 'instagram', NOW.date())
        from engine import creative_ui
        release['alt_text'] = item['alt_text']
        next(e for e in release['exports'] if e['role'] == 'cover').update(manifest['files']['cover'])
        next(e for e in release['exports'] if e['role'] == 'layout').update(manifest['files']['reel_layout'])
        review['binding'] = creative_ui.digest(release)
        base = self.root / 'local/creative-ui' / REVISION
        (base / (CID + '.release.json')).write_text(json.dumps(release))
        (base / (CID + '.review.json')).write_text(json.dumps(review))
        return item

    def test_empty_ledger_is_schema_valid_and_unknown_objectives_stay_null_with_reasons(self):
        report = self.build()
        self.assertEqual(validate(SCHEMA, report), [])
        self.assertEqual(report['payload_sha256'], report_digest(report))
        for objective in report['objectives']:
            self.assertIsNone(objective['value'])
            self.assertEqual(objective['availability'], 'missing')
            self.assertTrue(objective['reason'])
        self.assertEqual(report['status'], 'held')
        self.assertIn('heartside PR 13', report['holds'][0]['detail'])
        self.assertEqual([p['proposal_id'] for p in report['proposals']], ['heartside:rec:product-readiness', 'heartside:rec:measurement'])
        self.assertTrue(all(p['wall'] == 'none' for p in report['proposals']))
        self.assertNotIn('spend', {p['wall'] for p in report['proposals']})

    def test_a_failed_scheduled_job_is_held_with_the_runner_s_reason(self):
        index = self.root / 'local/automation/index.json'
        index.parent.mkdir(parents=True, exist_ok=True)
        reason = 'the approved blanket image is no longer in the live blanket gallery'
        index.write_text(json.dumps({
            '2026-10-19/daily-pack': {'status': 'failed', 'attempts': 3, 'error_type': 'ValueError', 'error': reason},
            '2026-10-18/radar': {'status': 'failed', 'attempts': 1, 'error_type': 'OSError'},
            '2026-10-19/numbers': {'status': 'completed', 'attempts': 1},
            '2026-10-18/numbers': {'status': 'failed', 'attempts': 2, 'error_type': 'ValueError'},
            '2026-10-10/daily-pack': {'status': 'failed', 'attempts': 9, 'error_type': 'ValueError', 'error': 'old'}}))
        report = self.build()
        failed = [h for h in report['holds'] if h['reason'] == 'A scheduled draft job failed']
        self.assertEqual([h['detail'] for h in failed], [
            f'daily-pack for 2026-10-19 failed after 3 attempt(s): {reason}. It retries while the job is due today.',
            'radar for 2026-10-18 failed after 1 attempt(s): OSError, with no reason recorded. That day is not run again.'])
        self.assertEqual(validate(SCHEMA, report), [])
        self.assertEqual(report['status'], 'held')
        # A job that completed on a later day is no longer held for an earlier failure.
        index.write_text(json.dumps({'2026-10-18/daily-pack': {'status': 'failed', 'attempts': 2, 'error_type': 'ValueError'},
                                     '2026-10-19/daily-pack': {'status': 'completed', 'attempts': 1}}))
        self.assertFalse(any(h['reason'] == 'A scheduled draft job failed' for h in self.build()['holds']))
        index.write_text('not json')
        self.assertFalse(any(h['reason'] == 'A scheduled draft job failed' for h in self.build()['holds']))

    def test_product_hold_follows_current_product_truth(self):
        live = {**STATE, 'store': [{'title': "Your Dog's Portrait", 'available': True, 'prices': [59.0, 119.0]}], 'homepage_v3': False}
        report = self.build(state=live)
        self.assertEqual([h['reason'] for h in report['holds']], ['Conversion editions held until the V3 homepage is public'])
        self.assertFalse(any(a['evidence_url'] == protocol.STORE_URL for a in report['activity']))
        report = self.build(state={**live, 'homepage_v3': True})
        self.assertEqual((report['holds'], report['status']), ([], 'ready'))
        released = [a for a in report['activity'] if a['evidence_url'] == protocol.STORE_URL]
        self.assertEqual(len(released), 1)
        self.assertIn('V3 gift journey', released[0]['line'])
        self.assertEqual(validate(SCHEMA, report), [])

    def test_no_ledger_is_degraded_not_zero(self):
        report = self.build(db=None)
        self.assertEqual(report['status'], 'degraded')
        self.assertIsNone(report['objectives'][0]['value'])
        self.assertEqual(validate(SCHEMA, report), [])

    def test_the_report_carries_the_north_star_objective_control_center_reads(self):
        # Control Center reads organic_net_sales_usd (api/_northStarRefresh.ts, HEARTSIDE_ORGANIC_OBJECTIVE).
        report = self.build()
        self.assertEqual([o['key'] for o in report['objectives']], ['net_sales_usd', 'organic_orders', 'organic_net_sales_usd'])
        self.assertEqual((report['objectives'][2]['value'], report['objectives'][2]['availability']), (None, 'missing'))
        from engine import attribution
        start, end = attribution.windows(dt.date(2026, 10, 19))['trailing_28d']
        attribution.store(self.db, 'trailing_28d', attribution.aggregate([], start, end), observed_at='2026-10-19T07:00:00+00:00')
        report = self.build()
        north_star = report['objectives'][2]
        self.assertEqual((north_star['key'], north_star['value'], north_star['unit'], north_star['availability']),
                         ('organic_net_sales_usd', 0, 'USD', 'measured'))
        self.assertEqual(validate(SCHEMA, report), [])
        self.assertEqual(report['payload_sha256'], report_digest(report))

    def import_sales(self, start, end, value, observed='2026-10-19T07:00:00Z'):
        ledger.import_report(self.db, {'platform': 'shopify', 'scope': 'store', 'currency': 'USD', 'source': 'Synthetic ShopifyQL',
                                       'observed_at': observed, 'period': {'start': start, 'end': end, 'timezone': 'Europe/London'},
                                       'values': {'net_sales': value, 'orders': 0}})

    def test_measured_zero_is_zero_and_never_a_float_one_point_oh(self):
        self.import_sales('2026-10-01', '2026-10-19', 0)
        sales = self.build()['objectives'][0]
        self.assertEqual((sales['value'], sales['availability'], sales['reason']), (0, 'measured', None))
        self.assertIs(type(sales['value']), int)
        self.assertEqual(sales['window_start'], '2026-10-01T00:00:00+01:00')
        self.assertEqual(sales['window_end'], '2026-10-19T00:00:00+01:00')

    def test_overlapping_windows_are_never_added_and_old_coverage_is_stale(self):
        self.import_sales('2026-10-01', '2026-10-15', 120.5)
        self.import_sales('2026-10-10', '2026-10-15', 80)
        sales = self.build()['objectives'][0]
        self.assertEqual((sales['value'], sales['availability']), (120.5, 'stale'))
        self.assertIn('2026-10-14', sales['reason'])
        self.import_sales('2026-10-01', '2026-10-19', 199)
        self.assertEqual(self.build()['objectives'][0]['value'], 199)

    def test_partial_coverage_is_missing(self):
        self.import_sales('2026-10-05', '2026-10-19', 50)
        sales = self.build()['objectives'][0]
        self.assertEqual((sales['value'], sales['availability']), (None, 'missing'))

    def test_approved_creative_is_a_post_proposal_bound_to_creative_revision_and_caption(self):
        self.approve()
        report = self.build()
        self.assertEqual(validate(SCHEMA, report), [])
        post = report['proposals'][0]
        self.assertEqual((post['proposal_id'], post['wall'], post['channel'], post['exact_payload']),
                         ('heartside:post:' + CID, 'post', 'instagram', CAPTION))
        self.assertEqual(post['payload_sha256'], protocol.post_payload_sha256(CID, REVISION, 'instagram', CAPTION))
        self.assertEqual(post['close_condition'], {'event': 'creative_published', 'reference': CID})
        self.assertEqual(post['expires_at'], '2026-10-26T04:00:00Z')
        changed = protocol.post_payload_sha256(CID, REVISION, 'instagram', CAPTION + ' Changed.')
        self.assertNotEqual(changed, post['payload_sha256'])

    def test_a_post_on_a_channel_krish_has_not_approved_is_held_not_proposed(self):
        # 14 Nov: Pinterest is not a posting channel (docs/CHANNEL-TASKS.md), yet nothing stopped an approved pin.
        self.approve()
        (self.root / 'config/channels.json').write_text(json.dumps({'posting': {'facebook': '2026-10-19'}}))
        report = self.build()
        self.assertEqual(validate(SCHEMA, report), [])
        self.assertFalse([p for p in report['proposals'] if p['wall'] == 'post'])
        self.assertTrue(any('not approved for posting' in h['reason'] and CID in h['detail'] for h in report['holds']))

    def test_the_approved_channels_are_the_three_and_never_pinterest_or_threads(self):
        self.assertEqual(protocol.posting_channels(ROOT), {'instagram', 'facebook', 'tiktok'})

    def test_a_tampered_caption_is_held_not_proposed(self):
        item = self.approve()
        pack = self.root / 'local/automation/runs/2026-10-19/daily-pack/pack.json'
        pack.write_text(json.dumps({'items': [{**item, 'text': 'Changed after review.'}]}))
        report = self.build()
        self.assertFalse([p for p in report['proposals'] if p['wall'] == 'post'])
        self.assertTrue(any(CID in (h['detail'] or '') for h in report['holds']))

    def test_approved_clean_export_without_native_ui_evidence_is_held(self):
        self.approve()
        receipt = self.root / 'local/creative-ui' / REVISION / (CID + '.review.json')
        receipt.write_text('{}')
        report = self.build()
        self.assertFalse([p for p in report['proposals'] if p['wall'] == 'post'])
        self.assertTrue(any('Placement UI' in h['reason'] for h in report['holds']))

    def test_declined_payload_is_not_proposed_again_and_publication_is_an_event(self):
        self.approve()
        digest = protocol.post_payload_sha256(CID, REVISION, 'instagram', CAPTION)
        directive = copy.deepcopy(DIRECTIVE)
        directive['directive']['decisions_since'] = [{'proposal_id': 'heartside:post:' + CID, 'decision': 'declined',
                                                      'decided_at': '2026-10-19T06:00:00Z', 'payload_sha256': digest}]
        report = self.build(directive=directive)
        self.assertNotIn('heartside:post:' + CID, [p['proposal_id'] for p in report['proposals']])
        directive['directive']['decisions_since'][0]['decision'] = 'approved'
        report = self.build(directive=directive)
        self.assertIn('heartside:post:' + CID, [p['proposal_id'] for p in report['proposals']])
        self.assertTrue(any('Krish approved' in a['line'] for a in report['activity']))
        self.assertEqual(report['events'], [])
        ledger.mark(self.db, CID, REVISION, 'published', 'https://www.instagram.com/reel/synthetic/')
        report = self.build()
        self.assertEqual(report['events'][0]['event'], 'creative_published')
        self.assertEqual(report['events'][0]['proposal_id'], 'heartside:post:' + CID)
        self.assertEqual(report['events'][0]['evidence_url'], 'https://www.instagram.com/reel/synthetic/')
        self.assertEqual(validate(SCHEMA, report), [])


class LoopTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.stand = StandIn()
        self.env = {'CONTROL_CENTER_ENGINE_TOKEN': TOKEN, 'CONTROL_CENTER_URL': self.stand.base,
                    'GITHUB_EVENT_NAME': 'repository_dispatch', 'GITHUB_RUN_ID': '42', 'GITHUB_RUN_ATTEMPT': '1',
                    'CC_DIRECTIVE_ID': 'heartside:2026-10-19'}

    def tearDown(self):
        self.stand.close()
        self.temporary.cleanup()

    def main(self, action='run', mode='synthetic', growth=None, code=None):
        out, err, logs = io.StringIO(), io.StringIO(), io.StringIO()
        handler = logging.StreamHandler(logs)
        logging.getLogger().addHandler(handler)
        try:
            with redirect_stdout(out), redirect_stderr(err):
                result = protocol.main(self.root, growth or FakeGrowth(), action, mode, code, env=self.env)
        finally:
            logging.getLogger().removeHandler(handler)
        everything = out.getvalue() + err.getvalue() + logs.getvalue() + '\n'.join(self.stand.logs)
        for path in self.root.rglob('*'):
            if path.is_file():
                everything += path.read_text(errors='ignore')
        self.assertNotIn(TOKEN, everything)
        self.assertNotIn(TOKEN[5:20], everything)
        return result, out.getvalue()

    def statuses(self, run_id):
        return [(a['status'], a['error_code']) for a in self.stand.attempts.get(run_id, [])]

    def test_full_loop_attempt_directive_report_readback_decisions(self):
        self.stand.decisions = [{'proposal_id': 'heartside:rec:measurement', 'decision': 'approved',
                                 'decided_at': '2026-10-19T07:00:00Z', 'payload_sha256': 'f' * 64}]
        code, out = self.main()
        self.assertEqual(code, 0)
        run_id = 'heartside:2026-10-19:synthetic-directive-42'
        self.assertEqual(self.statuses(run_id), [('started', None), ('succeeded', None)])
        started, terminal = self.stand.attempts[run_id]
        self.assertNotIn('finished_at', started)
        self.assertIn('finished_at', terminal)
        order = [(c[0], c[1].split('?')[0]) for c in self.stand.calls]
        self.assertEqual(order, [('POST', 'attempts'), ('GET', 'directive'), ('GET', 'capabilities'), ('POST', 'reports'),
                                 ('GET', 'reports/' + urllib.parse.quote(run_id, safe='')), ('GET', 'decisions'), ('POST', 'attempts')])
        posted = self.stand.routes('POST', 'reports')[0]
        self.assertEqual(posted[3], run_id)
        self.assertEqual(validate(SCHEMA, posted[2]), [])
        self.assertEqual(posted[2]['mode'], 'synthetic')
        summary = json.loads(out)
        self.assertEqual(summary['delivery'], {'replayed': False, 'readback': 'match'})
        # The live recommendations.json is empty since 14 Nov, so a decision on the withdrawn advice is not in this report.
        self.assertEqual(summary['decisions'], [{'proposal_id': 'heartside:rec:measurement', 'decision': 'approved', 'binding': 'not_in_this_report'}])
        self.assertEqual((summary['posted'], summary['sent'], summary['spent_usd']), (0, 0, 0))

    def test_exact_replay_is_answered_replayed_and_read_back(self):
        client = Client(self.stand.base, TOKEN)
        report = protocol.build_report(root=self.root, state=copy.deepcopy(STATE), db=None, now=NOW, run_id='heartside:2026-10-19:synthetic-replay',
                                       mode='synthetic', directive=None, recommendations=recommendations())
        self.assertEqual(protocol.deliver(client, report), {'replayed': False, 'readback': 'match'})
        self.assertEqual(protocol.deliver(client, report), {'replayed': True, 'readback': 'match'})
        self.assertEqual(client.read_report(report['run_id'])['payload_sha256'], report['payload_sha256'])

    def test_conflict_is_read_back_never_retried_blindly(self):
        run_id = 'heartside:2026-10-19:synthetic-directive-42'
        self.stand.reports[run_id] = {'run_id': run_id, 'mode': 'synthetic', 'payload_sha256': 'e' * 64}
        code, _ = self.main()
        self.assertEqual(code, 1)
        self.assertEqual(len(self.stand.routes('POST', 'reports')), 1)
        self.assertEqual(self.statuses(run_id), [('started', None), ('failed', 'report_conflict')])
        self.assertEqual(self.stand.reports[run_id]['payload_sha256'], 'e' * 64)

    def test_inactive_engine_is_a_coded_failure(self):
        self.stand.inactive = True
        code, _ = self.main(mode='live')
        self.assertEqual(code, 1)
        self.assertEqual(self.statuses('heartside:2026-10-19:directive-42'), [('started', None), ('failed', 'engine_inactive')])

    def test_unauthorized_is_a_failed_attempt_with_a_code_and_no_token_in_output(self):
        self.env['CONTROL_CENTER_ENGINE_TOKEN'] = TOKEN[:-4] + 'nope'
        code, out = self.main()
        self.assertEqual(code, 1)
        summary = json.loads(out)
        self.assertEqual((summary['attempt']['status'], summary['attempt']['error_code']), ('failed', 'unauthorized'))
        self.assertFalse(summary['attempt']['recorded'])
        self.assertNotIn(self.env['CONTROL_CENTER_ENGINE_TOKEN'], out)
        self.assertFalse(self.stand.routes('POST', 'reports'))

    def test_start_then_restore_failure_closes_the_attempt_once(self):
        self.assertEqual(self.main('start')[0], 0)
        self.assertEqual(self.main('finish', code='checkpoint_restore_failed')[0], 1)
        self.assertEqual(self.main('finish', code='checkpoint_restore_failed')[0], 0)
        self.assertEqual(self.statuses('heartside:2026-10-19:synthetic-directive-42'),
                         [('started', None), ('failed', 'checkpoint_restore_failed')])

    def test_failed_sync_uses_the_published_snapshot_and_reports_degraded(self):
        code, _ = self.main(growth=FakeGrowth(fail=True))
        self.assertEqual(code, 0)
        report = self.stand.routes('POST', 'reports')[0][2]
        self.assertEqual(report['status'], 'degraded')
        self.assertTrue(any('Product sync failed' in a['line'] for a in report['activity']))

    def test_missing_secret_says_so_and_makes_no_request(self):
        self.env['CONTROL_CENTER_ENGINE_TOKEN'] = ''
        code, out = self.main()
        self.assertEqual(code, 1)
        self.assertIn('CONTROL_CENTER_ENGINE_TOKEN is not set', out)
        self.assertFalse(self.stand.calls)

    def test_redirects_are_refused_and_cleartext_remote_origins_rejected(self):
        self.stand.redirect = True
        with self.assertRaises(ProtocolError) as caught:
            Client(self.stand.base, TOKEN).directive()
        self.assertEqual(caught.exception.code, 'redirect_refused')
        self.assertEqual(len(self.stand.calls), 1)
        for base in ('http://controlcenter.krishraja.com', 'https://user:pw@controlcenter.krishraja.com'):
            with self.assertRaises(ProtocolError):
                Client(base, TOKEN)
        self.assertNotIn(TOKEN, repr(Client(self.stand.base, TOKEN)))

    def test_run_ids_are_one_per_wake_and_never_reuse_the_dispatch_id(self):
        env = {'GITHUB_EVENT_NAME': 'repository_dispatch', 'GITHUB_RUN_ID': '42', 'GITHUB_RUN_ATTEMPT': '1'}
        self.assertEqual(protocol.run_identity('2026-10-19', 'live', env, NOW), 'heartside:2026-10-19:directive-42')
        self.assertEqual(protocol.run_identity('2026-10-19', 'live', {**env, 'GITHUB_RUN_ATTEMPT': '2'}, NOW), 'heartside:2026-10-19:directive-42-a2')
        # A second wake the same day (Krish's instruction, protocol 1.20.0) is a new GitHub run, so a new id.
        self.assertEqual(protocol.run_identity('2026-10-19', 'live', {**env, 'GITHUB_RUN_ID': '43'}, NOW), 'heartside:2026-10-19:directive-43')
        self.assertEqual(protocol.run_identity('2026-10-19', 'live', {'GITHUB_EVENT_NAME': 'workflow_dispatch', 'GITHUB_RUN_ID': '7'}, NOW),
                         'heartside:2026-10-19:manual-7')
        self.assertTrue(protocol.ID.match(protocol.run_identity('2026-10-19', 'synthetic', {**env, 'GITHUB_RUN_ATTEMPT': '3'}, NOW)))


if __name__ == '__main__':
    unittest.main()


class LoopMechanicsTests(unittest.TestCase):
    """14 Nov: the same two advice proposals were re-sent every day since 19 Oct; a plan could not be sent at all."""

    def test_replaced_proposals_are_withdrawn_only_when_served_and_not_proposed(self):
        served = {'features': {'withdrawn': True}}
        taken = protocol.withdrawals(served, [])
        self.assertEqual({w['proposal_id'] for w in taken}, set(protocol.WITHDRAWN))
        self.assertTrue(all(0 < len(w['reason']) <= 300 for w in taken))
        self.assertEqual(protocol.withdrawals({'features': {}}, []), [])
        self.assertEqual(len(protocol.withdrawals({}, [], {'withdrawn': True})), len(protocol.WITHDRAWN))
        live = protocol.recommendation_proposals(recommendations())
        self.assertEqual(protocol.withdrawals(served, live), [])

    def test_the_live_file_proposes_nothing_stale(self):
        self.assertEqual(json.loads((ROOT / 'recommendations.json').read_text()), [])

    def test_a_plan_goes_behind_its_wall_with_its_words_bound(self):
        rec = dict(recommendations()[0], wall='strategy', plan='the exact plan')
        proposal = protocol.recommendation_proposals([rec])[0]
        self.assertEqual((proposal['stage'], proposal['wall'], proposal['kind'], proposal['exact_payload']),
                         ('plan', 'strategy', 'prepared', 'the exact plan'))
        changed = protocol.recommendation_proposals([dict(rec, plan='another plan')])[0]
        self.assertNotEqual(proposal['payload_sha256'], changed['payload_sha256'])
        with self.assertRaises(ValueError):
            protocol.recommendation_proposals([dict(rec, wall='none')])
