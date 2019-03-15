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

from rest_framework import serializers
from tark_drf.utils.drf_mixin import SerializerMixin
from release.models import ReleaseSet, ExonReleaseTag, ReleaseSource,\
    TranscriptReleaseTagRelationship
from tark_drf.utils.drf_fields import AssemblyField, ReleaseSourceField


class ExonReleaseTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExonReleaseTag
        fields = '__all__'


class ReleaseSetSerializer(SerializerMixin, serializers.ModelSerializer):
    assembly = AssemblyField(read_only=True)
    source = ReleaseSourceField(read_only=True)

    class Meta:
        model = ReleaseSet
        fields = ('assembly', 'shortname', 'description', 'release_date', 'source')


class ReleaseSourceSerializer(SerializerMixin, serializers.ModelSerializer):

    ONE2MANY_SERIALIZER = {ReleaseSource.ONE2MANY_RELATED['RELEASE_SET']: ReleaseSetSerializer}

    class Meta:
        model = ReleaseSource
        fields = '__all__'
