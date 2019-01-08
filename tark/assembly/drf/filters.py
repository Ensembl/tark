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


from rest_framework.filters import BaseFilterBackend
from assembly.models import Assembly
from tark_drf.utils.drf_fields import DrfFields

# Fields
assembly_name_field = DrfFields.assembly_name_field()


class AssemblyExpandFilterBackend(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        return queryset

    def get_schema_fields(self, view):
        return [DrfFields.get_expand_field(Assembly), DrfFields.get_expand_all_field()]


class AssemblyFilterBackend(BaseFilterBackend):
    """
    Filter to filter by assembly_name
    """
    def filter_queryset(self, request, queryset, view):
        assembly_name = request.query_params.get('assembly_name', None)
        if assembly_name is not None:
            queryset = queryset.filter(assembly_name__icontains=assembly_name)

        return queryset

    def get_schema_fields(self, view):
        return [assembly_name_field]


class AssemblySequenceFilterBackend(BaseFilterBackend):
    """
    Filter to filter by assembly_name
    """
    def filter_queryset(self, request, queryset, view):

        assembly_name = request.query_params.get('assembly_name', None)
        if assembly_name is not None:
            queryset = queryset.filter(assembly__assembly_name__icontains=assembly_name)
        return queryset

    def get_schema_fields(self, view):
        return [assembly_name_field]
