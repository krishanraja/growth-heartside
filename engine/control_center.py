"""Read-only reporting capability probe. Its output never includes a credential."""
import datetime as dt
import json
import urllib.error
import urllib.parse
import urllib.request


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def probe(base, bearer, opener=None):
    result = {'checked_at': dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'),
              'credential_present': bool(bearer), 'authenticated': False,
              'http_status': None, 'venture_isolation': False}
    if not bearer:
        return {**result, 'outcome': 'missing_runner_secret'}
    origin = urllib.parse.urlsplit(base)
    if (origin.scheme != 'https' and not (origin.scheme == 'http' and origin.hostname in ('localhost', '127.0.0.1'))
            or origin.username or origin.password or origin.query or origin.fragment or origin.path not in ('', '/')):
        return {**result, 'outcome': 'invalid_reporting_origin'}
    req = urllib.request.Request(base.rstrip('/') + '/api/growth/packs?days=1&venture=heartside',
                                 headers={'Authorization': 'Bearer ' + bearer,
                                          'User-Agent': 'growth-heartside reporting-access', 'Accept': 'application/json'})
    call = opener or urllib.request.build_opener(NoRedirect()).open
    try:
        with call(req, timeout=20) as response:
            result['http_status'] = response.status
            body = json.loads(response.read(2_000_000))
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
