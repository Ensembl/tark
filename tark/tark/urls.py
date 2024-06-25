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

from django.urls.conf import include, path
from rest_framework_swagger.views import get_swagger_view

from django.conf.urls import url
from tark import views
from django.views.generic.base import TemplateView
import socket

"""tark URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

api_version = "api/"
tark_apis = [
    url(r'^' + api_version + 'assembly/', include('assembly.urls')),
    url(r'^' + api_version + 'gene/', include('gene.urls')),
    url(r'^' + api_version + 'transcript/', include('transcript.urls')),
    url(r'^' + api_version + 'translation/', include('translation.urls')),
    url(r'^' + api_version + 'exon/', include('exon.urls')),
    url(r'^' + api_version + 'release/', include('release.urls')),
    url(r'^' + api_version + 'sequence/', include('sequence.urls')),
]

schema_view = get_swagger_view(title='Tark REST API Endpoints', patterns=tark_apis)

try:
    HOSTNAME = socket.gethostname()
except:
    HOSTNAME = 'localhost'

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # url(r'^docs/', schema_view),
    url(r'^' + api_version + '$', schema_view),
    url(r'^' + api_version + 'status', views.PingService.as_view()),
    url(r'^web/', include('tark_web.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^documentation/$', TemplateView.as_view(template_name='documentation.html'),
        {"hostname": "http://" + HOSTNAME}, name="tark_help"),
    url(r'^privacy_notice_tark', TemplateView.as_view(template_name='privacy_notice_tark.html'),
        name="privacy_notice_tark"),
    url(r'^robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'),
        name="robots_file"),
        # path("__debug__/", include("debug_toolbar.urls")),

]

internal_apis = []  # hide your urls here

urlpatterns = urlpatterns + tark_apis + internal_apis
