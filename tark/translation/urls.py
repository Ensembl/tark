'''
Copyright [1999-2015] Wellcome Trust Sanger Institute and the EMBL-European Bioinformatics Institute
Copyright [2016-2024] EMBL-European Bioinformatics Institute

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

# from django.conf.urls import url
from django.urls import re_path
from django.urls import path
from translation import views

urlpatterns = [
    re_path(r'^$', views.TranslationList.as_view(), name='translation_list'),
    re_path(r'^(?P<pk>[0-9]+)/$', views.TranslationDetail.as_view(), name='translation_detail'),
    path(r"stable_id/<str:stable_id>/", views.TranslationListByStableID.as_view(), name='translation_list_by_stable_id'),

]
