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
from tark_drf.utils.drf_mixin import SerializerMixin
from assembly.drf.serializers import AssemblySerializer
from release.drf.serializers import ReleaseSetSerializer
from tark_drf.utils.drf_fields import AssemblyField, CommonFields
from release.models import TranscriptReleaseTag
from transcript.models import Transcript
from sequence.drf.serializers import SequenceSerializer
from gene.drf.serializers import GeneSerializer
from exon.drf.serializers import ExonTranscriptSerializer, ExonSerializer
from translation.drf.serializers import TranslationTranscriptSerializer,\
    TranslationSerializer


class TranscriptReleaseTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranscriptReleaseTag
        fields = '__all__'


class TranscriptSerializer(SerializerMixin, serializers.ModelSerializer):

    MANY2ONE_SERIALIZER = {Transcript.MANY2ONE_RELATED['SEQUENCE']: SequenceSerializer,
                           Transcript.MANY2ONE_RELATED['ASSEMBLY']: AssemblySerializer}
    ONE2MANY_SERIALIZER = {Transcript.ONE2MANY_RELATED['RELEASE_SET']: ReleaseSetSerializer,
                           Transcript.ONE2MANY_RELATED['GENE']: GeneSerializer,
                           Transcript.ONE2MANY_RELATED['TRANSLATION']: TranslationSerializer,
                           Transcript.ONE2MANY_RELATED['EXONTRANSCRIPT']: ExonTranscriptSerializer,
                           }

    assembly = AssemblyField(read_only=True)
    #genes = GeneSerializer(many=True, read_only=True)
    #exons = ExonTranscriptSerializer(source="exontranscript_set", many=True, read_only=True)
#     translations = TranslationTranscriptSerializer(source='translationtranscript_set', many=True)

    class Meta:
        model = Transcript
        fields = CommonFields.COMMON_FIELD_SET + ('exon_set_checksum', 'transcript_checksum', 'sequence', )

    def __init__(self, *args, **kwargs):
        super(TranscriptSerializer, self).__init__(*args, **kwargs)
        self.set_related_fields(TranscriptSerializer, **kwargs)


class TranscriptDiffSerializer(TranscriptSerializer):

    def __init__(self, *args, **kwargs):
        super(TranscriptDiffSerializer, self).__init__(*args, **kwargs)
        self.set_related_fields(TranscriptDiffSerializer, **kwargs)


class TranscriptSearchSerializer(TranscriptSerializer):

    def __init__(self, *args, **kwargs):
        super(TranscriptSearchSerializer, self).__init__(*args, **kwargs)
        self.set_related_fields(TranscriptSearchSerializer, **kwargs)
