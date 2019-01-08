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
from tark_drf.utils.decorators import setup_eager_loading, expand_all_related
from transcript.models import Transcript
from transcript.drf.serializers import TranscriptSerializer,\
    TranscriptDiffSerializer, TranscriptSearchSerializer,\
    TranscriptDataTableSerializer
from transcript.drf.filters import TranscriptFilterBackend,\
    TranscriptDiffFilterBackend, TranscriptSearchFilterBackend
from tark.utils.diff_utils import DiffUtils
from release.utils.release_utils import ReleaseUtils
from tark.views import DataTableListApi
from tark.utils.schema_utils import SchemaUtils
from rest_framework.pagination import PageNumberPagination
from tark_web.utils.apiutils import ApiUtils
import requests
from tark_web.templatetags import search_result_formatter
from translation.models import Translation
import json
from rest_framework.response import Response
from tark.utils.request_utils import RequestUtils
from lib2to3.tests.pytree_idempotency import diff


class TranscriptList(generics.ListAPIView):
    queryset = Transcript.objects.all()
    serializer_class = TranscriptSerializer
    filter_backends = (TranscriptFilterBackend, )

    @setup_eager_loading(TranscriptSerializer)
    def get_queryset(self):
        queryset = Transcript.objects.order_by('pk')
        return queryset


class TranscriptDatatableView(DataTableListApi):
    # serializer_class = TranscriptSerializer
    serializer_class = TranscriptDataTableSerializer
    search_parameters = SchemaUtils.get_field_names(app_name='transcript', model_name='transcript', exclude_pk=False,
                                                    include_parents_=True,
                                                    exclude_fields=["loc_strand", "loc_region", "loc_checksum",
                                                                    "exon_set_checksum",
                                                                    "transcript_checksum"],
                                                    include_fields=["genes"])
    # search_parameters.append("genes")
    default_order_by = 1


class TranscriptDetail(generics.RetrieveAPIView):
    queryset = Transcript.objects.all()
    serializer_class = TranscriptSerializer(queryset, many=True)


class TranscriptDiff(generics.ListAPIView):
    queryset = Transcript.objects.all()
    serializer_class = TranscriptDiffSerializer
    filter_backends = (TranscriptDiffFilterBackend, )

    def get(self, request, *args, **kwargs):

        # get diff me transcript
        params_diff_me = RequestUtils.get_query_params(request, "diff_me")
        diff_me_transcript = self.get_search_results(request, params_diff_me, True)
        print("diff_me_transcript==========")
        print(diff_me_transcript)

        # get diff with trancscript
        params_diff_with = RequestUtils.get_query_params(request, "diff_with")
        diff_with_transcript = self.get_search_results(request, params_diff_with, True)
        print("diff_with_transcript=========")
        print(diff_with_transcript)

        # compare the two transcripts
        compare_results = DiffUtils.compare_transcripts(diff_me_transcript, diff_with_transcript)

        # for tark rest, add count, previous, next
        #compare_result_response_body = DiffUtils.get_results_as_response_body(compare_results)

        print("===========compare_results===============")
        print(compare_results)
        return Response(compare_results)

    def get_search_results(self, request, diff_query_params, attach_translation_seq=True, attach_gene=True):

        host_url = ApiUtils.get_host_url(request)
        query_url = "/api/transcript/?"

        query_param_string = RequestUtils.get_query_param_string(diff_query_params)
        query_url = query_url + query_param_string
        print("==========query url==============")
        print(query_url)

        response = requests.get(host_url + query_url)
        if response.status_code == 200:
            search_result = response.json()
            
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        print(search_result)
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        
        if search_result is not None and "count" in search_result and search_result["count"] == 1 and "results" in search_result:  # @IgnorePep8
            search_result = search_result["results"][0]

            if "transcript_release_set" in search_result:
                for release_set in search_result["transcript_release_set"]:
                    if "release_short_name" in diff_query_params and "shortname" in release_set:
                        if diff_query_params["release_short_name"] == release_set["shortname"]:
                            search_result["transcript_release_set"] = release_set

            if attach_translation_seq is True:
                if "translations" in search_result:
                    translation = search_result["translations"][0]
                    if "translation_id" in translation:
                        tl_translation_id = translation["translation_id"]
                        tl_query_set = Translation.objects.filter(translation_id=tl_translation_id).select_related('sequence')  # @IgnorePep8
                        print("===========tl_query_et========")
                        print(tl_query_set)
                        if tl_query_set is not None and len(tl_query_set) == 1:
                            tl_obj = tl_query_set[0]
                            print("Entering tl_query_set================")
                            print(tl_obj.sequence.sequence)
                            translation["sequence"] = tl_obj.sequence.sequence
                            translation["seq_checksum"] = tl_obj.sequence.seq_checksum
                            search_result["translations"] = translation
            if attach_gene is True:
                if "genes" in search_result:
                    gene = search_result["genes"][0]
                    search_result["gene"] = gene

        return search_result


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
