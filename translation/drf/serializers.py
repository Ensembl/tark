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


from rest_framework import serializers
from tark_drf.utils.drf_mixin import SerializerMixin
from assembly.drf.serializers import AssemblySerializer
from release.drf.serializers import ReleaseSetSerializer
from tark_drf.utils.drf_fields import AssemblyField, CommonFields
from release.models import TranslationReleaseTag
from translation.models import Translation, TranslationTranscript
from sequence.drf.serializers import SequenceSerializer


class TranslationReleaseTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranslationReleaseTag
        fields = '__all__'


class TranslationSerializer(SerializerMixin, serializers.ModelSerializer):

    MANY2ONE_SERIALIZER = {Translation.MANY2ONE_RELATED['SEQUENCE']: SequenceSerializer,
                           Translation.MANY2ONE_RELATED['ASSEMBLY']: AssemblySerializer}
    ONE2MANY_SERIALIZER = {Translation.ONE2MANY_RELATED['RELEASE_SET']: ReleaseSetSerializer,
                           Translation.ONE2MANY_RELATED['TRANSCRIPT']:
                           "transcript.drf.serializers.TranscriptSerializer"}

    assembly = AssemblyField(read_only=True)

    class Meta:
        model = Translation
        fields = CommonFields.COMMON_FIELD_SET + ('translation_id', 'translation_checksum',)

    def __init__(self, *args, **kwargs):
        super(TranslationSerializer, self).__init__(*args, **kwargs)
        self.set_related_fields(TranslationSerializer, **kwargs)


class TranslationTranscriptSerializer(SerializerMixin, serializers.ModelSerializer):
    translation_id = serializers.ReadOnlyField(source='translation.translation_id')
    stable_id = serializers.ReadOnlyField(source='translation.stable_id')
    stable_id_version = serializers.ReadOnlyField(source='translation.stable_id_version')
    assembly = serializers.ReadOnlyField(source='translation.assembly.assembly_name')
    loc_start = serializers.ReadOnlyField(source='translation.loc_start')
    loc_end = serializers.ReadOnlyField(source='translation.loc_end')
    loc_strand = serializers.ReadOnlyField(source='translation.loc_strand')
    loc_region = serializers.ReadOnlyField(source='translation.loc_region')
    loc_checksum = serializers.ReadOnlyField(source='translation.loc_checksum')
    translation_checksum = serializers.ReadOnlyField(source='translation.translation_checksum')
    translation_sequence = serializers.ReadOnlyField(source='translation.sequence.seq_checksum')

    class Meta:
        model = TranslationTranscript
        fields = ('stable_id', 'stable_id_version', 'assembly', 'loc_start', 'loc_end', 'loc_strand', 'loc_region',
                  'loc_checksum', 'translation_checksum', 'translation_sequence')
