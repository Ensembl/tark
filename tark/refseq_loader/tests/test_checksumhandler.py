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
                               'loc_checksum': '51BA025EBD0EFEC96758D44D82C0B21FD450989F',
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
        self.assertEqual('2CA3A84E6B88426315EFC032BE0026464B1732F0', gene_checksum, "Got back the gene_checksum")

    def test_get_exonset_checksum(self):

        exon_annotated_list = [
                    {'exon_checksum': '5BA7824E11A730B9698576162647EE5484B80698'},
                    {'exon_checksum': 'AC2B51B3552E23A2A29335E59F00BDEF7479FD58'},
                    {'exon_checksum': 'C9AF9E2E270E7AFD690664C80DCCBF74D970DC91'},
                    {'exon_checksum': '1C510AC68E16A324A94E914C91DBEB5CE9BAA789'},
                    {'exon_checksum': '9BA73E58C5233E2A2B5B85EBA1BBD136060A61BB'},
                    {'exon_checksum': 'ECDD2E3366ADA9CF56688C64E74B5D35DD70A855'},
                    {'exon_checksum': '29EFBD053BD00437A75A84ACABACB843D154C644'},
                    {'exon_checksum': '570D61944862E9A0939055D2A4F93C14B97806F9'}]

        exon_set_checksum = ChecksumHandler.get_exon_set_checksum(exon_annotated_list)
        self.assertEqual("41AAF60E3E251CF7AB2798BD7AF05B3630B82B6D", exon_set_checksum,
                         "Got the right exon_set_checksum")

    def test_get_transcript_checksum(self):
        transcript = {'stable_id': 'NM_000417', 'stable_id_version': '2',
                      'seq_checksum': '74EB357B801F80AAC6345D1B7300F3723B9561DC',
                      'exon_set_checksum': '41AAF60E3E251CF7AB2798BD7AF05B3630B82B6D',
                      'loc_checksum': '61407C2B6D7BE167F878F15680D3A6ECC9DFFD3F'}
        expected_transcript_checksum = '43BBAEF6504868906601FC91F144E2811CC0F585'
        transcript_checksum = ChecksumHandler.get_transcript_checksum(transcript)
        self.assertEqual(expected_transcript_checksum, transcript_checksum, "Got back the right transcript checksum")
