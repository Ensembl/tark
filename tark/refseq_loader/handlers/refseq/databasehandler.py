'''
Copyright [1999-2015] Wellcome Trust Sanger Institute and the EMBL-European Bioinformatics Institute
Copyright [2016-2019] EMBL-European Bioinformatics Institute

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
from datetime import datetime
import mysql.connector.pooling as pooling_connector
from refseq_loader.handlers.refseq.confighandler import ConfigHandler
from refseq_loader.handlers.refseq.checksumhandler import ChecksumHandler
import collections


# Singleton
class DatabaseHandler(object):

    # Here the instance will be stored
    __instance = None

    @staticmethod
    def getInstance():
        """static access method"""
        if DatabaseHandler.__instance is None:
            DatabaseHandler()
        return DatabaseHandler.__instance

    def __init__(self, ini_file=None):
        if DatabaseHandler.__instance is not None:
            raise Exception("This class is a singleton")

        dbconfig = {
            "user": "prem",
            "password": "prem",
            "host": "localhost",
            "database": "tark_refseq_2019"
        }
        self.cnxpool = pooling_connector.MySQLConnectionPool(pool_name="mypool",
                                                             **dbconfig)
#         self.cnx = self.cnxpool.get_connection()
#         self.cur = self.cnx.cursor()
        DatabaseHandler.__instance = self

    def execute_set_statements(self, set_statement):
        # print(set_statement)
        try:
            self.cnx = self.cnxpool.get_connection()
            self.cur = self.cnx.cursor()
            status = self.cur.execute(set_statement)
            self.cnx.commit()
            self.cnx.close()
            self.cur.close()
        except Exception as e:
            print('Failed to insert: ' + str(e))
            exit(0)
        return status

    def insert_data(self, insert_sql, insert_data, FOREIGN_KEY_CHECKS=1):
        # print(insert_sql)
        # print(insert_data)

        checksum_keys = [key for key in list(insert_data.keys()) if "checksum" in key and insert_data[key] is None]

        for key in checksum_keys:
            if key in insert_sql:
                sql_str = "X%(" + key + ")s"
                sql_str_to_replace = "%(" + key + ")s"
                insert_sql = insert_sql.replace(sql_str, sql_str_to_replace, 1)

        row_id = None
        try:
            self.cnx = self.cnxpool.get_connection()
            self.cur = self.cnx.cursor()
            if FOREIGN_KEY_CHECKS == 0:
                self.cur.execute("SET FOREIGN_KEY_CHECKS=0")

            self.cur.execute(insert_sql, insert_data)
            self.cnx.commit()
            row_id = self.cur.lastrowid

            if FOREIGN_KEY_CHECKS == 0:
                self.cur.execute("SET FOREIGN_KEY_CHECKS=1")

            self.cnx.close()
            self.cur.close()
        except Exception as e:
            print('Failed to insert: ' + str(e))
            exit(0)
        # print("Returning row_id " + str(row_id))
        return row_id

    def save_features_to_database(self,  features, parent_ids):
        # print("****************FINAL OBJECT TO SAVE******************")
        # print(features)
        # print("*******************************************************")
        session_id_ = parent_ids["session_id"]
        assembly_id_ = parent_ids["assembly_id"]
        release_id_ = parent_ids["release_id"]

        feature_handler = FeatureHandler(session_id=session_id_, assembly_id=assembly_id_, release_id=release_id_)
        transcript_gene = feature_handler.add_features(features)
        print(transcript_gene)
        return transcript_gene

    @classmethod
    def populate_parent_tables(cls, init_table_list=None):

        if init_table_list is None:
            init_table_list = ["session", "genome", "assembly", "assembly_alias", "release_source"]

        session_id = None
        genome_id = None
        assembly_id = None

        parent_ids = {}
        if "session" in init_table_list:
            session_id = SessionHandler.start_session("Test Client")
            parent_ids['session_id'] = session_id
            print(".........Popultating SESSION table.........\n")

        if "genome" in init_table_list:
            genome_data = {"name": "homo_sapiens", "tax_id": str(9606), "session_id": str(session_id)}
            genome_id = GenomeHandler.load_genome(genome_data)
            parent_ids['genome_id'] = genome_id
            print(".........Popultating GENOME table.........\n")

        if "assembly" in init_table_list:
            assembly_data = {"genome_id": str(genome_id), "assembly_name": "GRCh38", "session_id": str(session_id)}
            assembly_id = AssemblyHandler.load_assembly(assembly_data)
            parent_ids['assembly_id'] = assembly_id
            print(".........Popultating ASSEMBLY table.........\n")

        if "assembly_alias" in init_table_list:
            assembly_alias_data = {"alias": "GCA_000001405.25", "genome_id": str(genome_id),
                                   "assembly_id": str(assembly_id), "session_id": str(session_id)}
            assembly_alias_id = AssemblyHandler.load_assembly_alias(assembly_alias_data)
            parent_ids['assembly_alias_id'] = assembly_alias_id
            print(".........Popultating ASSEMBLY ALIAS table.........\n")

        if "release_source" in init_table_list:
            release_source = {"shortname": "Ensembl", "description": "Ensembl data imports from Human Core DBs"}
            release_source_ensembl = ReleaseSourceHandler.load_release_source(release_source)
            parent_ids['release_source_ensembl'] = release_source_ensembl
            print(".........Popultating RELEASE SOURCE table.........\n")

            release_source = {"shortname": "RefSeq", "description": "RefSeq data imports from RefSeq GFF"}
            release_source_refseq = ReleaseSourceHandler.load_release_source(release_source)
            parent_ids['release_source_refseq'] = release_source_refseq
            print(".........Popultating REFSEQ table.........\n")

        # load data_release_set
        today = datetime.now().date()
        default_config = ConfigHandler().get_section_config()
        data_release_set = collections.OrderedDict()
        data_release_set["shortname"] = default_config["shortname"]
        data_release_set["description"] = default_config["description"]
        data_release_set["assembly_id"] = str(assembly_id)
        data_release_set["release_date"] = str(today)
        data_release_set["session_id"] = str(session_id)
        data_release_set["source_id"] = str(release_source_refseq)
        release_set_id = ReleaseHandler.load_release_set(assembly_id, session_id, data_release_set)
        parent_ids['release_id'] = release_set_id

        return parent_ids


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
        session_id = DatabaseHandler.getInstance().insert_data(insert_session, data_session)
        return session_id


class ReleaseHandler(object):

    @classmethod
    def load_release_set(cls, assembly_id, session_id, data_release_set=None):
        if data_release_set is None:
            today = datetime.now().date()
            default_config = ConfigHandler().get_section_config()
            data_release_set = collections.OrderedDict()
            data_release_set["shortname"] = default_config["shortname"]
            data_release_set["description"] = default_config["description"]
            data_release_set["assembly_id"] = str(assembly_id)
            data_release_set["release_date"] = str(today)
            data_release_set["session_id"] = str(session_id)
            data_release_set["source_id"] = default_config["source"]

        release_set_checksum = ChecksumHandler.checksum_list(list(data_release_set.values()))
        data_release_set["release_checksum"] = release_set_checksum
        # data_release_set["release_checksum"] = None
        # print(data_release_set)
        # Insert release set
        insert_release_set = ("INSERT INTO release_set (shortname, description, assembly_id, release_date, session_id, \
                                release_checksum, source_id) VALUES \
                                (%(shortname)s,  %(description)s, %(assembly_id)s, %(release_date)s,  %(session_id)s, \
                                X%(release_checksum)s, %(source_id)s)\
                                ON DUPLICATE KEY UPDATE release_id=LAST_INSERT_ID(release_id)")

        release_id = DatabaseHandler.getInstance().insert_data(insert_release_set, data_release_set)
        return release_id


class ReleaseSourceHandler(object):

    @classmethod
    def load_release_source(cls, release_source):
        insert_release_source = ("INSERT INTO release_source (shortname, description) VALUES \
                        (%(shortname)s, %(description)s)\
                        ON DUPLICATE KEY UPDATE source_id=LAST_INSERT_ID(source_id)")
        release_source_id = DatabaseHandler.getInstance().insert_data(insert_release_source, release_source)
        return release_source_id


class GenomeHandler(object):

    @classmethod
    def load_genome(cls, genome):

        insert_genome = ("INSERT INTO genome (name, tax_id, session_id) VALUES \
                        (%(name)s, %(tax_id)s, %(session_id)s)\
                        ON DUPLICATE KEY UPDATE genome_id=LAST_INSERT_ID(genome_id)")
        genome_id = DatabaseHandler.getInstance().insert_data(insert_genome, genome)

        return genome_id


class AssemblyHandler(object):

    @classmethod
    def load_assembly(cls, assembly):

        insert_assembly = ("INSERT INTO assembly (genome_id, assembly_name, session_id) VALUES \
                        (%(genome_id)s, %(assembly_name)s, %(session_id)s)\
                        ON DUPLICATE KEY UPDATE assembly_id=LAST_INSERT_ID(assembly_id)")
        assembly_id = DatabaseHandler.getInstance().insert_data(insert_assembly, assembly)

        return assembly_id

    @classmethod
    def load_assembly_alias(cls, assembly_alias):

        insert_assembly_alias = ("INSERT INTO assembly_alias (genome_id, assembly_id, alias, session_id) VALUES\
                                (%(genome_id)s, %(assembly_id)s, %(alias)s, %(session_id)s)\
                                ON DUPLICATE KEY UPDATE assembly_id=LAST_INSERT_ID(assembly_id)")
        assembly_alias_id = DatabaseHandler.getInstance().insert_data(insert_assembly_alias, assembly_alias)

        return assembly_alias_id


class FeatureHandler(object):

    def __init__(self, session_id=0, assembly_id=0, release_id=0):
        self._session_id = session_id
        self._assembly_id = assembly_id
        self._release_id = release_id

    @property
    def session_id(self):
        return self._session_id

    @session_id.setter
    def session_id(self, session_id):
        self._session_id = session_id

    @property
    def assembly_id(self):
        return self._assembly_id

    @assembly_id.setter
    def assembly_id(self, assembly_id):
        self._assembly_id = assembly_id

    @property
    def release_id(self):
        return self._release_id

    @release_id.setter
    def release_id(self, release_id):
        self._release_id = release_id

    def add_features(self, features):

        gene_id = None
        gene_feature = None
        if "gene" in features:
            gene_feature = features["gene"]
            if "transcripts" in gene_feature and len(gene_feature["transcripts"]) > 0:
                gene_id = self.add_gene(gene_feature)
            else:
                return None

        transcript_gene_ids_list = []
        if "transcripts" in gene_feature and gene_id:
            transcript_gene_ids = self.add_transcripts(gene_feature["transcripts"], gene_id)
            transcript_gene_ids_list.append(transcript_gene_ids)

        return transcript_gene_ids_list

    def add_gene(self, gene):
        gene_data = {k: v for (k, v) in gene.items() if k not in ["transcripts"]}
        gene_data["session_id"] = self.session_id
        gene_data["assembly_id"] = self.assembly_id

        insert_gene = ("INSERT INTO gene (stable_id, stable_id_version, assembly_id, \
                        loc_region, loc_start, loc_end, loc_strand, loc_checksum, \
                        hgnc_id, gene_checksum, session_id) \
                        VALUES (\
                        %(stable_id)s, %(stable_id_version)s,  %(assembly_id)s, \
                        %(loc_region)s, %(loc_start)s,  %(loc_end)s,  %(loc_strand)s,  X%(loc_checksum)s, \
                        %(hgnc_id)s,  X%(gene_checksum)s,  %(session_id)s) \
                        ON DUPLICATE KEY UPDATE gene_id=LAST_INSERT_ID(gene_id)")

        gene_id = DatabaseHandler.getInstance().insert_data(insert_gene, gene_data, FOREIGN_KEY_CHECKS=0)

        self.add_release_tag(feature_id=gene_id, feature_type="gene")
        return gene_id

    def add_transcripts(self, transcripts, gene_id):

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

        transcript_ids = []
        for transcript in transcripts:
            transcript_data = {k: v for (k, v) in transcript.items() if k not in ["exons", "translation"]}
            transcript_data["session_id"] = self.session_id
            transcript_data["assembly_id"] = self.assembly_id

            sequence_data = {"sequence": transcript_data["sequence"],
                             "seq_checksum": transcript_data["seq_checksum"],
                             }
            seq_id = self.add_sequence(sequence_data)
            # print("Seq id " + str(seq_id))
            transcript_id = DatabaseHandler.getInstance().insert_data(insert_transcript, transcript_data)

            self.add_release_tag(feature_id=transcript_id, feature_type="transcript")
            exon_transcript_ids = self.add_exons(transcript["exons"], transcript_id)  # @UnusedVariable

            if transcript["translation"]:
                translation_id = self.add_translation(transcript["translation"], transcript_id)
                self.add_release_tag(feature_id=translation_id, feature_type="translation")
                translation_transcript_id = self.add_translation_transcript(translation_id,  # @UnusedVariable
                                                                            transcript_id)
            transcript_ids.append(transcript_id)

        transcript_gene_ids = self.add_transcript_gene(transcript_ids, gene_id)
        return transcript_gene_ids

    def add_exons(self, exons, transcript_id):
        insert_exon = ("INSERT INTO exon (stable_id, stable_id_version, assembly_id,\
                        loc_region, loc_start, loc_end, loc_strand, loc_checksum,\
                        exon_checksum, seq_checksum, session_id)\
                        VALUES (%(stable_id)s, %(stable_id_version)s, %(assembly_id)s,\
                        %(loc_region)s, %(loc_start)s, %(loc_end)s, %(loc_strand)s, X%(loc_checksum)s,\
                        X%(exon_checksum)s, X%(seq_checksum)s, %(session_id)s)\
                        ON DUPLICATE KEY UPDATE exon_id=LAST_INSERT_ID(exon_id)")
        exon_ids = []
        for exon in exons:
            exon["session_id"] = self.session_id
            exon["assembly_id"] = self.assembly_id

            sequence_data = {"sequence": exon["exon_seq"],
                             "seq_checksum": exon["seq_checksum"],
                             }
            seq_id = self.add_sequence(sequence_data)
            # print("Seq id " + str(seq_id))
            exon_id = DatabaseHandler.getInstance().insert_data(insert_exon, exon)
            self.add_release_tag(feature_id=exon_id, feature_type="exon")
            exon_ids.append(exon_id)

        exon_transcript_ids = self.add_exon_transcript(exon_ids, transcript_id)
        return exon_transcript_ids

    def add_translation(self, translation, transcript_idd):
        translation["session_id"] = self.session_id
        translation["assembly_id"] = self.assembly_id

        insert_translation = ("INSERT INTO translation (stable_id, stable_id_version, assembly_id,\
                                loc_region, loc_start, loc_end, loc_strand, loc_checksum,\
                                translation_checksum, seq_checksum, session_id)\
                                VALUES\
                                (%(stable_id)s, %(stable_id_version)s, %(assembly_id)s,\
                                %(loc_region)s, %(loc_start)s, %(loc_end)s, %(loc_strand)s, X%(loc_checksum)s,\
                                X%(translation_checksum)s, X%(seq_checksum)s, %(session_id)s)\
                                ON DUPLICATE KEY UPDATE translation_id=LAST_INSERT_ID(translation_id)")

        sequence_data = {"sequence": translation["translation_seq"],
                         "seq_checksum": translation["seq_checksum"],
                         }
        seq_id = self.add_sequence(sequence_data)
        # print("Seq id " + str(seq_id))
        translation_id = DatabaseHandler.getInstance().insert_data(insert_translation, translation)
        return translation_id

    def add_translation_transcript(self, translation_id, transcript_id):
        insert_translation = ("INSERT INTO translation_transcript (transcript_id, translation_id, session_id)\
                                VALUES\
                                (%(transcript_id)s, %(translation_id)s, %(session_id)s)\
                                ON DUPLICATE KEY UPDATE\
                                transcript_translation_id=LAST_INSERT_ID(transcript_translation_id)")
        translation_transcript_data = {"transcript_id": transcript_id, "translation_id": translation_id,
                                       "session_id": self.session_id}
        translation_transcript_id = DatabaseHandler.getInstance().insert_data(insert_translation, translation_transcript_data)
        return translation_transcript_id

    def add_transcript_gene(self, transcript_ids, gene_id):
        insert_transcript_gene = ("INSERT INTO transcript_gene (gene_id, transcript_id, session_id) \
                                    VALUES (\
                                    %(gene_id)s, %(transcript_id)s, %(session_id)s) \
                                    ON DUPLICATE KEY UPDATE \
                                    gene_transcript_id=LAST_INSERT_ID(gene_transcript_id)")
        transcript_gene_ids_list = []
        for transcript_id in transcript_ids:
            transcript_gene_data = {"gene_id": gene_id, "transcript_id": transcript_id, "session_id": self.session_id}
            DatabaseHandler.getInstance().insert_data(insert_transcript_gene, transcript_gene_data)
            transcript_gene_ids = {"transcript_id": transcript_id, "gene_id": gene_id}
            transcript_gene_ids_list.append(transcript_gene_ids)

        return transcript_gene_ids_list

    def add_release_tag(self, feature_id, feature_type):
        session_id = self.session_id
        release_id = self.release_id

        release_tag = {"feature_id": feature_id, "release_id": release_id, "session_id": session_id}
        insert_release_tag = ("INSERT IGNORE INTO " + feature_type+"_release_tag (feature_id, release_id, session_id) \
                                VALUES \
                                (%(feature_id)s,  %(release_id)s, %(session_id)s )")
        feature_release_tag_id = DatabaseHandler.getInstance().insert_data(insert_release_tag, release_tag)  # @UnusedVariable

    def add_exon_transcript(self, exon_ids, transcript_id):
        insert_exon_transcript = ("INSERT INTO exon_transcript (transcript_id, exon_id, exon_order, session_id)\
                                    VALUES (%(transcript_id)s, %(exon_id)s, %(exon_order)s, %(session_id)s)\
                                    ON DUPLICATE KEY UPDATE exon_transcript_id=LAST_INSERT_ID(exon_transcript_id)")
        exon_order = 1
        for exon_id in exon_ids:
            exon_transcript_data = {"transcript_id": transcript_id, "exon_id": exon_id, "exon_order": exon_order,
                                    "session_id": self.session_id}
            exon_transcript_id = DatabaseHandler.getInstance().insert_data(insert_exon_transcript,  # @UnusedVariable
                                                               exon_transcript_data)
            exon_order = exon_order + 1

    def add_sequence(self, sequence_data):
        sequence_data["session_id"] = self.session_id
        insert_sequence = ("INSERT IGNORE INTO sequence (seq_checksum, sequence, session_id) \
                            VALUES (X%(seq_checksum)s, %(sequence)s, %(session_id)s)")
        seq_id = DatabaseHandler.getInstance().insert_data(insert_sequence, sequence_data)
        return seq_id
