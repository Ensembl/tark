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

from django import template
register = template.Library()


@register.filter
def column_mappings(col_name):
        col_names = {}
        col_names["stable_id"] = "StableID"
        col_names["stable_id_version"] = "Version"
        col_names["loc_start"] = "Start"
        col_names["loc_end"] = "End"
        col_names["loc_strand"] = "Strand"
        col_names["loc_region"] = "Region"
#         col_names["loc_checksum"] = "LocationChecksum"
#         col_names["exon_set_checksum"] = "ExonSetChecksum"
#         col_names["transcript_checksum"] = "TranscriptChecksum"
        col_names["genes"] = "Gene"

        if col_name in col_names:
            return col_names[col_name]

        return col_name
