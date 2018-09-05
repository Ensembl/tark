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

from BCBio import GFF
from refseq_loader.handlers.refseq.fastahandler import FastaHandler
from refseq_loader.handlers.refseq.annotationhandler import AnnotationHandler
from refseq_loader.handlers.refseq.databasehandler import DatabaseHandler
from refseq_loader.handlers.refseq.genbankhandler import GenBankHandler


class GFFHandler(AnnotationHandler, DatabaseHandler):

    @classmethod
    def parse_gff_with_genbank(cls, gff_file, sequence_file, protein_sequence_file, filter_region=None, filter_feature_gene=None, filter_feature_transcript=None):  # @IgnorePep8
        """
        Builds the gene model from GFF file and uses the genbank to fetch the sequence
        Use the filters while testing the loader
        """
        print(" GFF file from parse_gff " + gff_file)
        print(" Sequence file from parse_gff " + sequence_file)

        try:
            sequence_handler = GenBankHandler(sequence_file)
            protein_sequence_handler = FastaHandler(protein_sequence_file)
            # Examine for available regions
            examiner = GFF.GFFExaminer()

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
                        # print("skipping...." + str(chrom))
                        continue

                with open(gff_file) as gff_handle:
                    limits["gff_id"] = chrom_tuple

                    # Chromosome seq level
                    for rec in GFF.parse(gff_handle, limit_info=limits):
                        # print("Processing ID " + rec.id)

                        for gene_feature in rec.features:
                            # print(gene_feature)
                            if not gene_feature.type == "gene":
                                continue

                            if filter_feature_gene is not None:
                                if not gene_feature.qualifiers['gene'][0] == filter_feature_gene:
                                    continue
                            # print("gene qualifiers")
                            print("\t Type: " + str(gene_feature.type) + " ID: " + str(gene_feature.id) +
                                  "  Ref: " + str(gene_feature.ref) +
                                  "  Location start:" + str(gene_feature.location.start) +
                                  "  Location end:" + str(gene_feature.location.end))
                            # print(gene_feature)
                            print("\n")
                            annotated_gene = cls.get_annotated_gene(seq_region, gene_feature)
                            # cls.load_to_database(annotated_gene) # Implement here

                            # gene level
                            annotated_transcripts = []
                            for mRNA_feature in gene_feature.sub_features:
                                transcript_id = mRNA_feature.qualifiers['transcript_id'][0]
                                if filter_feature_transcript is not None and 'transcript_id' in mRNA_feature.qualifiers:
                                    if filter_feature_transcript not in mRNA_feature.qualifiers['transcript_id'][0]:
                                        continue

                                annotated_transcript = cls.get_annotated_transcript(sequence_handler, seq_region,
                                                                                    mRNA_feature)
                                print("\n")
    #                             # mRNA level
                                refseq_exon_list = []
                                refseq_exon_order = 1

                                refseq_cds_list = []
                                refseq_cds_order = 1
                                for mRNA_sub_feature in mRNA_feature.sub_features:
                                    refseq_exon_dict = {}
                                    if 'exon' in mRNA_sub_feature.type:
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

                                    print("\t\t\t    Type: " + str(mRNA_sub_feature.type) +
                                          " ID: " + str(mRNA_sub_feature.id) +
                                          "    Ref: " + str(mRNA_sub_feature.ref) +
                                          "  Location " + str(mRNA_sub_feature.location))

                                    print("\n")

                                print("=========BEFORE ANNOTATIONS")
                                print(refseq_exon_list)
                                print(refseq_cds_list)
                                print("==========END ==========")

                                annotated_exons = {}
                                annotated_translation = {}
                                # add sequence and other annotations
                                if len(refseq_exon_list) > 0:
                                    annotated_exons = cls.get_annotated_exons(sequence_handler, seq_region,
                                                                              transcript_id,
                                                                              refseq_exon_list)
                                if len(refseq_cds_list) > 0:
                                    protein_id = refseq_cds_list[0]['protein_id']
                                    annotated_translation = cls.get_annotated_cds(protein_sequence_handler, seq_region,
                                                                                  protein_id,
                                                                                  refseq_cds_list)
                                print("=========AFTER ANNOTATIONS")
                                print(annotated_exons)
                                print("=================")
                                print(annotated_translation)
                                print("=================")
                                # print(annotated_exons)
                                annotated_transcript['exons'] = annotated_exons
                                annotated_transcript['translation'] = annotated_translation

                                annotated_transcripts.append(annotated_transcript)
                            annotated_gene['transcripts'] = annotated_transcripts
                            feature_object_to_save = {}
                            feature_object_to_save["gene"] = annotated_gene
                            cls.save_features_to_database(feature_object_to_save)
        except:
            return False

        return True

#     @classmethod
#     def parse_gff(cls, gff_file, fasta_file, filter_region=None, filter_feature_gene=None, filter_feature_transcript=None):  # @IgnorePep8
#         print(" GFF file from parse_gff " + gff_file)
#         print(" Fasta file from parse_gff " + fasta_file)
#         
#         try:
#             # fasta_handler = FastaHandler(fasta_file)
#             fasta_handler = GenBankHandler(fasta_file)
#             # Examine for available regions
#             examiner = GFF.GFFExaminer()
#             # with gzip.open(gff_file, "rt") as gff_handle:
#             with open(gff_file) as gff_handle_examiner:
#                 possible_limits = examiner.available_limits(gff_handle_examiner)
#                 chromosomes = sorted(possible_limits["gff_id"].keys())
#     
#             limits = dict()
#     
#             for chrom_tuple in chromosomes:
#                 chrom = chrom_tuple[0]
#                 if not chrom.startswith("NC_"):
#                     continue
#     
#                 seq_region = cls.get_seq_region_from_refseq_accession(chrom)
#                 # print(chrom)
#                 # print("Examining " + chrom + " test")
#                 # Restrict only for chr13
#                 if filter_region is not None:
#                     if filter_region not in chrom:
#                         # print("skipping...." + str(chrom))
#                         continue
#     
#                 with open(gff_file) as gff_handle:
#                     limits["gff_id"] = chrom_tuple
#     
#                     # Chromosome seq level
#                     for rec in GFF.parse(gff_handle, limit_info=limits):
#                         # print("Processing ID " + rec.id)
#     
#                         for gene_feature in rec.features:
#                             # print(gene_feature)
#                             if not gene_feature.type == "gene":
#                                 continue
#     
#                             if filter_feature_gene is not None:
#                                 if not gene_feature.qualifiers['gene'][0] == filter_feature_gene:
#                                     continue
#                             # print("gene qualifiers")
#                             print("\t Type: " + str(gene_feature.type) + " ID: " + str(gene_feature.id) +
#                                   "  Ref: " + str(gene_feature.ref) +
#                                   "  Location start:" + str(gene_feature.location.start) +
#                                   "  Location end:" + str(gene_feature.location.end))
#                             # print(gene_feature)
#                             print("\n")
#                             annotated_gene = cls.get_annotated_gene(seq_region, gene_feature)
#                             # cls.load_to_database(annotated_gene) # Implement here
#     
#                             # gene level
#                             annotated_transcripts = []
#                             for mRNA_feature in gene_feature.sub_features:
#                                 if filter_feature_transcript is not None and 'transcript_id' in mRNA_feature.qualifiers:
#                                     if filter_feature_transcript not in mRNA_feature.qualifiers['transcript_id'][0]:
#                                         continue
#     
#                                 annotated_transcript = cls.get_annotated_transcript(fasta_handler, seq_region, mRNA_feature)
#                                 print("\n")
#     #                             # mRNA level
#                                 refseq_exon_list = []
#                                 refseq_exon_order = 1
#     
#                                 refseq_cds_list = []
#                                 refseq_cds_order = 1
#                                 for mRNA_sub_feature in mRNA_feature.sub_features:
#                                     refseq_exon_dict = {}
#                                     if 'exon' in mRNA_sub_feature.type:
#                                         # print("=======Reached exon========")
#                                         refseq_exon_dict['exon_stable_id'] = str(mRNA_sub_feature.id)
#                                         refseq_exon_dict['exon_stable_id_version'] = 1  # dummmy version
#                                         refseq_exon_dict['exon_order'] = refseq_exon_order
#                                         refseq_exon_dict['exon_start'] = str(mRNA_sub_feature.location.start)
#                                         refseq_exon_dict['exon_end'] = str(mRNA_sub_feature.location.end)
#                                         refseq_exon_dict['exon_strand'] = str(mRNA_sub_feature.location.strand)
#                                         refseq_exon_list.append(refseq_exon_dict)
#                                         refseq_exon_order += 1
#     
#                                     refseq_cds_dict = {}
#                                     if 'CDS' in mRNA_sub_feature.type:
#                                         # print("=======Reached cds=========")
#                                         refseq_cds_dict['cds_order'] = refseq_cds_order
#                                         print(mRNA_sub_feature)
#                                         refseq_cds_dict['cds_start'] = str(mRNA_sub_feature.location.start)
#                                         refseq_cds_dict['cds_end'] = str(mRNA_sub_feature.location.end)
#                                         refseq_cds_dict['cds_strand'] = str(mRNA_sub_feature.location.strand)
#                                         refseq_cds_dict['cds_id'] = str(mRNA_sub_feature.id)
#                                         refseq_cds_dict['protein_id'] = str(mRNA_sub_feature.qualifiers['protein_id'][0])
#                                         refseq_cds_list.append(refseq_cds_dict)
#                                         refseq_cds_order += 1
#     
#                                     print("\t\t\t    Type: " + str(mRNA_sub_feature.type) +
#                                           " ID: " + str(mRNA_sub_feature.id) +
#                                           "    Ref: " + str(mRNA_sub_feature.ref) +
#                                           "  Location " + str(mRNA_sub_feature.location))
# 
#                                     print("\n")
# 
#                                 relative_exon_locations = cls.get_relative_exon_location(seq_region, refseq_exon_list)
#                                 relative_exon_locations_with_seq = cls.add_feature_sequence(fasta_handler,
#                                                                                          relative_exon_locations,
#                                                                                      mRNA_feature.qualifiers['transcript_id'][0], 'exon')  # @IgnorePep8
# 
#                                 print(relative_exon_locations_with_seq)
#                                 annotated_exons = cls.get_annotated_exons(seq_region, relative_exon_locations_with_seq)
#                                 annotated_translation = cls.get_annotated_cds(seq_region, refseq_cds_list)
#                                 print(refseq_cds_list)
#                                 print("=================")
#                                 print(annotated_translation)
#                                 print("=================")
#                                 # print(annotated_exons)
#                                 annotated_transcript['exons'] = annotated_exons
#                                 annotated_transcript['translation'] = annotated_translation
# 
#                                 annotated_transcripts.append(annotated_transcript)
#                             annotated_gene['transcripts'] = annotated_transcripts
#                             feature_object_to_save = {}
#                             feature_object_to_save["gene"] = annotated_gene
#                             cls.save_features_to_database(feature_object_to_save)
#         except:
#             return False
# 
#         return True
