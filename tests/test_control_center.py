from unittest.mock import patch
import io
import json
import unittest
from unittest.mock import Mock
import urllib.error

from engine.control_center import NoRedirect, probe


def response(body):
    value = io.BytesIO(json.dumps(body).encode())
    value.status = 200
    return value


class ReportingAccessTests(unittest.TestCase):
    def test_missing_secret_never_makes_a_request(self):
        opener = Mock()
        result = probe('https://controlcenter.krishraja.com', '', opener)
        self.assertEqual(result['outcome'], 'missing_runner_secret')
        opener.assert_not_called()

    def test_legacy_api_authentication_is_separate_from_venture_readiness(self):
        opener = Mock(return_value=response({'ok': True, 'packs': []}))
        result = probe('https://controlcenter.krishraja.com', 'test-secret', opener)
        self.assertTrue(result['authenticated'])
        self.assertFalse(result['venture_isolation'])
        self.assertEqual(result['outcome'], 'authenticated_legacy_api')
        req = opener.call_args.args[0]
        self.assertEqual(req.get_method(), 'GET')
        self.assertIn('venture=heartside', req.full_url)
        self.assertEqual(req.get_header('Authorization'), 'Bearer test-secret')
        self.assertNotIn('test-secret', json.dumps(result))

    def test_isolated_api_is_ready_without_copying_any_pack_content(self):
        opener = Mock(return_value=response({'ok': True, 'ventures': ['heartside'], 'packs': [{'text': 'private draft'}]}))
        result = probe('https://controlcenter.krishraja.com', 'test-secret', opener)
        self.assertEqual(result['outcome'], 'ready')
        self.assertNotIn('private draft', json.dumps(result))

    def test_errors_expose_only_controlled_diagnostics(self):
        for code in (401, 403, 503, 302):
            opener = Mock(side_effect=urllib.error.HTTPError('https://controlcenter.krishraja.com', code, 'test-secret', {}, None))
            result = probe('https://controlcenter.krishraja.com', 'test-secret', opener)
            self.assertFalse(result['authenticated'])
            self.assertEqual(result['http_status'], code)
            self.assertNotIn('test-secret', json.dumps(result))
        self.assertIsNone(NoRedirect().redirect_request(None, None, 302, '', {}, 'https://elsewhere.invalid'))

    def test_cleartext_or_credential_bearing_origins_are_refused(self):
        for base in ('http://controlcenter.krishraja.com', 'https://test-secret@controlcenter.krishraja.com', 'https://controlcenter.krishraja.com?x=1'):
            opener = Mock()
            result = probe(base, 'test-secret', opener)
            self.assertEqual(result['outcome'], 'invalid_reporting_origin')
            self.assertNotIn('test-secret', json.dumps(result))
            opener.assert_not_called()


class ScopeBoundaryTests(unittest.TestCase):
    def test_reporting_token_does_not_enable_central_requests(self):
        import os
        import growth
        with patch.dict(os.environ, {'GROWTH_ENGINE_TOKEN': 'test-only'}, clear=True), patch('engine.control_center.probe', side_effect=AssertionError('outside current scope')):
            allowed, reason = growth.control_center_takes_heartside()
            self.assertFalse(allowed)
            self.assertIn('disabled', reason)


if __name__ == '__main__':
    unittest.main()
