'''
Copyright [1999-2015] Wellcome Trust Sanger Institute and the EMBL-European Bioinformatics Institute
Copyright [2016-2018] EMBL-European Bioinformatics Institute

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

from __future__ import print_function
from datetime import date, datetime, timedelta
import mysql.connector.pooling as pooling_connector
from refseq_loader.handlers.refseq.confighandler import ConfigHandler
from refseq_loader.handlers.refseq.checksumhandler import ChecksumHandler
from pip._vendor.requests.sessions import session
from numpy import insert
import collections


class DatabaseHandler(object):

    def __init__(self, ini_file=None):
        dbconfig = {
            "user": "prem",
            "password": "prem",
            "host": "localhost",
            "database": "test_tark_refseq_new"
        }
        self.cnxpool = pooling_connector.MySQLConnectionPool(pool_name="mypool",
                                                             **dbconfig)

    def get_connection(self):
        return self.cnxpool.get_connection()

    def get_cursor(self):
        return self.cnxpool.get_connection().cursor()

    def insert_data(self, insert_sql, insert_data):
        print(insert_sql)
        print(insert_data)
        row_id = None
        try:
            con = self.get_connection()
            cur = con.cursor()
            cur.execute(insert_sql, insert_data)
            con.commit()
            con.close()
            cur.close()
            row_id = cur.lastrowid
        except Exception as e:
            print('Failed to insert: ' + str(e))
            exit(0)

        return row_id


    @classmethod
    def save_features_to_database(cls,  annotated_gene):
        print("****************FINAL OBJECT TO SAVE******************")
        print(annotated_gene)
        print("*******************************************************")

class SessionHandler(object):

    @classmethod
    def start_session(cls, session_name="Test session"):
        today = datetime.now().date()
        insert_session = ("INSERT INTO session (client_id, start_date, status) VALUES (%(client_id)s, \
                            %(start_date)s, %(status)s)")

        # Insert session information
        data_session = {
                'client_id': session_name,
                'status': 1,
                'start_date': today
                }

        # Insert new session
        session_id = DatabaseHandler().insert_data(insert_session, data_session)
        return session_id


class ReleaseHandler(object):

    @classmethod
    def load_release_set(cls, session_id, data_release_set=None):
        if data_release_set is None:
            today = datetime.now().date()
            default_config = ConfigHandler().get_section_config()
            data_release_set = collections.OrderedDict()
            data_release_set["shortname"] = default_config["shortname"]
            data_release_set["description"] = default_config["description"]
            data_release_set["assembly_id"] = default_config["assembly_id"]
            data_release_set["release_date"] = str(today)
            data_release_set["session_id"] = str(session_id)
            data_release_set["source_id"] = default_config["source"]

        print(list(data_release_set.values()))
        release_set_checksum = ChecksumHandler.checksum_list(list(data_release_set.values()))
        data_release_set["release_checksum"] = release_set_checksum
        #data_release_set["release_checksum"] = None
        print(data_release_set)
        # Insert release set
        insert_release_set = ("INSERT INTO release_set (shortname, description, assembly_id, release_date, session_id, \
                                release_checksum, source_id) VALUES \
                                (%(shortname)s,  %(description)s, %(assembly_id)s, %(release_date)s,  %(session_id)s, \
                                X%(release_checksum)s, %(source_id)s)")

        release_id = DatabaseHandler().insert_data(insert_release_set, data_release_set)
        return release_id


class ReleaseSourceHandler(object):

    @classmethod
    def load_release_source(cls, release_source):
        insert_release_source = ("INSERT INTO release_source (shortname, description) VALUES \
                        (%(shortname)s, %(description)s)")
        release_source_id = DatabaseHandler().insert_data(insert_release_source, release_source)
        return release_source_id


class GenomeHandler(object):

    @classmethod
    def load_genome(cls, genome):

        insert_genome = ("INSERT INTO genome (name, tax_id, session_id) VALUES \
                        (%(name)s, %(tax_id)s, %(session_id)s)\
                        ON DUPLICATE KEY UPDATE genome_id=LAST_INSERT_ID(genome_id)")
        genome_id = DatabaseHandler().insert_data(insert_genome, genome)

        return genome_id


class AssemblyHandler(object):

    @classmethod
    def load_assembly(cls, assembly):

        insert_assembly = ("INSERT INTO assembly (genome_id, assembly_name, session_id) VALUES \
                        (%(genome_id)s, %(assembly_name)s, %(session_id)s)\
                        ON DUPLICATE KEY UPDATE assembly_id=LAST_INSERT_ID(assembly_id)")
        assembly_id = DatabaseHandler().insert_data(insert_assembly, assembly)

        return assembly_id

    @classmethod
    def load_assembly_alias(cls, assembly_alias):

        insert_assembly_alias = ("INSERT INTO assembly_alias (genome_id, assembly_id, alias, session_id) VALUES\
                                (%(genome_id)s, %(assembly_id)s, %(alias)s, %(session_id)s)\
                                ON DUPLICATE KEY UPDATE assembly_id=LAST_INSERT_ID(assembly_id)")
        assembly_alias_id = DatabaseHandler().insert_data(insert_assembly_alias, assembly_alias)

        return assembly_alias_id


class FeatureHandler(object):

    @classmethod
    def add_features(cls, features):
        gene_feature = features["gene"]
        cls.add_gene(gene_feature)
        pass

    @classmethod
    def add_gene(cls, gene, session_id):
        gene_data = {k: v for (k, v) in gene.items() if k not in ["transcripts"]}
        gene_data["session_id"] = session_id

        insert_gene = ("INSERT INTO gene (stable_id, stable_id_version, assembly_id, \
                        loc_region, loc_start, loc_end, loc_strand, loc_checksum, \
                        hgnc_id, gene_checksum, session_id) \
                        VALUES (\
                        %(stable_id)s, %(stable_id_version)s,  %(assembly_id)s, \
                        %(loc_region)s, %(loc_start)s,  %(loc_end)s,  %(loc_strand)s,  X%(loc_checksum)s, \
                        %(hgnc_id)s,  X%(gene_checksum)s,  %(session_id)s) \
                        ON DUPLICATE KEY UPDATE gene_id=LAST_INSERT_ID(gene_id)")
        gene_id = DatabaseHandler().insert_data(insert_gene, gene_data)
        return gene_id

    @classmethod
    def add_transcripts(cls, transcripts, gene_id, session_id):

        insert_transcript = ("INSERT INTO transcript (stable_id, stable_id_version, assembly_id, \
                            loc_region, loc_start, loc_end, loc_strand, loc_checksum, \
                            transcript_checksum, \
                            exon_set_checksum, seq_checksum, session_id) \
                            VALUES (\
                            %(stable_id)s, %(stable_id_version)s, %(assembly_id)s, \
                            %(loc_region)s, %(loc_start)s, %(loc_end)s, %(loc_strand)s, X%(loc_checksum)s, \
                            X%(transcript_checksum)s, \
                            X%(exon_set_checksum)s, X%(seq_checksum)s, %(session_id)s) \
                            ON DUPLICATE KEY UPDATE transcript_id=LAST_INSERT_ID(transcript_id)")

        loaded_transcript_list = []
        for transcript in transcripts:
            transcript_data = {k: v for (k, v) in transcript.items() if k not in ["exons", "translation"]}
            transcript_data["session_id"] = session_id

            transcript_sequence = transcript_data["sequence"]
            print(transcript_data)
            sequence_data = {"sequence": transcript_data["sequence"], \
                             "seq_checksum": transcript_data["seq_checksum"],
                             }
            seq_id = cls.add_sequence(sequence_data, session_id)
            print("Seq id " + str(seq_id))
            transcript_id = DatabaseHandler().insert_data(insert_transcript, transcript_data)
            loaded_transcript_list.append(transcript_id)

        print(loaded_transcript_list)

    @classmethod
    def add_exons(cls, exon_data):
        # $sth = $dbh->prepare("INSERT INTO exon (stable_id, stable_id_version, assembly_id, loc_region, loc_start, loc_end, loc_strand, loc_checksum, exon_checksum, seq_checksum, session_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ON DUPLICATE KEY UPDATE exon_id=LAST_INSERT_ID(exon_id)");
        pass

    @classmethod
    def add_translation(cls, translation):
        #     $sth = $dbh->prepare("INSERT INTO translation (stable_id, stable_id_version, assembly_id, loc_region, loc_start, loc_end, loc_strand, loc_checksum, translation_checksum, seq_checksum, session_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ON DUPLICATE KEY UPDATE translation_id=LAST_INSERT_ID(translation_id)");
        pass

    @classmethod
    def add_transcript_gene(cls, transcript_gene):
        #     $sth = $dbh->prepare("INSERT INTO transcript_gene (gene_id, transcript_id, session_id) VALUES (?, ?, ?) ON DUPLICATE KEY UPDATE gene_transcript_id=LAST_INSERT_ID(gene_transcript_id)");
        pass

    @classmethod
    def add_exon_transcript(cls, exon_transcript):
        #$sth = $dbh->prepare("INSERT INTO exon_transcript (transcript_id, exon_id, exon_order, session_id) VALUES (?, ?, ?, ?) ON DUPLICATE KEY UPDATE exon_transcript_id=LAST_INSERT_ID(exon_transcript_id)");
        pass

    @classmethod
    def add_translation_transcript(cls, translation_transcript):
        #     $sth = $dbh->prepare("INSERT INTO translation_transcript (transcript_id, translation_id, session_id) VALUES (?, ?, ?) ON DUPLICATE KEY UPDATE transcript_translation_id=LAST_INSERT_ID(transcript_translation_id)");
        pass

    @classmethod
    def add_sequence(cls, sequence_data, session_id):
        # $sth = $dbh->prepare("INSERT IGNORE INTO sequence (seq_checksum, sequence, session_id) VALUES (?, ?, ?)");
        sequence_data["session_id"] = session_id
        insert_sequence = ("INSERT IGNORE INTO sequence (seq_checksum, sequence, session_id) \
                            VALUES (X%(seq_checksum)s, %(sequence)s, %(session_id)s)")
        seq_id = DatabaseHandler().insert_data(insert_sequence, sequence_data)
        
        print(seq_id)
        return seq_id



