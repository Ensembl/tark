'''
Copyright [1999-2015] Wellcome Trust Sanger Institute and the EMBL-European Bioinformatics Institute
Copyright [2016-2018] EMBL-European Bioinformatics Institute

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

from django import template
register = template.Library()


@register.filter
def compare_transcript(diff_result, compare_attr):
    is_equal = False

    if len(diff_result['diff_me_transcript']['results']) == 0 or \
            len(diff_result['diff_with_transcript']['results']) == 0:
        return is_equal

    diff_me_tr = diff_result['diff_me_transcript']['results'][0]
    diff_with_tr = diff_result['diff_with_transcript']['results'][0]
    diff_me_tr_attr = None
    diff_with_tr_attr = None

    if diff_me_tr and compare_attr in diff_me_tr:
        diff_me_tr_attr = diff_me_tr[compare_attr]

    if diff_with_tr and compare_attr in diff_with_tr:
        diff_with_tr_attr = diff_with_tr[compare_attr]

    if diff_me_tr_attr and diff_with_tr_attr:
        is_equal = str(diff_me_tr_attr) == str(diff_with_tr_attr)

    return is_equal


@register.filter
def compare_exon(diff_result, compare_attrs):

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

    if len(diff_result['diff_me_transcript']['results']) == 0 or \
            len(diff_result['diff_with_transcript']['results']) == 0:
        return compare_result

    diff_me_tr = diff_result['diff_me_transcript']['results'][0]
    diff_with_tr = diff_result['diff_with_transcript']['results'][0]

    if 'translations' in diff_me_tr:
        diff_me_tr_translations = diff_me_tr['translations']

    if 'translations' in diff_with_tr:
        diff_with_tr_translations = diff_with_tr['translations']

    diff_me_translation_attr = False
    diff_with_translation_attr = False

    for (diff_me_tr_translation, diff_with_tr_translation) in zip(diff_me_tr_translations, diff_with_tr_translations):
        exon_result = []
        for compare_attr in compare_attr_list:
            is_equal = False
            if compare_attr in diff_me_tr_translation:
                diff_me_translation_attr = diff_me_tr_translation[compare_attr]

            if compare_attr in diff_with_tr_translation:
                diff_with_translation_attr = diff_with_tr_translation[compare_attr]

            if diff_me_translation_attr and diff_with_translation_attr:
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
