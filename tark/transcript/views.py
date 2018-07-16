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

from __future__ import unicode_literals
from rest_framework import generics
from tark_drf.utils.decorators import setup_eager_loading, expand_all_related
from transcript.models import Transcript
from transcript.drf.serializers import TranscriptSerializer,\
    TranscriptDiffSerializer, TranscriptSearchSerializer
from transcript.drf.filters import TranscriptFilterBackend,\
    TranscriptDiffFilterBackend, TranscriptSearchFilterBackend
from tark.utils.diff_utils import DiffUtils
from release.utils.release_utils import ReleaseUtils
from tark.views import DataTableListApi
from tark.utils.schema_utils import SchemaUtils
from django_filters.rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q


class TranscriptList(generics.ListAPIView):
    queryset = Transcript.objects.all()
    serializer_class = TranscriptSerializer
    filter_backends = (TranscriptFilterBackend, )

    @setup_eager_loading(TranscriptSerializer)
    def get_queryset(self):
        queryset = Transcript.objects.order_by('pk')
        return queryset


class TranscriptDatatableView(DataTableListApi):
    serializer_class = TranscriptSerializer
    search_parameters = SchemaUtils.get_field_names(app_name='transcript', model_name='transcript', exclude_pk=False)
    default_order_by = 1
    
    # queryset = Transcript.objects.all()
#     latest_release = ReleaseUtils.get_latest_release()
#     latest_assembly = ReleaseUtils.get_latest_assembly()
#     print(" Lastest assembly : " + str(latest_assembly))
#     print(" Lastest release : " + str(latest_release))
#     queryset = Transcript.objects.filter(Q(transcript_release_set__shortname__icontains=latest_release) &
#                                          Q(assembly__assembly_name__icontains=latest_assembly))


class TranscriptDetail(generics.RetrieveAPIView):
    queryset = Transcript.objects.all()
    serializer_class = TranscriptSerializer(queryset, many=True)


class TranscriptDiff(generics.ListAPIView):
    queryset = Transcript.objects.all()
    serializer_class = TranscriptDiffSerializer
    filter_backends = (TranscriptDiffFilterBackend, )

#     @expand_all_related(TranscriptDiffSerializer)
#     def get_queryset(self):
#         queryset = Transcript.objects.order_by('pk')
#         return queryset
    # @setup_eager_loading(TranscriptDiffSerializer)
    def get(self, request, *args, **kwargs):
        diff_me_stable_id = request.query_params.get('diff_me_stable_id', None)
        diff_with_stable_id = request.query_params.get('diff_with_stable_id', None)

        diff_me_release = request.query_params.get('diff_me_release', None)
        diff_with_release = request.query_params.get('diff_with_release', ReleaseUtils.get_latest_release())

        diff_me_assembly = request.query_params.get('diff_me_assembly', None)
        diff_with_assembly = request.query_params.get('diff_with_assembly', ReleaseUtils.get_latest_assembly())

        diff_me_source = request.query_params.get('diff_me_source', ReleaseUtils.get_default_source())
        diff_with_source = request.query_params.get('diff_with_source', ReleaseUtils.get_default_source())

        expand = request.query_params.get('expand', "transcript_release_set")

        print("===========GET===================\n")
        print("Diff Me Stable id " + str(diff_me_stable_id) + "Diff With Stable id " + str(diff_with_stable_id) +
              "Diff me " + str(diff_me_release) +
              "Diff with " + str(diff_with_release) + "expand " + expand)

        params = {'diff_me_stable_id': diff_me_stable_id, 'diff_with_stable_id': diff_with_stable_id,
                  'diff_me_release': diff_me_release, 'diff_with_release': diff_with_release,
                  'diff_me_assembly': diff_me_assembly, 'diff_with_assembly': diff_with_assembly,
                  'diff_me_source': diff_me_source, 'diff_with_source': diff_with_source,
                  'expand': expand}

        result = super(TranscriptDiff, self).get(request, *args, **kwargs)
        updated_result = DiffUtils.get_diff_dict(request, result, params)
        print("========UPDATED RESULT START======\n")
        print(updated_result)
        print("========UPDATED RESULT END=======\n")
        return updated_result


class NotPaginatedSetPagination(PageNumberPagination):
    page_size = None


class TranscriptSearch(generics.ListAPIView):
    queryset = Transcript.objects.all()
    serializer_class = TranscriptSearchSerializer
    filter_backends = (TranscriptSearchFilterBackend, )
    pagination_class = NotPaginatedSetPagination

    @expand_all_related(TranscriptDiffSerializer)
    def get_queryset(self):
        queryset = Transcript.objects.order_by('pk')
        return queryset

    def get(self, request, *args, **kwargs):

        result = super(TranscriptSearch, self).get(request, *args, **kwargs)
        return result
