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

from Bio.Alphabet import generic_dna
from Bio.SeqRecord import SeqRecord
from io import StringIO
from Bio.Seq import Seq
from Bio import SeqIO
import subprocess
import os
import re


class TarkSeqUtils(object):

    @classmethod
    def format_fasta(cls, sequence, id_="ID_", name_="", description_=""):
        record = SeqRecord(Seq(sequence, generic_dna),
                           id=id_, name=name_, description=description_)

        sequences = [record]
        fh = StringIO()
        SeqIO.write(sequences, fh, "fasta")
        return fh.getvalue()

    @classmethod
    def align_sequences(cls, query_fasta, target_fasta):
        # print(str(os.path.isfile(query_fasta)) + str(query_fasta))
        # print(str(os.path.isfile(target_fasta)) + str(target_fasta))

        if os.path.isfile(query_fasta) and os.path.isfile(target_fasta):
            p = subprocess.Popen(["exonerate", query_fasta, target_fasta], stdout=subprocess.PIPE)
            (output, err) = p.communicate()  # @UnusedVariable
            return output

    @classmethod
    def parse_location_string(cls, loc_string):
        loc_string = loc_string.replace(" ", "")
        matchloc = re.search(r'(\w+):(\d+)-(\d+)', loc_string)
        loc_region = matchloc.group(1)
        loc_start = matchloc.group(2)
        loc_end = matchloc.group(3)
        return (loc_region, loc_start, loc_end)

    @classmethod
    def difference_transcript_set(cls, release1, release2):
        pass
