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

from BCBio import GFF
from refseq_loader.handlers.refseq.fastahandler import FastaHandler
from refseq_loader.handlers.refseq.annotationhandler import AnnotationHandler
from refseq_loader.handlers.refseq.databasehandler import DatabaseHandler
from refseq_loader.handlers.refseq.genbankhandler import GenBankHandler
from refseq_loader.handlers.refseq.checksumhandler import ChecksumHandler
import sys
import traceback
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class GFFHandler(AnnotationHandler):

    @classmethod
    def parse_gff_with_genbank(cls, downloaded_files, filter_region=None, filter_feature_gene=None, filter_feature_transcript=None, dryrun=False):  # @IgnorePep8
        """
        Builds the gene model from GFF file and uses the genbank to fetch the sequence
        Use the filters while testing the loader
        """
        # Try to populate this hash
        # stats_counter = {}

        gff_file = downloaded_files["gff"]
        protein_sequence_file = downloaded_files["protein"]
        genbank_file = downloaded_files["gbff"]

        logger.info(" GFF file from parse_gff " + gff_file)
        logger.info(" Protein file from parse_gff " + protein_sequence_file)
        logger.info(" Genbank file from parse_gff " + genbank_file)

        try:
            sequence_handler = GenBankHandler(genbank_file)
            protein_sequence_handler = FastaHandler(protein_sequence_file)
            # Examine for available regions
            examiner = GFF.GFFExaminer()

            # load the parent tables
            parent_ids = None
            if not dryrun:
                parent_ids = DatabaseHandler.getInstance().populate_parent_tables()
                # print(parent_ids)

            with open(gff_file) as gff_handle_examiner:
                possible_limits = examiner.available_limits(gff_handle_examiner)
                chromosomes = sorted(possible_limits["gff_id"].keys())

            limits = dict()

            for chrom_tuple in chromosomes:
                chrom = chrom_tuple[0]
                if not chrom.startswith("NC_"):
                    continue

                seq_region = cls.get_seq_region_from_refseq_accession(chrom)
                # Restrict only for filter_region
                if filter_region is not None:
                    if filter_region not in chrom:
                        continue

                with open(gff_file) as gff_handle:
                    limits["gff_id"] = chrom_tuple

                    # Chromosome seq level
                    for rec in GFF.parse(gff_handle, limit_info=limits):

                        for gene_feature in rec.features:

                            # skip regions
                            if gene_feature.type == "region":
                                continue

                            if filter_feature_gene is not None:
                                if not gene_feature.qualifiers['gene'][0] == filter_feature_gene:
                                    continue

                            annotated_gene = cls.get_annotated_gene(seq_region, gene_feature)

                            # gene level
                            annotated_transcripts = []
                            for mRNA_feature in gene_feature.sub_features:

                                if 'transcript_id' in mRNA_feature.qualifiers:
                                    transcript_id = mRNA_feature.qualifiers['transcript_id'][0]
                                    # print("Has transcript id " + str(transcript_id))
                                else:
                                    continue

                                if filter_feature_transcript is not None and 'transcript_id' in mRNA_feature.qualifiers:
                                    if filter_feature_transcript not in mRNA_feature.qualifiers['transcript_id'][0]:
                                        continue

                                refseq_exon_list = []
                                refseq_exon_order = 1

                                refseq_cds_list = []
                                refseq_cds_order = 1
                                for mRNA_sub_feature in mRNA_feature.sub_features:
                                    refseq_exon_dict = {}
                                    if 'exon' in mRNA_sub_feature.type:
                                        # print("Transcript Has exons" + str(mRNA_sub_feature.id))
                                        refseq_exon_dict['exon_stable_id'] = str(mRNA_sub_feature.id)
                                        refseq_exon_dict['exon_stable_id_version'] = 1  # dummmy version
                                        refseq_exon_dict['exon_order'] = refseq_exon_order
                                        # note that we are shifting one base here
                                        refseq_exon_dict['exon_start'] = str(mRNA_sub_feature.location.start + 1)
                                        refseq_exon_dict['exon_end'] = str(mRNA_sub_feature.location.end)
                                        refseq_exon_dict['exon_strand'] = str(mRNA_sub_feature.location.strand)
                                        refseq_exon_list.append(refseq_exon_dict)
                                        refseq_exon_order += 1

                                    refseq_cds_dict = {}
                                    if 'CDS' in mRNA_sub_feature.type:

                                        refseq_cds_dict['cds_order'] = refseq_cds_order
                                        # note that we are shifting one base here
                                        refseq_cds_dict['cds_start'] = str(mRNA_sub_feature.location.start + 1)
                                        refseq_cds_dict['cds_end'] = str(mRNA_sub_feature.location.end)
                                        refseq_cds_dict['cds_strand'] = str(mRNA_sub_feature.location.strand)
                                        refseq_cds_dict['cds_id'] = str(mRNA_sub_feature.id)
                                        refseq_cds_dict['protein_id'] = str(mRNA_sub_feature.qualifiers['protein_id'][0])  # @IgnorePep8
                                        refseq_cds_list.append(refseq_cds_dict)
                                        refseq_cds_order += 1

                                annotated_transcript = cls.get_annotated_transcript(sequence_handler, seq_region,
                                                                                    mRNA_feature)

                                # add sequence and other annotations
                                annotated_exons = []
                                if len(refseq_exon_list) > 0:
                                    annotated_exons = cls.get_annotated_exons(sequence_handler, seq_region,
                                                                              transcript_id,
                                                                              refseq_exon_list)

                                    if annotated_exons is not None and len(annotated_exons) > 0:

                                        exon_set_checksum = ChecksumHandler.get_exon_set_checksum(annotated_exons)
                                        annotated_transcript['exon_set_checksum'] = exon_set_checksum
                                        annotated_transcript['exons'] = annotated_exons
                                    else:
                                        annotated_transcript['exons'] = []

                                annotated_translation = []
                                if len(refseq_cds_list) > 0:
                                    protein_id = refseq_cds_list[0]['protein_id']
                                    annotated_translation = cls.get_annotated_cds(protein_sequence_handler, seq_region,
                                                                                  protein_id,
                                                                                  refseq_cds_list)
                                    annotated_transcript['translation'] = annotated_translation
                                else:
                                    annotated_transcript['translation'] = []

                                annotated_transcript['transcript_checksum'] = ChecksumHandler.get_transcript_checksum(annotated_transcript)  # @IgnorePep8
                                annotated_transcripts.append(annotated_transcript)

                            annotated_gene['transcripts'] = annotated_transcripts
                            feature_object_to_save = {}
                            feature_object_to_save["gene"] = annotated_gene

                            if not dryrun:
                                status = DatabaseHandler.getInstance().save_features_to_database(feature_object_to_save,
                                                                                                 parent_ids)
                                if status is None:
                                    print("====Feature not save for " + str(parent_ids))
        except Exception as e:
            logger.error('Failed to parse id: ' + str(e))
            logger.error("Exception in user code:")
            logger.error("-"*60)
            traceback.print_exc(file=sys.stdout)
            logger.error("-"*60)

            return False

        return True
