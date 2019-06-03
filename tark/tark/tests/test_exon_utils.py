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
from collections import OrderedDict


# ./manage.py test tark.tests.test_exon_utils --settings=tark.settings.test
class ExonUtilsTest(TestCase):

    def test_exon_set_compare(self):
        pass
#         compare_result = ExonUtils.diff_exon_sets(exon_set1, exon_set2)
#         print(compare_result)

    def test_compute_overelap(self):
        pass
#             start1, end1, start2, end2 = 10, 15, 8, 13
#             overlap = ExonUtils.compute_overlap(start1, end1, start2, end2)
#             self.assertEqual(overlap, 3, "Got the right overlap")
#
#             start1, end1, start2, end2 = 8, 13, 10, 15
#             overlap = ExonUtils.compute_overlap(start1, end1, start2, end2)
#             self.assertEqual(overlap, 3, "Got the right overlap")
#
#             start1, end1, start2, end2 = 10, 15, 10, 15
#             overlap = ExonUtils.compute_overlap(start1, end1, start2, end2)
#             self.assertEqual(overlap, 5, "Got the right overlap")
#
#             start1, end1, start2, end2 = 10, 15, 20, 25
#             overlap = ExonUtils.compute_overlap(start1, end1, start2, end2)
#             self.assertEqual(overlap, 0, "Got the right overlap")
