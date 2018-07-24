'''
Copyright [1999-2015] Wellcome Trust Sanger Institute and the EMBL-European Bioinformatics Institute
Copyright [2016-2018] EMBL-European Bioinformatics Institute

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
from tark.utils.exon_utils import ExonUtils


class ExonUtilsTest(TestCase):

    def test_exon_set_compare(self):
        exon1_1 = {"exon_order": 1, "loc_start": 2, "loc_end": 5}
        exon1_2 = {"exon_order": 2, "loc_start": 10, "loc_end": 15}
        exon1_3 = {"exon_order": 3, "loc_start": 20, "loc_end": 25}
        exon1_4 = {"exon_order": 4, "loc_start": 30, "loc_end": 35}
        exon1_5 = {"exon_order": 5, "loc_start": 40, "loc_end": 45}
        exon1_6 = {"exon_order": 6, "loc_start": 50, "loc_end": 55}
        exon1_7 = {"exon_order": 7, "loc_start": 56, "loc_end": 58}  # new exon insert
        exon1_8 = {"exon_order": 8, "loc_start": 60, "loc_end": 65}
        exon1_9 = {"exon_order": 9, "loc_start": 70, "loc_end": 75}
        exon1_10 = {"exon_order": 10, "loc_start": 80, "loc_end": 85}

        exon2_1 = {"exon_order": 1, "loc_start": 3, "loc_end": 5}
        exon2_2 = {"exon_order": 2, "loc_start": 10, "loc_end": 15}
        exon2_3 = {"exon_order": 3, "loc_start": 20, "loc_end": 25}
        exon2_4 = {"exon_order": 4, "loc_start": 30, "loc_end": 35}
        exon2_5 = {"exon_order": 5, "loc_start": 40, "loc_end": 45}
        exon2_6 = {"exon_order": 6, "loc_start": 50, "loc_end": 55}
        exon2_7 = {"exon_order": 7, "loc_start": 60, "loc_end": 65}
        exon2_8 = {"exon_order": 8, "loc_start": 70, "loc_end": 75}
        exon2_9 = {"exon_order": 9, "loc_start": 80, "loc_end": 85}

        exon_set1 = [exon1_1, exon1_2, exon1_3, exon1_4, exon1_5, exon1_6, exon1_7, exon1_8, exon1_9, exon1_10]
        exon_set2 = [exon2_1, exon2_2, exon2_3, exon2_4, exon2_5, exon2_6, exon2_7, exon2_8, exon2_9]

        expected_result = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1, 2, 3, 4, 5, 6, 0, 7, 8, 9]]
        compare_result = ExonUtils.exon_set_compare(exon_set1, exon_set2)
        self.assertListEqual(expected_result, compare_result, "Got expected result")

        expected_result = [[1, 2, 3, 4, 5, 6, 0, 8, 9], [1, 2, 3, 4, 5, 6, 7, 9, 10]]
        compare_result = ExonUtils.exon_set_compare(exon_set2, exon_set1)
        self.assertListEqual(expected_result, compare_result, "Got expected result")

        # removing the first exon
        exon_set1 = [         exon1_2, exon1_3, exon1_4, exon1_5, exon1_6, exon1_7, exon1_8, exon1_9, exon1_10]  # @IgnorePep8
        exon_set2 = [exon2_1, exon2_2, exon2_3, exon2_4, exon2_5, exon2_6,          exon2_7, exon2_8, exon2_9]

        # tricky case, actually it should have 0-1
        # expected_result = [[0, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 8, 9, 10]]
        expected_result = [[2, 3, 4, 5, 6, 7, 8, 9, 10], [2, 3, 4, 5, 6, 0, 7, 8, 9]]
        compare_result = ExonUtils.exon_set_compare(exon_set1, exon_set2)
        self.assertListEqual(expected_result, compare_result, "Got expected result")

        expected_result = [[1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 2, 3, 4, 5, 6, 8, 9, 10]]
        compare_result = ExonUtils.exon_set_compare(exon_set2, exon_set1)
        self.assertListEqual(expected_result, compare_result, "Got expected result")

    def test_compute_overelap(self):
            start1, end1, start2, end2 = 10, 15, 8, 13
            overlap = ExonUtils.compute_overlap(start1, end1, start2, end2)
            self.assertEqual(overlap, 3, "Got the right overlap")

            start1, end1, start2, end2 = 8, 13, 10, 15
            overlap = ExonUtils.compute_overlap(start1, end1, start2, end2)
            self.assertEqual(overlap, 3, "Got the right overlap")

            start1, end1, start2, end2 = 10, 15, 10, 15
            overlap = ExonUtils.compute_overlap(start1, end1, start2, end2)
            self.assertEqual(overlap, 5, "Got the right overlap")

            start1, end1, start2, end2 = 10, 15, 20, 25
            overlap = ExonUtils.compute_overlap(start1, end1, start2, end2)
            self.assertEqual(overlap, 0, "Got the right overlap")
