"""The one Control Center transport: the packs probe and the growth engine protocol client.

HTTPS only (plain HTTP only on loopback, for the local stand-in in tests), no
redirects, bounded timeouts, JSON only. The bearer is read by the caller at run
time and is never printed, logged, returned or written anywhere. Every failure
is reduced to a lower_snake code; no body, URL or header leaves this module.
"""
import datetime as dt
import hashlib
import json
import re
import socket
import urllib.error
import urllib.parse
import urllib.request

LOOPBACK = ('localhost', '127.0.0.1')
CODE = re.compile(r'^[a-z][a-z0-9_]{0,63}$')
MAX_RESPONSE = 2_000_000


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def origin_ok(base):
    origin = urllib.parse.urlsplit(base or '')
    secure = origin.scheme == 'https' or (origin.scheme == 'http' and origin.hostname in LOOPBACK)
    return bool(secure and origin.hostname and not origin.username and not origin.password
                and not origin.query and not origin.fragment and origin.path in ('', '/'))


def opener_for(base):
    handlers = [NoRedirect()]
    if urllib.parse.urlsplit(base).hostname in LOOPBACK:
        handlers.append(urllib.request.ProxyHandler({}))  # the local stand-in is never proxied
    return urllib.request.build_opener(*handlers).open


def probe(base, bearer, opener=None):
    result = {'checked_at': dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'),
              'credential_present': bool(bearer), 'authenticated': False,
              'http_status': None, 'venture_isolation': False}
    if not bearer:
        return {**result, 'outcome': 'missing_runner_secret'}
    if not origin_ok(base):
        return {**result, 'outcome': 'invalid_reporting_origin'}
    req = urllib.request.Request(base.rstrip('/') + '/api/growth/packs?days=1&venture=heartside',
                                 headers={'Authorization': 'Bearer ' + bearer,
                                          'User-Agent': 'growth-heartside reporting-access', 'Accept': 'application/json'})
    call = opener or opener_for(base)
    try:
        with call(req, timeout=20) as response:
            result['http_status'] = response.status
            body = json.loads(response.read(MAX_RESPONSE))
    except urllib.error.HTTPError as e:
        result['http_status'] = e.code
        outcome = 'control_center_unauthorized' if e.code in (401, 403) else 'reporting_endpoint_unavailable'
        return {**result, 'outcome': outcome}
    except (urllib.error.URLError, TimeoutError, ValueError, OSError):
        return {**result, 'outcome': 'reporting_connection_or_response_failed'}
    if result['http_status'] != 200 or not isinstance(body, dict) or body.get('ok') is not True:
        return {**result, 'outcome': 'unexpected_reporting_response'}
    ventures = body.get('ventures')
    isolated = isinstance(ventures, list) and 'heartside' in ventures
    return {**result, 'authenticated': True, 'venture_isolation': isolated,
            'outcome': 'ready' if isolated else 'authenticated_legacy_api'}


# ---------------------------------------------------------------------------
# Growth engine protocol 1.0.0 (docs/control-center/ENGINE-PROTOCOL.md).
# ---------------------------------------------------------------------------
def _wire_safe(value):
    """Refuse numbers that JavaScript and Python would write differently."""
    if isinstance(value, float):
        if value != value or value in (float('inf'), float('-inf')):
            raise ValueError('numbers must be finite')
        if value.is_integer():
            raise ValueError('send whole numbers as int: JavaScript writes 1 where Python writes 1.0')
        if 'e' in repr(value):
            raise ValueError('number too large or small for a shared canonical form')
    elif isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise ValueError('object keys must be strings')
            _wire_safe(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            _wire_safe(item)


def canonical(value):
    """Keys sorted at every depth, no whitespace, strings as JSON.stringify writes them."""
    _wire_safe(value)
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False)


def sha256(value):
    return hashlib.sha256(canonical(value).encode('utf-8')).hexdigest()


def report_digest(report):
    return sha256({k: v for k, v in report.items() if k != 'payload_sha256'})


class ProtocolError(Exception):
    """Carries only a lower_snake code and the HTTP status, never a body or credential."""

    def __init__(self, code, status=None):
        super().__init__(code)
        self.code = code if CODE.match(code or '') else 'protocol_error'
        self.status = status


def _code(status, body):
    named = body.get('error') or body.get('code') if isinstance(body, dict) else None
    if isinstance(named, str) and CODE.match(named) and status in (409, 500):
        return named  # engine_inactive, store_failed
    if 300 <= status < 400:
        return 'redirect_refused'
    return {400: 'bad_request', 401: 'unauthorized', 403: 'forbidden', 404: 'not_found',
            409: 'conflict', 413: 'report_too_large', 429: 'rate_limited'}.get(
                status, 'server_error' if status >= 500 else 'unexpected_status')


class Client:
    """The six engine calls. One bearer, one engine, no retries of a write."""

    def __init__(self, base, token, slug='heartside', opener=None, timeout=20):
        if not token:
            raise ProtocolError('missing_engine_token')
        if not origin_ok(base):
            raise ProtocolError('invalid_control_center_url')
        self._root = base.rstrip('/') + f'/api/growth/engines/{slug}/'
        self._token = token
        self._open = opener or opener_for(base)
        self._timeout = timeout

    def __repr__(self):
        return '<control_center.Client>'

    def _call(self, method, path, body=None, headers=None):
        data = canonical(body).encode('utf-8') if body is not None else None
        req = urllib.request.Request(self._root + path, data=data, method=method, headers={
            'Authorization': 'Bearer ' + self._token, 'Accept': 'application/json',
            'User-Agent': 'growth-heartside engine-protocol',
            **({'Content-Type': 'application/json'} if data is not None else {}), **(headers or {})})
        try:
            with self._open(req, timeout=self._timeout) as response:
                status, raw = response.status, response.read(MAX_RESPONSE + 1)
        except urllib.error.HTTPError as e:
            status = e.code
            try:
                raw = e.read(65536) if e.fp else b''
            except OSError:
                raw = b''
            finally:
                e.close()
        except (socket.timeout, TimeoutError):
            raise ProtocolError('timeout') from None
        except urllib.error.URLError as e:
            raise ProtocolError('timeout' if isinstance(e.reason, TimeoutError) else 'connection_failed') from None
        except (OSError, ValueError):
            raise ProtocolError('connection_failed') from None
        if len(raw) > MAX_RESPONSE:
            raise ProtocolError('response_too_large', status)
        try:
            parsed = json.loads(raw) if raw else None
        except ValueError:
            parsed = None
        if 200 <= status < 300 and not isinstance(parsed, dict):
            raise ProtocolError('invalid_response', status)
        return status, parsed

    def _expect(self, status, body, allow_missing=False):
        if 200 <= status < 300:
            return body
        if status == 404 and allow_missing:
            return None
        raise ProtocolError(_code(status, body), status)

    def attempt(self, record):
        status, body = self._call('POST', 'attempts', record)
        body = self._expect(status, body)
        if body.get('ok') is not True:
            raise ProtocolError('attempt_not_recorded', status)
        return body

    def directive(self, date=None):
        query = '?' + urllib.parse.urlencode({'date': date}) if date else ''
        status, body = self._call('GET', 'directive' + query)
        body = self._expect(status, body, allow_missing=True)
        if body is not None and (body.get('ok') is not True or not isinstance(body.get('directive'), dict)):
            raise ProtocolError('invalid_directive', status)
        return body

    def post_report(self, report):
        status, body = self._call('POST', 'reports', report, {'Idempotency-Key': report['run_id']})
        body = self._expect(status, body)
        if body.get('accepted') is not True or body.get('payload_sha256') != report['payload_sha256']:
            raise ProtocolError('report_digest_mismatch', status)
        return body

    def read_report(self, run_id):
        status, body = self._call('GET', 'reports/' + urllib.parse.quote(run_id, safe=''))
        return self._expect(status, body, allow_missing=True)

    def decisions(self, since):
        status, body = self._call('GET', 'decisions?' + urllib.parse.urlencode({'since': since}))
        body = self._expect(status, body)
        if body.get('ok') is not True or not isinstance(body.get('decisions'), list):
            raise ProtocolError('invalid_decisions', status)
        return body['decisions']
