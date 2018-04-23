'''
Copyright [1999-2015] Wellcome Trust Sanger Institute and the EMBL-European Bioinformatics Institute
Copyright [2016-2017] EMBL-European Bioinformatics Institute

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

from __future__ import unicode_literals
from assembly.models import Assembly, AssemblyAlias
from assembly.drf.serializers import AssemblySerializer, AssemblyAliasSerializer
from rest_framework import generics
from assembly.drf.filters import AssemblyExpandFilterBackend,\
    AssemblyFilterBackend
from tark.views import DataTableListApi
from tark.utils.schema_utils import SchemaUtils


class AssemblyList(generics.ListAPIView):
    queryset = Assembly.objects.all()
    serializer_class = AssemblySerializer
    filter_backends = (AssemblyExpandFilterBackend, AssemblyFilterBackend,)


class AssemblyDetail(generics.RetrieveAPIView):
    queryset = Assembly.objects.all()
    serializer_class = AssemblySerializer


class AssemblyAliasList(generics.ListAPIView):
    queryset = AssemblyAlias.objects.all()
    serializer_class = AssemblyAliasSerializer


class AssemblyAliasListDetail(generics.RetrieveAPIView):
    queryset = AssemblyAlias.objects.all()
    serializer_class = AssemblyAliasSerializer


class AssemblyDatatableView(DataTableListApi):
    serializer_class = AssemblySerializer
    search_parameters = SchemaUtils.get_field_names(app_name='assembly', model_name='assembly', exclude_pk=False)
    default_order_by = 3
    queryset = Assembly.objects.all()
