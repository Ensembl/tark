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
from tark.utils.exon_utils import ExonUtils
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

    cds_seq = ExonUtils.compute_cds_sequence(transcript)
    return cds_seq
