import json
import argparse

from mysql.connector import connect, Error

import tark.settings.secrets


def populate_manelist_file(args):
    try:
        with connect(
                host=args.host,
                user=args.user,
                db=args.db,
                password=args.password,
                port=args.port) as connection:
            with connection.cursor(dictionary=True) as cursor:
                sqlquery = """
                SELECT DISTINCT gn1.name                                             as gene,
                relationship_type.shortname                                          as mane,
                concat(t1.stable_id, '.', t1.stable_id_version)                      as ens_stable_id,
                concat(t2.stable_id, '.', t2.stable_id_version)                      as refseq_stable_id,
                concat(t3.stable_id, '.', t3.stable_id_version)                      as grch37_stable_id,
                IF(t3.five_prime_utr_checksum = t1.five_prime_utr_checksum AND t3.five_prime_utr_checksum IS NOT NULL
                       AND t1.five_prime_utr_checksum IS NOT NULL, 'True', 'False')  as five_prime_utr,
                'True'                                                               as cds,
                IF(t3.three_prime_utr_checksum = t1.three_prime_utr_checksum AND t3.three_prime_utr_checksum IS NOT NULL
                       AND t1.three_prime_utr_checksum IS NOT NULL, 'True', 'False') as three_prime_utr
                FROM transcript t1
                         JOIN transcript_release_tag trt1 ON t1.transcript_id = trt1.feature_id
                         JOIN transcript_release_tag_relationship ON
                        trt1.transcript_release_id = transcript_release_tag_relationship.transcript_release_object_id
                         JOIN transcript_release_tag trt2 ON
                        transcript_release_tag_relationship.transcript_release_subject_id = trt2.transcript_release_id
                         JOIN transcript t2 ON trt2.feature_id = t2.transcript_id
                         JOIN relationship_type ON
                        transcript_release_tag_relationship.relationship_type_id = relationship_type.relationship_type_id
                         JOIN transcript_gene tg1 ON
                    t1.transcript_id = tg1.transcript_id
                         JOIN gene gene1 ON
                    tg1.gene_id = gene1.gene_id
                         JOIN gene_names gn1 ON
                    gene1.name_id = gn1.external_id and gn1.primary_id = 1
                         JOIN transcript t3 ON t3.stable_id = t1.stable_id
                    AND t3.assembly_id = 1
                         JOIN translation_transcript tt1 ON tt1.transcript_id = t1.transcript_id
                         JOIN translation tl1 ON tl1.translation_id = tt1.translation_id
                         JOIN translation_transcript tt3 ON tt3.transcript_id = t3.transcript_id
                         JOIN translation tl3 ON tl3.translation_id = tt3.translation_id
                WHERE t1.assembly_id = 1001
                  and tl3.seq_checksum = tl1.seq_checksum
                ORDER BY gn1.name
                """
                cursor.execute(sqlquery)
                result = cursor.fetchall()
    except Error as e:
        print(e)

    with open(args.output_file, 'w') as out_handle:
        json.dump(result, out_handle)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Load data comparing MANE GRCh37 and GRCh38.")
    arg_parser.add_argument("--output_file",
                            help="The location where this script will output a list of comparison data",
                            default='./tark/static/apache/txt/mane_grch37.txt')
    arg_parser.add_argument("--host", default=tark.settings.secrets.DATABASE_HOST)
    arg_parser.add_argument("--user", default=tark.settings.secrets.DATABASE_USER)
    arg_parser.add_argument("--db", default=tark.settings.secrets.DATABASE_NAME)
    arg_parser.add_argument("--password", default=tark.settings.secrets.DATABASE_PASSWORD)
    arg_parser.add_argument("--port", default=tark.settings.secrets.DATABASE_PORT)
    cli_args = arg_parser.parse_args()
    populate_manelist_file(cli_args)
