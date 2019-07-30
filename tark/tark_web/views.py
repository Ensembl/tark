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

import os

from django.shortcuts import render
from release.utils.release_utils import ReleaseUtils
from .forms import DiffForm
import requests
from tark_web.forms import SearchForm, FormUtils, DiffFormRelease
import json
import logging
from tark_web.utils.apiutils import ApiUtils
from django.urls.base import resolve
from tark.utils.exon_utils import ExonUtils
from tark_web.utils.sequtils import TarkSeqUtils
from setuptools.dist import sequence

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
    diff_release = False

    if request.method == 'POST':
        form = DiffForm(request.POST)
        if form.is_valid():
            form_data_dict = form.get_cleaned_data()

            transcript_diff_url = ApiUtils.get_feature_diff_url(request, "transcript", form_data_dict)
            response = requests.get(transcript_diff_url)

            if response.status_code == 200:
                diff_result = response.json()
                # print(diff_result)

            return render(request, 'diff_compare_result.html',
                          context={'form': form,
                                   'diff_result': diff_result,
                                   'diff_release': diff_release,
                                   'form_data_dict': form_data_dict})
        else:
            logger.error(form.errors)
    else:
        form = DiffForm()

    return render(request, 'tark_diff.html', context={'form': form,
                                                      'diff_release': diff_release,
                                                      })


def diff_release_home(request):
    """
    View function for diff query page
    """
    # Render the HTML template index.html with data in the context variable
    current_url = resolve(request.path_info).url_name

    if "diff_home_release" in current_url:
        diff_release = True

    if request.method == 'POST':
        form = DiffFormRelease(request.POST)
        if form.is_valid():
            form_data_dict = form.get_cleaned_data()

            diff_dict = {}
            diff_dict['release_set_1'] = {"source": form_data_dict["diff_me_source"].lower(),
                                          "assembly": form_data_dict["diff_me_assembly"].lower(),
                                          "version": form_data_dict["diff_me_release"]}

            diff_dict['release_set_2'] = {"source":  form_data_dict["diff_with_source"].lower(),
                                          "assembly": form_data_dict["diff_with_assembly"].lower(),
                                          "version": form_data_dict["diff_with_release"]}

            diff_result_release = ReleaseUtils.get_release_diff(diff_dict)

            return render(request, 'diff_compare_release_set_result.html',
                          context={'form': form,
                                   'diff_release': diff_release,
                                   'diff_result_release': json.dumps(diff_result_release),
                                   'form_data_dict': json.dumps(form_data_dict)})
        else:
            logger.error(form.errors)
    else:
        form = DiffForm()
    return render(request, 'release_diff.html', context={'form': form})


def show_fasta(request, sequence_data, stable_id, stable_id_version, outut_format="fasta"):

    return render(request, 'sequence_fasta.html', context={'sequence_data': sequence_data,
                                                           'stable_id': stable_id + '.' + stable_id_version,
                                                           })


def fetch_sequence(request, feature_type, stable_id, stable_id_version,
                   release_short_name=None, assembly_name=None, source_name=None,
                   seq_type=None, output_format="fasta"):

    if seq_type is not None and seq_type in ["cds", "five_prime", "three_prime"]:
        sequence_data = TarkSeqUtils.fetch_cds_sequence(request, feature_type, stable_id, stable_id_version,
                                                        release_short_name, assembly_name, source_name,
                                                        seq_type, output_format)
    else:
        sequence_data = TarkSeqUtils.fetch_fasta_sequence(request, feature_type, stable_id, stable_id_version,
                                                          release_short_name, assembly_name, source_name,
                                                          output_format)

    return render(request, 'sequence_fasta.html', context={'sequence_data': sequence_data,
                                                           'stable_id': stable_id + '.' + stable_id_version,
                                                           })


def search_link(request, search_identifier):

    search_form = SearchForm(request.POST)
    host_url = ApiUtils.get_host_url(request)

    query_url = "/api/transcript/search/?identifier_field=" + search_identifier + \
        "&expand=transcript_release_set,genes"
    response = requests.get(host_url + query_url)
    if response.status_code == 200:
        search_result = response.json()
        return render(request, 'search_result.html', context={'form': search_form,
                                                              'search_result': search_result,
                                                              'search_identifier': search_identifier})


def search_home(request):
    """
    View function for search query page
    """
    host_url = ApiUtils.get_host_url(request)
    search_identifier = ""
    query_url = "/api/transcript/search/?expand=transcript_release_set,genes&identifier_field="

    # Render the HTML template index.html with data in the context variable
    search_result = {}
    if request.method == 'GET' and "identifier" in request.GET:

        search_identifier = request.GET['identifier']
        if search_identifier is not None:
            # replace white space
            search_identifier = search_identifier.replace(" ", "")
            search_form = SearchForm(request.GET)
            query_url = query_url+search_identifier
            response = requests.get(host_url + query_url)
            if response.status_code == 200:
                search_result = response.json()
                return render(
                    request,
                    'search_result.html',
                    context={
                        'form': search_form,
                        'search_result': search_result,
                        'search_identifier': search_identifier
                    }
                )
            else:
                logger.error("Error from search")

        else:
            search_form = SearchForm()
    elif request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():

            search_identifier = search_form.cleaned_data['search_identifier']
            # replace white space
            search_identifier = search_identifier.replace(" ", "")
            query_url = query_url+search_identifier
            response = requests.get(host_url + query_url)
            if response.status_code == 200:
                search_result = response.json()
                return render(
                    request,
                    'search_result.html',
                    context={
                        'form': search_form,
                        'search_result': search_result,
                        'search_identifier': search_identifier
                    }
                )
            else:
                logger.error("Error from search")
        else:
            logger.error(search_form.errors)
    else:
        search_form = SearchForm()

    return render(request, 'tark_search.html', context={'form': search_form})


def load_releases(request):
    assembly_name = request.GET.get('assembly_name')
    rleases = FormUtils.get_all_release_name_tuples(assembly_name)
    return render(request, 'populate_release.html', {'releases': rleases})


def datatable_view_release_set(request):
    return render(request, 'datatable_view_release_set.html')


def statistics(request):

    reports = ReleaseUtils.get_release_loading_stats()

    return render(
        request,
        'statistics_view.html',
        context={
            'reports': reports
        }
    )


def transcript_details(request, stable_id_with_version, search_identifier):
    host_url = ApiUtils.get_host_url(request)

    # get transcript details
    query_url_details = "/api/transcript/stable_id_with_version/?stable_id_with_version=" + stable_id_with_version + \
        "&expand=transcript_release_set,genes"
    response = requests.get(host_url + query_url_details)
    transcript_details = {}
    if response.status_code == 200:
        search_result = response.json()
        if "results" in search_result and len(search_result["results"]) > 0:
            transcript_details = search_result["results"][0]
    else:
        logger.error("Error")

    # get transcript history
    transcript_history = {}
    if '.' in stable_id_with_version:
        (identifier, identifier_version) = stable_id_with_version.split('.')  # @UnusedVariable

        query_url_history = "/api/transcript/?stable_id=" + identifier + \
            "&expand=transcript_release_set"
        response = requests.get(host_url + query_url_history)

        if response.status_code == 200:
            search_result = response.json()
            if "results" in search_result:
                transcript_history = search_result["results"]

    return render(request, 'transcript_details.html', context={'transcript_details': transcript_details,
                                                               'transcript_history': transcript_history,
                                                               'search_identifier': search_identifier,
                                                               'stable_id_with_version': stable_id_with_version})
