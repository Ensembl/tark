import pprint
from BCBio.GFF import GFFExaminer
from BCBio import GFF

in_file = "Homo_sapiens.GRCh38.91.chromosome.22.gff3"
examiner = GFFExaminer()
in_handle = open(in_file)
pprint.pprint(examiner.available_limits(in_handle))
in_handle.close()

limit_info = dict(
    gff_source=["ensembl"])

in_handle = open(in_file)
for rec in GFF.parse(in_handle, limit_info=limit_info):
    print(rec.features)

in_handle.close()
