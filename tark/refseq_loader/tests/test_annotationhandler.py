from django.test import TestCase
from Bio.SeqFeature import SeqFeature, FeatureLocation
import os
from refseq_loader.handlers.refseq.fastahandler import FastaHandler
from refseq_loader.handlers.refseq.gffhandler import GFFHandler


'''
/manage.py test refseq_loader.tests --settings=tark.settings.test
'''


class AnnotationHandlerTest(TestCase):
    def setUp(self):
        APP_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print("APP_BASE_DIR dir " + str(APP_BASE_DIR))
        TEST_DATA_DIR = APP_BASE_DIR + "/tests/data/"

        self.fasta_file = TEST_DATA_DIR + "IL2RA_GCF_000001405.38_GRCh38.p12_rna.fna"

        self.gff_file = TEST_DATA_DIR + "GCF_000001405.38_GRCh38.p12_genomic_test.gff"
        # print(fasta_file)
        # fasta_file = ''
        if not os.path.exists(self.fasta_file):
            raise FileNotFoundError("File not found " + self.fasta_file)  # @UndefinedVariable

        if not os.path.exists(self.gff_file):
            raise FileNotFoundError("File not found " + self.gff_file)  # @UndefinedVariable

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

        self.cds_list = [
            {'cds_strand': '-1', 'cds_id': 'cds56040', 'cds_end': '6062151', 'cds_start': '6062087',
             'protein_id': 'NP_000408.1', 'cds_order': 1},
            {'cds_strand': '-1', 'cds_id': 'cds56040', 'cds_end': '6026025', 'cds_start': '6025833',
             'protein_id': 'NP_000408.1', 'cds_order': 2},
            {'cds_strand': '-1', 'cds_id': 'cds56040', 'cds_end': '6024354', 'cds_start': '6024243',
             'protein_id': 'NP_000408.1', 'cds_order': 3},
            {'cds_strand': '-1', 'cds_id': 'cds56040', 'cds_end': '6021693', 'cds_start': '6021477',
             'protein_id': 'NP_000408.1', 'cds_order': 4},
            {'cds_strand': '-1', 'cds_id': 'cds56040', 'cds_end': '6019941', 'cds_start': '6019869',
             'protein_id': 'NP_000408.1', 'cds_order': 5},
            {'cds_strand': '-1', 'cds_id': 'cds56040', 'cds_end': '6019499', 'cds_start': '6019427',
             'protein_id': 'NP_000408.1', 'cds_order': 6},
            {'cds_strand': '-1', 'cds_id': 'cds56040', 'cds_end': '6018119', 'cds_start': '6018052',
             'protein_id': 'NP_000408.1', 'cds_order': 7},
            {'cds_strand': '-1', 'cds_id': 'cds56040', 'cds_end': '6012896', 'cds_start': '6012871',
             'protein_id': 'NP_000408.1', 'cds_order': 8}]

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

        expected_annotated_gene = {'loc_start': '6010693', 'hgnc_id': '6008',
                                   'gene_checksum': '98F8C355517BB7A39D9114B66995A88CF71EEDA0',  # @IgnorePep8
                                   'loc_checksum': '51BA025EBD0EFEC96758D44D82C0B21FD450989F',
                                   'loc_end': '6062370', 'loc_region': '10', 'stable_id': '3559',
                                   'session_id': None, 'loc_strand': '-1', 'assembly_id': "1",
                                   'stable_id_version': 1}

        chrome = '10'
        annotated_gene = GFFHandler.get_annotated_gene(chrome, gene)
        self.assertEqual(expected_annotated_gene, annotated_gene,
                         "Got back the right annotated gene")

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
                                   'seq_checksum': '3A3213F5881F100D287F48FB856CEA3620D90964',
                                   'session_id': None, 'loc_strand': '-1', 'loc_end': '6018119',
                                   'assembly_id': '1', 'stable_id': 'id977755',
                                   'stable_id_version': '1',
                                   'exon_checksum': '3492543A164740DD8E0E083D7F730FB0BBA38E94',
                                   'loc_checksum': '1129869BCB84288854E9C320B2ACC12ED5E6E130',
                                   'loc_start': '6018052',
                                   'exon_seq': 'TGGCCGGCTGTGTTTTCCTGCTGATCAGCGTCCTCCTCCTGAGTGGGCTCACCTGGCAGCGGAGACA'}

        self.assertDictEqual(expected_annotated_exon, annotated_exon, "Got back the right annotated exon")

    def test_get_translation_loc(self):

        (translation_start, translation_end) = GFFHandler.get_translation_loc(self.cds_list)
        self.assertEqual('6012871', translation_start, "Got the right translation start")
        self.assertEqual('6062151', translation_end, "Got the right translation end")

    def test_get_annotated_cds(self):

        expected_translation = {'assembly_id': None, 'seq_checksum': None,
                                'loc_start': '6012871', 'loc_end': '6062151',
                                'session_id': None, 'translation_checksum': None,
                                'stable_id': 'NP_000408', 'loc_region': 10,
                                'loc_strand': '-1', 'stable_id_version': '1'}

        seq_region = 10
        translation = GFFHandler.get_annotated_cds(seq_region, self.cds_list)
        self.assertEqual(translation, expected_translation, "Got the right translation")
