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

from Bio import SeqIO, SeqFeature
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class GenBankHandler():

    def __init__(self, gbff_file):
        self.gbff_file = gbff_file
        logger.info("Loading genbank file...please wait...")
        self.indexed_data = SeqIO.index(gbff_file, "genbank")

    def get_seq_record_by_id(self, identifier):
        if self.indexed_data is not None:
            try:
                seq_record = self.indexed_data[identifier]
                return seq_record
            except Exception as e:
                print('Failed to parse id: ' + str(identifier) + " " + str(e))
                return None
        else:
            raise ValueError("Genbank Handler not initialized")

    def get_sequence_by_id(self, identifier):
        if self.indexed_data is not None:
            try:
                seq = self.indexed_data[identifier].seq
                return str(seq)
            except Exception as e:
                logger.error('Failed to parse id: ' + str(identifier) + " " + str(e))
                return None
        else:
            raise ValueError("Genbank Handler not initialized")

    def get_seq_record_by_id_location(self, identifier, start=None, end=None, strand_=None):
        logger.info("Identifier {0}  Start {1}  End {2} Strand {3} ".format(identifier, start, end, strand_))
        if self.indexed_data is not None:
            if start is not None and end is not None and strand_ is not None:
                seq = self.get_sequence_by_id(identifier)
                feature = SeqFeature.FeatureLocation(start, end, strand=strand_)
                return str(feature.extract(seq))
            else:
                return self.get_sequence_by_id(identifier)

        else:
            raise ValueError("Genbank Handler not initialized")

    def get_exon_sequences_by_identifier(self, identifier):
        logger.info("get_exon_sequences_by_identifier " + str(identifier))
        seq_record = self.get_seq_record_by_id(identifier)
        if seq_record is None:
            return None
        exon_sequences = []
        for feature in seq_record.features:
            if feature.type == 'exon':
                logger.info("Start: {0}  End {1}  Strand {2}".format(str(feature.location.start),
                                                                     str(feature.location.end),
                                                                     str(feature.location.strand)))
                sequence = self.get_seq_record_by_id_location(identifier,
                                                              feature.location.start,
                                                              feature.location.end,
                                                              feature.location.strand)
                exon_sequences.append(str(sequence))

        return exon_sequences
