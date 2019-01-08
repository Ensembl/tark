'''
Copyright [1999-2015] Wellcome Trust Sanger Institute and the EMBL-European Bioinformatics Institute
Copyright [2016-2019] EMBL-European Bioinformatics Institute

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''


from django.test.testcases import TestCase
from tark.utils.diff_utils import DiffUtils


# ./manage.py test tark.tests.test_diff_utils --settings=tark.settings.test
class DiffUtilsTest(TestCase):

    def test_compare_transcripts(self):

        diff_me_transcript = {'sequence': {'seq_checksum': 'D2C34F223CFA61D10CD5CBD22BEA1189BAABC0A8',
                                           'sequence': 'GGGCTTGTGGCGCGAGCTTCTGAAACT'},
                              'transcript_checksum': '78287E1D4D9DF3AA437555886C2DDF2D03789D56',
                              'loc_end': 32400266, 'loc_checksum': '66D0AE073CF5E8C3C55EC29AB1392AD363376D23',
                              'stable_id_version': 7, 'loc_region': '13', 'assembly': 'GRCh38',
                              'exon_set_checksum': '2A5C848C6EF11AB2D259B09D640603154DA2C221',
                              'stable_id': 'ENST00000380152', 'loc_strand': 1, 'loc_start': 32315474,
                              'translations': {'loc_region': '13', 'stable_id_version': 3,
                                               'translation_checksum': '2DAFEEE4E4394F56F26660F8012FE2B2579E5FA9',
                                               'assembly': 'GRCh38', 'translation_id': 115985,
                                               'stable_id': 'ENSP00000369497', 'loc_end': 32398770, 'loc_strand': 1,
                                               'loc_checksum': 'BF8226A4BB25F655B4545ACEB2C0E1233D21C814',
                                               'sequence': '70543E7B80F8B964B126A5AA165F236CA9DC132F',
                                               'loc_start': 32316461},
                              'transcript_release_set': {'session': 3,
                                                         'release_checksum':
                                                         'B5D865F6D56C10E878B6D2DE5D3F997D32546D5C',
                                                         'description': 'Ensembl release 93',
                                                         'release_date': '2018-10-03',
                                                         'assembly': 1, 'release_id': 2, 'source': 1,
                                                         'shortname': '93'}}

        # initially test that both transcripts are same
        diff_with_transcript = diff_me_transcript.copy()

        compare_results_all = DiffUtils.compare_transcripts(diff_me_transcript, diff_with_transcript)
        compare_results = compare_results_all["results"]

        self.assertEqual(compare_results["diff_me_stable_id"], "ENST00000380152", "Got the right diff_me_stable_id")
        self.assertEqual(compare_results["diff_with_stable_id"], "ENST00000380152", "Got the right diff_with_stable_id")

        self.assertEqual(compare_results["diff_me_stable_id_version"], 7, "Got the right diff_me_stable_id_version")
        self.assertEqual(compare_results["diff_with_stable_id_version"], 7,
                         "Got the right diff_with_stable_id_version")

        self.assertEqual(compare_results["diff_me_release"], "93", "Got the right diff_me_shortname")
        self.assertEqual(compare_results["diff_with_release"], "93", "Got the right diff_with_shortname")

        self.assertEqual(compare_results["has_transcript_changed"], False, "Got the right has_transcript_changed")
        self.assertEqual(compare_results["has_location_changed"], False, "Got the right has_location_changed")
        self.assertEqual(compare_results["has_exon_set_changed"], False, "Got the right has_exon_set_changed")
        self.assertEqual(compare_results["has_seq_changed"], False, "Got the right has_seq_changed")

        self.assertEqual(compare_results["has_translation_changed"], False, "Got the right has_translation_changed")
        self.assertEqual(compare_results["has_translation_location_changed"], False,
                         "Got the right has_translation_location_changed")

        self.assertEqual(compare_results["has_translation_seq_changed"], False,
                         "Got the right has_translation_seq_changed")

        expected_diff_me_transcript = compare_results_all["diff_me_transcript"]
        expected_diff_with_transcript = compare_results_all["diff_with_transcript"]

        self.assertDictEqual(diff_me_transcript, expected_diff_me_transcript,
                             "Got back the right diff me transcript")
        self.assertDictEqual(diff_with_transcript, expected_diff_with_transcript,
                             "Got back the right diff with transcript")

        # now just change the transcript loc_checksum
        diff_with_transcript["loc_checksum"] = '66D0AE073CF5E8C3C55EC29AB1392AD363376D24'
        compare_results_all = DiffUtils.compare_transcripts(diff_me_transcript, diff_with_transcript)

        compare_has_results = compare_results_all["results"]
        self.assertEqual(compare_has_results["has_location_changed"], True, "Got the right has_location_changed")

        expected_compare_has_results = {'has_hgnc_changed': None,
                                        'has_exon_set_changed': False,
                                        'diff_me_stable_id_version': 7,
                                        'diff_with_stable_id_version': 7,
                                        'diff_me_stable_id': 'ENST00000380152',
                                        'diff_with_stable_id': 'ENST00000380152',
                                        'diff_with_assembly': 'GRCh38',
                                        'diff_me_assembly': 'GRCh38',
                                        'diff_me_release': '93',
                                        'diff_with_release': '93',
                                        'has_translation_changed': False,
                                        'has_translation_seq_changed': False,
                                        'has_gene_changed': None,
                                        'has_gene_location_changed': True,
                                        'has_stable_id_version_changed': False,
                                        'has_gene_stable_id_version_changed': False,
                                        'has_translation_location_changed': False,
                                        'has_gene_stable_id_changed': False,
                                        'has_transcript_changed': False,
                                        'has_location_changed': True,
                                        'has_stable_id_changed': False,
                                        'has_seq_changed': False,
                                        'has_translation_stable_id_version_changed': False,
                                        'has_translation_stable_id_changed': False}

        self.assertDictEqual(compare_has_results, expected_compare_has_results, "Got the expected has_changed results")
