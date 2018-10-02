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


from rest_framework import serializers
import binascii
from tark_drf.utils.drf_utils import DrfUtils
import coreapi
from release.utils.release_utils import ReleaseUtils


class DrfFields(object):

    @classmethod
    def get_expand_field(cls, model):

        related_models = DrfUtils.get_related_entities(model)
        counter = 1
        description_ = "comma separated list of objects to expand (eg:<br/> "
        for _model in related_models:
            if counter > 5:
                description_ = description_ + _model + ',<br/>'
                counter = 1
            else:
                description_ += _model + ','
                counter += 1
        description_ += ")"

        expand_field = coreapi.Field(
                name='expand',
                location='query',
                required=False,
                type='string',
                description=description_)
        return expand_field

    @classmethod
    def get_expand_all_field(cls):
        expand_all_field = coreapi.Field(
            name='expand_all',
            location='query',
            required=False,
            type='boolean',
            description='selecting true will expand all the related fields, to selectively expand, use expand above')
        return expand_all_field

    @classmethod
    def get_expand_all_mandatory_field(cls):
        expand_all_field = coreapi.Field(
            name='expand_all',
            location='query',
            required=True,
            type='boolean',
            example=True,
            description='Please leave it as true')
        return expand_all_field

    @classmethod
    def get_expand_transcript_release_set_field(cls):
        expand_transcript_release_set_field = coreapi.Field(
            name='expand',
            location='query',
            required=True,
            type='string',
            example="transcript_release_set",
            description='We need the release set to compute the difference, please enter "transcript_release_set"')
        return expand_transcript_release_set_field

    @classmethod
    def source_name_field(cls):
        source_name_field = coreapi.Field(
            name='source_name',
            location='query',
            required=False,
            type='string',
            description='source_name to filter(eg: Ensembl, RefSeq)')
        return source_name_field

    @classmethod
    def assembly_name_field(cls):
        assembly_name_field = coreapi.Field(
            name='assembly_name',
            location='query',
            required=False,
            type='string',
            description='assembly_name to filter(eg: GRCh37, GRCh38)')
        return assembly_name_field

    @classmethod
    def release_short_name_field(cls):
        release_short_name_field = coreapi.Field(
            name='release_short_name',
            location='query',
            required=False,
            type='string',
            description='release_short_name to filter(eg: 90)')
        return release_short_name_field

    @classmethod
    def identifier_field(cls):
        identifier_field = coreapi.Field(
            name='identifier_field',
            location='query',
            required=True,
            type='string',
            description='any valid identifiers (eg: BRCA2, ENSG00000139618, ENST00000380152)')
        return identifier_field

    @classmethod
    def stable_id_field(cls, model_name):
        stable_id_field = coreapi.Field(
            name='stable_id',
            location='query',
            required=False,
            type='string',
            description='stable id (eg:  ' + cls.get_stable_id_example(model_name) + ')')
        return stable_id_field

    @classmethod
    def stable_id_version_field(cls):
        stable_id_version_field = coreapi.Field(
            name='stable_id_version',
            location='query',
            required=False,
            type='integer',
            description='stable id version (eg: 1)')
        return stable_id_version_field

    @classmethod
    def loc_region_field(cls):
        loc_end_field = coreapi.Field(
            name='loc_region',
            location='query',
            required=False,
            type='string',
            description='chromosomal region (eg: 1, 6, CHR_HSCHR7_2_CTG6, LRG_192)')
        return loc_end_field

    @classmethod
    def loc_start_field(cls):
        loc_start_field = coreapi.Field(
            name='loc_start',
            location='query',
            required=False,
            type='integer',
            description='start location')
        return loc_start_field

    @classmethod
    def loc_end_field(cls):
        loc_end_field = coreapi.Field(
            name='loc_end',
            location='query',
            required=False,
            type='integer',
            description='end location')
        return loc_end_field

    @classmethod
    def loc_strand_field(cls):
        loc_end_field = coreapi.Field(
            name='loc_strand',
            location='query',
            required=False,
            type='integer',
            description='strand')
        return loc_end_field

    @classmethod
    def search_release_field(cls):
        diff_me_release_field = coreapi.Field(
            name='search_release',
            location='query',
            required=False,
            type='string',
            description='release_short_name to diff me(eg: 84)')
        return diff_me_release_field

    @classmethod
    def search_assembly_field(cls):
        diff_me_assembly_field = coreapi.Field(
            name='search_assembly',
            location='query',
            required=False,
            type='string',
            description='assembly_name for diff_me (eg: GRCh38)')
        return diff_me_assembly_field

    @classmethod
    def diff_me_stable_id_field(cls):
        diff_me_stable_id_field = coreapi.Field(
            name='diff_me_stable_id',
            location='query',
            required=True,
            type='string',
            description='Diff me stable_id (eg: ENST00000380152)')
        return diff_me_stable_id_field

    @classmethod
    def diff_me_release_field(cls):
        diff_me_release_field = coreapi.Field(
            name='diff_me_release',
            location='query',
            required=False,
            type='string',
            description='release_short_name to diff me(eg: 88)')
        return diff_me_release_field

    @classmethod
    def diff_me_assembly_field(cls):
        diff_me_assembly_field = coreapi.Field(
            name='diff_me_assembly',
            location='query',
            required=False,
            type='string',
            description='assembly_name for diff_me (eg: GRCh38)')
        return diff_me_assembly_field

    @classmethod
    def diff_with_stable_id_field(cls):
        diff_with_stable_id_field = coreapi.Field(
            name='diff_with_stable_id',
            location='query',
            required=True,
            type='string',
            description='Diff with stable_id (eg: ENST00000380152)')
        return diff_with_stable_id_field

    @classmethod
    def diff_with_release_field(cls):
        diff_with_release_field = coreapi.Field(
            name='diff_with_release',
            location='query',
            required=False,
            type='string',
            description='release_short_name to diff with(eg: 86 default to highest release in the releaset set - ' +
            str(ReleaseUtils.get_latest_release()) + ' )')
        return diff_with_release_field

    @classmethod
    def diff_with_assembly_field(cls):
        diff_with_assembly_field = coreapi.Field(
            name='diff_with_assembly',
            location='query',
            required=False,
            type='string',
            description='assembly_name for diff with (eg: GRCh38)')
        return diff_with_assembly_field

    @classmethod
    def get_stable_id_example(cls, model_name):
        example_dict = {'Gene': 'ENSG00000139618', 'Transcript': 'ENST00000380152', 'Exon': 'ENSE00001184784',
                        'Translation': 'ENSP00000369497'}
        print ("Model anme  " + str(model_name))
        if model_name in example_dict:
            return example_dict[model_name]
        return ""


class ChecksumFieldSerializer(serializers.Field):
    """
    Does the binary to hex conversion
    """
    def to_internal_value(self, value):
        '''
        The to_internal_value() method is called to restore a primitive datatype into
        its internal python representation.
        '''
        if value is not None:
            try:
                return binascii.hexlify(value.strip()).decode('ascii').upper()
            except:
                print("Validation Error")
                raise(serializers.ValidationError)

        return None


class AssemblyField(serializers.RelatedField):
    print("*******AssemblyField***************************")
    def to_representation(self, value):
        if value is not None:
            return value.assembly_name
        return None


class CommonFields(object):

    COMMON_FIELD_SET = ('stable_id', 'stable_id_version', 'assembly', 'loc_start', 'loc_end', 'loc_strand',
                        'loc_region', 'loc_checksum', )

    COMMON_QUERY_SET = [DrfFields.stable_id_version_field(),
                        DrfFields.loc_start_field(), DrfFields.loc_end_field(),
                        DrfFields.loc_region_field(), DrfFields.loc_strand_field()
                        ]

    COMMON_RELATED_QUERY_SET = [DrfFields.assembly_name_field(), DrfFields.release_short_name_field(),
                                DrfFields.source_name_field()]

    @classmethod
    def get_common_query_set(cls, model_name=None):
        return [DrfFields.stable_id_field(model_name)] + CommonFields.COMMON_QUERY_SET

    @classmethod
    def get_expand_query_set(cls, model_instance):
        return [DrfFields.get_expand_field(model_instance), DrfFields.get_expand_all_field()]

    @classmethod
    def get_expand_all_mandatory_query_set(cls, model_instance):
        return [DrfFields.get_expand_all_mandatory_field()]
