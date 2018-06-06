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
from rest_framework.filters import BaseFilterBackend
from tark_web.utils.sequtils import TarkSeqUtils


class CommonFilterBackend(BaseFilterBackend):

    @classmethod
    def get_common_filter_querysets(cls, request, queryset, view):
        stable_id = request.query_params.get('stable_id', None)
        if stable_id is not None:
            queryset = queryset.filter(stable_id=stable_id)

        stable_id_version = request.query_params.get('stable_id_version', None)
        if stable_id_version is not None:
            queryset = queryset.filter(stable_id_version=stable_id_version)

        loc_region = request.query_params.get('loc_region', None)
        if loc_region is not None:
            queryset = queryset.filter(loc_region=loc_region)

        loc_start = request.query_params.get('loc_start', None)
        if loc_start is not None:
            queryset = queryset.filter(loc_start__lte=loc_start).filter(loc_end__gte=loc_start)

        loc_end = request.query_params.get('loc_end', None)
        if loc_end is not None:
            queryset = queryset.filter(loc_start__lte=loc_end).filter(loc_end__gte=loc_end)

        return queryset

    @classmethod
    def get_common_related_querysets(cls, request, queryset, view):
        assembly_name = request.query_params.get('assembly_name', None)
        if assembly_name is not None:
            queryset = queryset.filter(assembly__assembly_name__icontains=assembly_name)

        return queryset

    @classmethod
    def get_location_filter_querysets(cls, request, queryset, view):
        loc_string = request.query_params.get('location', None)

        # 5: 62797383-63627669
        (loc_region, loc_start, loc_end) = TarkSeqUtils.parse_location_string(loc_string)

        # loc_region = request.query_params.get('loc_region', None)
        if loc_region is not None:
            queryset = queryset.filter(loc_region=loc_region)

        # loc_start = request.query_params.get('loc_start', None)
        if loc_start is not None:
            queryset = queryset.filter(loc_start__lte=loc_start).filter(loc_end__gte=loc_start)

        # loc_end = request.query_params.get('loc_end', None)
        if loc_end is not None:
            queryset = queryset.filter(loc_start__lte=loc_end).filter(loc_end__gte=loc_end)

        return queryset
