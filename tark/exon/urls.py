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
from exon import views

urlpatterns = [
    re_path(r'^$', views.ExonList.as_view(), name='exon_list'),
    re_path(r'^(?P<pk>[0-9]+)/$', views.ExonDetail.as_view(), name='exon_detail'),

]
