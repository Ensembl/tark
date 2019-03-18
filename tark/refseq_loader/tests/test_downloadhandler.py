"""
.. See the NOTICE file distributed with this work for additional information
   regarding copyright ownership.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from django.test import TestCase
import os
from refseq_loader.handlers.refseq.confighandler import ConfigHandler


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
