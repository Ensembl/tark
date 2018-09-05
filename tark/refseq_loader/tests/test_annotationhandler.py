from django.test import TestCase
from Bio.SeqFeature import SeqFeature, FeatureLocation
import os
from refseq_loader.handlers.refseq.fastahandler import FastaHandler
from refseq_loader.handlers.refseq.gffhandler import GFFHandler
from refseq_loader.handlers.refseq.genbankhandler import GenBankHandler


'''
/manage.py test refseq_loader.tests --settings=tark.settings.test
'''


class AnnotationHandlerTest(TestCase):
    def setUp(self):
        APP_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print("APP_BASE_DIR dir " + str(APP_BASE_DIR))
        TEST_DATA_DIR = APP_BASE_DIR + "/tests/data/"

        self.fasta_file = TEST_DATA_DIR + "IL2RA_GCF_000001405.38_GRCh38.p12_rna.fna"

        self.fasta_file_protein = TEST_DATA_DIR + "IL2RA_GCF_000001405.38_GRCh38.p12_protein.faa"

        self.gff_file = TEST_DATA_DIR + "GCF_000001405.38_GRCh38.p12_genomic_test.gff"

        self.genbank_file = TEST_DATA_DIR + "il2ra_tnni3.gb"

        if not os.path.exists(self.fasta_file):
            raise FileNotFoundError("File not found " + self.fasta_file)  # @UndefinedVariable

        if not os.path.exists(self.gff_file):
            raise FileNotFoundError("File not found " + self.gff_file)  # @UndefinedVariable

        if not os.path.exists(self.genbank_file):
            raise FileNotFoundError("File not found " + self.genbank_file)  # @UndefinedVariable

        if not os.path.exists(self.fasta_file_protein):
            raise FileNotFoundError("File not found " + self.fasta_file_protein)  # @UndefinedVariable

        self.fasta_handler = FastaHandler(self.fasta_file)

        self.fasta_handler_protein = FastaHandler(self.fasta_file_protein)

        self.sequence_handler = GenBankHandler(self.genbank_file)

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

        self.translation_seq = "MDSYLLMWGLLTFIMVPGCQAELCDDDPPEIPHATFKAMAYKEGTMLNCECKRGFRRIKSGSLYMLCTGNSSHSS"\
                               "WDNQCQCTSSATRNTTKQVTPQPEEQKERKTTEMQSPMQPVDQASLPGHCREPPPWENEATERIYHFVVGQMVYYQCV"\
                               "QGYRALHRGPAESVCKMTHGKTRWTQPQLICTGEMETSQFPGEEKPQASPEGRPESETSCLVTTTDFQIQTEMAATMETS"\
                               "IFTTEYQVAVAGCVFLLISVLLLSGLTWQRRQRKSRRTI"

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
        annotated_transcript = GFFHandler.get_annotated_transcript(self.sequence_handler, chrom, mRNA_feature)

        expected_annotated_transcript = {'loc_region': '10',
                                         'sequence': self.mRNA_sequence,
                                         'session_id': None, 'loc_strand': '-1', 'loc_end': '6062370',
                                         'assembly_id': '1', 'stable_id': 'NM_000417',
                                         'stable_id_version': '2', 'transcript_checksum': None,
                                         'seq_checksum': '74EB357B801F80AAC6345D1B7300F3723B9561DC',
                                         'exon_set_checksum': None,
                                         'loc_checksum': '61407C2B6D7BE167F878F15680D3A6ECC9DFFD3F',
                                         'loc_start': '6010694'}

        self.assertEqual(expected_annotated_transcript, annotated_transcript, "Got back the right annotated transcript")

    def test_get_annotated_exons(self):

        refseq_exon_list = [{'exon_stable_id_version': 1, 'exon_order': 1, 'exon_end': '6062370', 'exon_strand': '-1',
                             'exon_stable_id': 'id977749', 'exon_start': '6062088'},
                            {'exon_stable_id_version': 1, 'exon_order': 2, 'exon_end': '6026025', 'exon_strand': '-1',
                             'exon_stable_id': 'id977750', 'exon_start': '6025834'},
                            {'exon_stable_id_version': 1, 'exon_order': 3, 'exon_end': '6024354', 'exon_strand': '-1',
                             'exon_stable_id': 'id977751', 'exon_start': '6024244'},
                            {'exon_stable_id_version': 1, 'exon_order': 4, 'exon_end': '6021693', 'exon_strand': '-1',
                             'exon_stable_id': 'id977752', 'exon_start': '6021478'},
                            {'exon_stable_id_version': 1, 'exon_order': 5, 'exon_end': '6019941', 'exon_strand': '-1',
                             'exon_stable_id': 'id977753', 'exon_start': '6019870'},
                            {'exon_stable_id_version': 1, 'exon_order': 6, 'exon_end': '6019499', 'exon_strand': '-1',
                             'exon_stable_id': 'id977754', 'exon_start': '6019428'},
                            {'exon_stable_id_version': 1, 'exon_order': 7, 'exon_end': '6018119', 'exon_strand': '-1',
                             'exon_stable_id': 'id977755', 'exon_start': '6018053'},
                            {'exon_stable_id_version': 1, 'exon_order': 8, 'exon_end': '6012896', 'exon_strand': '-1',
                             'exon_stable_id': 'id977756', 'exon_start': '6010694'}]

        expected_annotated_list = [{'stable_id': 'id977749', 'assembly_id': '1', 'loc_start': '6062088',
                                    'loc_region': '10', 'stable_id_version': 1,
                                    'exon_seq': self.fasta_handler.get_fasta_seq_by_id("NM_000417.2:1-283"),
                                    'seq_checksum': '0C101E2B507F093970F9D4CAA1457CCA56197F56',
                                    'exon_order': 1, 'loc_strand': '-1',
                                    'loc_checksum': '4200AA8E78206DFFDF840248A43461056B835273', 'loc_end': '6062370',
                                    'exon_checksum': '5BA7824E11A730B9698576162647EE5484B80698', 'session_id': None},
                                   {'stable_id': 'id977750', 'assembly_id': '1', 'loc_start': '6025834',
                                    'loc_region': '10', 'stable_id_version': 1,
                                    'exon_seq': self.fasta_handler.get_fasta_seq_by_id("NM_000417.2:284-475"),
                                    'seq_checksum': '10994FB1A1A133807915D17A800ADE839F3D06CB', 'exon_order': 2,
                                    'loc_strand': '-1', 'loc_checksum': '2DF03B96057555691BBFD2045B6661B3794E1CBC',
                                    'loc_end': '6026025', 'exon_checksum': 'AC2B51B3552E23A2A29335E59F00BDEF7479FD58',
                                    'session_id': None},
                                   {'stable_id': 'id977751', 'assembly_id': '1',
                                    'loc_start': '6024244', 'loc_region': '10', 'stable_id_version': 1,
                                    'exon_seq': self.fasta_handler.get_fasta_seq_by_id("NM_000417.2:476-586"),
                                    'seq_checksum': '1287D56D5AC372EB4FB0872D9330C678E03114DB',
                                    'exon_order': 3, 'loc_strand': '-1',
                                    'loc_checksum': 'B9C5340E12BFB4E14E392B2AFD840B1CF830D23C',
                                    'loc_end': '6024354', 'exon_checksum': 'C9AF9E2E270E7AFD690664C80DCCBF74D970DC91',
                                    'session_id': None},
                                   {'stable_id': 'id977752', 'assembly_id': '1', 'loc_start': '6021478',
                                    'loc_region': '10', 'stable_id_version': 1,
                                    'exon_seq': self.fasta_handler.get_fasta_seq_by_id("NM_000417.2:587-802"),
                                    'seq_checksum': '93EBE214ACB31AE95E471DF89E98184AF4DC1134',
                                    'exon_order': 4, 'loc_strand': '-1',
                                    'loc_checksum': '43620745774864525A343060C34A7F8790307FE9',
                                    'loc_end': '6021693', 'exon_checksum': '1C510AC68E16A324A94E914C91DBEB5CE9BAA789',
                                    'session_id': None},
                                   {'stable_id': 'id977753', 'assembly_id': '1', 'loc_start': '6019870',
                                    'loc_region': '10',
                                    'stable_id_version': 1,
                                    'exon_seq': self.fasta_handler.get_fasta_seq_by_id("NM_000417.2:803-874"),
                                    'seq_checksum': 'ECD0E61FC953F07C32BB7004386F73D087D98A05',
                                    'exon_order': 5, 'loc_strand': '-1',
                                    'loc_checksum': '4E4B1749209C6F2BF02F7FE0E061C1DC9F90450F',
                                    'loc_end': '6019941', 'exon_checksum': '9BA73E58C5233E2A2B5B85EBA1BBD136060A61BB',
                                    'session_id': None},
                                   {'stable_id': 'id977754', 'assembly_id': '1', 'loc_start': '6019428',
                                    'loc_region': '10', 'stable_id_version': 1,
                                    'exon_seq': self.fasta_handler.get_fasta_seq_by_id("NM_000417.2:875-946"),
                                    'seq_checksum': '5EACEA93762E843E1B63102EAA5A74C634ACDE17', 'exon_order': 6,
                                    'loc_strand': '-1', 'loc_checksum': '176CDA12ECF6AC434F2B4B1843EA02D63BA43479',
                                    'loc_end': '6019499', 'exon_checksum': 'ECDD2E3366ADA9CF56688C64E74B5D35DD70A855',
                                    'session_id': None},
                                   {'stable_id': 'id977755', 'assembly_id': '1',
                                    'loc_start': '6018053', 'loc_region': '10', 'stable_id_version': 1,
                                    'exon_seq': self.fasta_handler.get_fasta_seq_by_id("NM_000417.2:947-1013"),
                                    'seq_checksum': '3A3213F5881F100D287F48FB856CEA3620D90964',
                                    'exon_order': 7,
                                    'loc_strand': '-1', 'loc_checksum': '02963E2BE0C0A607804B9BAFE51EA1CC4B8F439C',
                                    'loc_end': '6018119', 'exon_checksum': '29EFBD053BD00437A75A84ACABACB843D154C644',
                                    'session_id': None},
                                   {'stable_id': 'id977756', 'assembly_id': '1', 'loc_start': '6010694',
                                    'loc_region': '10', 'stable_id_version': 1,
                                    'exon_seq': self.fasta_handler.get_fasta_seq_by_id("NM_000417.2:1014-3216"),
                                    'seq_checksum': '4C86D6CF0D14A91AE7EC17B4B1DF35E39EDAA8F9', 'exon_order': 8,
                                    'loc_strand': '-1',
                                    'loc_checksum': 'DE9473C749EADD94BE705C8A8E174DAFE92E89EB', 'loc_end': '6012896',
                                    'exon_checksum': '570D61944862E9A0939055D2A4F93C14B97806F9', 'session_id': None}]

        actual_annotated_exons = GFFHandler.get_annotated_exons(self.sequence_handler, "10", "NM_000417.2",
                                                                refseq_exon_list)
        self.assertListEqual(expected_annotated_list, actual_annotated_exons, "Got the right annotated exons")

    def test_get_annotated_exon(self):

        exon_feature = {'exon_order': '7',
                        'exon_strand': '-1', 'exon_stable_id': 'id977755',
                        'exon_start': '6018052',
                        'exon_seq': 'TGGCCGGCTGTGTTTTCCTGCTGATCAGCGTCCTCCTCCTGAGTGGGCTCACCTGGCAGCGGAGACA',
                        'exon_seq_region': '10', 'exon_stable_id_version': '1',
                        'exon_end': '6018119'}
        chrom = '10'

        exon_sequence = exon_feature['exon_seq']
        annotated_exon = GFFHandler.get_annotated_exon(chrom, exon_feature, exon_sequence)

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
                                'loc_strand': '-1', 'stable_id_version': '1',
                                'translation_seq': self.translation_seq,
                                'seq_checksum': 'D51D73686E3257015EC2BF894ECC394ADE844270'}

        seq_region = 10

        translation = GFFHandler.get_annotated_cds(self.fasta_handler_protein, seq_region, "NP_000408.1", self.cds_list)
        self.assertEqual(translation, expected_translation, "Got the right translation")

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
