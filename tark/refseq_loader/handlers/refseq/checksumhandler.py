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

import hashlib
import binascii


class ChecksumHandler(object):

    # Join an array of values with a ':' delimeter and find a sha1 checksum of it
    @classmethod
    def checksum_list(cls, attr_list):
        print("===checksum_list called====")
        cs = hashlib.sha1()  # update to other latest sha implementations

        if len(attr_list) > 1:
            attr_list_joined = ':'.join(attr_list)
        elif len(attr_list) == 1:
            attr_list_joined = attr_list[0]
        else:
            return None

        cs.update(attr_list_joined.encode('utf-8').strip())
        hex_digest = binascii.hexlify(cs.digest()).decode('ascii').upper()
        print("===from checusm list2")
        print(hex_digest)
        return hex_digest

    @classmethod
    def checksum_hexlify(cls, byte_checksum):
        hex_digest = binascii.hexlify(byte_checksum.strip()).decode('ascii').upper()
        return hex_digest

    @classmethod
    def get_location_checksum(cls, feature):
        loc_attrs = cls.get_loc_attributes()
        return cls.checksum_list(cls.get_attribute_values(loc_attrs, feature))

    @classmethod
    def get_exon_checksum(cls, feature):
        exon_loc_checksum = cls.get_location_checksum(feature)
        exon_seq_checksum = cls.get_seq_checksum(feature, "exon_seq")

        return cls.checksum_list([exon_loc_checksum, exon_seq_checksum])

    @classmethod
    def get_gene_checksum(cls, gene):
        attr_list = cls.get_attribute_values(cls.get_gene_attributes(), gene)
        attrs_checksum = cls.checksum_list(attr_list)

        return cls.checksum_list([attrs_checksum])

    @classmethod
    def get_transcript_checksum(cls, transcript):
        attr_list = cls.get_attribute_values(cls.get_transcript_attributes(), transcript)
        attrs_checksum = cls.checksum_list(attr_list)
        return cls.checksum_list([attrs_checksum])

    @classmethod
    def get_translation_checksum(cls, translation):
        attr_list = cls.get_attribute_values(cls.get_translation_attributes(), translation)
        attrs_checksum = cls.checksum_list(attr_list)
        return cls.checksum_list([attrs_checksum])

    @classmethod
    def get_exon_set_checksum(cls, exons_list):
        exon_checksum_list = [exon['exon_checksum'] for exon in exons_list]
        exon_set_checksum = ChecksumHandler.checksum_list(exon_checksum_list)
        return exon_set_checksum

    @classmethod
    def get_seq_checksum(cls, feature, seq_attr=None):
        if seq_attr is None:
            seq_attr = 'sequence'

        seq_checksum = cls.checksum_list([feature[seq_attr]])

        return seq_checksum

    @classmethod
    def get_attribute_values(cls, attr_list, feature):
        attr_value_list = [str(feature[attr]) for attr in attr_list if attr in feature]
        return attr_value_list

    @classmethod
    def get_loc_attributes(cls):
        return ['assembly_id', 'loc_region', 'loc_start', 'loc_end', 'loc_strand']

    @classmethod
    def get_gene_attributes(cls):
        return ['loc_checksum', 'hgnc_id', 'stable_id', 'stable_id_version']

    @classmethod
    def get_transcript_attributes(cls):
        return ['loc_checksum', 'stable_id', 'stable_id_version', 'exon_set_checksum', 'seq_checksum']

    @classmethod
    def get_translation_attributes(cls):
        return ['loc_checksum', 'stable_id', 'stable_id_version', 'seq_checksum']

  