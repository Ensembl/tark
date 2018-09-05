from django.test import TestCase
import os

'''
/manage.py test refseq_loader.tests.test_filehandler --settings=tark.settings.test
'''
from refseq_loader.handlers.refseq.confighandler import ConfigHandler


class ConfigHandlerTest(TestCase):
    def setUp(self):
        APP_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print("APP_BASE_DIR dir " + str(APP_BASE_DIR))
        TEST_DATA_DIR = APP_BASE_DIR + "/tests/data/"

        self.ini_file = TEST_DATA_DIR + "refseq_source.ini"

        if not os.path.exists(self.ini_file):
            raise FileNotFoundError("File not found " + self.ini_file)  # @UndefinedVariable

        self.config_handler = ConfigHandler(self.ini_file)

    def test_get_config(self):
        default_config = self.config_handler.get_section_config()
        config_ftp_root = default_config['refseq_ftp_root']
        config_ftp_root_via_get = default_config.get('refseq_ftp_root')
        expected_ftp_root = 'ftp://ftp.ncbi.nlm.nih.gov/genomes/refseq/vertebrate_mammalian/Homo_sapiens/latest_assembly_versions/GCF_000001405.38_GRCh38.p12/'  # @IgnorePep8
        self.assertEqual(expected_ftp_root, config_ftp_root, "Got back ftp root")
        self.assertEqual(expected_ftp_root, config_ftp_root_via_get, "Got back ftp root via get")
