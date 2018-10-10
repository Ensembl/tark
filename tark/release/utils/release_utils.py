'''
Copyright [1999-2015] Wellcome Trust Sanger Institute and the EMBL-European Bioinformatics Institute
Copyright [2016-2017] EMBL-European Bioinformatics Institute

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
from release.models import ReleaseSet, ReleaseSource
from django.db.models.aggregates import Max
from django.conf import settings
from assembly.models import Assembly
from numpy import source


class ReleaseUtils(object):

    @classmethod
    def get_latest_release(cls):
        current_release = getattr(settings, "CURRENT_RELEASE", "92")

        if current_release is None:
            current_release = ReleaseSet.objects.all().aggregate(Max('shortname'))
            if 'shortname__max' in current_release:
                return current_release['shortname__max']

        return current_release

    @classmethod
    def get_latest_assembly(cls):
        current_assembly = getattr(settings, "CURRENT_ASSEMBLY", "GRCh38")
        return current_assembly

    @classmethod
    def get_default_source(cls):
        default_source = getattr(settings, "DEFAULT_SOURCE", "ensembl")
        return default_source

    @classmethod
    def get_all_releases(cls, assembly_name=None):
        if assembly_name is None:
            assembly_name = cls.get_latest_assembly()

        all_releases = ReleaseSet.objects.filter(assembly__assembly_name__iexact=assembly_name)
        return all_releases

    @classmethod
    def get_all_release_short_names(cls, assembly_name=None, source_name=None):
        if assembly_name is None:
            assembly_name = cls.get_latest_assembly()

        if source_name is None:
            source_name = cls.get_default_source()

        if source_name is "all":
            all_releases = ReleaseSet.objects.filter(assembly__assembly_name__iexact=assembly_name).values('shortname')
        else:
            all_releases = ReleaseSet.objects.filter(assembly__assembly_name__iexact=assembly_name).\
                filter(source__shortname__iexact=source_name).values('shortname')

        all_release_short_names = [release["shortname"] for release in all_releases]

        return sorted(all_release_short_names, reverse=True)

    @classmethod
    def get_all_assemblies(cls):
        all_assemblies = Assembly.objects.all()
        return all_assemblies

    @classmethod
    def get_all_assembly_names(cls):
        all_assemblies = Assembly.objects.all().values('assembly_name')
        all_assembly_names = [assembly["assembly_name"] for assembly in all_assemblies]
        return all_assembly_names

    @classmethod
    def get_all_assembly_releases(cls, source_name=None):
        assembly_releases = {}
        all_assembly_names = cls.get_all_assembly_names()
        for assembly_name in all_assembly_names:
            assembly_releases[assembly_name] = cls.get_all_release_short_names(assembly_name, source_name)

        return assembly_releases

    @classmethod
    def get_all_release_sources(cls):
        all_sources = ReleaseSource.objects.all().values('shortname')
        all_source_names = [source["shortname"] for source in all_sources]
        return all_source_names
