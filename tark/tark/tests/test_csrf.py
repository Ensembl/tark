import os
from pathlib import Path
import runpy
from unittest.mock import patch

from django.conf import settings
from django.http import HttpResponse
from django.middleware.csrf import CsrfViewMiddleware, get_token
from django.test import RequestFactory, SimpleTestCase, override_settings


@override_settings(
    ALLOWED_HOSTS=['dev-tark.ensembl.org', 'tark.ensembl.org', 'localhost'],
    CSRF_TRUSTED_ORIGINS=[],
    CSRF_USE_SESSIONS=False,
    SECURE_PROXY_SSL_HEADER=('HTTP_X_FORWARDED_PROTO', 'https'),
)
class CsrfOriginTests(SimpleTestCase):
    def check_post(self, origin, host, token_state='valid', include_cookie=True, **headers):
        factory = RequestFactory()
        cookie_request = factory.get('/')
        token = get_token(cookie_request)
        if token_state == 'invalid':
            token = token[:-1] + ('A' if token[-1] != 'A' else 'B')
        data = {} if token_state == 'missing' else {'csrfmiddlewaretoken': token}
        request = factory.post('/web/search/', data, HTTP_HOST=host, HTTP_ORIGIN=origin, **headers)
        if include_cookie:
            request.COOKIES[settings.CSRF_COOKIE_NAME] = cookie_request.META['CSRF_COOKIE']

        middleware = CsrfViewMiddleware(lambda request: HttpResponse('ok'))
        middleware.process_request(request)
        return request, middleware.process_view(request, lambda request: HttpResponse('ok'), (), {})

    def test_configured_public_origins_are_accepted_over_http_upstream(self):
        for host in ('dev-tark.ensembl.org', 'tark.ensembl.org'):
            origin = 'https://' + host
            with self.subTest(origin=origin), self.settings(CSRF_TRUSTED_ORIGINS=[origin]):
                request, rejection = self.check_post(origin, host)
                self.assertFalse(request.is_secure())
                self.assertIsNone(rejection)

    def test_https_origin_is_rejected_over_http_without_explicit_trust(self):
        _, rejection = self.check_post('https://dev-tark.ensembl.org', 'dev-tark.ensembl.org')
        self.assertEqual(rejection.status_code, 403)

    @override_settings(CSRF_TRUSTED_ORIGINS=['https://dev-tark.ensembl.org'])
    def test_untrusted_origin_is_rejected_with_valid_token(self):
        _, rejection = self.check_post('https://untrusted.example', 'dev-tark.ensembl.org')
        self.assertEqual(rejection.status_code, 403)

    @override_settings(CSRF_TRUSTED_ORIGINS=['https://dev-tark.ensembl.org'])
    def test_trusted_origin_still_requires_valid_form_token(self):
        for token_state in ('missing', 'invalid'):
            with self.subTest(token_state=token_state):
                _, rejection = self.check_post(
                    'https://dev-tark.ensembl.org', 'dev-tark.ensembl.org', token_state=token_state,
                )
                self.assertEqual(rejection.status_code, 403)

    @override_settings(CSRF_TRUSTED_ORIGINS=['https://dev-tark.ensembl.org'])
    def test_trusted_origin_still_requires_csrf_cookie(self):
        _, rejection = self.check_post(
            'https://dev-tark.ensembl.org', 'dev-tark.ensembl.org', include_cookie=False,
        )
        self.assertEqual(rejection.status_code, 403)

    def test_forwarded_https_same_origin_is_accepted_without_explicit_trust(self):
        request, rejection = self.check_post(
            'https://dev-tark.ensembl.org', 'dev-tark.ensembl.org', HTTP_X_FORWARDED_PROTO='https',
        )
        self.assertTrue(request.is_secure())
        self.assertIsNone(rejection)

    def test_local_http_same_origin_is_accepted_without_explicit_trust(self):
        request, rejection = self.check_post('http://localhost:8000', 'localhost:8000')
        self.assertFalse(request.is_secure())
        self.assertIsNone(rejection)


class CsrfSettingsTests(SimpleTestCase):
    def load_trusted_origins(self, value):
        settings_path = Path(__file__).resolve().parents[1] / 'settings' / 'base.py'
        with patch.dict(os.environ):
            if value is None:
                os.environ.pop('DJANGO_CSRF_TRUSTED_ORIGINS', None)
            else:
                os.environ['DJANGO_CSRF_TRUSTED_ORIGINS'] = value
            return runpy.run_path(str(settings_path))['CSRF_TRUSTED_ORIGINS']

    def test_missing_environment_setting_defaults_to_empty_list(self):
        self.assertEqual(self.load_trusted_origins(None), [])

    def test_whitespace_separated_environment_origins_are_parsed(self):
        self.assertEqual(
            self.load_trusted_origins(' https://dev-tark.ensembl.org\t https://tark.ensembl.org  '),
            ['https://dev-tark.ensembl.org', 'https://tark.ensembl.org'],
        )
