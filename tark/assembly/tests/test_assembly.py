"""
.. See the NOTICE file distributed with this work for additional information
   regarding copyright ownership.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from rest_framework.test import APITestCase
from django.urls.base import reverse
from rest_framework import status
import json

# ./manage.py test assembly.tests --settings=tark.settings.test


class AssemblyTest(APITestCase):
    fixtures = ['assembly']

    def test_assembly(self):
        """
        Test the list endpoint and filters
        """
        url = reverse('assembly_list')
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url, data, format='json')
        assembly_all = json.loads(json.dumps(response.data))
        expected_assemblies = [{'assembly_id': 1, 'assembly_name': 'GRCh38', 'genome': 1, 'session': 1},
                               {'assembly_id': 6, 'assembly_name': 'GRCh37', 'genome': 1, 'session': 6}]
        self.assertListEqual(assembly_all['results'], expected_assemblies, "Got expected assemblies")

        data = {'assembly_name': 'GRCh38'}
        response = self.client.get(url, data, format='json')
        assembly_grch38 = json.loads(json.dumps(response.data))
        expected_assembly = [{'assembly_id': 1, 'assembly_name': 'GRCh38', 'genome': 1, 'session': 1}]
        self.assertListEqual(assembly_grch38['results'], expected_assembly, "Got expected assembly")
