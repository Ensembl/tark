from BioSQL import BioSeqDatabase
from Bio import GenBank


server = BioSeqDatabase.open_database(driver = "MySQLdb", user = "prem", passwd = "prem", host = "localhost", db = "bioseqdb")

db = server["refseq_db"]
#server.commit()

parser = GenBank.FeatureParser()
iterator = GenBank.Iterator(open("GCF_000001405.38_GRCh38.p12_genomic.gbff"), parser)
try:
     db.load(iterator)
except:
     print("Exception.....")

print("loaded success................")