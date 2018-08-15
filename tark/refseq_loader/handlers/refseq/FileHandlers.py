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
from pyfaidx import Fasta


class FastaHandler(object):

    def __init__(self, fasta_file):
        self.fasta_file = fasta_file
        print("Loading fasta file...please wait...")
        self.fasta_handler = Fasta(fasta_file, sequence_always_upper=True)

    def get_fasta_seq_by_location(self, chrom, start, end):
        if self.fasta_handler is not None:
            seq = self.fasta_handler[chrom][start:end].seq
            return seq
        else:
            raise ValueError("Fasta Handler not initialized")

    def get_fasta_seq_by_id(self, identifier, start=None, end=None):
        if self.fasta_handler is not None:
            # print("Identifier from get_fasta_seq_by_id=======" + str(identifier) +
            #      " start " + str(start) + " end " + str(end))
            print(identifier)
            if start is not None and end is not None:
                seq_record = self.fasta_handler.get_seq(identifier, start, end)
            else:
                fasta_record = self.fasta_handler[identifier]
                len_fasta_record = len(fasta_record)
                print("len_fasta_record " + str(len_fasta_record))
                seq_record = self.fasta_handler.get_seq(identifier, 1, len_fasta_record)

#             len_fasta_record = len(fasta_record)
#             print("len_fasta_record " + str(len_fasta_record))
#             seq = self.fasta_handler.get_seq(identifier[0], 1, len_fasta_record)
            return seq_record.seq
        else:
            raise ValueError("Fasta seq not found for id " + identifier)


#     @classmethod
#     def get_fasta_handler(self):
#         if self.fasta_handler is None:
#             print("Loading fasta file......please be patient...")
#             cls.fasta_handler = Fasta(cls.fasta_file, sequence_always_upper=True)
#         else:
#             return self.fasta_handler


class GFFHandler(object):

    @classmethod
    def parse_gff(cls, gff_file, fasta_file, filter_region=None, filter_feature_gene=None, filter_feature_transcript=None):  # @IgnorePep8
        print(" GFF file from parse_gff " + gff_file)
        print(" Fasta file from parse_gff " + fasta_file)
        fasta_handler = FastaHandler(fasta_file)
        # Examine for available regions
        examiner = GFF.GFFExaminer()
        # with gzip.open(gff_file, "rt") as gff_handle:
        with open(gff_file) as gff_handle_examiner:
            possible_limits = examiner.available_limits(gff_handle_examiner)
            chromosomes = sorted(possible_limits["gff_id"].keys())

        limits = dict()

        for chrom_tuple in chromosomes:
            chrom = chrom_tuple[0]
            # print(chrom)
            # print("Examining " + chrom + " test")
            # Restrict only for chr13
            if filter_region is not None:
                if filter_region not in chrom:
                    # print("skipping...." + str(chrom))
                    continue

            with open(gff_file) as gff_handle:
                limits["gff_id"] = chrom_tuple

                # Chromosome seq level
                for rec in GFF.parse(gff_handle, limit_info=limits):
                    print("ID " + rec.id + "  Name: " + rec.name)

                    for gene_feature in rec.features:
                        if not gene_feature.type == "gene":
                            continue

                        if not gene_feature.qualifiers['gene'][0] == filter_feature_gene:
                            continue
                        # print("gene qualifiers")
                        print("\t Type: " + str(gene_feature.type) + " ID: " + str(gene_feature.id) +
                              "  Ref: " + str(gene_feature.ref) +
                              "  Location start:" + str(gene_feature.location.start) +
                              "  Location end:" + str(gene_feature.location.end))
                        print(gene_feature.qualifiers)
                        print("\n")

                        # gene level
                        for mRNA_feature in gene_feature.sub_features:
                            if filter_feature_transcript is not None and 'transcript_id' in mRNA_feature.qualifiers:
                                if filter_feature_transcript not in mRNA_feature.qualifiers['transcript_id'][0]:
                                    continue

                            print("\t\t    Type: " + str(mRNA_feature.type) +
                                  "  ID: " + str(mRNA_feature.id) +
                                  "    Ref: " + str(mRNA_feature.ref) +
                                  "  Location start:" + str(mRNA_feature.location.start) +
                                  "  Location end: " + str(mRNA_feature.location.end))
                            print(mRNA_feature.qualifiers)
                            print(fasta_handler.get_fasta_seq_by_id(mRNA_feature.qualifiers['transcript_id'][0]))
#                             print(fasta_handler.get_fasta_seq(rec.id,
#                                                               mRNA_feature.location.start, mRNA_feature.location.end))

                            print("\n")
#                             # mRNA level
                            refseq_exon_list = []
                            refseq_exon_order = 1

                            refseq_cds_list = []
                            refseq_cds_order = 1
                            for mRNA_sub_feature in mRNA_feature.sub_features:
                                refseq_exon_dict = {}
                                if 'exon' in mRNA_sub_feature.type:
                                    print("=======Reached exon========")
                                    refseq_exon_dict['exon_order'] = refseq_exon_order
                                    refseq_exon_dict['exon_start'] = str(mRNA_sub_feature.location.start)
                                    refseq_exon_dict['exon_end'] = str(mRNA_sub_feature.location.end)
                                    refseq_exon_dict['exon_strand'] = str(mRNA_sub_feature.location.strand)
                                    refseq_exon_list.append(refseq_exon_dict)
                                    refseq_exon_order += 1

                                refseq_cds_dict = {}
                                if 'CDS' in mRNA_sub_feature.type:
                                    print("=======Reached cds=========")
                                    refseq_cds_dict['cds_order'] = refseq_cds_order
                                    refseq_cds_dict['cds_start'] = str(mRNA_sub_feature.location.start)
                                    refseq_cds_dict['cds_end'] = str(mRNA_sub_feature.location.end)
                                    refseq_cds_dict['cds_strand'] = str(mRNA_sub_feature.location.strand)
                                    refseq_cds_list.append(refseq_cds_dict)
                                    refseq_cds_order += 1

                                print("\t\t\t    Type: " + str(mRNA_sub_feature.type) +
                                      " ID: " + str(mRNA_sub_feature.id) +
                                      "    Ref: " + str(mRNA_sub_feature.ref) +
                                      "  Location " + str(mRNA_sub_feature.location))
                                print(mRNA_sub_feature.qualifiers)
#                                 print(fasta_handler.get_fasta_seq_by_location(rec.id, mRNA_sub_feature.location.start,
#                                                                   mRNA_sub_feature.location.end))

                                print("\n")

                            # print(refseq_exon_list)
                            # print("===============\n")
                            # print(refseq_cds_list)

                        relative_exon_locations = cls.get_relative_exon_location(refseq_exon_list)
                        relative_exon_locations_with_seq = cls.add_exon_sequence(fasta_handler,
                                                                                 relative_exon_locations,
                                                                                 mRNA_feature.qualifiers['transcript_id'])  # @IgnorePep8

                        # print(relative_exon_locations_with_seq)

                print("=========================================\n\n")

    @classmethod
    def add_exon_sequence(cls, fasta_handler, relative_exon_locations, transcript_id):
        relative_exon_locations_with_seq = []
        for exon in relative_exon_locations:
            exon_seq = fasta_handler.get_fasta_seq_by_id(transcript_id,
                                                         exon['exon_start'], exon['exon_end'])
            exon['exon_seq'] = exon_seq
            relative_exon_locations_with_seq.append(exon)
            # print(exon_seq)

        # print(relative_exon_locations_with_seq)
        return relative_exon_locations_with_seq

    @classmethod
    def get_relative_exon_location(cls, refseq_exon_list):

        relative_refseq_exon_list = []
        current_exon_end = 1
        for exon in refseq_exon_list:
            relative_refseq_exon_dict = {}
            relative_refseq_exon_dict['exon_order'] = exon['exon_order']
            # print("Processing Exon order " + str(relative_refseq_exon_dict['exon_order']))
            if relative_refseq_exon_dict['exon_order'] == 1:
                relative_refseq_exon_dict['exon_start'] = 1
                relative_refseq_exon_dict['exon_end'] = int(exon['exon_end']) - int(exon['exon_start'])
            else:
                relative_refseq_exon_dict['exon_start'] = current_exon_end + 1
                relative_refseq_exon_dict['exon_end'] = current_exon_end + \
                    int(exon['exon_end']) - int(exon['exon_start'])

            # current_exon_start = relative_refseq_exon_dict['exon_start']
            current_exon_end = relative_refseq_exon_dict['exon_end']

            relative_refseq_exon_list.append(relative_refseq_exon_dict)
            # print("=========")
            # print(relative_refseq_exon_dict)
            # print("=========")

        # print(relative_refseq_exon_list)
        return relative_refseq_exon_list
