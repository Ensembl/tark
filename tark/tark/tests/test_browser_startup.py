from unittest.mock import patch

from django.test import SimpleTestCase
from django.urls import resolve, reverse

from release.utils.release_utils import ReleaseUtils


class BrowserStartupTests(SimpleTestCase):
    def setUp(self):
        # These tests exercise request handling without requiring an archive database.
        for method, value in (
            ('get_latest_release', '116'),
            ('get_latest_assembly', 'GRCh38'),
            ('get_default_source', 'Ensembl'),
        ):
            patcher = patch.object(ReleaseUtils, method, return_value=value)
            patcher.start()
            self.addCleanup(patcher.stop)

    def test_home_page_renders(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_api_documentation_renders(self):
        response = self.client.get('/api/')
        self.assertContains(response, 'SwaggerUIBundle')
        self.assertContains(response, reverse('api_schema'))

    def test_existing_api_route_resolves(self):
        self.assertEqual(resolve('/api/assembly/').url_name, 'assembly_list')

    def test_openapi_preserves_filter_parameters(self):
        response = self.client.get(reverse('api_schema'), HTTP_ACCEPT='application/json')
        self.assertEqual(response.status_code, 200)
        schema = response.json()
        self.assertTrue(schema['openapi'].startswith('3.'))
        parameters = {
            parameter['name']: parameter
            for parameter in schema['paths']['/api/assembly/']['get']['parameters']
        }
        self.assertIn('assembly_name', parameters)
        self.assertIn('expand', parameters)
        self.assertEqual(parameters['expand_all']['schema']['type'], 'boolean')
        self.assertIn('loc_start', {
            parameter['name']
            for parameter in schema['paths']['/api/transcript/']['get']['parameters']
        })
