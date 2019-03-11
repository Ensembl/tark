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
from gene.models import Gene
from assembly.drf.serializers import AssemblySerializer
from release.drf.serializers import ReleaseSetSerializer
from tark_drf.utils.drf_fields import AssemblyField, CommonFields
from release.models import GeneReleaseTag
from genenames.drf.serializers import GeneNamesSerializer


class GeneReleaseTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneReleaseTag
        fields = '__all__'


class HgncNameField(serializers.RelatedField):
    def to_representation(self, value):
        if value is not None:
            return value.name
        return None


class GeneSerializer(SerializerMixin, serializers.ModelSerializer):

    MANY2ONE_SERIALIZER = {Gene.MANY2ONE_RELATED['ASSEMBLY']: AssemblySerializer,
                           Gene.MANY2ONE_RELATED['HGNC']: GeneNamesSerializer}
    ONE2MANY_SERIALIZER = {Gene.ONE2MANY_RELATED['RELEASE_SET']: ReleaseSetSerializer}

    assembly = AssemblyField(read_only=True)
    name = HgncNameField(read_only=True)

    class Meta:
        model = Gene
        fields = CommonFields.COMMON_FIELD_SET + ('name', 'gene_checksum', )

    def __init__(self, *args, **kwargs):
        super(GeneSerializer, self).__init__(*args, **kwargs)
        self.set_related_fields(GeneSerializer, **kwargs)
