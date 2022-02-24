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


from django.test.testcases import TestCase
from tark.utils.exon_utils import ExonUtils


# ./manage.py test tark.tests.test_exon_utils --settings=tark.settings.test
class ExonUtilsTest(TestCase):

    def setUp(self):
        self.diff_me_transcript = {'stable_id': 'ENST00000252934', 'stable_id_version': 9,
                                   'assembly': {'assembly_id': 1001, 'assembly_name': 'GRCh38',
                                                'genome': 1, 'session': 1001},
                                   'loc_start': 10, 'loc_end': 55,
                                   'loc_strand': 1, 'loc_region': '22',
                                   'loc_checksum': '95BA3AB8257D176F1854369C1812523151872A7D',
                                   'exon_set_checksum': '8A832489D82C44B27487109F9A2EB92C13D8C6A1',
                                   'transcript_checksum': 'AEF6C679C719A1B79FDD17CF2130CFB2B7F521B7',
                                   'sequence': {'sequence': 'AAATGTTTTTGGGGGCCCCCATATA',
                                                'seq_checksum': '5A2D3E0EFA1D7397AEB95F4256E0336541F068FD'},
                                   'mane_transcript': '', 'mane_transcript_type': '',
                                   'transcript_release_set': {'assembly': 'GRCh38', 'shortname': '95',
                                                              'description': 'Ensembl release 95',
                                                              'release_date': '2019-01-09', 'source': 'Ensembl'},
                                   'genes': [{'stable_id': 'ENSG00000130638', 'stable_id_version': 15,
                                              'assembly': 'GRCh38', 'loc_start': 45671798, 'loc_end': 45845307,
                                              'loc_strand': 1,
                                              'loc_region': '22',
                                              'loc_checksum': '8D695BF0131F40841A0763E0C5959DC23B1B4909',
                                              'name': 'ATXN10',
                                              'gene_checksum': '01F45233B3D4FA90ACEAB4E1D8588FE9D4633DC2'},
                                             {'stable_id': 'ENSG00000130638', 'stable_id_version': 16,
                                              'assembly': 'GRCh38',
                                              'loc_start': 45671798, 'loc_end': 45845307, 'loc_strand': 1,
                                              'loc_region': '22',
                                              'loc_checksum': '8D695BF0131F40841A0763E0C5959DC23B1B4909',
                                              'name': 'ATXN10',
                                              'gene_checksum': '521AE29733E454A44ED1C9ABEDA8A9EB34965E1D'}],
                                   'translations': {'stable_id': 'ENSP00000252934', 'stable_id_version': 4,
                                                    'assembly': 'GRCh38', 'loc_start': 12, 'loc_end': 52,
                                                    'loc_strand': 1, 'loc_region': '22',
                                                    'loc_checksum': 'FA956BFCD3E4B2FD5BEEE4B1113AFC2AC72B0FCC',
                                                    'translation_id': 106423,
                                                    'translation_checksum': '02B7FF66B998305BBCB0ECD6E3AB8E2FEC5C23CA',
                                                    'sequence': 'MAAPRPPPARLSGVMVPAPIQDL',
                                                    'seq_checksum': '910FB568CE59133225A47DA5296146552AC20F0C'},
                                   }

        diff_me_exon_set = [
            {'stable_id': 'ENSE1', 'stable_id_version': '1', 'exon_order': 1, 'seq_checksum': 'seq_A',
             'loc_checksum': 'loc_A', 'exon_checksum': 'exon_A', 'assembly': 'GRCh38',
             'loc_region': 22, 'loc_start': 10, 'loc_end': 15, 'loc_strand': 1, 'sequence': 'AAATG'},
            {'stable_id': 'ENSE2', 'stable_id_version': '1', 'exon_order': 2, 'seq_checksum': 'seq_B',
             'loc_checksum': 'loc_B', 'exon_checksum': 'exon_B', 'assembly': 'GRCh38',
             'loc_region': 22, 'loc_start': 20, 'loc_end': 25, 'loc_strand': 1, 'sequence': 'TTTTT'},
            {'stable_id': 'ENSE3', 'stable_id_version': '1', 'exon_order': 3, 'seq_checksum': 'seq_C',
             'loc_checksum': 'loc_C', 'exon_checksum': 'exon_C', 'assembly': 'GRCh38',
             'loc_region': 22, 'loc_start': 30, 'loc_end': 35, 'loc_strand': 1, 'sequence': 'GGGGG'},
            {'stable_id': 'ENSE4', 'stable_id_version': '1', 'exon_order': 4, 'seq_checksum': 'seq_D',
             'loc_checksum': 'loc_D', 'exon_checksum': 'exon_D', 'assembly': 'GRCh38',
             'loc_region': 22, 'loc_start': 40, 'loc_end': 45, 'loc_strand': 1, 'sequence': 'CCCCC'},
            {'stable_id': 'ENSE5', 'stable_id_version': '1', 'exon_order': 5, 'seq_checksum': 'seq_E',
             'loc_checksum': 'loc_E', 'exon_checksum': 'exon_E', 'assembly': 'GRCh38',
             'loc_region': 22, 'loc_start': 50, 'loc_end': 55, 'loc_strand': 1, 'sequence': 'ATATA'},
            ]
        diff_with_exon_set = diff_me_exon_set.copy()

        self.diff_me_transcript['exons'] = diff_me_exon_set
        # initially test that both transcripts are same
        self.diff_with_transcript = self.diff_me_transcript.copy()
        self.diff_with_transcript['exons'] = diff_with_exon_set

    def test_diff_exon_sets(self):
        exonset1 = self.diff_me_transcript['exons']
        exonset2 = self.diff_with_transcript['exons']

        exon_set_diff = ExonUtils.diff_exon_sets(exonset1, exonset2)

        cumulative_score = exon_set_diff[0]
        self.assertEqual(cumulative_score[0], 'cumulative_overlap_score')
        self.assertEqual(cumulative_score[1], 5)

        exon1_tuple = exon_set_diff[1]
        exon1 = exon1_tuple[0]
        exon1_overlaps = exon1_tuple[1]

        expected_exon1 = {'stable_id': 'ENSE1', 'stable_id_version': '1', 'exon_order': 1,
                          'seq_checksum': 'seq_A',
                          'loc_checksum': 'loc_A', 'exon_checksum': 'exon_A',
                          'assembly': 'GRCh38', 'loc_region': 22,
                          'loc_start': 10, 'loc_end': 15, 'loc_strand': 1, 'sequence': 'AAATG'}

        expected_exon1_overlaps = [{'overlapping_exon': {'stable_id': 'ENSE1', 'stable_id_version': '1',
                                                         'exon_order': 1,
                                                         'seq_checksum': 'seq_A', 'loc_checksum': 'loc_A',
                                                         'exon_checksum': 'exon_A', 'assembly': 'GRCh38',
                                                         'loc_region': 22, 'loc_start': 10, 'loc_end': 15,
                                                         'loc_strand': 1, 'sequence': 'AAATG'},
                                    'loc_checksum': True,
                                    'seq_checksum': True}]

        self.assertDictEqual(exon1, expected_exon1)
        self.assertListEqual(exon1_overlaps, expected_exon1_overlaps)

    def test_compute_overlap(self):

        # full overlap score=5
        overlap_score = ExonUtils.compute_overlap(10, 15, 10, 15)
        self.assertEqual(overlap_score, 5)

        # no overlap score=0
        overlap_score = ExonUtils.compute_overlap(10, 15, 20, 25)
        self.assertEqual(overlap_score, 0)

        # partial overlap score=3
        overlap_score = ExonUtils.compute_overlap(10, 15, 11, 14)
        self.assertEqual(overlap_score, 3)

        # full overlap  score=5
        overlap_score = ExonUtils.compute_overlap(10, 15, 8, 18)
        self.assertEqual(overlap_score, 5)

        # partial overlap score=3
        overlap_score = ExonUtils.compute_overlap(10, 15, 12, 18)
        self.assertEqual(overlap_score, 3)

    def test_fetch_cds_info(self):
        cds_info = ExonUtils.fetch_cds_info(self.diff_me_transcript)
        expected_cds_info = {
                            'translation_start': 12, 'translation_end': 52,
                            'loc_strand': 1, 'five_prime_utr_end': 11, 'three_prime_utr_start': 53,
                            'five_prime_utr_start': 10, 'loc_region': 22,
                            'three_prime_utr_end': 55, 'five_prime_utr_seq': 'AA',
                            'five_prime_utr_length': 2,
                            'three_prime_utr_seq': 'ATA', 'three_prime_utr_length': 3,
                            'cds_seq': 'ATGTTTTTGGGGGCCCCCAT'}
        self.assertDictEqual(expected_cds_info, cds_info)

    def test_compute_cds_sequence(self):
        cds_seq = ExonUtils.compute_cds_sequence(self.diff_me_transcript)
        self.assertEqual(cds_seq, "ATGTTTTTGGGGGCCCCCAT")
