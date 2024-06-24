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

from rest_framework.filters import BaseFilterBackend
from tark_drf.utils.drf_fields import CommonFields, DrfFields
from tark_drf.utils.drf_filters import CommonFilterBackend
from transcript.models import Transcript
from release.utils.release_utils import ReleaseUtils
from tark_web.utils.sequtils import TarkSeqUtils

import logging
from transcript.utils.search_utils import SearchUtils
from django.core import serializers
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


class TranscriptFilterBackend(BaseFilterBackend):
    """
    Filter to filter by common fields..
    """

    def filter_queryset(self, request, queryset, view):
        queryset = CommonFilterBackend.get_common_filter_querysets(request, queryset, view)
        queryset = CommonFilterBackend.get_common_related_querysets(request, queryset, view)

        release_short_name = request.query_params.get('release_short_name', None)
        if release_short_name is not None:
            queryset = queryset.filter(transcript_release_set__shortname=release_short_name)

        source_name = request.query_params.get('source_name', None)
        if source_name is not None:
            queryset = queryset.filter(transcript_release_set__source__shortname__icontains=source_name)

        if queryset is not None:
            return queryset.distinct()
        else:
            return None

    def get_schema_fields(self, view):
        return CommonFields.get_common_query_set("Transcript") + CommonFields.COMMON_RELATED_QUERY_SET + \
               CommonFields.get_expand_query_set(Transcript)


class TranscriptDiffFilterBackend(BaseFilterBackend):
    """
    Diff Filter
    """

    def filter_queryset(self, request, queryset, view):

        # handle diff me
        diff_me_stable_id = request.query_params.get('diff_me_stable_id', None)
        diff_me_stable_id_version = request.query_params.get('diff_me_stable_id_version', 1)

        if diff_me_stable_id is not None and diff_me_stable_id_version is not None:
            queryset_me = queryset.filter(stable_id=diff_me_stable_id). \
                filter(stable_id_version=diff_me_stable_id_version)
        else:
            queryset_me = queryset.filter(stable_id=diff_me_stable_id)

        diff_me_release = request.query_params.get('diff_me_release', ReleaseUtils.get_latest_release())
        diff_me_assembly = request.query_params.get('diff_me_assembly', ReleaseUtils.get_latest_assembly())
        diff_me_source = request.query_params.get('diff_me_source', ReleaseUtils.get_default_source())

        if diff_me_release is not None and diff_me_assembly is not None:
            queryset_me = queryset_me.filter(transcript_release_set__source__shortname=diff_me_source). \
                filter(assembly__assembly_name__icontains=diff_me_assembly). \
                filter(transcript_release_set__shortname=diff_me_release)

        # handle diff with
        diff_with_stable_id = request.query_params.get('diff_with_stable_id', None)
        diff_with_stable_id_version = request.query_params.get('diff_with_stable_id_version', 1)

        if diff_with_stable_id is not None and diff_with_stable_id_version is not None:
            queryset_with = queryset.filter(stable_id=diff_with_stable_id). \
                filter(stable_id_version=diff_with_stable_id_version)
        else:
            queryset_with = queryset.filter(stable_id=diff_with_stable_id)

        diff_with_release = request.query_params.get('diff_with_release', ReleaseUtils.get_latest_release())
        diff_with_assembly = request.query_params.get('diff_with_assembly', ReleaseUtils.get_latest_assembly())
        diff_with_source = request.query_params.get('diff_with_source', ReleaseUtils.get_default_source())

        if diff_with_release is not None and diff_with_assembly is not None:
            queryset_with = queryset_with.filter(transcript_release_set__source__shortname=diff_with_source). \
                filter(assembly__assembly_name__icontains=diff_with_assembly). \
                filter(transcript_release_set__shortname=diff_with_release)

        queryset = queryset_me | queryset_with  # queryset will contain all unique records of q1 + q2

        return queryset.distinct()

    def get_schema_fields(self, view):
        return [DrfFields.diff_me_stable_id_field(), DrfFields.diff_me_release_field(),
                DrfFields.diff_me_source_field(),
                DrfFields.diff_me_assembly_field(), DrfFields.diff_with_stable_id_field(),
                DrfFields.diff_with_source_field(),
                DrfFields.diff_with_release_field(),
                DrfFields.diff_with_assembly_field()]


class TranscriptSearchFilterBackend(BaseFilterBackend):
    """
    Diff Filter
    """

    def filter_queryset(self, request, queryset, view):
        identifier = request.query_params.get('identifier_field', None)
        # replace space and comma
        identifier = identifier.replace(" ", "")
        identifier = identifier.replace(",", "")

        identifier_type = SearchUtils.get_identifier_type(identifier)

        identifier_version = None
        if '.' in identifier and identifier_type != SearchUtils.HGVS_GENOMIC_REF and identifier_type != SearchUtils.HGVS_REFSEQ_CDS:  # @IgnorePep8
            (identifier, identifier_version) = identifier.split('.')

        if identifier is not None:
            if identifier_type == SearchUtils.ENSEMBL_TRANSCRIPT or \
                    identifier_type == SearchUtils.REFSEQ_TRANSCRIPT or \
                    identifier_type == SearchUtils.LRG_TRANSCRIPT:
                queryset = queryset.filter(stable_id=identifier)
                if identifier_version is not None:
                    queryset = queryset.filter(stable_id_version=identifier_version)
            elif identifier_type == SearchUtils.ENSEMBL_GENE:
                queryset = queryset.filter(genes__stable_id=identifier)
                if identifier_version is not None:
                    queryset = queryset.filter(stable_id_version=identifier_version)
            elif identifier_type == SearchUtils.ENSEMBL_PROTEIN or identifier_type == SearchUtils.REFSEQ_PROTEIN:
                queryset = queryset.filter(translations__stable_id=identifier)
                if identifier_version is not None:
                    queryset = queryset.filter(translations__stable_id_version=identifier_version)
            elif identifier_type == SearchUtils.GENOMIC_LOCATION:
                (loc_region_, loc_start_, loc_end_) = SearchUtils.parse_location_string(identifier)

                if loc_region_ is not None:
                    queryset = queryset.filter(loc_region=loc_region_)

                if loc_start_ is not None and loc_end_ is not None:
                    queryset = queryset.filter(loc_start__lte=loc_start_).filter(loc_end__gte=loc_start_) | \
                               queryset.filter(loc_start__lte=loc_end_).filter(loc_end__gte=loc_end_) | \
                               queryset.filter(loc_start__gte=loc_start_).filter(loc_end__lte=loc_end_)
            elif identifier_type == SearchUtils.HGVS_GENOMIC_REF:
                (loc_region_, loc_start_, loc_end_, assembly_) = SearchUtils.parse_hgvs_genomic_location_string(
                    identifier)  # @IgnorePep8
                if loc_region_ is not None and assembly_:
                    queryset = queryset.filter(assembly__assembly_name__icontains=assembly_).filter(
                        loc_region=loc_region_)  # @IgnorePep8

                if loc_start_ is not None and loc_end_ is not None:
                    queryset = queryset.filter(loc_start__lte=loc_start_).filter(loc_end__gte=loc_start_) | \
                               queryset.filter(loc_start__lte=loc_end_).filter(loc_end__gte=loc_end_) | \
                               queryset.filter(loc_start__gte=loc_start_).filter(loc_end__lte=loc_end_)
            elif identifier_type == SearchUtils.HGVS_REFSEQ_CDS:

                (refseq_identifier, coding_location) = SearchUtils.parse_hgvs_refseq_cds_string(
                    identifier)  # @IgnorePep8

                (identifier, identifier_version) = refseq_identifier.split('.')
                queryset_ref_stable_id = queryset.filter(stable_id=identifier)
                if identifier_version is not None:
                    queryset_ref_stable_id = queryset_ref_stable_id.filter(stable_id_version=identifier_version)

                # get the location
                refseq_transcript = queryset_ref_stable_id.first()

                if refseq_transcript is not None:

                    # try to get the translation and add the coding location to the translation start
                    translation_qs = refseq_transcript.translations.all().values()
                    if translation_qs is not None:
                        translation_list = list(translation_qs)

                        if len(translation_list) > 0:
                            translation_dict = translation_list[0]
                            cds_start = translation_dict["loc_start"]
                            # cds_end = translation_dict["loc_end"]

                            # cds_strand = translation_dict["loc_strand"]
                            loc_start_ = cds_start + int(coding_location)

                            loc_region_ = refseq_transcript.loc_region
                            loc_start_ = loc_start_
                            loc_end_ = loc_start_
                            assembly_name = refseq_transcript.assembly.assembly_name

                            queryset_ = Transcript.objects.filter(
                                assembly__assembly_name__icontains=assembly_name).filter(
                                loc_region=loc_region_)  # @IgnorePep8
                            if loc_start_ is not None and loc_end_ is not None:
                                queryset_ = queryset_.filter(loc_start__lte=loc_start_).filter(
                                    loc_end__gte=loc_start_) | \
                                            queryset_.filter(loc_start__lte=loc_end_).filter(loc_end__gte=loc_end_) | \
                                            queryset_.filter(loc_start__gte=loc_start_).filter(loc_end__lte=loc_end_)
                                return queryset_.distinct()

            elif identifier_type == SearchUtils.LRG_GENE:
                queryset = queryset.filter(genes__stable_id__exact=identifier)
            elif identifier_type == SearchUtils.HGNC_SYMBOL:
                queryset = queryset.filter(genes__name__name__exact=identifier)

        return queryset.distinct()

    def get_schema_fields(self, view):
        return [DrfFields.identifier_field(), DrfFields.get_expand_transcript_release_set_genes_field()]


class TranscriptDetailFilterBackend(BaseFilterBackend):
    """
    Detail Filter
    """

    def filter_queryset(self, request, queryset, view):
        identifier = request.query_params.get('stable_id_with_version', None)
        assembly_name = request.query_params.get('assembly_name', None)

        # to support version search
        identifier_version = None
        if '.' in identifier:
            (identifier, identifier_version) = identifier.split('.')

        if identifier is not None and identifier_version is not None:
            queryset = queryset.filter(stable_id=identifier).filter(stable_id_version=str(identifier_version))
            
            if assembly_name:
                queryset = queryset.select_related('assembly').filter(assembly__assembly_name=assembly_name)

            return queryset.distinct()


        return Transcript.objects.none()

    def get_schema_fields(self, view):
        return [DrfFields.stable_id_with_version_field("Transcript"),
                DrfFields.get_expand_transcript_release_set_genes_field()]


class TranscriptSetFilterBackent(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        stable_id = request.query_params.get('stable_id', 'ENST00000171111')
        if stable_id is not None:
            queryset = queryset.filter(stable_id=stable_id)

        diff_me_release = request.query_params.get('diff_me_release', None)
        diff_with_release = request.query_params.get('diff_with_release', ReleaseUtils.get_latest_release())

        diff_me_assembly = request.query_params.get('diff_me_assembly', ReleaseUtils.get_latest_assembly())
        diff_with_assembly = request.query_params.get('diff_with_assembly', ReleaseUtils.get_latest_assembly())

        expand_all = request.query_params.get('expand_all', "true")  # @UnusedVariable

        if diff_me_release is not None and diff_me_assembly is not None:
            queryset_me = queryset.filter(assembly__assembly_name__icontains=diff_me_assembly). \
                filter(transcript_release_set__shortname=diff_me_release)

            queryset_with = queryset.filter(assembly__assembly_name__icontains=diff_with_assembly). \
                filter(transcript_release_set__shortname=diff_with_release)

            queryset = queryset_me | queryset_with  # queryset will contain all unique records of q1 + q2

        return queryset.distinct()

    def get_schema_fields(self, view):
        return [DrfFields.stable_id_field("Transcript"), DrfFields.diff_me_release_field(),
                DrfFields.diff_me_assembly_field(), DrfFields.diff_with_release_field(),
                DrfFields.diff_with_assembly_field(), DrfFields.get_expand_transcript_release_set_field()]
