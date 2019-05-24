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

import collections
from translation.models import Translation
from django.db.models.query_utils import Q
from tark.utils.exon_utils import ExonUtils


class DiffUtils(object):

    @classmethod
    def compare_transcripts(cls, diff_me_transcript, diff_with_transcript):

        diff_set = DiffSet(first_object=diff_me_transcript, second_object=diff_with_transcript)
        compare_diff_dict = diff_set.compare_objects()
        (compare_exon_sets_diffme2diffwith, compare_exon_sets_diffwith2diffme) = diff_set.compare_exons()

        compare_results = cls.get_results_as_response_body(compare_diff_dict, compare_exon_sets_diffme2diffwith,
                                                           compare_exon_sets_diffwith2diffme, diff_set)

        return compare_results

    @classmethod
    def get_results_as_response_body(cls, compare_diff_dict, compare_exon_sets_diffme2diffwith, compare_exon_sets_diffwith2diffme, diff_set):  # @IgnorePep8
        response_body_dict = {"count": 1, "next": None, "previous": None, "results": []}
        results = {key: value for (key, value) in compare_diff_dict.items()}
        response_body_dict["results"] = results
        response_body_dict["diff_me_transcript"] = diff_set.first_object
        response_body_dict["diff_with_transcript"] = diff_set.second_object
        response_body_dict["exonsets_diffme2diffwith"] = compare_exon_sets_diffme2diffwith
        response_body_dict["exonsets_diffwith2diffme"] = compare_exon_sets_diffwith2diffme
        return response_body_dict

    # to be deprecated
    @classmethod
    def get_coding_exons(cls, diff_result):
        if "results" in diff_result:
            for result in diff_result["results"]:
                if "translations" in result:
                    updated_translations = []

                    for translation in result['translations']:
                        tl_stable_id = translation["stable_id"]
                        tl_stable_id_version = translation["stable_id_version"]
                        tl_translation_id = translation["translation_id"]

                        criterion1 = Q(stable_id=tl_stable_id)
                        criterion2 = Q(stable_id_version=tl_stable_id_version)
                        criterion3 = Q(translation_id=tl_translation_id)

                        tl_query_set = Translation.objects.filter(criterion1 & criterion2 & criterion3).select_related('sequence').distinct()  # @IgnorePep8

                        for tl_obj in tl_query_set:
                            translation["sequence"] = {"sequence": tl_obj.sequence.sequence,
                                                       "seq_checksum": tl_obj.sequence. seq_checksum}
                            if "exons" in result:  # work here again
                                exon_set_cds = cls.update_coding_exons(result['exons'], translation)
                                translation["exons"] = exon_set_cds
                            updated_translations.append(translation)
                    result['translations'] = updated_translations
                else:
                    result['translations'] = None

    # to be deprecated
    @classmethod
    def update_coding_exons(cls, exon_set, translation):
        tl_start = translation["loc_start"]
        tl_end = translation["loc_end"]
        tl_strand = translation["loc_strand"]
        exon_set_cds = []
        if tl_strand == 1:
            exon_set_list = exon_set
        else:
            exon_set_list = reversed(list(exon_set))

        for exon in exon_set_list:
                exon_cds = exon.copy()
#                 print(exon_cds["exon_order"])
#                 print("exon start " + str(exon_cds["loc_start"]) + " exon end " + str(exon_cds["loc_end"]))
                # check if exon_start is between tl_start and tl_end
                # check if exon_end is between tl_start and tl_end
                if exon_cds["loc_start"] >= tl_start and exon_cds["loc_end"] <= tl_end:
                    exon_set_cds.append(exon_cds)
                else:
                    if exon_cds["loc_start"] <= tl_start:
                        exon_cds["loc_start"] = tl_start

                    if exon_cds["loc_end"] >= tl_end:
                        exon_cds["loc_end"] = tl_end
                    exon_set_cds.append(exon_cds)
                    break

        return exon_set_cds


class DiffSet(object):

    def __init__(self, first_object, second_object):

        self.first_object = first_object
        self.second_object = second_object
        self.diff_dict = self.init_attributes()

    def init_attributes(self):

        self.diff_dict = collections.OrderedDict()
        self.diff_dict['diff_me_stable_id'] = self.first_object['stable_id']
        self.diff_dict['diff_with_stable_id'] = self.second_object['stable_id']

        self.diff_dict['diff_me_stable_id_version'] = self.first_object['stable_id_version']
        self.diff_dict['diff_with_stable_id_version'] = self.second_object['stable_id_version']

        self.diff_dict['diff_me_assembly'] = self.first_object['assembly']
        self.diff_dict['diff_with_assembly'] = self.second_object['assembly']

        self.diff_dict['diff_me_release'] = self.first_object["transcript_release_set"]["shortname"]
        self.diff_dict['diff_with_release'] = self.second_object["transcript_release_set"]["shortname"]
        return self.diff_dict

    def compare_objects(self):

        # For transcript/cdna
        self.diff_dict['has_stable_id_changed'] = self.has_feature_attribute_changed(
                                                    feature_attribute="stable_id")
        self.diff_dict['has_stable_id_version_changed'] = self.has_feature_attribute_changed(
                                                    feature_attribute="stable_id_version")
        self.diff_dict['has_transcript_changed'] = self.has_feature_attribute_changed(
                                                    feature_attribute="transcript_checksum")
        self.diff_dict['has_location_changed'] = self.has_feature_attribute_changed(
                                                    feature_attribute="loc_checksum")
        self.diff_dict['has_exon_set_changed'] = self.has_feature_attribute_changed(
                                                    feature_attribute="exon_set_checksum")

        self.diff_dict['has_seq_changed'] = self.has_feature_attribute_changed(
                                                    feature_attribute="seq_checksum",
                                                    feature_type="sequence")

        # For translation
        self.diff_dict['has_translation_stable_id_changed'] = self.has_feature_attribute_changed(
                                                    feature_attribute="stable_id",
                                                    feature_type="translations")
        self.diff_dict['has_translation_stable_id_version_changed'] = self.has_feature_attribute_changed(
                                                    feature_attribute="stable_id_version",
                                                    feature_type="translations")
        self.diff_dict['has_translation_changed'] = self.has_feature_attribute_changed(
                                                    feature_attribute="translation_checksum",
                                                    feature_type="translations")
        self.diff_dict['has_translation_location_changed'] = self.has_feature_attribute_changed(
                                                    feature_attribute="loc_checksum",
                                                    feature_type="translations")

        self.diff_dict['has_translation_seq_changed'] = self.has_feature_attribute_changed(
                                                    feature_attribute="sequence",
                                                    feature_type="translations")
        # For cds
        # todo include for cds here, currently calculated in template

        # For genes
        self.diff_dict['has_gene_stable_id_changed'] = self.has_feature_attribute_changed(
                                                    feature_attribute="stable_id",
                                                    feature_type="gene")
        self.diff_dict['has_gene_stable_id_version_changed'] = self.has_feature_attribute_changed(
                                                    feature_attribute="stable_id_version",
                                                    feature_type="gene")
        self.diff_dict['has_gene_changed'] = self.has_feature_attribute_changed(
                                                    feature_attribute="gene_checksum",
                                                    feature_type="gene")
        self.diff_dict['has_gene_location_changed'] = self.has_feature_attribute_changed(
                                                    feature_attribute="loc_checksum",
                                                    feature_type="gene")
        self.diff_dict['has_hgnc_changed'] = self.has_feature_attribute_changed(
                                                    feature_attribute="name",
                                                    feature_type="gene")

        return self.diff_dict

    def compare_exons(self):
        first_exon_list = None
        if 'exons' in self.first_object:
            first_exon_list = self.first_object['exons']

        second_exon_list = None
        if 'exons' in self.second_object:
            second_exon_list = self.second_object['exons']

        if first_exon_list is not None and second_exon_list is not None:
            #             compare_results_first2second = ExonUtils.compare_exon_sets(first_exon_list, second_exon_list)
            #             compare_results_second2first = ExonUtils.compare_exon_sets(second_exon_list, first_exon_list)
            compare_results_first2second = ExonUtils.diff_exon_sets(first_exon_list, second_exon_list)
            compare_results_second2first = ExonUtils.diff_exon_sets(second_exon_list, first_exon_list)
            return (compare_results_first2second, compare_results_second2first)

        return None

    def has_feature_attribute_changed(self, feature_attribute=None, feature_type=None):
        if feature_type is not None and feature_type in self.first_object and feature_type in self.second_object:
            if feature_attribute in self.first_object[feature_type] and \
                    feature_attribute in self.second_object[feature_type]:
                return not(self.first_object[feature_type][feature_attribute] == self.second_object[
                                            feature_type][feature_attribute])
        else:
            if feature_attribute in self.first_object and feature_attribute in self.second_object:
                return not(self.first_object[feature_attribute] == self.second_object[feature_attribute])

        return None
