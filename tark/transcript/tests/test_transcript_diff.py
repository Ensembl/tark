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


from django.test.testcases import LiveServerTestCase
from rest_framework.test import APITestCase
from django.test.client import RequestFactory
from tark_web.utils.apiutils import ApiUtils
import json
from transcript.views import TranscriptList
from django.test.utils import override_settings
import requests


# Using the APITestCase
# ./manage.py test transcript.tests.test_transcript_diff.TranscriptTest --settings=tark.settings.test
class TranscriptTest(APITestCase):

    fixtures = ['assembly', 'gene', 'gene_names', 'release_set', 'sequence', 'transcript']

    def setUp(self):
        # Every test can have access to the request factory.
        self.factory = RequestFactory()

    def test_get_host_url(self):
        # Create an instance of a GET request.
        request = self.factory.get('/api')
        host_url = ApiUtils.get_host_url(request)
        self.assertEqual("http://testserver", host_url, "Got the testserver url")

    def test_transcript(self):

        test_host = "http://testserver"
        test_api = "/api/transcript/"
        test_params = "?stable_id=ENST00000293217&release_short_name=96&" + \
            "assembly_name=GRCh38&source_name=Ensembl&expand_all=true"

        request = self.factory.get(test_host + test_api + test_params)
        # Use this syntax for class-based views.
        response = TranscriptList.as_view()(request)
        test_transcript_json = json.loads(json.dumps(response.data))
        self.assertIsNotNone(test_transcript_json["results"])
        test_transcript = test_transcript_json["results"][0]
        self.assertEqual(test_transcript["stable_id"], "ENST00000293217")
        self.assertEqual(test_transcript["stable_id_version"], 10)
        transcript_release_set = test_transcript["transcript_release_set"][0]

        expected_tr_release_set = {'assembly': 'GRCh38', 'shortname': '96', 'description': 'Ensembl release',
                                   'release_date': '2019-04-09', 'source': 'Ensembl'}
        self.assertDictEqual(transcript_release_set, expected_tr_release_set)


# Using the LiveServerTestCase
# ./manage.py test transcript.tests.test_transcript_diff.TranscriptDiffTest --settings=tark.settings.test
class TranscriptDiffTest(LiveServerTestCase):

    fixtures = ['assembly', 'gene', 'gene_names', 'release_set', 'sequence', 'transcript']

    def test_transcript_diff(self):

        test_host = self.live_server_url
        test_api = "/api/transcript/diff/"
        diff_params = "?diff_me_stable_id=ENST00000293217" + \
            "&diff_me_release=96" + \
            "&diff_me_source=Ensembl" + \
            "&diff_me_assembly=GRCh38" + \
            "&diff_with_stable_id=ENST00000293217" + \
            "&diff_with_source=Ensembl" + \
            "&diff_with_release=96" + \
            "&diff_with_assembly=GRCh38"

        response = requests.get(test_host + test_api + diff_params)

        test_transcript_diff_json = {}
        if response.status_code == 200:
            test_transcript_diff_json = response.json()

        expected_diff_dict = {'count': 1, 'next': None, 'previous': None,
                              'results': {'diff_me_stable_id': 'ENST00000293217',
                                          'diff_with_stable_id': 'ENST00000293217',
                                          'diff_me_stable_id_version': 10, 'diff_with_stable_id_version': 10,
                                          'diff_me_assembly': {'assembly_id': 1, 'assembly_name': 'GRCh38',
                                                               'genome': 1, 'session': 1},
                                          'diff_with_assembly': {'assembly_id': 1, 'assembly_name': 'GRCh38',
                                                                 'genome': 1, 'session': 1},
                                          'diff_me_release': '96', 'diff_with_release': '96',
                                          'has_stable_id_changed': False, 'has_stable_id_version_changed': False,
                                          'has_transcript_changed': False,
                                          'has_location_changed': False, 'has_exon_set_changed': False,
                                          'has_seq_changed': None, 'has_translation_stable_id_changed': None,
                                          'has_translation_stable_id_version_changed': None,
                                          'has_translation_changed': None, 'has_translation_location_changed': None,
                                          'has_translation_seq_changed': None, 'has_gene_stable_id_changed': False,
                                          'has_gene_stable_id_version_changed': False, 'has_gene_changed': False,
                                          'has_gene_location_changed': False,
                                          'has_hgnc_changed': False},
                              'diff_me_transcript': {'stable_id': 'ENST00000293217', 'stable_id_version': 10,
                                                     'assembly': {'assembly_id': 1, 'assembly_name': 'GRCh38',
                                                                  'genome': 1, 'session': 1},
                                                     'loc_start': 75941507, 'loc_end': 75979166,
                                                     'loc_strand': -1, 'loc_region': '17',
                                                     'loc_checksum': '3600000000000000000000000000000000000000',
                                                     'exon_set_checksum': '3800000000000000000000000000000000000000',
                                                     'transcript_checksum': '3600000000000000000000000000000000000000',
                                                     'sequence': None,
                                                     'transcript_release_set': {'assembly': 'GRCh38', 'shortname': '96',
                                                                                'description': 'Ensembl release',
                                                                                'release_date': '2019-04-09',
                                                                                'source': 'Ensembl'},
                                                     'genes': [{'stable_id': 'ENSG00000161533', 'stable_id_version': 12,
                                                                'assembly': 'GRCh38',
                                                                'loc_start': 75941507, 'loc_end': 75979177,
                                                                'loc_strand': -1, 'loc_region': '17',
                                                                'loc_checksum': '3246383400000000000000000000000000000000',  # @IgnorePep8
                                                                'name': 'ACOT13',
                                                                'gene_checksum': '3846383800000000000000000000000000000000'}],  # @IgnorePep8
                                                     'translations': [], 'exons': [], 'cds_info': {},
                                                     'gene': {'stable_id': 'ENSG00000161533',
                                                              'stable_id_version': 12, 'assembly': 'GRCh38',
                                                              'loc_start': 75941507, 'loc_end': 75979177,
                                                              'loc_strand': -1,
                                                              'loc_region': '17',
                                                              'loc_checksum':
                                                              '3246383400000000000000000000000000000000',
                                                              'name': 'ACOT13',
                                                              'gene_checksum':
                                                              '3846383800000000000000000000000000000000'}},
                              'diff_with_transcript': {'stable_id': 'ENST00000293217', 'stable_id_version': 10,
                                                       'assembly': {'assembly_id': 1, 'assembly_name': 'GRCh38',
                                                                    'genome': 1, 'session': 1},
                                                       'loc_start': 75941507, 'loc_end': 75979166,
                                                       'loc_strand': -1, 'loc_region': '17',
                                                       'loc_checksum': '3600000000000000000000000000000000000000',
                                                       'exon_set_checksum': '3800000000000000000000000000000000000000',
                                                       'transcript_checksum':
                                                       '3600000000000000000000000000000000000000',
                                                       'sequence': None, 'transcript_release_set': {
                                                           'assembly': 'GRCh38', 'shortname': '96',
                                                           'description': 'Ensembl release',
                                                           'release_date': '2019-04-09', 'source': 'Ensembl'},
                                                       'genes': [{'stable_id': 'ENSG00000161533',
                                                                  'stable_id_version': 12, 'assembly': 'GRCh38',
                                                                  'loc_start': 75941507, 'loc_end': 75979177,
                                                                  'loc_strand': -1, 'loc_region': '17',
                                                                  'loc_checksum':
                                                                  '3246383400000000000000000000000000000000',
                                                                  'name': 'ACOT13', 'gene_checksum':
                                                                  '3846383800000000000000000000000000000000'}],
                                                       'translations': [], 'exons': [], 'cds_info': {},
                                                       'gene': {'stable_id': 'ENSG00000161533', 'stable_id_version': 12,
                                                                'assembly': 'GRCh38', 'loc_start': 75941507,
                                                                'loc_end': 75979177, 'loc_strand': -1,
                                                                'loc_region': '17', 'loc_checksum':
                                                                '3246383400000000000000000000000000000000',
                                                                'name': 'ACOT13', 'gene_checksum':
                                                                '3846383800000000000000000000000000000000'}},
                              'exonsets_diffme2diffwith': [['cumulative_overlap_score', 0]],
                              'exonsets_diffwith2diffme': [['cumulative_overlap_score', 0]]}

        self.assertDictEqual(test_transcript_diff_json, expected_diff_dict)
