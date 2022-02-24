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
from exon.models import Exon

# ./manage.py test exon.tests --settings=tark.settings.test


class ExonTest(APITestCase):
    fixtures = ['transcript', 'exon']

    def test_assembly(self):
        """
        Test the list endpoint and filters
        """
        url = reverse('exon_list')
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url, data, format='json')
        exon_all = json.loads(json.dumps(response.data))
        self.assertEqual(Exon.objects.count(), 5)
        self.assertEqual(Exon.objects.count(), len(exon_all["results"]))

#         expected_assemblies = [{'assembly_id': 1, 'assembly_name': 'GRCh38', 'genome': 1, 'session': 1},
#                                {'assembly_id': 6, 'assembly_name': 'GRCh37', 'genome': 1, 'session': 6}]
#         self.assertListEqual(assembly_all['results'], expected_assemblies, "Got expected assemblies")
# 
        data = {'stable_id': 'ENSE00001184784'}
        response = self.client.get(url, data, format='json')
        exon_784 = json.loads(json.dumps(response.data))
        expected_exon_784 = {'stable_id': 'ENSE00001184784', 'stable_id_version': 4, 'assembly': 'GRCh38',
                             'loc_start': 32315474, 'loc_end': 32315667,
                             'loc_strand': 1, 'loc_region': '13',
                             'loc_checksum': '3643364534000000000000000000000000000000',
                             'exon_checksum': '3537323932000000000000000000000000000000',
                             'sequence': None}
        self.assertDictEqual(exon_784['results'][0], expected_exon_784, "Got expected exon")
'''
Created on 2 Aug 2019

@author: prem
'''
