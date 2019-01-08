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

from __future__ import unicode_literals
from exon.models import Exon
from rest_framework import generics

from exon.drf.serializers import ExonSerializer
from tark_drf.utils.decorators import setup_eager_loading
from exon.drf.filters import ExonFilterBackend
from tark.views import DataTableListApi
from tark.utils.schema_utils import SchemaUtils


class ExonDatatableView(DataTableListApi):
    serializer_class = ExonSerializer
    search_parameters = SchemaUtils.get_field_names(app_name='exon', model_name='exon', exclude_pk=True)
    default_order_by = 1
    queryset = Exon.objects.all()


class ExonList(generics.ListAPIView):
    queryset = Exon.objects.all()
    serializer_class = ExonSerializer
    filter_backends = (ExonFilterBackend, )

    @setup_eager_loading(ExonSerializer)
    def get_queryset(self):
        queryset = Exon.objects.order_by('pk')
        return queryset


class ExonDetail(generics.RetrieveAPIView):
    queryset = Exon.objects.all()
    serializer_class = ExonSerializer
