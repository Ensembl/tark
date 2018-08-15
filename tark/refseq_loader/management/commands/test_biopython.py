import sys
from BCBio import GFF
from pyfaidx import Fasta

# Pass the GFF file
gff_file = sys.argv[1]
fasta_file = sys.argv[2]


def init_fasta(fasta_file):
    print("Loading fasta file......please be patient...")
    fasta_handler = Fasta(fasta_file, sequence_always_upper=True)
    return fasta_handler
    print("Fasta file loaded......")


def get_fasta_seq(chrom, start, end):
    seq = fasta_handler[chrom][start:end].seq
    return seq


fasta_handler = init_fasta(fasta_file)
# Examine for available regions
examiner = GFF.GFFExaminer()
with open(gff_file) as gff_handle:
    possible_limits = examiner.available_limits(gff_handle)
chromosomes = sorted(possible_limits["gff_id"].keys())

limits = dict()
for chrom in chromosomes:
    # Restrict only for chr13
    if "NC_000013.11" not in chrom:
        # print("skipping...." + str(chrom))
        continue

    with open(gff_file) as gff_handle:
        limits["gff_id"] = chrom

        # Chromosome seq level
        for rec in GFF.parse(gff_handle, limit_info=limits):
            print("ID " + rec.id + "  Name: " + rec.name)

            for gene_feature in rec.features:
                if not gene_feature.type == "gene":
                    continue

                if not gene_feature.id == 'gene35217':
                    continue
                # print("gene qualifiers")
                print("\t Type: " + str(gene_feature.type) + " ID: " + str(gene_feature.id) +
                      "  Ref: " + str(gene_feature.ref) +
                      "  Location start:" + str(gene_feature.location.start) +
                      "  Location end:" + str(gene_feature.location.end))
                print(gene_feature.qualifiers)
                print("\n")

#                 # gene level
                for mRNA_feature in gene_feature.sub_features:
                    print("\t\t    Type: " + str(mRNA_feature.type) +
                          "  ID: " + str(mRNA_feature.id) +
                          "    Ref: " + str(mRNA_feature.ref) +
                          "  Location start:" + str(mRNA_feature.location.start) +
                          "  Location end: " + str(mRNA_feature.location.end))
                    print(mRNA_feature.qualifiers)
                    print(get_fasta_seq(rec.id, mRNA_feature.location.start, mRNA_feature.location.end))

                    print("\n")
#                     # mRNA level
                    for mRNA_sub_feature in mRNA_feature.sub_features:
                        print("\t\t\t    Type: " + str(mRNA_sub_feature.type) +
                              " ID: " + str(mRNA_sub_feature.id) +
                              "    Ref: " + str(mRNA_sub_feature.ref) +
                              "  Location " + str(mRNA_sub_feature.location))
                        print(mRNA_sub_feature.qualifiers)
                        print(get_fasta_seq(rec.id, mRNA_sub_feature.location.start, mRNA_sub_feature.location.end))
                        print("\n")

                print("=========================================\n\n")




