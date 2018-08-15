from Bio import SeqIO
import sys

gbk_filename = sys.argv[1]

# in_file = sys.argv[1]
# 
# examiner = GFF.GFFExaminer()
# with open(in_file) as gff_handle:
#     possible_limits = examiner.available_limits(gff_handle)
# chromosomes = sorted(possible_limits["gff_id"].keys())
# print(chromosomes)
# limits = dict(gff_type=["gene", "mRNA"])


for seq_record in SeqIO.parse(gbk_filename, "genbank"):
    print("Dealing with GenBank record %s ..............................." % seq_record.id)
    for seq_feature in seq_record.features:
        print(seq_feature)
#         if seq_feature.type=="CDS":
#             assert len(seq_feature.qualifiers['translation'])==1
#             print("> Start: %s Stop: %s Strand: %s From %s\n" % (
#                    seq_feature.location.start,
#                    seq_feature.location.end,
#                    seq_feature.strand,
#                    seq_record.name))

print("Done")