from django.test import TestCase
from Bio.SeqFeature import SeqFeature, FeatureLocation
import os
from refseq_loader.handlers.refseq.fastahandler import FastaHandler
from refseq_loader.handlers.refseq.gffhandler import GFFHandler
from refseq_loader.handlers.refseq.databasehandler import SessionHandler,\
    ReleaseHandler, GenomeHandler, AssemblyHandler, ReleaseSourceHandler,\
    FeatureHandler
import gene
from pip._vendor.requests.sessions import session
import collections


'''
/manage.py test refseq_loader.tests --settings=tark.settings.test
'''


class DatabaseHandlerTest(TestCase):

    SESSION_ID = None

    @classmethod
    def setUpTestData(cls):
        session_id = cls.populate_parent_tables()
        DatabaseHandlerTest.SESSION_ID = session_id

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

        # self.session_id = self.populate_parent_tables()

        self.il2ra_obj2save = {'gene':
                               {'loc_end': '6062370', 'loc_strand': '-1', 'hgnc_id': None,
                                'gene_checksum': '2CA3A84E6B88426315EFC032BE0026464B1732F0', 'session_id': None,
                                'loc_region': '10', 'loc_start': '6010693', 'stable_id': '3559', 'assembly_id': '1',
                                'loc_checksum': '51BA025EBD0EFEC96758D44D82C0B21FD450989F', 'stable_id_version': 1,
                                'transcripts': [{
                                    'loc_end': '6062370', 'loc_strand': '-1',
                                    'session_id': None, 'loc_region': '10',
                                    'transcript_checksum': '43BBAEF6504868906601FC91F144E2811CC0F585',
                                    'loc_start': '6010694', 'stable_id': 'NM_000417', 'assembly_id': '1',
                                    'loc_checksum': '61407C2B6D7BE167F878F15680D3A6ECC9DFFD3F',
                                    'seq_checksum': '74EB357B801F80AAC6345D1B7300F3723B9561DC',
                                    'sequence': self.fasta_handler.get_fasta_seq_by_id("NM_000417.2"),
                                    'exon_set_checksum': '41AAF60E3E251CF7AB2798BD7AF05B3630B82B6D',
                                    'stable_id_version': '2',
                                    'exons': [
                                        {'exon_seq': '',
                                         'loc_end': '6062370', 'loc_strand': '-1',
                                         'exon_checksum': '5BA7824E11A730B9698576162647EE5484B80698',
                                         'session_id': None, 'loc_region': '10', 'loc_start': '6062088',
                                         'stable_id': 'id977749', 'assembly_id': '1',
                                         'loc_checksum': '4200AA8E78206DFFDF840248A43461056B835273',
                                         'seq_checksum': '0C101E2B507F093970F9D4CAA1457CCA56197F56',
                                         'exon_order': 1, 'stable_id_version': 1},
                                        {'exon_seq': '',
                                         'loc_end': '6026025', 'loc_strand': '-1',
                                         'exon_checksum': 'AC2B51B3552E23A2A29335E59F00BDEF7479FD58',
                                         'session_id': None,
                                         'loc_region': '10', 'loc_start': '6025834', 'stable_id': 'id977750',
                                         'assembly_id': '1', 'loc_checksum': '2DF03B96057555691BBFD2045B6661B3794E1CBC',
                                         'seq_checksum': '10994FB1A1A133807915D17A800ADE839F3D06CB', 'exon_order': 2,
                                         'stable_id_version': 1},
                                        {'exon_seq': '', 'loc_end': '6024354', 'loc_strand': '-1',
                                         'exon_checksum': 'C9AF9E2E270E7AFD690664C80DCCBF74D970DC91',
                                         'session_id': None, 'loc_region': '10', 'loc_start': '6024244',
                                         'stable_id': 'id977751', 'assembly_id': '1',
                                         'loc_checksum': 'B9C5340E12BFB4E14E392B2AFD840B1CF830D23C',
                                         'seq_checksum': '1287D56D5AC372EB4FB0872D9330C678E03114DB',
                                         'exon_order': 3, 'stable_id_version': 1},
                                        {'exon_seq': '', 'loc_end': '6021693', 'loc_strand': '-1',
                                         'exon_checksum': '1C510AC68E16A324A94E914C91DBEB5CE9BAA789',
                                         'session_id': None, 'loc_region': '10', 'loc_start': '6021478',
                                         'stable_id': 'id977752', 'assembly_id': '1',
                                         'loc_checksum': '43620745774864525A343060C34A7F8790307FE9',
                                         'seq_checksum': '93EBE214ACB31AE95E471DF89E98184AF4DC1134',
                                         'exon_order': 4, 'stable_id_version': 1},
                                        {'exon_seq': 'GTGAAGAGAAGCCTCAGGCAAGCCCCGAAGGCCGTCCTGAGAGTGAGACTTCCTGCCTCGTCACAACAACAG',  # @IgnorePep8
                                         'loc_end': '6019941', 'loc_strand': '-1',
                                         'exon_checksum': '9BA73E58C5233E2A2B5B85EBA1BBD136060A61BB',
                                         'session_id': None, 'loc_region': '10', 'loc_start': '6019870',
                                         'stable_id': 'id977753', 'assembly_id': '1',
                                         'loc_checksum': '4E4B1749209C6F2BF02F7FE0E061C1DC9F90450F',
                                         'seq_checksum': 'ECD0E61FC953F07C32BB7004386F73D087D98A05', 'exon_order': 5,
                                         'stable_id_version': 1},
                                        {'exon_seq': '', 'loc_end': '6019499', 'loc_strand': '-1',
                                         'exon_checksum': 'ECDD2E3366ADA9CF56688C64E74B5D35DD70A855',
                                         'session_id': None, 'loc_region': '10', 'loc_start': '6019428',
                                         'stable_id': 'id977754', 'assembly_id': '1',
                                         'loc_checksum': '176CDA12ECF6AC434F2B4B1843EA02D63BA43479',
                                         'seq_checksum': '5EACEA93762E843E1B63102EAA5A74C634ACDE17',
                                         'exon_order': 6, 'stable_id_version': 1},
                                        {'exon_seq': 'TGGCCGGCTGTGTTTTCCTGCTGATCAGCGTCCTCCTCCTGAGTGGGCTCACCTGGCAGCGGAGACA',  # @IgnorePep8
                                         'loc_end': '6018119', 'loc_strand': '-1',
                                         'exon_checksum': '29EFBD053BD00437A75A84ACABACB843D154C644',
                                         'session_id': None, 'loc_region': '10', 'loc_start': '6018053',
                                         'stable_id': 'id977755',
                                         'assembly_id': '1', 'loc_checksum': '02963E2BE0C0A607804B9BAFE51EA1CC4B8F439C',
                                         'seq_checksum': '3A3213F5881F100D287F48FB856CEA3620D90964',
                                         'exon_order': 7, 'stable_id_version': 1},
                                        {'exon_seq': '', 'loc_end': '6012896', 'loc_strand': '-1',
                                         'exon_checksum': '570D61944862E9A0939055D2A4F93C14B97806F9',
                                         'session_id': None, 'loc_region': '10', 'loc_start': '6010694',
                                         'stable_id': 'id977756', 'assembly_id': '1',
                                         'loc_checksum': 'DE9473C749EADD94BE705C8A8E174DAFE92E89EB',
                                         'seq_checksum': '4C86D6CF0D14A91AE7EC17B4B1DF35E39EDAA8F9', 'exon_order': 8,
                                         'stable_id_version': 1}],
                                    'translation': {
                                                     'loc_end': '6062151', 'loc_strand': '-1',
                                                     'translation_checksum': 'DE5121D7D310E2F853461A055B8072E6874EECB8',
                                                     'session_id': None, 'loc_region': 10, 'loc_start': '6012872',
                                                     'stable_id': 'NP_000408',
                                                     'translation_seq': '', 'assembly_id': '1',
                                                     'loc_checksum': 'E61A7AE27083F32E99E8D1F1C1AAB467484D6CE5',
                                                     'seq_checksum': 'D51D73686E3257015EC2BF894ECC394ADE844270',
                                                     'stable_id_version': '1'},
                                                }],
                                }}

    def test_start_session(self):
        session_id = SessionHandler.start_session("Test Client1")
        self.assertIsNotNone(session_id, "Got back session id")
        session_id = SessionHandler.start_session("Test Client2")
        self.assertIsNotNone(session_id, "Got back session id")

    def test_load_release_set(self):
        session_id = SessionHandler.start_session("Test Client3")
        self.assertIsNotNone(session_id, "Got back session id")

        genome_data = {"name": "homo_sapiens", "tax_id": str(9606), "session_id": str(session_id)}
        genome_id = GenomeHandler.load_genome(genome_data)
        self.assertIsNotNone(genome_id, "Got back genome_id")

        assembly_data = {"genome_id": str(1), "assembly_name": "GRCh38", "session_id": str(1)}
        assembly_id = AssemblyHandler.load_assembly(assembly_data)
        self.assertIsNotNone(assembly_id, "Got back assembly_id")

        release_source = {"shortname": "Ensembl_test", "description": "Ensembl data imports from Human Core DBs"}
        release_source_id = ReleaseSourceHandler.load_release_source(release_source)
        self.assertIsNotNone(release_source_id, "Got back release_source_id")

        release_source = {"shortname": "RefSeq_test", "description": "RefSeq data imports from RefSeq GFF"}
        release_source_id = ReleaseSourceHandler.load_release_source(release_source)
        self.assertIsNotNone(release_source_id, "Got back release_source_id")

        data_release_set = collections.OrderedDict()
        data_release_set["shortname"] = "94"
        data_release_set["description"] = "Refseq release 94"
        data_release_set["assembly_id"] = "1"
        data_release_set["release_date"] = "12-09-2018"
        data_release_set["session_id"] = "1"
        data_release_set["source_id"] = "2"
        release_id = ReleaseHandler.load_release_set(session_id, data_release_set)
        self.assertIsNotNone(release_id, "Got back release_id")

    def test_add_gene(self):

        # note: have issues with hgnc_id, so remove it for now
        gene_id = FeatureHandler.add_gene(self.il2ra_obj2save["gene"], DatabaseHandlerTest.SESSION_ID)
        self.assertEqual(1, gene_id, "Got back gene_id")

        # try to load the same gene again
        gene_id = FeatureHandler.add_gene(self.il2ra_obj2save["gene"], DatabaseHandlerTest.SESSION_ID)
        self.assertEqual(1, gene_id, "Got back same gene_id")

    def test_add_transcripts(self):

        # note: have issues with hgnc_id, so remove it for now
        gene_id = FeatureHandler.add_gene(self.il2ra_obj2save["gene"], DatabaseHandlerTest.SESSION_ID)
        self.assertEqual(1, gene_id, "Got back gene_id")

        transcript_ids = FeatureHandler.add_transcripts(self.il2ra_obj2save["gene"]["transcripts"],
                                                        gene_id, DatabaseHandlerTest.SESSION_ID)
        print(transcript_ids)

    def test_add_sequence(self):
        sequence_data = {"sequence": self.fasta_handler.get_fasta_seq_by_id("NM_000417.2"),
                         "seq_checksum": "74EB357B801F80AAC6345D1B7300F3723B9561DC",
                         }
        sequence_id = FeatureHandler.add_sequence(sequence_data, DatabaseHandlerTest.SESSION_ID)
        self.assertEqual(0, sequence_id, "Inserted sequence")
        sequence_id = FeatureHandler.add_sequence(sequence_data, DatabaseHandlerTest.SESSION_ID)
        self.assertEqual(0, sequence_id, "Sequence not inserted")

    @classmethod
    def populate_parent_tables(cls):
        session_id = SessionHandler.start_session("Test Client")

        genome_data = {"name": "homo_sapiens", "tax_id": str(9606), "session_id": str(session_id)}
        GenomeHandler.load_genome(genome_data)

        assembly_data = {"genome_id": str(1), "assembly_name": "GRCh38", "session_id": str(1)}
        AssemblyHandler.load_assembly(assembly_data)

        release_source = {"shortname": "Ensembl", "description": "Ensembl data imports from Human Core DBs"}
        ReleaseSourceHandler.load_release_source(release_source)

        release_source = {"shortname": "RefSeq", "description": "RefSeq data imports from RefSeq GFF"}
        ReleaseSourceHandler.load_release_source(release_source)

        ReleaseHandler.load_release_set(session_id)

        return session_id
