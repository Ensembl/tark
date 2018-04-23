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
from tark_web.utils.sequtils import TarkSeqUtils
import os


class SeqUtilsTest(TestCase):
    # fixtures = ['genomeinfo_division', 'genomeinfo_genome', ]
    multi_db = True

    def test_format_fasta(self):
        sequence = "GATTGCGCCACTGCACTCCAGCCTGGGCGTGCAGATCAGAGCGAGACCTTGTCTCTAAAGGAAAAAAAAAAAGAAAGAAAGAAAGAAAAGAAAAGAAAAGAAAACCTAGCGAGGTAGATAATTTT"  # @IgnorePep8
        formatted_seq = TarkSeqUtils.format_fasta(sequence)
        expected_seq = ">ID_\nGATTGCGCCACTGCACTCCAGCCTGGGCGTGCAGATCAGAGCGAGACCTTGTCTCTAAAG\nGAAAAAAAAAAAGAAAGAAAGAAAGAAAAGAAAAGAAAAGAAAACCTAGCGAGGTAGATA\nATTTT\n"  # @IgnorePep8
        self.assertEqual(formatted_seq, expected_seq, "Sequences are equal")

    def test_align_sequences(self):
        path = os.path.abspath(__file__)
        current_dir = os.path.dirname(path)

        print("current dir " + current_dir + "\n")
        query_seq = current_dir + "/data/query.fasta"
        target_seq = current_dir + "/data/target.fasta"
        align_result = TarkSeqUtils.align_sequences(query_seq, target_seq)
        print(align_result)
