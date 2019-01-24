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
from django.shortcuts import render
from release.utils.release_utils import ReleaseUtils
from .forms import DiffForm
import requests
from tark_web.forms import SearchForm, FormUtils
import json
import logging
from tark_web.utils.apiutils import ApiUtils
# Get an instance of a logger
logger = logging.getLogger("tark")


def web_home(request):
    """
    View function for home page
    """
    # Render the HTML template web_home.html with data in the context variable
    return render(
        request,
        'web_home.html'
     )


def diff_home(request):
    """
    View function for diff query page
    """
    # Render the HTML template index.html with data in the context variable
    diff_result = {}
    if request.method == 'POST':
        print("reached if")
        form = DiffForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            form_data_dict = form.get_cleaned_data()
            print("=======form_data_dict============")
            print(form_data_dict)

            transcript_diff_url = ApiUtils.get_feature_diff_url(request, "transcript", form_data_dict)
            response = requests.get(transcript_diff_url)
            print(response.status_code)
            if response.status_code == 200:
                diff_result = response.json()

            print("========diff_result========")
            print(diff_result)
            print("==================")
            return render(request, 'diff_compare_result.html',
                          context={'form': form,
                                   'diff_result': diff_result,
                                   'form_data_dict': form_data_dict })
#             return render(request, 'diff_result.html', context={'form': form,
#                                                                 'diff_result': diff_result})
        else:
            print("Reached else1")
            print(form.errors)
    else:
        print("Reached else2")

        form = DiffForm()
    return render(request, 'tark_diff.html', context={'form': form,
                                                      })


def search_home(request):
    """
    View function for search query page
    """

    # Render the HTML template index.html with data in the context variable
    search_result = {}
    if request.method == 'POST':
        print("reached if")
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            print("Form is valid")
            search_identifier = search_form.cleaned_data['search_identifier']
#             search_assembly = search_form.cleaned_data['search_assembly']
#             search_release = search_form.cleaned_data['search_release']

            print("Stable id " + search_identifier)
#             print("assembly " + search_assembly)
#             print("release " + search_release)
            host_url = ApiUtils.get_host_url(request)

#             query_url = "/api/transcript/search/?identifier_field=" + search_identifier + \
#                         "&expand_all=true&search_release=" + search_release + \
#                 "&search_assembly=" + search_assembly
            query_url = "/api/transcript/search/?identifier_field=" + search_identifier + \
                        "&expand_all=true"
            response = requests.get(host_url + query_url)
            print(response.status_code)
            if response.status_code == 200:
                print("Reached if ")
                search_result = response.json()
                #print(search_result)
                return render(request, 'search_result.html', context={'form': search_form,
                                                                      'search_result': search_result})
            else:
                print("Error")
        else:
            print("Reached else1")
            print(search_form.errors)
    else:
        print("Reached else2")

        search_form = SearchForm()
    return render(request, 'tark_search.html', context={'form': search_form })

def load_releases(request):
    assembly_name = request.GET.get('assembly_name')
    rleases = FormUtils.get_all_release_name_tuples(assembly_name)
    return render(request, 'populate_release.html', {'releases': rleases})


def datatable_view_release_set(request):
    return render(request, 'datatable_view_release_set.html')
    #return render(request, 'datatable_view_release_set.html', {'release_set_data': json.dumps(release_set_json)})

def release_set_stats_view(request):
    diff_dict = {}
    diff_dict['release_set_1'] = {"source":"ensembl", "assembly":"grch38", "version": 93}
    diff_dict['release_set_2'] = {"source":"ensembl", "assembly":"grch38", "version": 94}

    ReleaseUtils.get_release_diff(diff_dict)



