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
            if start is not None and end is not None:
                seq_record = self.fasta_handler.get_seq(identifier, start, end)
                if seq_record is not None:
                    return seq_record
            else:
                try:
                    fasta_record = self.fasta_handler[identifier]
                    len_fasta_record = len(fasta_record)
                    print("len_fasta_record " + str(len_fasta_record))
                    seq_record = self.fasta_handler.get_seq(identifier, 1, len_fasta_record)
                    return seq_record.seq
                except Exception as e:
                    print('Failed to get seq id: ' + str(identifier) + " " + str(e))
                    return None
        else:
            raise ValueError("Fasta seq not found for id " + identifier)
