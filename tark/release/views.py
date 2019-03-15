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
from rest_framework import generics
from tark.views import DataTableListApi
from tark.utils.schema_utils import SchemaUtils
from release.models import ReleaseSource, ReleaseSet,\
    TranscriptReleaseTagRelationship
from release.drf.serializers import ReleaseSourceSerializer,\
    ReleaseSetSerializer
from release.drf.filters import ReleaseSetFilterBackend
from rest_framework.pagination import PageNumberPagination
from tark_drf.utils.decorators import setup_eager_loading
from transcript.drf.serializers import TranscriptReleaseTagRelationshipSerializer


# ============For Datatables========
class NotPaginatedSetPagination(PageNumberPagination):
    page_size = None


class ReleaseSourceList(generics.ListAPIView):
    queryset = ReleaseSource.objects.all()
    serializer_class = ReleaseSourceSerializer


class ReleaseSourceDetail(generics.RetrieveAPIView):
    queryset = ReleaseSource.objects.all()
    serializer_class = ReleaseSourceSerializer


class ReleaseSourceDatatableView(DataTableListApi):
    serializer_class = ReleaseSourceSerializer
    search_parameters = SchemaUtils.get_field_names(app_name='release', model_name='releasesource', exclude_pk=False)
    default_order_by = 3
    queryset = ReleaseSource.objects.all()


class ReleaseSetList(generics.ListAPIView):
    queryset = ReleaseSet.objects.all()
    serializer_class = ReleaseSetSerializer
    filter_backends = (ReleaseSetFilterBackend, )


class ReleaseSetDetail(generics.RetrieveAPIView):
    queryset = ReleaseSet.objects.all()
    serializer_class = ReleaseSetSerializer


class TranscriptReleaseTagRelationshipList(generics.ListAPIView):
    queryset = TranscriptReleaseTagRelationship.objects.all()
    serializer_class = TranscriptReleaseTagRelationshipSerializer


class TranscriptReleaseTagRelationshipListAll(generics.ListAPIView):
    queryset = TranscriptReleaseTagRelationship.objects.all()
    serializer_class = TranscriptReleaseTagRelationshipSerializer
    pagination_class = None


class ReleaseSetDatatableView(generics.ListAPIView):
    serializer_class = ReleaseSetSerializer
    pagination_class = NotPaginatedSetPagination

    @setup_eager_loading(ReleaseSetSerializer)
    def get_queryset(self):
        queryset = ReleaseSet.objects.order_by('pk')
        return queryset
