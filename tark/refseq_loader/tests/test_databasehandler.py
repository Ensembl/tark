from django.test import TestCase
from Bio.SeqFeature import SeqFeature, FeatureLocation
import os
from refseq_loader.handlers.refseq.fastahandler import FastaHandler
from refseq_loader.handlers.refseq.gffhandler import GFFHandler


'''
/manage.py test refseq_loader.tests --settings=tark.settings.test
'''


class DatabaseHandlerTest(TestCase):
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
        
        self.annotated_gene = {}