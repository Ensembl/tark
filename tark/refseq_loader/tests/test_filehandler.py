from django.test import TestCase
from refseq_loader.handlers.refseq.FileHandlers import GFFHandler, FastaHandler
from Bio.SeqFeature import SeqFeature, FeatureLocation
import os

'''
/manage.py test refseq_loader.tests --settings=tark.settings.local
'''

class GFFHandlerTest(TestCase):
    def setUp(self):
        APP_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print("APP_BASE_DIR dir " + str(APP_BASE_DIR))
        TEST_DATA_DIR = APP_BASE_DIR + "/tests/data/"
        fasta_file = TEST_DATA_DIR + "IL2RA_GCF_000001405.38_GRCh38.p12_rna.fna"
        # print(fasta_file)
        #fasta_file = ''
        if not os.path.exists(fasta_file):
            raise FileNotFoundError

        self. fasta_handler = FastaHandler(fasta_file)

        self.mRNA_sequence = "GGCAGTTTCCTGGCTGAACACGCCAGCCCAATACTTAAAGAGAGCAACTCCTGACTCCGATAGAGACTGGATGGACCCACAAGGGTG"\
            "ACAGCCCAGGCGGACCGATCTTCCCATCCCACATCCTCCGGCGCGATGCCAAAAAGAGGCTGACGGCAACTGGGCCTTCTGCAGAGAA"\
            "AGACCTCCGCTTCACTGCCCCGGCTGGTCCCAAGGGTCAGGAAGATGGATTCATACCTGCTGATGTGGGGACTGCTCACGTTCATCAT"\
            "GGTGCCTGGCTGCCAGGCAGAGCTCTGTGACGATGACCCGCCAGAGATCCCACACGCCACATTCAAAGCCATGGCCTACAAGGAAGGA"\
            "ACCATGTTGAACTGTGAATGCAAGAGAGGTTTCCGCAGAATAAAAAGCGGGTCACTCTATATGCTCTGTACAGGAAACTCTAGCCACT"\
            "CGTCCTGGGACAACCAATGTCAATGCACAAGCTCTGCCACTCGGAACACAACGAAACAAGTGACACCTCAACCTGAAGAACAGAAAGA"\
            "AAGGAAAACCACAGAAATGCAAAGTCCAATGCAGCCAGTGGACCAAGCGAGCCTTCCAGGTCACTGCAGGGAACCTCCACCATGGGAA"\
            "AATGAAGCCACAGAGAGAATTTATCATTTCGTGGTGGGGCAGATGGTTTATTATCAGTGCGTCCAGGGATACAGGGCTCTACACAGAG"\
            "GTCCTGCTGAGAGCGTCTGCAAAATGACCCACGGGAAGACAAGGTGGACCCAGCCCCAGCTCATATGCACAGGTGAAATGGAGACCAG"\
            "TCAGTTTCCAGGTGAAGAGAAGCCTCAGGCAAGCCCCGAAGGCCGTCCTGAGAGTGAGACTTCCTGCCTCGTCACAACAACAGATTTT"\
            "CAAATACAGACAGAAATGGCTGCAACCATGGAGACGTCCATATTTACAACAGAGTACCAGGTAGCAGTGGCCGGCTGTGTTTTCCTGC"\
            "TGATCAGCGTCCTCCTCCTGAGTGGGCTCACCTGGCAGCGGAGACAGAGGAAGAGTAGAAGAACAATCTAGAAAACCAAAAGAACAAG"\
            "AATTTCTTGGTAAGAAGCCGGGAACAGACAACAGAAGTCATGAAGCCCAAGTGAAATCAAAGGTGCTAAATGGTCGCCCAGGAGACAT"\
            "CCGTTGTGCTTGCCTGCGTTTTGGAAGCTCTGAAGTCACATCACAGGACACGGGGCAGTGGCAACCTTGTCTCTATGCCAGCTCAGTC"\
            "CCATCAGAGAGCGAGCGCTACCCACTTCTAAATAGCAATTTCGCCGTTGAAGAGGAAGGGCAAAACCACTAGAACTCTCCATCTTATT"\
            "TTCATGTATATGTGTTCATTAAAGCATGAATGGTATGGAACTCTCTCCACCCTATATGTAGTATAAAGAAAAGTAGGTTTACATTCAT"\
            "CTCATTCCAACTTCCCAGTTCAGGAGTCCCAAGGAAAGCCCCAGCACTAACGTAAATACACAACACACACACTCTACCCTATACAACT"\
            "GGACATTGTCTGCGTGGTTCCTTTCTCAGCCGCTTCTGACTGCTGATTCTCCCGTTCACGTTGCCTAATAAACATCCTTCAAGAACTC"\
            "TGGGCTGCTACCCAGAAATCATTTTACCCTTGGCTCAATCCTCTAAGCTAACCCCCTTCTACTGAGCCTTCAGTCTTGAATTTCTAAA"\
            "AAACAGAGGCCATGGCAGAATAATCTTTGGGTAACTTCAAAACGGGGCAGCCAAACCCATGAGGCAATGTCAGGAACAGAAGGATGAA"\
            "TGAGGTCCCAGGCAGAGAATCATACTTAGCAAAGTTTTACCTGTGCGTTACTAATTGGCCTCTTTAAGAGTTAGTTTCTTTGGGATTG"\
            "CTATGAATGATACCCTGAATTTGGCCTGCACTAATTTGATGTTTACAGGTGGACACACAAGGTGCAAATCAATGCGTACGTTTCCTGA"\
            "GAAGTGTCTAAAAACACCAAAAAGGGATCCGTACATTCAATGTTTATGCAAGGAAGGAAAGAAAGAAGGAAGTGAAGAGGGAGAAGGG"\
            "ATGGAGGTCACACTGGTAGAACGTAACCACGGAAAAGAGCGCATCAGGCCTGGCACGGTGGCTCAGGCCTATAACCCCAGCTCCCTAG"\
            "GAGACCAAGGCGGGAGCATCTCTTGAGGCCAGGAGTTTGAGACCAGCCTGGGCAGCATAGCAAGACACATCCCTACAAAAAATTAGAA"\
            "ATTGGCTGGATGTGGTGGCATACGCCTGTAGTCCTAGCCACTCAGGAGGCTGAGGCAGGAGGATTGCTTGAGCCCAGGAGTTCGAGGC"\
            "TGCAGTCAGTCATGATGGCACCACTGCACTCCAGCCTGGGCAACAGAGCAAGATCCTGTCTTTAAGGAAAAAAAGACAAGATGAGCAT"\
            "ACCAGCAGTCCTTGAACATTATCAAAAAGTTCAGCATATTAGAATCACCGGGAGGCCTTGTTAAAAGAGTTCGCTGGGCCCATCTTCA"\
            "GAGTCTCTGAGTTGTTGGTCTGGAATAGAGCCAAATGTTTTGTGTGTCTAACAATTCCCAGGTGCTGTTGCTGCTGCTACTATTCCAG"\
            "GAACACACTTTGAGAACCATTGTGTTATTGCTCTGCACGCCCACCCACTCTCAACTCCCACGAAAAAAATCAACTTCCAGAGCTAAGA"\
            "TTTCGGTGGAAGTCCTGGTTCCATATCTGGTGCAAGATCTCCCCTCACGAATCAGTTGAGTCAACATTCTAGCTCAACAACATCACAC"\
            "GATTAACATTAACGAAAATTATTCATTTGGGAAACTATCAGCCAGTTTTCACTTCTGAAGGGGCAGGAGAGTGTTATGAGAAATCACG"\
            "GCAGTTTTCAGCAGGGTCCAGATTCAGATTAAATAACTATTTTCTGTCATTTCTGTGACCAACCACATACAAACAGACTCATCTGTGC"\
            "ACTCTCCCCCTCCCCCTTCAGGTATATGTTTTCTGAGTAAAGTTGAAAAGAATCTCAGACCAGAAAATATAGATATATATTTAAATCT"\
            "TACTTGAGTAGAACTGATTACGACTTTTGGGTGTTGAGGGGTCTATAAGATCAAAACTTTTCCATGATAATACTAAGATGTTATCGAC"\
            "CATTTATCTGTCCTTCTCTCAAAAGTGTATGGTGGAATTTTCCAGAAGCTATGTGATACGTGATGATGTCATCACTCTGCTGTTAACA"\
            "TATAATAAATTTATTGCTATTGTTTATAAAAGAATAAATGATATTTTTT"

    def test_fasta_handler(self):
        fasta_seq_il2ra = self.fasta_handler.get_fasta_seq_by_id("NM_000417.2")
        self.assertEqual(fasta_seq_il2ra, self.mRNA_sequence, "Got the right sequence")
        self.assertEqual(len(fasta_seq_il2ra), len(self.mRNA_sequence), "Got the sequence with same length")

        # check exons
        fasta_seq_il2ra_exon1 = self.fasta_handler.get_fasta_seq_by_id("NM_000417.2", 1, 283)
        expected_exon_seeq = "GGCAGTTTCCTGGCTGAACACGCCAGCCCAATACTTAAAGAGAGCAACTCCTGACTCCGATAGAGACTGGATGG"\
            "ACCCACAAGGGTGACAGCCCAGGCGGACCGATCTTCCCATCCCACATCCTCCGGCGCGAT"\
            "GCCAAAAAGAGGCTGACGGCAACTGGGCCTTCTGCAGAGAAAGACCTCCGCTTCACTGCCCCG"\
            "GCTGGTCCCAAGGGTCAGGAAGATGGATTCATACCTGCTGATGTGGGGACTGCTCACGTTCATCATGGTGCCTGGCTGCCAGGCAG"
        self.assertEqual(len(fasta_seq_il2ra_exon1), len(expected_exon_seeq), "Exon seq length is equal")
        self.assertEqual(fasta_seq_il2ra_exon1, expected_exon_seeq, "Exon seq is equal")

    def test_get_relative_exon_location(self):

        # mRNA_feature_negative = SeqFeature(FeatureLocation(6010693, 6062370, strand=-1), type="mRNA")

        refseq_exon_list_negative = [
                            {'exon_order': 1, 'exon_start': '6062087', 'exon_end': '6062370', 'exon_strand': '-1'},
                            {'exon_order': 2, 'exon_start': '6025833', 'exon_end': '6026025', 'exon_strand': '-1'},
                            {'exon_order': 3, 'exon_start': '6024243', 'exon_end': '6024354', 'exon_strand': '-1'},
                            {'exon_order': 4, 'exon_start': '6021477', 'exon_end': '6021693', 'exon_strand': '-1'},
                            {'exon_order': 5, 'exon_start': '6019869', 'exon_end': '6019941', 'exon_strand': '-1'},
                            {'exon_order': 6, 'exon_start': '6019427', 'exon_end': '6019499', 'exon_strand': '-1'},
                            {'exon_order': 7, 'exon_start': '6018052', 'exon_end': '6018119', 'exon_strand': '-1'},
                            {'exon_order': 8, 'exon_start': '6010693', 'exon_end': '6012896', 'exon_strand': '-1'}]

        expected_list_negative = [{'exon_start': 1, 'exon_order': 1, 'exon_end': 283},
                                  {'exon_start': 284, 'exon_order': 2, 'exon_end': 475},
                                  {'exon_start': 476, 'exon_order': 3, 'exon_end': 586},
                                  {'exon_start': 587, 'exon_order': 4, 'exon_end': 802},
                                  {'exon_start': 803, 'exon_order': 5, 'exon_end': 874},
                                  {'exon_start': 875, 'exon_order': 6, 'exon_end': 946},
                                  {'exon_start': 947, 'exon_order': 7, 'exon_end': 1013},
                                  {'exon_start': 1014, 'exon_order': 8, 'exon_end': 3216}]
        relative_exon_list_negative = GFFHandler.get_relative_exon_location(refseq_exon_list_negative)
        self.assertListEqual(expected_list_negative, relative_exon_list_negative,
                             "Received the list with right relative locations")

        relative_exon_list_negative_with_seq = GFFHandler.add_exon_sequence(self.fasta_handler,
                                                                            relative_exon_list_negative,
                                                                            "NM_000417.2")

        # check if the mrna sequence is the same with concatinated exon sequence
        all_exon_seq = ""
        for exon in relative_exon_list_negative_with_seq:
            all_exon_seq += exon['exon_seq']

        self.assertEquals(all_exon_seq, self.mRNA_sequence, "Got the right sequence back ")

        # check if the distance is same
        seq_length = 0
        for exon1, exon2 in zip(refseq_exon_list_negative, expected_list_negative):
            # print(str(exon1['exon_order']) + " == " + str(exon2['exon_order']))
            exon1_diff = int(exon1['exon_end']) - int(exon1['exon_start'])

            exon2_diff = int(exon2['exon_end']) - int(exon2['exon_start'])
            exon2_diff = exon2_diff + 1  # as it is 1 based
            # print(str(exon1_diff) + " == " + str(exon2_diff))
            seq_length += exon2_diff
            self.assertEqual(exon1_diff, exon2_diff, "The diff is equal")

        # Test positive strand
        # mRNA_feature_positive = SeqFeature(FeatureLocation(6010693, 6062370, strand=1), type="mRNA")

        refseq_exon_list_positive = [
                            {'exon_order': 1, 'exon_start': '6010693', 'exon_end': '6012896', 'exon_strand': '1'},
                            {'exon_order': 2, 'exon_start': '6018052', 'exon_end': '6018119', 'exon_strand': '1'},
                            {'exon_order': 3, 'exon_start': '6019427', 'exon_end': '6019499', 'exon_strand': '1'},
                            {'exon_order': 4, 'exon_start': '6019869', 'exon_end': '6019941', 'exon_strand': '1'},
                            {'exon_order': 5, 'exon_start': '6021477', 'exon_end': '6021693', 'exon_strand': '1'},
                            {'exon_order': 6, 'exon_start': '6024243', 'exon_end': '6024354', 'exon_strand': '1'},
                            {'exon_order': 7, 'exon_start': '6025833', 'exon_end': '6026025', 'exon_strand': '1'},
                            {'exon_order': 8, 'exon_start': '6062087', 'exon_end': '6062370', 'exon_strand': '1'}
                            ]

        expected_list_positive = [{'exon_start': 1, 'exon_order': 1, 'exon_end': 2203},
                                  {'exon_start': 2204, 'exon_order': 2, 'exon_end': 2270},
                                  {'exon_start': 2271, 'exon_order': 3, 'exon_end': 2342},
                                  {'exon_start': 2343, 'exon_order': 4, 'exon_end': 2414},
                                  {'exon_start': 2415, 'exon_order': 5, 'exon_end': 2630},
                                  {'exon_start': 2631, 'exon_order': 6, 'exon_end': 2741},
                                  {'exon_start': 2742, 'exon_order': 7, 'exon_end': 2933},
                                  {'exon_start': 2934, 'exon_order': 8, 'exon_end': 3216}]
        relative_exon_list_positive = GFFHandler.get_relative_exon_location(refseq_exon_list_positive)
        self.assertListEqual(expected_list_positive, relative_exon_list_positive,
                             "Received the list with right relative locations")

        for exon1, exon2 in zip(refseq_exon_list_positive, expected_list_positive):
            # print(str(exon1['exon_order']) + " == " + str(exon2['exon_order']))
            exon1_diff = int(exon1['exon_end']) - int(exon1['exon_start'])
            exon2_diff = int(exon2['exon_end']) - int(exon2['exon_start'])
            exon2_diff = exon2_diff + 1  # as it is 1 based
            # print(str(exon1_diff) + " == " + str(exon2_diff))
            self.assertEqual(exon1_diff, exon2_diff, "The diff is equal")

        # print(self.mRNA_sequence)
        # check the sequence length
        self.assertEqual(len(self.mRNA_sequence), seq_length, 'Sequence length is equal')
