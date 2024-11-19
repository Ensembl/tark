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

# from django.conf.urls import url
from django.urls import re_path
from tark_web import views

from tark.views import datatable_view, datatable_fetch
from assembly.views import AssemblyDatatableView
from transcript.views import TranscriptDatatableView
from gene.views import GeneDatatableView
from exon.views import ExonDatatableView
from sequence.views import align_sequence, check_service_status, \
    align_cds_sequence, call_align_sequence_clustal
from release.views import ReleaseSetDatatableView
from tark_web.views import datatable_view_release_set, feature_diff, statistics, manelist
from django.views.generic.base import TemplateView

urlpatterns = [
    re_path(r'^$', views.web_home, name='web_home'),

    # diff
    re_path(r'^diff/$', views.diff_home, name='diff_home'),
    re_path(r'^diff/release/$', views.diff_release_home, name='diff_home_release'),

    # search
    re_path(r'^search/$', views.search_home, name='search_home'),
    re_path(r'^search_link/(?P<search_identifier>[a-zA-Z0-9\.\-\_\:\>]+)$', views.search_link, name='search_link'),

    re_path(r'^sequence/(?P<feature_type>[\w]+)/(?P<stable_id>[\w\-\.]+)/(?P<stable_id_version>[\w]+)/(?P<release_short_name>[\w]+)/(?P<assembly_name>[\w]+)/(?P<source_name>[\w]+)/(?P<output_format>[\w]+)/$',
        views.fetch_sequence,
        name='fetch_sequence'),

    re_path(r'^sequence/(?P<feature_type>[\w]+)/(?P<stable_id>[\w\-\.]+)/(?P<stable_id_version>[\w]+)/(?P<release_short_name>[\w]+)/(?P<assembly_name>[\w]+)/(?P<source_name>[\w]+)/(?P<seq_type>[\w]+)/(?P<output_format>[\w]+)/$',
        views.fetch_sequence,
        name='fetch_cds_sequence'),

    re_path(r'^alignsequence/(?P<feature_type>[\w]+)/(?P<stable_id_a>[\w\-\.]+)/(?P<stable_id_version_a>[\w]+)/(?P<stable_id_b>[\w\-\.]+)/(?P<stable_id_version_b>[\w]+)/(?P<input_type>[\w]+)/(?P<outut_format>[\w]+)/',
        align_sequence, name='align_sequence'),

    re_path(r'^call_align_sequence_clustal/$',
        call_align_sequence_clustal, name='call_align_sequence_clustal'),

    re_path(r'^aligncdssequence/(?P<feature_type>[\w]+)/(?P<stable_id_a>[\w\-\.]+)/(?P<stable_id_version_a>[\w]+)/(?P<release_short_name_a>[\w]+)/(?P<assembly_name_a>[\w]+)/(?P<source_name_a>[\w]+)/(?P<stable_id_b>[\w\-\.]+)/(?P<stable_id_version_b>[\w]+)/(?P<release_short_name_b>[\w]+)/(?P<assembly_name_b>[\w]+)/(?P<source_name_b>[\w]+)/(?P<cds_type>[\w]+)/(?P<output_format>[\w]+)/',
        align_cds_sequence,
        name='align_cds_sequence'),

    #  datatables
    re_path(
        r'^datatable/release_set/',
        datatable_view_release_set,
        name="datatable_view_release_set"
    ),

    re_path(
        r'^datatable/(?P<table_name>[\w]+)/(?P<assembly_name>[\w]+)/(?P<release_name>[\w]+)/(?P<source_name>[\w]+)/(?P<assembly_name_compare>[\w]+)/(?P<release_name_compare>[\w]+)/(?P<source_name_compare>[\w]+)/',
        # pylint:disable=line-too-long
        datatable_view,
        name="datatable_view"
    ),

    re_path(
        r'^datatable_clientside/(?P<table_name>[\w]+)/',
        datatable_fetch,
        name="datatablefetch_clientside"
    ),

    re_path(
        r'^datatable_serverside/assembly',
        AssemblyDatatableView.as_view(),
        name="datatablefetch_serverside_assembly"
    ),

    re_path(
        r'^datatable_serverside/transcript/(?P<assembly_name>[\w]+)/(?P<release_name>[\w]+)/(?P<source_name>[\w]+)/',
        # pylint:disable=line-too-long
        TranscriptDatatableView.as_view(),
        name="datatablefetch_serverside_transcript"
    ),

    re_path(
        r'^datatable_serverside/gene/(?P<assembly_name>[\w]+)/(?P<release_name>[\w]+)/',  # pylint:disable=line-too-long
        GeneDatatableView.as_view(),
        name="datatablefetch_serverside_gene"
    ),

    re_path(
        r'^datatable_serverside/exon/(?P<assembly_name>[\w]+)/(?P<release_name>[\w]+)/',  # pylint:disable=line-too-long
        ExonDatatableView.as_view(),
        name="datatablefetch_serverside_exon"
    ),

    re_path(
        r'^datatable_serverside/release_set/',
        ReleaseSetDatatableView.as_view(),
        name="datatablefetch_serverside_release"
    ),

    re_path(
        r'statistics/(?P<feature>[\w]+)/(?P<from_release>[\w]+)/(?P<to_release>[\w]+)/(?P<source>[\w]+)/(?P<direction>[\w]+)',
        feature_diff,
        name="feature_diff"
    ),

    re_path(
        r'statistics',
        statistics,
        name="statistics"
    ),

    re_path(
        r'^ajax/load-releases/',
        views.load_releases,
        name='ajax_load_releases'
    ),
    # commented old mane list 
    # re_path(
    #    r'^manelist/$',
    #    TemplateView.as_view(
    #        template_name='mane_list.html'
    #    )
    # ),

    # new mane list page
    re_path(
        r'^manelist/$',
        manelist,
        name="manelist"
    ),

    # new mane GRCh37 page
    re_path(
        r'^mane_GRCh37_list/$',
        TemplateView.as_view(
                   template_name='mane_GRCh37_list.html'
               )
    ),

    re_path(
        r'^mane_project/$',
        TemplateView.as_view(
            template_name='mane_project.html'
        ),
        name="mane_project"
    ),

    re_path(
        r'^about_mane_collaboration/$',
        TemplateView.as_view(
            template_name='mane_collaboration_about.html'
        ),
        name="about_mane_collaboration"
    ),

    re_path(
        r'^access_mane_data/$',
        TemplateView.as_view(
            template_name='mane_data_access.html'
        ),
        name="access_mane_data"
    ),

    re_path(
        r'^mane_feedback/$',
        TemplateView.as_view(
            template_name='mane_feedback.html'
        ),
        name="mane_feedback"
    ),

    re_path(
        r'^view_alignment/$',
        TemplateView.as_view(
            template_name='alignment_viewer.html'
        )
    ),

    re_path(
        r'^transcript_details/(?P<stable_id_with_version>[a-zA-Z0-9\.\_]+)(?:/(?P<search_identifier>[a-zA-Z0-9\.\-\_\:\>]+))?/$',
        # pylint:disable=line-too-long
        views.transcript_details,
        name='transcript_details'
    ),

    re_path(r'^check_service_status/(?P<job_id>[a-zA-Z0-9\.\_\-]+)$', check_service_status, name='check_service_status')
]
