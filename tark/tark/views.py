"""
.. See the NOTICE file distributed with this work for additional information
   regarding copyright ownership.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from __future__ import unicode_literals
from django.shortcuts import render
from release.utils.release_utils import ReleaseUtils
from rest_framework import generics
from django.db.models import Q
from rest_framework.pagination import LimitOffsetPagination
from tark.utils.schema_utils import SchemaUtils
import requests
import json
from django.http.response import JsonResponse
from transcript.models import Transcript
from tark_web.forms import CompareSetForm


def index(request):
    """
    View function for home page
    """
    current_release = ReleaseUtils.get_latest_release()
    # Render the HTML template index.html with data in the context variable
    return render(
        request,
        'index.html',
        context={'current_release': current_release},
    )


class DataTablePagination(LimitOffsetPagination):
        limit_query_param = 'length'
        offset_query_param = 'start'


class DataTableListApi(generics.ListAPIView):
    """
    Base Class for DataTable View
    Provides support for datatable searching, pagination and sorting at server-side
    """
    pagination_class = DataTablePagination
    search_parameters = ()
    unfiltered_query_set = None

    def get_queryset(self):

        latest_release = self.kwargs['release_name']
        latest_assembly = self.kwargs['assembly_name']
        latest_source = self.kwargs['source_name']

        if latest_release is None:
            latest_release = ReleaseUtils.get_latest_release()

        if latest_assembly is None:
            latest_assembly = ReleaseUtils.get_latest_assembly()

        if latest_source is None:
            latest_source = ReleaseUtils.get_default_source()

        self.unfiltered_query_set = query_set = Transcript.objects.filter(
                Q(transcript_release_set__shortname__icontains=latest_release) &
                Q(assembly__assembly_name__icontains=latest_assembly) &
                Q(transcript_release_set__source__shortname__icontains=latest_source))

        order_by_index = int(self.request.query_params.get('order[0][column]', 0))
        orderable = bool(self.request.query_params.get('columns[{}][orderable]'.format(order_by_index), 'false'))

        if order_by_index == 0 or not orderable:
            order_by_index = 1

        order_by = self.request.query_params.get('columns[{}][data]'.format(order_by_index), self.default_order_by).\
            replace('.', '__')
        order_by_dir = self.request.query_params.get('order[0][dir]', 'asc')

        if order_by_dir == 'desc':
            order_by = '-{}'.format(order_by)

        search_queries = self.request.query_params.get('search[value]', '').strip().split(' ')

        q = Q()
        if len(search_queries) > 0 and search_queries[0] != u'':
            for params in self.search_parameters:
                if "genes" == params:
                    for query in search_queries:
                        temp = {
                            '{}__hgnc__name__icontains'.format(params): query,
                        }
                        q |= Q(**temp)
                else:
                    for query in search_queries:
                        if not query.isdigit() and params in ["transcript_id", "stable_id_version", "loc_start",
                                                              "loc_end"]:
                            continue

                        temp = {
                            '{}__icontains'.format(params): query,
                        }
                        q |= Q(**temp)

        query_set = query_set.filter(q).distinct()

        if order_by == '':
            return query_set

        return query_set.order_by(order_by)

    def get(self, request, *args, **kwargs):
        result = super(DataTableListApi, self).get(request, *args, **kwargs)
        result.data['draw'] = int(request.query_params.get('draw', 0))

        result.data['recordsFiltered'] = result.data['count']
        result.data['recordsTotal'] = self.unfiltered_query_set.count()
        del result.data['count']

        result.data['data'] = result.data['results']
        del result.data['results']
        return result



def datatable_view(request, table_name, assembly_name, release_name, source_name, assembly_name_compare, release_name_compare, source_name_compare):  # @IgnorePep8

    server_side_processing = "false"
    if table_name in ['gene', 'transcript', 'translation', 'exon']:
        server_side_processing = "true"

    data_fields = []
    mappings = SchemaUtils.get_app_model_mappings()
    # print(mappings)

    if table_name in mappings:
        data_fields = SchemaUtils.get_field_names(mappings[table_name], table_name,
                                                  exclude_pk=True,
                                                  include_parents_=True,
                                                  exclude_fields=["loc_checksum",
                                                                  "exon_set_checksum",
                                                                  "transcript_checksum"],
                                                  include_fields=["genes"])

    print("server_side_processing " + str(server_side_processing))

    if request.method == 'POST':
        compare_set_form = CompareSetForm(request.POST)
        if compare_set_form.is_valid():
            assembly_name_compare = compare_set_form.cleaned_data['diff_with_assembly']
            release_name_compare = compare_set_form.cleaned_data['diff_with_release']
    else:
        compare_set_form = CompareSetForm()

    return render(request, 'datatable_view.html', {'table_name': table_name,
                                                   "assembly_name": assembly_name,
                                                   "release_name": release_name,
                                                   "source_name": source_name,
                                                   'assembly_name_compare': assembly_name_compare,
                                                   'release_name_compare': release_name_compare,
                                                   'server_side_processing': server_side_processing,
                                                   "source_name_compare": source_name_compare,
                                                   'data_fields': data_fields,
                                                   'form': compare_set_form})


def datatable_fetch(request, table_name):

    draw = request.GET.get('draw', None)
    server_side = request.GET.get('serverSide', False)

    hostname = request.get_host()
    http_protocal = 'https' if request.is_secure() else 'http'

    # print('hostname ' + hostname)
    # print('http_protocal ' + http_protocal)
    host_url = http_protocal + '://' + hostname + '/'
    if draw is None and server_side is False:
        url = host_url + table_name + "/nopagination"
        response = requests.get(url)
        json_data = json.loads(response.text)
        data = {"data": json_data}
        return JsonResponse(data, safe=False)

    return JsonResponse(json_data, safe=False)
