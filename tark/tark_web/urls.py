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


from django.conf.urls import url
from tark_web import views

from tark.views import datatable_view, datatable_fetch
from assembly.views import AssemblyDatatableView
from transcript.views import TranscriptDatatableView
from gene.views import GeneDatatableView
from exon.views import ExonDatatableView
from release.views import ReleaseSetDatatableView
from tark_web.views import datatable_view_release_set
from django.views.generic.base import TemplateView


urlpatterns = [
    url(r'^$', views.web_home, name='web_home'),
    # diff
    url(r'^diff/$', views.diff_home, name='diff_home'),
    url(r'^diff/release/$', views.diff_release_home, name='diff_home_release'),

    # search
    url(r'^search/$', views.search_home, name='search_home'),
    url(r'^sequence/(?P<feature_type>[\w]+)/(?P<stable_id>[\w]+)/(?P<stable_id_version>[\w]+)/(?P<outut_format>[\w]+)/',
        views.fetch_sequence, name='fetch_sequence'),

    #  datatables
    url(r'^datatable/release_set/', datatable_view_release_set, name="datatable_view_release_set"),

    url(r'^datatable/(?P<table_name>[\w]+)/(?P<assembly_name>[\w]+)/(?P<release_name>[\w]+)/(?P<source_name>[\w]+)/(?P<assembly_name_compare>[\w]+)/(?P<release_name_compare>[\w]+)/(?P<source_name_compare>[\w]+)/',  # @IgnorePep8
        datatable_view, name="datatable_view"),
    url(r'^datatable_clientside/(?P<table_name>[\w]+)/', datatable_fetch, name="datatablefetch_clientside"),
    url(r'^datatable_serverside/assembly', AssemblyDatatableView.as_view(),
        name="datatablefetch_serverside_assembly"),
    url(r'^datatable_serverside/transcript/(?P<assembly_name>[\w]+)/(?P<release_name>[\w]+)/(?P<source_name>[\w]+)/',
        TranscriptDatatableView.as_view(),
        name="datatablefetch_serverside_transcript"),
    url(r'^datatable_serverside/gene/(?P<assembly_name>[\w]+)/(?P<release_name>[\w]+)/', GeneDatatableView.as_view(),
        name="datatablefetch_serverside_gene"),
    url(r'^datatable_serverside/exon/(?P<assembly_name>[\w]+)/(?P<release_name>[\w]+)/', ExonDatatableView.as_view(),
        name="datatablefetch_serverside_exon"),
    url(r'^datatable_serverside/release_set/', ReleaseSetDatatableView.as_view(),
        name="datatablefetch_serverside_release"),
    url(r'^ajax/load-releases/', views.load_releases, name='ajax_load_releases'),
    url(r'^mane/$', TemplateView.as_view(template_name='mane_list.html')),
    url(r'^view_alignment/$', TemplateView.as_view(template_name='alignment_viewer.html'))

]
