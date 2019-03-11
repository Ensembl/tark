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
from tark.views import DataTableListApi
from tark.utils.schema_utils import SchemaUtils
from rest_framework.pagination import PageNumberPagination
from tark_web.utils.apiutils import ApiUtils
import requests
from translation.models import Translation
from rest_framework.response import Response
from tark.utils.request_utils import RequestUtils
from exon.models import Exon


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

        render_as_string = request.query_params.get("render_as_string", "False")
        print("==========render_as_string========== " + str(render_as_string) + "========")
        # get diff me transcript
        params_diff_me = RequestUtils.get_query_params(request, "diff_me")
        diff_me_transcript = self.get_search_results(request, params_diff_me, attach_translation_seq=True,
                                                     attach_exon_seq=True)
        print("diff_me_transcript==========")
        print(diff_me_transcript)

        # get diff with trancscript
        params_diff_with = RequestUtils.get_query_params(request, "diff_with")
        diff_with_transcript = self.get_search_results(request, params_diff_with, attach_translation_seq=True,
                                                       attach_exon_seq=True)
        print("diff_with_transcript=========")
        print(diff_with_transcript)

        # compare the two transcripts
        compare_results = DiffUtils.compare_transcripts(diff_me_transcript, diff_with_transcript)

        print("===========compare_results===============")
        print(compare_results)

        if "True" in render_as_string:
            print("Return render as string ..............")
            from django.template.loader import render_to_string
            gene_include_html = render_to_string('gene_include.html', {'diff_result': compare_results})
            transcript_include_html = render_to_string('transcript_include.html', {'diff_result': compare_results})
            translation_include_html = render_to_string('translation_include.html', {'diff_result': compare_results})
            exonset_include_html = render_to_string('exonset_include.html', {'diff_result': compare_results})
            rendered_result = {"gene": gene_include_html, "transcript": transcript_include_html,
                               "translation": translation_include_html,
                               "exonset": exonset_include_html}
            return Response(rendered_result)

        return Response(compare_results)

    def get_search_results(self, request, diff_query_params, attach_translation_seq=True, attach_exon_seq=True,
                           attach_gene=True):

        host_url = ApiUtils.get_host_url(request)
        query_url = "/api/transcript/?"

        query_param_string = RequestUtils.get_query_param_string(diff_query_params)
        query_url = query_url + query_param_string

        response = requests.get(host_url + query_url)
        if response.status_code == 200:
            search_result = response.json()

        if search_result is not None and "count" in search_result and search_result["count"] == 1 and "results" in search_result:  # @IgnorePep8
            search_result = search_result["results"][0]

            if "transcript_release_set" in search_result:
                for release_set in search_result["transcript_release_set"]:
                    if "release_short_name" in diff_query_params and "shortname" in release_set:
                        if diff_query_params["release_short_name"] == release_set["shortname"]:
                            search_result["transcript_release_set"] = release_set

            if attach_translation_seq is True:
                if "translations" in search_result and len(search_result["translations"]) > 0:
                    print(search_result["translations"])
                    print(len(search_result["translations"]))
                    translation = search_result["translations"][0]
                    #translation = search_result["translations"]
                    if "translation_id" in translation:
                        tl_translation_id = translation["translation_id"]
                        tl_query_set = Translation.objects.filter(translation_id=tl_translation_id).select_related('sequence')  # @IgnorePep8
                        if tl_query_set is not None and len(tl_query_set) == 1:
                            tl_obj = tl_query_set[0]
                            translation["sequence"] = tl_obj.sequence.sequence
                            translation["seq_checksum"] = tl_obj.sequence.seq_checksum
                            search_result["translations"] = translation

            if attach_exon_seq is True:
                if "exons" in search_result:
                    all_exons = search_result["exons"]
                    new_exons = []
                    for exon in all_exons:
                        if "exon_id" in exon:
                            current_exon_query_set = Exon.objects.filter(exon_id=exon["exon_id"]).select_related('sequence')  # @IgnorePep8

                            if current_exon_query_set is not None and len(current_exon_query_set) == 1:
                                current_exon_with_sequence = current_exon_query_set[0]
                                exon["sequence"] = current_exon_with_sequence.sequence.sequence
                                exon["seq_checksum"] = current_exon_with_sequence.sequence.seq_checksum
                                new_exons.append(exon)

                    if len(new_exons) > 0:
                        search_result["exons"] = new_exons

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
