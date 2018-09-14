from django.test import TestCase
import os
from refseq_loader.handlers.refseq.confighandler import ConfigHandler
from refseq_loader.handlers.refseq.downloadhandler import DownloadHandler


'''
/manage.py test refseq_loader.tests.test_filehandler --settings=tark.settings.test
'''


class DownloadHandlerTest(TestCase):

    def setUp(self):
        APP_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print("APP_BASE_DIR dir " + str(APP_BASE_DIR))
        TEST_DATA_DIR = APP_BASE_DIR + "/tests/data/"

        self.ini_file = TEST_DATA_DIR + "refseq_source.ini"
        config_handler = ConfigHandler(self.ini_file)
        default_config = config_handler.get_section_config()

        self.refseq_ftp_root = default_config.get("refseq_ftp_root")
        self.refseq_gff_file_gz = default_config.get("refseq_gff_file_gz")
        self.refseq_fasta_file_gz = default_config.get("refseq_fasta_file_gz")
        self.refseq_protein_file_gz = default_config.get("refseq_protein_file_gz")

    def test_download_file(self):

        self.assertIsNotNone(self.refseq_ftp_root, "refseq_ftp_root is not None")
        self.assertIsNotNone(self.refseq_gff_file_gz, "refseq_gff_file_gz is not None")
        self.assertIsNotNone(self.refseq_fasta_file_gz, "refseq_fasta_file_gz is not None")
        self.assertIsNotNone(self.refseq_protein_file_gz, "refseq_protein_file_gz is not None")
