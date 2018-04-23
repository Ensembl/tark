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
from release.models import ReleaseSet
from django.db.models.aggregates import Max


class ReleaseUtils(object):

    @classmethod
    def get_latest_release(cls):
        current_release = ReleaseSet.objects.all().aggregate(Max('shortname'))
        if 'shortname__max' in current_release:
            return current_release['shortname__max']

        return None

    @classmethod
    def get_latest_assembly(cls):
        # change this later
        return "GRCh38"

