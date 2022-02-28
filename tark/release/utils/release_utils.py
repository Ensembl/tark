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

import json

from release.models import ReleaseSet
from release.models import ReleaseSource
from release.models import ReleaseStats
from release.models import TranscriptReleaseTag
from django.db.models.aggregates import Max
from django.conf import settings
from assembly.models import Assembly
from django.db.models import Q
from transcript.models import Transcript
from django.db import connection

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


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
            all_releases = ReleaseSet.objects.filter(assembly__assembly_name__iexact=assembly_name). \
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
            if len(cls.get_all_release_short_names(assembly_name, source_name)) > 0:
                assembly_releases[assembly_name] = cls.get_all_release_short_names(assembly_name, source_name)

        return assembly_releases

    @classmethod
    def get_all_release_sources(cls):
        all_sources = ReleaseSource.objects.all().values('shortname')
        all_source_names = [source["shortname"] for source in all_sources]
        return all_source_names

    @classmethod
    def get_release_diff(cls, diff_dict):
        print("get release diff called")
        set1_params = diff_dict['release_set_1']
        set2_params = diff_dict['release_set_2']

        # param_keys = ["source", "assembly", "version"]
        if set1_params["source"] != set2_params["source"]:
            return {}

        queryset_all = TranscriptReleaseTag.objects.all()
        queryset1 = queryset_all.filter(Q(release__source__shortname__iexact=str(set1_params["source"]))
                                        & Q(release__shortname__iexact=set1_params["version"])  # @IgnorePep8
                                        & Q(release__assembly__assembly_name__iexact=str(set1_params["assembly"]))
                                        # @IgnorePep8
                                        ).values("feature_id").distinct()  # @IgnorePep8

        queryset1_count = queryset1.count()

        queryset_all = TranscriptReleaseTag.objects.all()
        queryset2 = queryset_all.filter(Q(release__source__shortname__iexact=str(set2_params["source"]))
                                        & Q(release__shortname__iexact=set2_params["version"])  # @IgnorePep8
                                        & Q(release__assembly__assembly_name__iexact=str(set2_params["assembly"]))
                                        # @IgnorePep8
                                        ).values("feature_id").distinct()  # @IgnorePep8

        queryset2_count = queryset2.count()
        logger.info("queryset2_count " + queryset2_count)

        # intersection
        qs_intersection = queryset1 & queryset2
        qs_intersection_count = qs_intersection.count()

        # difference set1-set2
        qs1_qs2_difference_count = queryset1_count - qs_intersection_count
        logger.info("qs1_qs2_difference_count " + qs1_qs2_difference_count)

        # difference is not supported by mysql
        # bigger_qs.exclude(id__in=smaller_qs)
        qs1_qs2_diff = queryset1.exclude(feature_id__in=queryset2)
        # get Transcripts
        qs1_qs2_transcripts = Transcript.objects.filter(pk__in=qs1_qs2_diff).values('stable_id', 'stable_id_version')

        result_dict = {}
        result_dict['qs1_qs2_transcripts'] = list(qs1_qs2_transcripts)

        qs2_qs1_diff = queryset2.exclude(feature_id__in=queryset1)

        # get Transcripts
        qs2_qs1_transcripts = Transcript.objects.filter(pk__in=qs2_qs1_diff).values('stable_id', 'stable_id_version')
        result_dict['qs2_qs1_transcripts'] = list(qs2_qs1_transcripts)

        return result_dict

    @classmethod
    def get_release_loading_stats(cls):
        """
        """
        source_loading_stats = {}

        release_stats_objects = ReleaseStats.objects.select_related(
            'release'
        )
        # print(release_stats_objects)
        for rso in release_stats_objects:
            if rso.release is not None:
                source_name = rso.release.source.shortname

                if source_name in source_loading_stats:
                    source_loading_stats[source_name].append(json.loads(rso.json))
                else:
                    source_loading_stats[source_name] = [json.loads(rso.json)]

        return source_loading_stats

    @classmethod
    def dictfetchall(cls, cursor):
        "Return all rows from a cursor as a dict"
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    @classmethod
    def get_features_gained(cls, feature, current_release, previous_release):
        cursor = connection.cursor()

        raw_sql = "SELECT SQL_NO_CACHE\
                    COUNT(*)\
                    FROM\
                      (\
                    SELECT\
                      feature_id\
                    FROM " + \
                  feature + "_release_tag AS f_tag\
                      JOIN release_set AS rs ON (f_tag.release_id=rs.release_id)\
                    WHERE\
                      rs.shortname=%s\
                  ) AS v0\
                  RIGHT JOIN (\
                    SELECT\
                      feature_id\
                    FROM " + \
                  feature + "_release_tag AS f_tag\
                      JOIN release_set AS rs ON (f_tag.release_id=rs.release_id)\
                    WHERE\
                      rs.shortname=%s\
                  ) AS v1 ON (v0.feature_id=v1.feature_id)\
                WHERE\
                  v0.feature_id IS NULL;\
                  "

        cursor.execute(raw_sql, [current_release, previous_release])
        row = cursor.fetchone()
        return row
