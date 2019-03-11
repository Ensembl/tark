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
import datetime
register = template.Library()


@register.filter
def format_release_set(search_result, source):

    release_dict = {result["shortname"]: result["release_date"] for result in search_result}

    prefix = ""
    if "ensembl" in source or "lrg" in source:
        prefix = "e"
    elif "refseq" in source:
        prefix = "r"

    sorted_release_dict = sorted(release_dict)
    if len(sorted_release_dict) == 1:
        min_release_shortname = sorted_release_dict[0]
        min_release_date = release_dict[min_release_shortname]
        min_dt = datetime.datetime.strptime(min_release_date, '%Y-%m-%d')
        min_release_value = prefix + min_release_shortname + " (" + datetime.date.strftime(min_dt, "%b%Y") + ")"
        return {'max_release': min_release_shortname, "date_range": min_release_value}
    elif len(sorted_release_dict) > 1:
        min_release_shortname = sorted_release_dict[0]
        min_release_date = release_dict[min_release_shortname]
        min_dt = datetime.datetime.strptime(min_release_date, '%Y-%m-%d')
        min_release_value = prefix + min_release_shortname + " (" + datetime.date.strftime(min_dt, "%b%Y") + ")"

        max_release_shortname = sorted_release_dict[-1]
        max_release_date = release_dict[max_release_shortname]
        max_dt = datetime.datetime.strptime(max_release_date, '%Y-%m-%d')
        max_release_value = prefix + max_release_shortname + " (" + datetime.date.strftime(max_dt, "%b%Y") + ")"

        return {'max_release': max_release_shortname, "date_range": min_release_value + ".." + max_release_value}

    return None


@register.filter
def get_release_as_list(search_result, search_attr):
    search_list = set()

    for result in search_result:
        if "shortname" in search_attr:
            search_list.add(result[search_attr])

    return list(search_list)


@register.filter
def get_values_as_list(search_result, search_attr):
    search_list = set()
    index = 1

    for result in search_result:
        if "stable_id" in search_attr:
            if "stable_id_exon" in search_attr:
                search_list.add(str(result['stable_id']) + "." +
                                str(result['stable_id_version']) +
                                "(" + str(index) + ") ")
                index = index + 1
            else:
                search_list.add(str(result['stable_id']) + "." + str(result['stable_id_version']))
        else:
            search_list.add(str(result[search_attr]))

    search_string_list = ",\n".join(search_list)

    if "stable_id_exon" in search_attr:
        search_string_list = str(len(search_list))

    return search_string_list
