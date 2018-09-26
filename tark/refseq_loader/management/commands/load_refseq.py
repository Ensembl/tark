from django.core.management.base import BaseCommand
import os
import wget

import sys
# import the logging library
import logging
from refseq_loader.handlers.refseq.gffhandler import GFFHandler
from refseq_loader.handlers.refseq.confighandler import ConfigHandler
from refseq_loader.handlers.refseq.downloadhandler import DownloadHandler

# Get an instance of a logger
logger = logging.getLogger(__name__)

# How to run
#  ./manage.py load_refseq --settings=tark.settings.local --download_dir=tmp_refseq2


class Command(BaseCommand):
    help = 'Load refseq data from GBFF and GFF3 files'
    ini_file = os.path.abspath(os.path.dirname(__file__)) + "/refseq_source.ini"
    config_handler = ConfigHandler(ini_file)
    print(config_handler)
    default_config = config_handler.get_section_config()
    print("default config==========")
    print(default_config)
#     refseq_ftp_root = "ftp://ftp.ncbi.nlm.nih.gov/genomes/refseq/vertebrate_mammalian/Homo_sapiens/latest_assembly_versions/GCF_000001405.38_GRCh38.p12/"  # @IgnorePep8
#     refseq_gff_file_gz = "GCF_000001405.38_GRCh38.p12_genomic.gff.gz"
#     refseq_fasta_file_gz = "GCF_000001405.38_GRCh38.p12_rna.fna.gz"

    refseq_ftp_root = default_config.get("refseq_ftp_root")
    refseq_gff_file_gz = default_config.get("refseq_gff_file_gz")
    refseq_fasta_file_gz = default_config.get("refseq_fasta_file_gz")
    refseq_protein_file_gz = default_config.get("refseq_protein_file_gz")
    refseq_genbank_file_gz = default_config.get("refseq_genbank_file")

    print("refseq_ftp_root " + refseq_ftp_root)
    print("refseq_gff_file_gz " + refseq_gff_file_gz)
    print("refseq_fasta_file_gz " + refseq_fasta_file_gz)
    print("refseq_protein_file_gz " + refseq_protein_file_gz)
    print("refseq_genbank_file_gz " + refseq_genbank_file_gz)

    def add_arguments(self, parser):
        parser.add_argument('--download_dir',  help='Download Dir')

    def handle(self, *args, **options):
        print(args)
        print('=========')
        print(options)

        download_dir_ = options['download_dir']

        download_dir_ = download_dir_ + "/" if download_dir_ else "tmp_refseq/"

        print('download_dir ' + download_dir_)

        if not os.path.exists(download_dir_):
            print("path doesn't exists. Creating dir at " + download_dir_)
            os.makedirs(download_dir_)

        files_names = [self.refseq_gff_file_gz, self.refseq_fasta_file_gz, self.refseq_protein_file_gz,
                       self.refseq_genbank_file_gz]
        downloaded_files = DownloadHandler.download_files(files_names, self.refseq_ftp_root, download_dir_)
        print("==============================download files====")
        print(downloaded_files)

        if len(downloaded_files) == 4:
                try:
#                     filter_region = 'NC_000010.11'  # chr10
#                     filter_feature_gene = 'IL2RA'
#                     filter_feature_transcript = 'NM_000417.2'
#                     GFFHandler.parse_gff_with_genbank(downloaded_files,
#                                                       filter_region,
#                                                       filter_feature_gene,
#                                                       filter_feature_transcript)
                    GFFHandler.parse_gff_with_genbank(downloaded_files)

                except:
                    print("Unexpected error:", sys.exc_info()[0])
                    raise

    def handle_depre(self, *args, **options):

        print(args)
        print('=========')
        print(options)

        download_dir_ = options['download_dir']

        download_dir_ = download_dir_ if download_dir_ else "tmp_refseq/"
        fasta_status = None

        print('download_dir ' + download_dir_)

        if not os.path.exists(download_dir_):
            print("path doesn't exists. Creating dir at " + download_dir_)
            os.makedirs(download_dir_)

        print('Beginning refseq gff file download with wget module..........')
        gff_url = self.refseq_ftp_root + self.refseq_gff_file_gz
        downloaded_gff_url = download_dir_ + self.refseq_gff_file_gz
        base = os.path.basename(self.refseq_gff_file_gz)
        downloaded_gff_url_unzipped = download_dir_ + os.path.splitext(base)[0]
        print(downloaded_gff_url_unzipped)
        if not os.path.exists(downloaded_gff_url):
            wget.download(gff_url, download_dir_)
            print('File doesnt exists ' + downloaded_gff_url + '\n')
        else:
            print("File already exists at " + downloaded_gff_url)
            if not os.path.exists(downloaded_gff_url_unzipped):
                gff_status = os.system('gunzip ' + downloaded_gff_url)
                if not gff_status == 0:
                    raise ValueError("Unzipped GFF file not found ")

        self.stdout.write(self.style.SUCCESS('\nSuccessfully Downloaded refseq gff file to ' + download_dir_ + '\n'))

        print('Beginning refseq fasta file download with wget module..........')
        fasta_url = self.refseq_ftp_root + self.refseq_fasta_file_gz
        downloaded_fasta_url = download_dir_ + self.refseq_fasta_file_gz
        if not os.path.exists(downloaded_fasta_url):
            print('File doesnt exists ' + downloaded_fasta_url + '\n')
            wget.download(fasta_url, download_dir_)
            self.stdout.write(self.style.SUCCESS('\nSuccessfully Downloaded refseq fasta file to ' +
                                                 download_dir_ + '\n'))
        else:
            print("File already exists at " + downloaded_fasta_url)
            base = os.path.basename(self.refseq_fasta_file_gz)
            downloaded_fasta_url_unzipped = download_dir_ + os.path.splitext(base)[0]
            print(downloaded_fasta_url_unzipped)
            if not os.path.exists(downloaded_fasta_url_unzipped):
                fasta_status = os.system('gunzip ' + downloaded_fasta_url)
                if fasta_status == 0:
                    raise ValueError("Unzipped fasta file not found ")

            if os.path.exists(downloaded_gff_url_unzipped) and os.path.exists(downloaded_fasta_url_unzipped):
                # filter_region ='NC_000011.10' # chr11
                # filter_feature_gene = 'OR8K1'
                # filter_feature_transcript = 'NM_001002907.1'

                #                 filter_region = 'NC_000010.11'  # chr10
                #                 filter_feature_gene = 'IL2RA'
                #                 filter_feature_transcript = 'NM_000417.2'
                # TNNAI3
                filter_region = 'NC_000019.10'  # chr19
                filter_feature_gene = 'TNNI3'
                filter_feature_transcript = 'NM_000363.4'
                try:
                    GFFHandler.parse_gff_with_genbank(downloaded_gff_url_unzipped, downloaded_fasta_url_unzipped, protein_sequence_file_url_unzipped, filter_region,
                                         filter_feature_gene, filter_feature_transcript)
                except:
                    print("Unexpected error:", sys.exc_info()[0])
                    raise
