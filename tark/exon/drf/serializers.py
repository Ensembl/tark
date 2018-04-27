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
from sequence.drf.serializers import SequenceSerializer
from release.drf.serializers import ReleaseSetSerializer
from assembly.drf.serializers import AssemblySerializer
from tark_drf.utils.drf_fields import AssemblyField, CommonFields
# from transcript.drf.serializers import TranscriptSerializer
from exon.models import Exon, ExonTranscript
from tark_drf.utils.drf_mixin import SerializerMixin


class ExonSerializer(SerializerMixin, serializers.ModelSerializer):

    MANY2ONE_SERIALIZER = {Exon.MANY2ONE_RELATED['SEQUENCE']: SequenceSerializer,
                           Exon.MANY2ONE_RELATED['ASSEMBLY']: AssemblySerializer}
    ONE2MANY_SERIALIZER = {Exon.ONE2MANY_RELATED['RELEASE_SET']: ReleaseSetSerializer,
                           Exon.ONE2MANY_RELATED['EXON_TRANSCRIPT']: "transcript.drf.serializers.TranscriptSerializer"
                           }

    assembly = AssemblyField(read_only=True)

    class Meta:
        model = Exon
        fields = CommonFields.COMMON_FIELD_SET + ('exon_checksum', 'seq_checksum')

    def __init__(self, *args, **kwargs):
        super(ExonSerializer, self).__init__(*args, **kwargs)
        self.set_related_fields(ExonSerializer, **kwargs)


class ExonTranscriptSerializer(serializers.ModelSerializer):

    stable_id = serializers.ReadOnlyField(source='exon.stable_id')
    stable_id_version = serializers.ReadOnlyField(source='exon.stable_id_version')
    assembly = serializers.ReadOnlyField(source='exon.assembly.assembly_name')
    loc_start = serializers.ReadOnlyField(source='exon.loc_start')
    loc_end = serializers.ReadOnlyField(source='exon.loc_end')
    loc_strand = serializers.ReadOnlyField(source='exon.loc_strand')
    loc_region = serializers.ReadOnlyField(source='exon.loc_region')
    loc_checksum = serializers.ReadOnlyField(source='exon.loc_checksum')
    exon_checksum = serializers.ReadOnlyField(source='exon.exon_checksum')
    seq_checksum = serializers.ReadOnlyField(source='exon.seq_checksum')

    class Meta:
        model = ExonTranscript
        fields = ('stable_id', 'stable_id_version', 'assembly', 'loc_start', 'loc_end', 'loc_strand', 'loc_region',
                  'loc_checksum', 'exon_checksum', 'seq_checksum', 'exon_order', )
