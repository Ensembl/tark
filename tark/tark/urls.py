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
from django.urls.conf import include
from rest_framework_swagger.views import get_swagger_view

from django.conf.urls import url
from django.conf import settings
from tark import views
from django.views.generic.base import TemplateView

api_version = "api/"
tark_apis = [
    url(r'^' + api_version + 'assembly/', include('assembly.urls')),
    url(r'^' + api_version + 'gene/', include('gene.urls')),
    url(r'^' + api_version + 'transcript/', include('transcript.urls')),
    url(r'^' + api_version + 'translation/', include('translation.urls')),
    url(r'^' + api_version + 'exon/', include('exon.urls')),
    ]


schema_view = get_swagger_view(title='TaRK REST API Endpoints', patterns=tark_apis)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # url(r'^docs/', schema_view),
    url(r'^' + api_version + '$', schema_view),
    url(r'^web/', include('tark_web.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^documentation/$', TemplateView.as_view(template_name='documentation.html')),

]


internal_apis = []  # hide your urls here

urlpatterns = urlpatterns + tark_apis + internal_apis

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
