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

from django import template
from tark.utils.exon_utils import ExonUtils
register = template.Library()


@register.filter
def compare_transcript(diff_result, compare_attr):
    has_changed = False

    diff_me_tr = diff_result['diff_me_transcript']
    diff_with_tr = diff_result['diff_with_transcript']
    diff_me_tr_attr = None
    diff_with_tr_attr = None

    if diff_me_tr and compare_attr in diff_me_tr:
        diff_me_tr_attr = diff_me_tr[compare_attr]

    if diff_with_tr and compare_attr in diff_with_tr:
        diff_with_tr_attr = diff_with_tr[compare_attr]

    if diff_me_tr_attr and diff_with_tr_attr:
        has_changed = str(diff_me_tr_attr) == str(diff_with_tr_attr)

    return not has_changed


@register.filter
def compare_exon(diff_me_exon, diff_with_exon):
    compare_attr_list = ['stable_id', 'stable_id_version', 'assembly',
                         'loc_region', 'loc_start', 'loc_end', 'length', 'loc_strand',
                         'loc_checksum', 'seq_checksum', 'exon_checksum']
    exon_result = []
    # computed attributes
    diff_me_exon["length"] = 0
    diff_with_exon["length"] = 0
    diff_me_exon["length"] = int(diff_me_exon["loc_end"]) - int(diff_me_exon["loc_start"])
    diff_with_exon["length"] = int(diff_with_exon["loc_end"]) - int(diff_with_exon["loc_start"])
    for compare_attr in compare_attr_list:
        is_equal = False
        if compare_attr in diff_me_exon:
            diff_me_exon_attr = diff_me_exon[compare_attr]

        if compare_attr in diff_with_exon:
            diff_with_exon_attr = diff_with_exon[compare_attr]

        if diff_me_exon_attr and diff_with_exon_attr:
            is_equal = str(diff_me_exon_attr) == str(diff_with_exon_attr)

            exon_result.append(is_equal)

    return exon_result


@register.filter
def compute_exon_overlap(diff_me_exon, diff_with_exon):
    start1, end1, start2, end2 = 0, 0, 0, 0

    if diff_me_exon:
        start1, end1 = diff_me_exon["loc_start"], diff_me_exon["loc_end"]

    if diff_with_exon:
        start2, end2 = diff_with_exon["loc_start"], diff_with_exon["loc_end"]

    overlap = ExonUtils.compute_overlap(start1, end1, start2, end2)
    return overlap


@register.filter
def subtract(value, arg):
    return value - arg


@register.filter
def get_exon_by_exon_order(exon_list, exon_order):

    for exon in exon_list:
        if exon_order is not None:
            if exon['exon_order'] == exon_order:
                return exon

    return None


@register.filter
def compare_exons(diff_result, compare_attrs):

    compare_result = []

    if compare_attrs is None:
        return compare_result

    compare_attr_list = [attr.strip() for attr in compare_attrs.split(',')]

    if len(diff_result['diff_me_transcript']['results']) == 0 or \
            len(diff_result['diff_with_transcript']['results']) == 0:
        return compare_result

    diff_me_tr = diff_result['diff_me_transcript']['results'][0]
    diff_with_tr = diff_result['diff_with_transcript']['results'][0]

    if 'exons' in diff_me_tr:
        diff_me_tr_exons = diff_me_tr['exons']

    if 'exons' in diff_with_tr:
        diff_with_tr_exons = diff_with_tr['exons']

    diff_me_exon_attr = False
    diff_with_exon_attr = False

    for (diff_me_tr_exon, diff_with_tr_exon) in zip(diff_me_tr_exons, diff_with_tr_exons):
        exon_result = []
        for compare_attr in compare_attr_list:
            is_equal = False
            if compare_attr in diff_me_tr_exon:
                diff_me_exon_attr = diff_me_tr_exon[compare_attr]

            if compare_attr in diff_with_tr_exon:
                diff_with_exon_attr = diff_with_tr_exon[compare_attr]

            if diff_me_exon_attr and diff_with_exon_attr:
                is_equal = str(diff_me_exon_attr) == str(diff_with_exon_attr)

            exon_result.append(is_equal)
        compare_result.append(exon_result)

    return compare_result


@register.filter
def compare_translation(diff_result, compare_attrs):

    compare_result = []

    if compare_attrs is None:
        return compare_result

    compare_attr_list = [attr.strip() for attr in compare_attrs.split(',')]
#
#     if len(diff_result['diff_me_transcript']['results']) == 0 or \
#             len(diff_result['diff_with_transcript']['results']) == 0:
#         return compare_result

    diff_me_tr = diff_result['diff_me_transcript']
    diff_with_tr = diff_result['diff_with_transcript']

    if 'translations' in diff_me_tr:
        diff_me_tr_translation = diff_me_tr['translations']

    if 'translations' in diff_with_tr:
        diff_with_tr_translation = diff_with_tr['translations']

    print("==========compare attrs list from translation===  " + str(compare_attrs))
 #   for (diff_me_tr_translation, diff_with_tr_translation) in zip(diff_me_tr_translations, diff_with_tr_translations):
    diff_me_translation_attr = None
    diff_with_translation_attr = None
    exon_result = []
    for compare_attr in compare_attr_list:
        is_equal = False
        if compare_attr == "seq_checksum":
            if "sequence" in diff_me_tr_translation and compare_attr in diff_me_tr_translation["sequence"]:
                diff_me_translation_attr = diff_me_tr_translation["sequence"][compare_attr]

            if "sequence" in diff_with_tr_translation and compare_attr in diff_with_tr_translation["sequence"]:
                diff_with_translation_attr = diff_with_tr_translation["sequence"][compare_attr]
        else:
            if compare_attr in diff_me_tr_translation:
                diff_me_translation_attr = diff_me_tr_translation[compare_attr]

            if compare_attr in diff_with_tr_translation:
                diff_with_translation_attr = diff_with_tr_translation[compare_attr]

        if diff_me_translation_attr and diff_with_translation_attr:
            print("Diff me tl  " + str(diff_me_translation_attr)  + "  Diff with tl   " + str(diff_with_translation_attr))
            is_equal = str(diff_me_translation_attr) == str(diff_with_translation_attr)

        exon_result.append(is_equal)
    compare_result.append(exon_result)

    return compare_result


@register.filter
def compare_location(diff_result):
    is_equal = False

    if len(diff_result['diff_me_transcript']['results']) == 0 or \
            len(diff_result['diff_with_transcript']['results']) == 0:
        return is_equal

    diff_me_tr = diff_result['diff_me_transcript']['results'][0]
    diff_with_tr = diff_result['diff_with_transcript']['results'][0]

    diff_me_tr_loc_region = diff_me_tr['loc_region']
    diff_me_tr_loc_start = diff_me_tr['loc_start']
    diff_me_tr_loc_end = diff_me_tr['loc_end']
    diff_me_tr_loc_strand = diff_me_tr['loc_end']

    diff_with_tr_loc_region = diff_with_tr['loc_region']
    diff_with_tr_loc_start = diff_with_tr['loc_start']
    diff_with_tr_loc_end = diff_with_tr['loc_end']
    diff_with_tr_loc_strand = diff_with_tr['loc_end']

    if diff_me_tr_loc_region == diff_with_tr_loc_region:
        if diff_me_tr_loc_start == diff_with_tr_loc_start:
            if diff_me_tr_loc_end == diff_with_tr_loc_end:
                if diff_me_tr_loc_strand == diff_with_tr_loc_strand:
                    return True

    return is_equal


@register.filter
def get_location_string(transcript):
    if 'loc_region' in transcript and 'loc_start' in transcript and 'loc_end' in transcript:
        return str(transcript['loc_region']) + " : " + str(transcript['loc_start']) + " - " + str(transcript['loc_end'])

    return ""


@register.filter
def get_sequence_length(feature):
    if 'loc_start' in feature and 'loc_end' in feature:
        return str(feature['loc_end'] - feature['loc_start'])

    return ""


@register.filter
def compare_sequence(diff_result, compare_attr):
    is_equal = False

    if len(diff_result['diff_me_transcript']['results']) == 0 or \
            len(diff_result['diff_with_transcript']['results']) == 0:
        return is_equal

    diff_me_tr = diff_result['diff_me_transcript']['results'][0]
    diff_with_tr = diff_result['diff_with_transcript']['results'][0]
    diff_me_tr_attr = None
    diff_with_tr_attr = None

    if diff_me_tr and compare_attr in diff_me_tr["sequence"]:
        diff_me_tr_attr = diff_me_tr["sequence"][compare_attr]

    if diff_with_tr and compare_attr in diff_with_tr["sequence"]:
        diff_with_tr_attr = diff_with_tr["sequence"][compare_attr]

    if diff_me_tr_attr and diff_with_tr_attr:
        is_equal = str(diff_me_tr_attr) == str(diff_with_tr_attr)

    return is_equal


@register.filter
def compare_coding_sequence(diff_result, compare_attr):
    print("compare coding sequence called")
    is_equal = False
    if len(diff_result['diff_me_transcript']['results']) == 0 or \
            len(diff_result['diff_with_transcript']['results']) == 0:
        return is_equal

    diff_me_tr = diff_result['diff_me_transcript']['results'][0]
    diff_with_tr = diff_result['diff_with_transcript']['results'][0]
    diff_me_tr_attr = None
    diff_with_tr_attr = None

    if diff_me_tr and "translations" in diff_me_tr and len(diff_me_tr["translations"]) > 0:
        print("reached here1====")
        diff_me_translation = diff_me_tr["translations"][0]
        if diff_me_translation and "sequence" in diff_me_translation and compare_attr in diff_me_translation["sequence"]:
            diff_me_tr_attr = diff_me_translation["sequence"][compare_attr]
            print("diff_me_tr_attr  " + str(diff_me_tr_attr))

    if diff_with_tr and "translations" in diff_with_tr and len(diff_with_tr["translations"]) > 0:
        print("reached here2====")
        diff_with_translation = diff_with_tr["translations"][0]
        if diff_with_translation and "sequence" in diff_with_translation and compare_attr in diff_with_translation["sequence"]:
            diff_with_tr_attr = diff_with_translation["sequence"][compare_attr]

    if diff_me_tr_attr and diff_with_tr_attr:
        is_equal = str(diff_me_tr_attr) == str(diff_with_tr_attr)

    return is_equal


@register.filter()
def zip_lists(a, b):
    print(zip(a, b))
    return zip(a, b)

  
