"""
.. See the NOTICE file distributed with this work for additional information
   regarding copyright ownership.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from django import template
from tark_web.utils.sequtils import TarkSeqUtils
register = template.Library()


@register.filter
def format_fasta(sequence, seq_id):
    fasta_seq = TarkSeqUtils.format_fasta(sequence, id_=seq_id)
    sequence = fasta_seq
    return sequence


# Write fasta to file and display alignment
@register.filter
def align_sequence(query_seq, target_seq):
    seq_alignment = TarkSeqUtils.align_sequences(query_seq, target_seq)
    return seq_alignment


@register.filter
def get_cds_sequence(transcript):



    transcript_seq = None
    if 'sequence' in transcript and 'sequence' in transcript['sequence']:
        transcript_seq = transcript['sequence']['sequence']
        transcript_start = transcript['loc_start']
        transcript_end = transcript['loc_end']
        print("================START====")
        print(transcript_seq)
        if 'translations' in transcript:
            translations = transcript['translations']
            print(translations)
            cds_start = int(translations['loc_start'])
            cds_end = int(translations['loc_end'])
            
            five_prime_utr_length =  transcript_start + cds_start
            three_prime_utr_length =  transcript_end - cds_end
            print("===========cds_start=====")
            print(cds_start)
            print(cds_end)
            
            print("===========cds_start=====")
            print(cds_start)
            print(cds_end)
            transcript_seq_5_3_chopped = transcript_seq[five_prime_utr_length:-three_prime_utr_length] #chop 5' and 3'
            print("======transcript_seq_5_3_chopped====================")
            print(transcript_seq_5_3_chopped)
            
            transcript_seq = transcript_seq_5_3_chopped
    
    #seq_id = str(transcript['stable_id']) + '.' + str(transcript['stable_id_version'])
    
    cds_sequence =  transcript_seq
    print(cds_sequence)
#     fasta_seq = TarkSeqUtils.format_fasta(cds_sequence, id_=seq_id)
#     sequence = fasta_seq
    return cds_sequence


