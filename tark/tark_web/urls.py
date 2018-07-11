'''
Copyright [1999-2015] Wellcome Trust Sanger Institute and the EMBL-European Bioinformatics Institute
Copyright [2016-2018] EMBL-European Bioinformatics Institute

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

from django.conf.urls import url
from tark_web import views

from tark.views import datatable_view, datatable_fetch
from assembly.views import AssemblyDatatableView
from transcript.views import TranscriptDatatableView
from gene.views import GeneDatatableView
from exon.views import ExonDatatableView


urlpatterns = [
    url(r'^$', views.web_home, name='web_home'),
    # diff
    url(r'^diff/$', views.diff_home, name='diff_home'),
    #print("From diff_from_set " + diff_me_stable_id  + " " + diff_me_assembly + " " +  diff_me_release + " " +  diff_with_stable_id + " " +  diff_with_assembly + " " +  diff_with_release )

    url(r'^diff/compare_set/(?P<diff_me_stable_id>[\w]+)/(?P<diff_me_assembly>[\w]+)/(?P<diff_me_release>[\w]+)/(?P<diff_with_stable_id>[\w]+)/(?P<diff_with_assembly>[\w]+)/(?P<diff_with_release>[\w]+)/', views.diff_compare_set, name='diff_compare_set'),

    # search
    url(r'^search/$', views.search_home, name='search_home'),
    #  datatables
    url(r'^datatable/(?P<table_name>[\w]+)/(?P<assembly_name>[\w]+)/(?P<release_name>[\w]+)/(?P<source_name>[\w]+)/(?P<assembly_name_compare>[\w]+)/(?P<release_name_compare>[\w]+)/(?P<source_name_compare>[\w]+)/', datatable_view, name="datatable_view"),
    url(r'^datatable_clientside/(?P<table_name>[\w]+)/', datatable_fetch, name="datatablefetch_clientside"),
    url(r'^datatable_serverside/assembly', AssemblyDatatableView.as_view(),
        name="datatablefetch_serverside_assembly"),
    url(r'^datatable_serverside/transcript/(?P<assembly_name>[\w]+)/(?P<release_name>[\w]+)/(?P<source_name>[\w]+)/', TranscriptDatatableView.as_view(),
        name="datatablefetch_serverside_transcript"),
    url(r'^datatable_serverside/gene/(?P<assembly_name>[\w]+)/(?P<release_name>[\w]+)/', GeneDatatableView.as_view(),
        name="datatablefetch_serverside_gene"),
    url(r'^datatable_serverside/exon/(?P<assembly_name>[\w]+)/(?P<release_name>[\w]+)/', ExonDatatableView.as_view(),
        name="datatablefetch_serverside_exon"),
    url(r'^ajax/load-releases/', views.load_releases, name='ajax_load_releases'),

]
