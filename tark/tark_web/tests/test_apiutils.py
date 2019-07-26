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


from django.test import RequestFactory
from tark_web.utils.apiutils import ApiUtils
import json
from rest_framework.test import APITestCase
from rest_framework import status
from transcript.utils.search_utils import SearchUtils


# ./manage.py test tark_web.tests.test_apiutils --settings=tark.settings.test
class ApiUtilsTest(APITestCase):

    fixtures = ['assembly', 'gene', 'gene_names', 'release_set', 'sequence', 'transcript']

    def setUp(self):
        # Every test can have access to the request factory.
        self.factory = RequestFactory()

    def test_get_host_url(self):
        # Create an instance of a GET request.
        request = self.factory.get('/api')
        host_url = ApiUtils.get_host_url(request)
        self.assertEqual("http://testserver", host_url, "Got the testserver url")

    def test_search(self):
        """
        Test search
        """
        identifier = "ENST00000380152"
        identifier_type = SearchUtils.ENSEMBL_TRANSCRIPT
        self.check_transcript_search_result(identifier, identifier_type)

        identifier = "13:32315474-32400266"
        identifier_type = SearchUtils.GENOMIC_LOCATION
        self.check_transcript_search_result(identifier, identifier_type)

        identifier = "NC_000013.11:g.32315674G>A"
        identifier_type = SearchUtils.HGVS_GENOMIC_REF
        self.check_transcript_search_result(identifier, identifier_type)

    def check_transcript_search_result(self, identifier, id_type):

        response = self.client.get("http://testserver/api/transcript/search/" +
                                   "?identifier_field=" + identifier +
                                   "&expand=transcript_release_set,genes")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        transcript = json.loads(json.dumps(response.data))

        current_transcript = transcript[0]

        self.assertEqual(current_transcript['stable_id'], 'ENST00000380152', "OK stable_id search with " + id_type)
        self.assertEqual(current_transcript['stable_id_version'], 7, "OK stable_id_version search with " + id_type)
        self.assertEqual(current_transcript['assembly'], "GRCh38", "OK assembly search with " + id_type)
        self.assertEqual(current_transcript['loc_region'], "13", "OK loc_region search with " + id_type)
        self.assertEqual(current_transcript['loc_start'], 32315474, "OK loc_start search with " + id_type)
        self.assertEqual(current_transcript['loc_end'], 32400266, "OK loc_end search with " + id_type)
