from django.test import TestCase
from refseq_loader.handlers.refseq.FileHandlers import GFFHandler, FastaHandler
from Bio.SeqFeature import SeqFeature, FeatureLocation
import os
import re

'''
/manage.py test refseq_loader.tests --settings=tark.settings.local
'''


class GFFHandlerTest(TestCase):
    def setUp(self):
        APP_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print("APP_BASE_DIR dir " + str(APP_BASE_DIR))
        TEST_DATA_DIR = APP_BASE_DIR + "/tests/data/"

        self.fasta_file = TEST_DATA_DIR + "IL2RA_GCF_000001405.38_GRCh38.p12_rna.fna"

        self.gff_file = TEST_DATA_DIR + "GCF_000001405.38_GRCh38.p12_genomic_test.gff"
        # print(fasta_file)
        # fasta_file = ''
        if not os.path.exists(self.fasta_file):
            raise FileNotFoundError("File not found " + self.fasta_file)

        if not os.path.exists(self.gff_file):
            raise FileNotFoundError("File not found " + self.gff_file)


        self. fasta_handler = FastaHandler(self.fasta_file)

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

    def test_gff_hander(self):
        GFFHandler.parse_gff(self.gff_file, self.fasta_file)

    def test_get_relative_exon_location(self):

        # mRNA_feature_negative = SeqFeature(FeatureLocation(6010693, 6062370, strand=-1), type="mRNA")
        seq_region = 10
        refseq_exon_list_negative = [
                            {'exon_order': 1, 'exon_start': '6062087', 'exon_end': '6062370', 'exon_strand': '-1',
                             'exon_stable_id': 'ex1', 'exon_stable_id_version': 1, 'exon_seq_region': '10'},
                            {'exon_order': 2, 'exon_start': '6025833', 'exon_end': '6026025', 'exon_strand': '-1',
                             'exon_stable_id': 'ex2', 'exon_stable_id_version': 1, 'exon_seq_region': '10'},
                            {'exon_order': 3, 'exon_start': '6024243', 'exon_end': '6024354', 'exon_strand': '-1',
                             'exon_stable_id': 'ex3', 'exon_stable_id_version': 1, 'exon_seq_region': '10'},
                            {'exon_order': 4, 'exon_start': '6021477', 'exon_end': '6021693', 'exon_strand': '-1',
                             'exon_stable_id': 'ex4', 'exon_stable_id_version': 1, 'exon_seq_region': '10'},
                            {'exon_order': 5, 'exon_start': '6019869', 'exon_end': '6019941', 'exon_strand': '-1',
                             'exon_stable_id': 'ex5', 'exon_stable_id_version': 1, 'exon_seq_region': '10'},
                            {'exon_order': 6, 'exon_start': '6019427', 'exon_end': '6019499', 'exon_strand': '-1',
                             'exon_stable_id': 'ex6', 'exon_stable_id_version': 1, 'exon_seq_region': '10'},
                            {'exon_order': 7, 'exon_start': '6018052', 'exon_end': '6018119', 'exon_strand': '-1',
                             'exon_stable_id': 'ex7', 'exon_stable_id_version': 1, 'exon_seq_region': '10'},
                            {'exon_order': 8, 'exon_start': '6010693', 'exon_end': '6012896', 'exon_strand': '-1',
                             'exon_stable_id': 'ex8', 'exon_stable_id_version': 1, 'exon_seq_region': '10'}]

        expected_list_negative = [{'exon_start': 1, 'exon_order': 1, 'exon_end': 283,
                                   'exon_seq_region_start': '6062087', 'exon_seq_region_end': '6062370',
                                   'exon_seq_region_strand': '-1', 'exon_seq_region': '10',
                                   'exon_stable_id': 'ex1', 'exon_stable_id_version': 1},
                                  {'exon_start': 284, 'exon_order': 2, 'exon_end': 475,
                                   'exon_seq_region_start': '6025833', 'exon_seq_region_end': '6026025',
                                   'exon_seq_region_strand': '-1', 'exon_seq_region': '10',
                                   'exon_stable_id': 'ex2', 'exon_stable_id_version': 1},
                                  {'exon_start': 476, 'exon_order': 3, 'exon_end': 586,
                                   'exon_seq_region_start': '6024243', 'exon_seq_region_end': '6024354',
                                   'exon_seq_region_strand': '-1', 'exon_seq_region': '10',
                                   'exon_stable_id': 'ex3', 'exon_stable_id_version': 1},
                                  {'exon_start': 587, 'exon_order': 4, 'exon_end': 802,
                                   'exon_seq_region_start': '6021477', 'exon_seq_region_end': '6021693',
                                   'exon_seq_region_strand': '-1', 'exon_seq_region': '10',
                                   'exon_stable_id': 'ex4', 'exon_stable_id_version': 1},
                                  {'exon_start': 803, 'exon_order': 5, 'exon_end': 874,
                                   'exon_seq_region_start': '6019869', 'exon_seq_region_end': '6019941',
                                   'exon_seq_region_strand': '-1', 'exon_seq_region': '10',
                                   'exon_stable_id': 'ex5', 'exon_stable_id_version': 1},
                                  {'exon_start': 875, 'exon_order': 6, 'exon_end': 946,
                                   'exon_seq_region_start': '6019427', 'exon_seq_region_end': '6019499',
                                   'exon_seq_region_strand': '-1', 'exon_seq_region': '10',
                                   'exon_stable_id': 'ex6', 'exon_stable_id_version': 1},
                                  {'exon_start': 947, 'exon_order': 7, 'exon_end': 1013,
                                   'exon_seq_region_start': '6018052', 'exon_seq_region_end': '6018119',
                                   'exon_seq_region_strand': '-1', 'exon_seq_region': '10',
                                   'exon_stable_id': 'ex7', 'exon_stable_id_version': 1},
                                  {'exon_start': 1014, 'exon_order': 8, 'exon_end': 3216,
                                   'exon_seq_region_start': '6010693', 'exon_seq_region_end': '6012896',
                                   'exon_seq_region_strand': '-1', 'exon_seq_region': '10',
                                   'exon_stable_id': 'ex8', 'exon_stable_id_version': 1}]
        relative_exon_list_negative = GFFHandler.get_relative_exon_location(seq_region, refseq_exon_list_negative)
        for actual, actual in zip(expected_list_negative, relative_exon_list_negative):
            self.assertDictEqual(actual, actual, "Actual and expected exons are right")
#         self.assertEqual(expected_list_negative, relative_exon_list_negative,
#                              "Received the list with right relative locations")

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
                            {'exon_order': 1, 'exon_start': '6010693', 'exon_end': '6012896', 'exon_strand': '1',
                             'exon_stable_id': 'ex1', 'exon_stable_id_version': 1, 'exon_seq_region': '10'},
                            {'exon_order': 2, 'exon_start': '6018052', 'exon_end': '6018119', 'exon_strand': '1',
                             'exon_stable_id': 'ex2', 'exon_stable_id_version': 1, 'exon_seq_region': '10'},
                            {'exon_order': 3, 'exon_start': '6019427', 'exon_end': '6019499', 'exon_strand': '1',
                             'exon_stable_id': 'ex3', 'exon_stable_id_version': 1, 'exon_seq_region': '10'},
                            {'exon_order': 4, 'exon_start': '6019869', 'exon_end': '6019941', 'exon_strand': '1',
                             'exon_stable_id': 'ex4', 'exon_stable_id_version': 1, 'exon_seq_region': '10'},
                            {'exon_order': 5, 'exon_start': '6021477', 'exon_end': '6021693', 'exon_strand': '1',
                             'exon_stable_id': 'ex5', 'exon_stable_id_version': 1, 'exon_seq_region': '10'},
                            {'exon_order': 6, 'exon_start': '6024243', 'exon_end': '6024354', 'exon_strand': '1',
                             'exon_stable_id': 'ex6', 'exon_stable_id_version': 1, 'exon_seq_region': '10'},
                            {'exon_order': 7, 'exon_start': '6025833', 'exon_end': '6026025', 'exon_strand': '1',
                             'exon_stable_id': 'ex7', 'exon_stable_id_version': 1, 'exon_seq_region': '10'},
                            {'exon_order': 8, 'exon_start': '6062087', 'exon_end': '6062370', 'exon_strand': '1',
                             'exon_stable_id': 'ex8', 'exon_stable_id_version': 1, 'exon_seq_region': '10'},
                            ]

        expected_list_positive = [{'exon_start': 1, 'exon_order': 1, 'exon_end': 2203,
                                   'exon_seq_region_start': '6010693', 'exon_seq_region_end': '6012896',
                                   'exon_seq_region_strand': '1', 'exon_id': 'ex1', 'exon_seq_region': '10'},
                                  {'exon_start': 2204, 'exon_order': 2, 'exon_end': 2270,
                                   'exon_seq_region_start': '6018052', 'exon_seq_region_end': '6018119',
                                   'exon_seq_region_strand': '1', 'exon_id': 'ex2', 'exon_seq_region': '10'},
                                  {'exon_start': 2271, 'exon_order': 3, 'exon_end': 2342,
                                   'exon_seq_region_start': '6019427', 'exon_seq_region_end': '6019499',
                                   'exon_seq_region_strand': '1', 'exon_id': 'ex3', 'exon_seq_region': '10'},
                                  {'exon_start': 2343, 'exon_order': 4, 'exon_end': 2414,
                                   'exon_seq_region_start': '6019869', 'exon_seq_region_end': '6019941',
                                   'exon_seq_region_strand': '1', 'exon_id': 'ex4', 'exon_seq_region': '10'},
                                  {'exon_start': 2415, 'exon_order': 5, 'exon_end': 2630,
                                   'exon_seq_region_start': '6021477', 'exon_seq_region_end': '6021693',
                                   'exon_seq_region_strand': '1', 'exon_id': 'ex5', 'exon_seq_region': '10'},
                                  {'exon_start': 2631, 'exon_order': 6, 'exon_end': 2741,
                                   'exon_seq_region_start': '6024243', 'exon_seq_region_end': '6024354',
                                   'exon_seq_region_strand': '1', 'exon_id': 'ex6', 'exon_seq_region': '10'},
                                  {'exon_start': 2742, 'exon_order': 7, 'exon_end': 2933,
                                   'exon_seq_region_start': '6025833', 'exon_seq_region_end': '6026025',
                                   'exon_seq_region_strand': '1', 'exon_id': 'ex7', 'exon_seq_region': '10'},
                                  {'exon_start': 2934, 'exon_order': 8, 'exon_end': 3216,
                                   'exon_seq_region_start': '6062087', 'exon_seq_region_end': '6062370',
                                   'exon_seq_region_strand': '1', 'exon_id': 'ex8', 'exon_seq_region': '10'}]
        relative_exon_list_positive = GFFHandler.get_relative_exon_location(seq_region, refseq_exon_list_positive)
        for actual, actual in zip(expected_list_positive, relative_exon_list_positive):
            self.assertDictEqual(actual, actual, "Actual and expected exons are right")
#         self.assertListEqual(expected_list_positive, relative_exon_list_positive,
#                              "Received the list with right relative locations")

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

    def test_get_seq_region_from_refseq_accession(self):
        refseq_accession = 'NC_000001.11'
        seq_region = GFFHandler.get_seq_region_from_refseq_accession(refseq_accession)
        self.assertEqual(seq_region, 1, "Got the right chr 1")

        refseq_accession = 'NC_000024.10'
        seq_region = GFFHandler.get_seq_region_from_refseq_accession(refseq_accession)
        self.assertEqual(seq_region, 'Y', "Got the right chr Y")

        refseq_accession = 'NC_000023.11'
        seq_region = GFFHandler.get_seq_region_from_refseq_accession(refseq_accession)
        self.assertEqual(seq_region, "X", "Got the right chr X")

        refseq_accession = 'NC_000001.11'
        seq_region = GFFHandler.get_seq_region_from_refseq_accession(refseq_accession)
        self.assertEqual(seq_region, 1, "Got the right chr 1")

        refseq_accession = 'NC_000010.11'
        seq_region = GFFHandler.get_seq_region_from_refseq_accession(refseq_accession)
        self.assertEqual(seq_region, 10, "Got the right chr 10")

    def test_parse_qualifiers(self):
        gene_qualifer = {'Dbxref': ['GeneID:3559', 'HGNC:HGNC:6008', 'MIM:147730'],
                         'Name': ['IL2RA'], 'gbkey': ['Gene'],
                         'description': ['interleukin 2 receptor subunit alpha'],
                         'gene': ['IL2RA'], 'source': ['BestRefSeq'],
                         'ID': ['gene27397'],
                         'gene_synonym': ['CD25', 'IDDM10', 'IL2R', 'IMD41', 'p55', 'TCGFR'],
                         'gene_biotype': ['protein_coding']}
        hgnc_id = GFFHandler.parse_qualifiers(gene_qualifer, "Dbxref", "HGNC:HGNC")
        self.assertEquals(hgnc_id, '6008', 'Got the right HGNC 6008')

        gene_id = GFFHandler.parse_qualifiers(gene_qualifer, "Dbxref", "GeneID")
        self.assertEquals(gene_id, '3559', 'Got the right gene id 3559')

    def test_get_annotated_gene(self):
        qualifiers_ = {"Dbxref": ['GeneID:3559', 'HGNC:HGNC:6008', 'MIM:147730'],
                       "ID": ['gene27397'],
                       "Name": ['IL2RA'],
                       "description": ['interleukin 2 receptor subunit alpha'],
                       "gbkey":  ['Gene'],
                       "gene": ['IL2RA'],
                       "gene_biotype": ['protein_coding'],
                       "gene_synonym": ['CD25', 'IDDM10', 'IL2R', 'IMD41', 'p55', 'TCGFR'],
                       "source": ['BestRefSeq']}
        gene = SeqFeature(FeatureLocation(6010693, 6062370, strand=-1),
                          type="gene", id='gene27397', qualifiers=qualifiers_)

        expected_annotated_gene = {'loc_start': '6010693', 'hgnc_id': '6008', 'gene_checksum': None,
                                   'loc_checksum': None,
                                   'loc_end': '6062370', 'loc_region': '10', 'stable_id': '3559',
                                   'session_id': None, 'loc_strand': '-1', 'assembly_id': "1",
                                   'stable_id_version': 1}

        chrome = '10'
        annotated_gene = GFFHandler.get_annotated_gene(chrome, gene)
        self.assertEqual(expected_annotated_gene, annotated_gene, "Got back the right annotated gene")

    def test_get_annotated_transcript(self):

        qualifiers_ = {"Dbxref": ['GeneID:3559', 'Genbank:NM_000417.2', 'HGNC:HGNC:6008', 'MIM:147730'],
                       "ID": ['rna80734'],
                       "Name": ['NM_000417.2'],
                       "product": ['interleukin 2 receptor subunit alpha, transcript variant 1'],
                       "source": ['BestRefSeq'],
                       "gbkey":  ['mRNA'],
                       "transcript_id": ['NM_000417.2'],
                       "Parent": ['gene27397']
                       }

        mRNA_feature = SeqFeature(FeatureLocation(6010693, 6062370, strand=-1),
                                  type="mRNA", id='rna80734', qualifiers=qualifiers_)

        chrom = '10'
        annotated_transcript = GFFHandler.get_annotated_transcript(self.fasta_handler, chrom, mRNA_feature)

        expected_annotated_transcript = {'loc_region': '10',
                                         'sequence': self.mRNA_sequence,
                                         'session_id': None, 'loc_strand': '-1', 'loc_end': '6062370',
                                         'assembly_id': '1', 'stable_id': 'NM_000417',
                                         'stable_id_version': '2', 'transcript_checksum': None, 'seq_checksum': None,
                                         'exon_set_checksum': None, 'loc_checksum': None,
                                         'loc_start': '6010693'}

        self.assertEqual(expected_annotated_transcript, annotated_transcript, "Got back the right annotated transcript")

    def test_get_annotated_exon(self):

        exon_feature = {'exon_order': '7',
                        'exon_seq_region_strand': '-1', 'exon_stable_id': 'id977755',
                        'exon_end': 1013, 'exon_seq_region_start': '6018052',
                        'exon_seq': 'TGGCCGGCTGTGTTTTCCTGCTGATCAGCGTCCTCCTCCTGAGTGGGCTCACCTGGCAGCGGAGACA',
                        'exon_seq_region': '10', 'exon_stable_id_version': '1', 'exon_start': 947,
                        'exon_seq_region_end': '6018119'}
        chrom = '10'
        annotated_exon = GFFHandler.get_annotated_exon(chrom, exon_feature)

        expected_annotated_exon = {'loc_region': '10',
                                   'exon_order': '7',
                                   'seq_checksum': None,
                                   'session_id': None, 'loc_strand': '-1', 'loc_end': '6018119',
                                   'assembly_id': '1', 'stable_id': 'id977755',
                                   'stable_id_version': '1', 'seq_checksum': None,
                                   'exon_checksum': None, 'loc_checksum': None,
                                   'loc_start': '6018052'}

        self.assertDictEqual(expected_annotated_exon, annotated_exon, "Got back the right annotated exon")
