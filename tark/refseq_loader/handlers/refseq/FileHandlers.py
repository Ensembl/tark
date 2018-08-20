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
import re
import exon


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
            if not chrom.startswith("NC_"):
                continue

            seq_region = cls.get_seq_region_from_refseq_accession(chrom)
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
                    print("Processing ID " + rec.id)

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
                        print(gene_feature)
                        print("\n")
                        annotated_gene = cls.get_annotated_gene(seq_region, gene_feature)
                        # cls.load_to_database(annotated_gene) # Implement here

                        # gene level
                        refseq_transcript_list = []
                        for mRNA_feature in gene_feature.sub_features:
                            if filter_feature_transcript is not None and 'transcript_id' in mRNA_feature.qualifiers:
                                if filter_feature_transcript not in mRNA_feature.qualifiers['transcript_id'][0]:
                                    continue

                            annotated_transcript = cls.get_annotated_transcript(fasta_handler, seq_region, mRNA_feature)

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
                                    refseq_exon_dict['exon_stable_id'] = str(mRNA_sub_feature.id)
                                    refseq_exon_dict['exon_stable_id_version'] = 1  # dummmy version
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

                        relative_exon_locations = cls.get_relative_exon_location(seq_region, refseq_exon_list)
                        relative_exon_locations_with_seq = cls.add_exon_sequence(fasta_handler,
                                                                                 relative_exon_locations,
                                                                                 mRNA_feature.qualifiers['transcript_id'][0])  # @IgnorePep8

                        print(relative_exon_locations_with_seq)
                        annotated_exons = cls.get_annotated_exons(seq_region, relative_exon_locations_with_seq)
                        print(annotated_exons)

                print("=========================================\n\n")

    @classmethod
    def load_to_database(cls):
        pass

    @classmethod
    def get_annotated_gene(cls, chrom, gene_feature):
        gene = {}
        gene['loc_start'] = str(gene_feature.location.start)
        gene['loc_end'] = str(gene_feature.location.end)
        gene['loc_strand'] = str(gene_feature.location.strand)
        gene['loc_region'] = str(chrom)
        gene['stable_id'] = cls.parse_qualifiers(gene_feature.qualifiers, "Dbxref", "GeneID")
        gene['stable_id_version'] = 1
        gene['assembly_id'] = "1"
        gene['hgnc_id'] = cls.parse_qualifiers(gene_feature.qualifiers, "Dbxref", "HGNC:HGNC")
        gene['session_id'] = None
        gene['gene_checksum'] = None
        gene['loc_checksum'] = None
        return gene

    @classmethod
    def get_annotated_transcript(cls, fasta_handler, chrom, mRNA_feature):
        print(mRNA_feature)
        print("\t\t    Type: " + str(mRNA_feature.type) +
              "  ID: " + str(mRNA_feature.id) +
              "  Location start:" + str(mRNA_feature.location.start) +
              "  Location end: " + str(mRNA_feature.location.end))
        print(mRNA_feature.qualifiers)
        # print(fasta_handler.get_fasta_seq_by_id(mRNA_feature.qualifiers['transcript_id'][0]))
        transcript = {}
        transcript['loc_start'] = str(mRNA_feature.location.start)
        transcript['loc_end'] = str(mRNA_feature.location.end)
        transcript['loc_strand'] = str(mRNA_feature.location.strand)
        transcript['loc_region'] = str(chrom)
        stable_id = mRNA_feature.qualifiers['transcript_id'][0]
        (transcript_stable_id, transcript_stable_id_version) = stable_id.split(".")
        transcript['stable_id'] = transcript_stable_id
        transcript['stable_id_version'] = transcript_stable_id_version
        transcript['assembly_id'] = "1"
        transcript['session_id'] = None
        transcript['transcript_checksum'] = None
        transcript['exon_set_checksum'] = None
        transcript['seq_checksum'] = None
        transcript['loc_checksum'] = None
        transcript['sequence'] = fasta_handler.get_fasta_seq_by_id(mRNA_feature.qualifiers['transcript_id'][0])
        return transcript

    @classmethod
    def get_annotated_exons(cls, seq_region, relative_exon_locations_with_seq):
        annotated_exons = []
        for exon_feature in relative_exon_locations_with_seq:
            annotated_exons.append(cls.get_annotated_exon(seq_region, exon_feature))

        return annotated_exons

    @classmethod
    def get_annotated_exon(cls, seq_region, exon_feature):
        print("****************************")
        print(exon_feature)
        print("****************************")
        exon = {}
        exon['loc_start'] = exon_feature["exon_seq_region_start"]
        exon['loc_end'] = exon_feature["exon_seq_region_end"]
        exon['loc_strand'] = exon_feature["exon_seq_region_strand"]
        exon['loc_region'] = str(seq_region)
        exon['exon_order'] = exon_feature["exon_order"]
        exon['stable_id'] = exon_feature["exon_stable_id"]
        exon['stable_id_version'] = exon_feature["exon_stable_id_version"]
        exon['assembly_id'] = "1"
        exon['session_id'] = None
        exon['exon_checksum'] = None
        exon['loc_checksum'] = None
        exon['seq_checksum'] = None
        return exon

    @classmethod
    def parse_qualifiers(cls, qualifiers, key_qualifier, attr=None):
        if key_qualifier in qualifiers:
            cur_qualifiers = qualifiers[key_qualifier]
            for cur_qualifier in cur_qualifiers:
                if attr is not None:
                    my_regex = attr + ":" + "(.*)"
                    matchObj = re.match( my_regex, cur_qualifier, re.M|re.I)  # @IgnorePep8
                    if matchObj and matchObj.group(1):
                        attr_value = matchObj.group(1)
                        return attr_value
        return None

    @classmethod
    def get_seq_region_from_refseq_accession(cls, refseq_accession):
        matchObj = re.match( r'NC_(\d+)\.\d+', refseq_accession, re.M|re.I)  # @IgnorePep8

        if matchObj and matchObj.group(1):
            chrom = int(matchObj.group(1))
            print("Chr " + str(chrom))
            if chrom == 23:
                return "X"
            elif chrom == 24:
                return "Y"
            else:
                return chrom

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
    def get_relative_exon_location(cls, seq_region, refseq_exon_list):

        relative_refseq_exon_list = []
        current_exon_end = 1
        for exon in refseq_exon_list:
            # print(exon)
            relative_refseq_exon_dict = {}
            relative_refseq_exon_dict['exon_order'] = exon['exon_order']
            relative_refseq_exon_dict['exon_stable_id'] = exon['exon_stable_id']
            relative_refseq_exon_dict['exon_stable_id_version'] = 1
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
            # annotate with actual data
            relative_refseq_exon_dict['exon_seq_region_start'] = exon['exon_start']
            relative_refseq_exon_dict['exon_seq_region_end'] = exon['exon_end']
            relative_refseq_exon_dict['exon_seq_region_strand'] = exon['exon_strand']
            relative_refseq_exon_dict['exon_seq_region'] = str(seq_region)

            relative_refseq_exon_list.append(relative_refseq_exon_dict)
            # print("=========")
            # print(relative_refseq_exon_dict)
            # print("=========")

        # print(relative_refseq_exon_list)
        return relative_refseq_exon_list
