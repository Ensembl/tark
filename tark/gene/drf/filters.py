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

from rest_framework.filters import BaseFilterBackend
from gene.models import Gene
from tark_drf.utils.drf_fields import CommonFields
from tark_drf.utils.drf_filters import CommonFilterBackend


class GeneFilterBackend(BaseFilterBackend):
    """
    Filter to filter by common fields..
    """

    def filter_queryset(self, request, queryset, view):
        queryset = CommonFilterBackend.get_common_filter_querysets(request, queryset, view)
        queryset = CommonFilterBackend.get_common_related_querysets(request, queryset, view)

        release_short_name = request.query_params.get('release_short_name', None)
        if release_short_name is not None:
            queryset = queryset.filter(gene_release_set__shortname__icontains=release_short_name)

        return queryset

    def get_schema_fields(self, view):
        return CommonFields.get_common_query_set("Gene") + CommonFields.COMMON_RELATED_QUERY_SET + \
               CommonFields.get_expand_query_set(Gene)
