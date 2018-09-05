from django.test import TestCase
from Bio.SeqFeature import SeqFeature, FeatureLocation
import os
from refseq_loader.handlers.refseq.fastahandler import FastaHandler
from refseq_loader.handlers.refseq.gffhandler import GFFHandler
from refseq_loader.handlers.refseq.genbankhandler import GenBankHandler


'''
/manage.py test refseq_loader.tests.test_genbankhandler --settings=tark.settings.test
'''


class GenBankHandlerTest(TestCase):
    def setUp(self):
        APP_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print("APP_BASE_DIR dir " + str(APP_BASE_DIR))
        TEST_DATA_DIR = APP_BASE_DIR + "/tests/data/"

        self.genbank_file = TEST_DATA_DIR + "il2ra_tnni3.gb"

        if not os.path.exists(self.genbank_file):
            raise FileNotFoundError("File not found " + self.genbank_file)  # @UndefinedVariable

        self.genbank_handler = GenBankHandler(self.genbank_file)

        self.mRNA_sequence_il2ra = "GGCAGTTTCCTGGCTGAACACGCCAGCCCAATACTTAAAGAGAGCAACTCCTGACTCCGATAGAGACTGGATGGACCCACAAGGGTG"\
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

        self.mRNA_sequence_tnni3 = "AGTGTCCTCGGGGAGTCTCAAGCAGCCCGGAGGAGACTGACGGTCCCTGGGACCCTGAAGGTCACCCGGGCGGCCCCCTC"\
            "ACTGACCCTCCAAACGCCCCTGTCCTCGCCCTGCCTCCTGCCATTCCCGGCCTGAGTCTCAGCATGGCGGATGGGAGCAG"\
            "CGATGCGGCTAGGGAACCTCGCCCTGCACCAGCCCCAATCAGACGCCGCTCCTCCAACTACCGCGCTTATGCCACGGAGC"\
            "CGCACGCCAAGAAAAAATCTAAGATCTCCGCCTCGAGAAAATTGCAGCTGAAGACTCTGCTGCTGCAGATTGCAAAGCAA"\
            "GAGCTGGAGCGAGAGGCGGAGGAGCGGCGCGGAGAGAAGGGGCGCGCTCTGAGCACCCGCTGCCAGCCGCTGGAGTTGGC"\
            "CGGGCTGGGCTTCGCGGAGCTGCAGGACTTGTGCCGACAGCTCCACGCCCGTGTGGACAAGGTGGATGAAGAGAGATACG"\
            "ACATAGAGGCAAAAGTCACCAAGAACATCACGGAGATTGCAGATCTGACTCAGAAGATCTTTGACCTTCGAGGCAAGTTT"\
            "AAGCGGCCCACCCTGCGGAGAGTGAGGATCTCTGCAGATGCCATGATGCAGGCGCTGCTGGGGGCCCGGGCTAAGGAGTC"\
            "CCTGGACCTGCGGGCCCACCTCAAGCAGGTGAAGAAGGAGGACACCGAGAAGGAAAACCGGGAGGTGGGAGACTGGCGCA"\
            "AGAACATCGATGCACTGAGTGGAATGGAGGGCCGCAAGAAAAAGTTTGAGAGCTGAGCCTTCCTGCCTACTGCCCCTGCC"\
            "CTGAGGAGGGCCCTGAGGAATAAAGCTTCTCTCTGAGCTGAAAAAAAAAAAAAAAAAAAAAAAAAA"

    def test_get_sequence_by_id(self):
        fasta_seq_il2ra = self.genbank_handler.get_sequence_by_id("NM_000417.2")
        self.assertEqual(fasta_seq_il2ra, self.mRNA_sequence_il2ra, "Got the right sequence")
        self.assertEqual(len(fasta_seq_il2ra), len(self.mRNA_sequence_il2ra), "Got the sequence with same length")

        fasta_seq_tnni3 = self.genbank_handler.get_sequence_by_id("NM_000363.4")
        self.assertEqual(fasta_seq_tnni3, self.mRNA_sequence_tnni3, "Got the right sequence")
        self.assertEqual(len(fasta_seq_tnni3), len(self.mRNA_sequence_tnni3), "Got the sequence with same length")

    def test_get_seq_record_by_id(self):
        identifier = "NM_000363.4"
        exon_sequences = self.genbank_handler.get_exon_sequences_by_identifier(identifier)
        print("\n\n")
        print(exon_sequences)
        # self.assertEqual(self.mRNA_sequence_tnni3.startswith(str(concatinated_exon_sequence)), "Got the right sequence")


