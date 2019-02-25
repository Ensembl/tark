from django.core.management.base import BaseCommand
import os


import sys
import logging
from refseq_loader.handlers.refseq.gffhandler import GFFHandler
from refseq_loader.handlers.refseq.confighandler import ConfigHandler
from refseq_loader.handlers.refseq.downloadhandler import DownloadHandler
from cProfile import Profile


# Get an instance of a logger
logger = logging.getLogger(__name__)

# How to run
#  ./manage.py load_refseq --settings=tark.settings.local --download_dir=refseq_files_release_92


class Command(BaseCommand):
    help = 'Load refseq data from GBFF and GFF3 files'
    ini_file = os.path.abspath(os.path.dirname(__file__)) + "/refseq_source.ini"
    config_handler = ConfigHandler(ini_file)
    logger.info(config_handler)
    default_config = config_handler.get_section_config(section_name="DEFAULT")
    logger.info(default_config)

    refseq_ftp_root = default_config.get("refseq_ftp_root")
    refseq_gff_file_gz = default_config.get("refseq_gff_file_gz")
    refseq_fasta_file_gz = default_config.get("refseq_fasta_file_gz")
    refseq_protein_file_gz = default_config.get("refseq_protein_file_gz")
    refseq_genbank_file_gz = default_config.get("refseq_genbank_file")

    logger.info("refseq_ftp_root " + refseq_ftp_root)
    logger.info("refseq_gff_file_gz " + refseq_gff_file_gz)
    logger.info("refseq_fasta_file_gz " + refseq_fasta_file_gz)
    logger.info("refseq_protein_file_gz " + refseq_protein_file_gz)
    logger.info("refseq_genbank_file_gz " + refseq_genbank_file_gz)

    database_config = config_handler.get_section_config(section_name="DATABASE")
    logger.info(database_config)

    db_host = database_config.get("host")
    db_port = database_config.get("port")
    db_user = database_config.get("user")
    db_pass = database_config.get("pass")
    db_name = database_config.get("database")

    logger.info("db_host " + db_host)
    logger.info("db_port  " + db_port)
    logger.info("db_user  " + db_user)
    logger.info("db_pass " + db_pass)
    logger.info("db_name " + db_name)

    def add_arguments(self, parser):
        parser.add_argument('--download_dir',  help='Download Dir')
        parser.add_argument('--profile',  help='Show cProfile information', default=False)

    def handle(self, *args, **options):
        if options.get('profile', False):
            profiler = Profile()
            profiler.runcall(self._handle, *args, **options)
            profiler.print_stats()
        else:
            self._handle(*args, **options)

    def _handle(self, *args, **options):
        logger.info(args)
        logger.info(options)

        download_dir_ = options['download_dir']

        download_dir_ = download_dir_ + "/" if download_dir_ else "tmp_refseq/"

        logger.info('download_dir ' + download_dir_)

        if not os.path.exists(download_dir_):
            logger.warn("path doesn't exists. Creating dir at " + download_dir_)
            os.makedirs(download_dir_)

        files_names = [self.refseq_gff_file_gz, self.refseq_fasta_file_gz, self.refseq_protein_file_gz,
                       self.refseq_genbank_file_gz]
        downloaded_files = DownloadHandler.download_files(files_names, self.refseq_ftp_root, download_dir_)
        logger.info(downloaded_files)

        if len(downloaded_files) == 4:
                try:
                    GFFHandler.parse_gff_with_genbank(downloaded_files)
                    logger.info("************ALL DONE********************")
                except:
                    logger.warn("Unexpected error:", sys.exc_info()[0])
                    raise
