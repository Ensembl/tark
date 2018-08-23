from django.test import TestCase
from refseq_loader.handlers.refseq.checksumhandler import ChecksumHandler


'''
/manage.py test refseq_loader.tests --settings=tark.settings.test
'''


class ChecksumHandlerTest(TestCase):

    def setUp(self):
        self.annotated_exon = {'loc_region': '10',
                               'exon_order': '7',
                               'seq_checksum': None,
                               'session_id': None, 'loc_strand': '-1', 'loc_end': '6018119',
                               'assembly_id': '1', 'stable_id': 'id977755',
                               'stable_id_version': '1',
                               'exon_checksum': None, 'loc_checksum': None,
                               'loc_start': '6018052',
                               'exon_seq': 'TGGCCGGCTGTGTTTTCCTGCTGATCAGCGTCCTCCTCCTGAGTGGGCTCACCTGGCAGCGGAGACA'}

        self.annotated_gene = {'loc_start': '6010693', 'hgnc_id': '6008',
                               'gene_checksum': None,
                               'loc_checksum': None,
                               'loc_end': '6062370', 'loc_region': '10', 'stable_id': '3559',
                               'session_id': None, 'loc_strand': '-1', 'assembly_id': "1",
                               'stable_id_version': 1}

    def test_checksum_list(self):
        assembly_id = '1'
        seq_region_name = '10'
        seq_region_start = "1"
        seq_region_end = "1000"
        test_loc_list = [assembly_id, seq_region_name, seq_region_start, seq_region_end]

        test_loc_checksum = ChecksumHandler.checksum_list(test_loc_list)

        self.assertEqual("<class 'str'>", str(type(test_loc_checksum)))
        self.assertEqual('E9D98ED721DD35A48743DA2CF54CE2FBA06FE214', test_loc_checksum, "Got the right loc_checksum")

        test_loc_checksum_reversed = ChecksumHandler.checksum_list(list(reversed(test_loc_list)))

        self.assertNotEqual(test_loc_checksum, test_loc_checksum_reversed, "checksum differs if list is reversed")
        self.assertEqual('B28A710535EE52DC5908A9E07AD2986A282B3C2B', test_loc_checksum_reversed,
                         "Got the right loc_checksum")

        test_loc_checksum_repeat = ChecksumHandler.checksum_list(test_loc_list)
        self.assertEqual(test_loc_checksum, test_loc_checksum_repeat, "checksum is same when repeated")

        hgnc_id = None
        stable_id = 'NM_000417'
        stable_id_version = '2'
        gene_list_bits = test_loc_list + [hgnc_id, stable_id, stable_id_version]

        test_loc_list = [bit for bit in gene_list_bits if bit is not None]
        gene_checksum = ChecksumHandler.checksum_list(test_loc_list)
        self.assertIsNotNone(gene_checksum, "Got back gene checksum")

    def test_checksum_loc(self):
        loc_checksum = ChecksumHandler.get_location_checksum(self.annotated_exon)
        self.assertEqual('1129869BCB84288854E9C320B2ACC12ED5E6E130', loc_checksum,
                         "Got loc checksum")

    def test_checksum_exon(self):
        exon_checksum = ChecksumHandler.get_exon_checksum(self.annotated_exon)
        self.assertEqual('3492543A164740DD8E0E083D7F730FB0BBA38E94', exon_checksum, "Got back the exon_checksum")

    def test_checksum_gene(self):
        gene_checksum = ChecksumHandler.get_gene_checksum(self.annotated_gene)
        self.assertEqual('D6F2AD08879C8D1705A5A1347A11726DE0C7F973', gene_checksum, "Got back the gene_checksum")
