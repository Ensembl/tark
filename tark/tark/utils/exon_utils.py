'''
Copyright [1999-2015] Wellcome Trust Sanger Institute and the EMBL-European Bioinformatics Institute
Copyright [2016-2019] EMBL-European Bioinformatics Institute

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
import collections


class ExonUtils(object):

    @classmethod
    def diff_exon_sets(cls, exonset1, exonset2):

        #compare_results = collections.OrderedDict()
        compare_results = []
        cumulative_overlap_score = 0;

        for exon1 in exonset1:
            cur_exon = exon1
            matched_exons = []
            exon1_stable_id_version = str(exon1['stable_id']) + '.' + str(exon1['stable_id_version'])
            print("++++++++++++++++++++++++++++++++++ " + exon1_stable_id_version)
            for exon2 in exonset2:
                exon2_stable_id_version = str(exon2['stable_id']) + '.' + str(exon2['stable_id_version'])
                # check if exon from exonset1 overlaps with any exon in exonset2
                current_compare_result = {}
                overlap_score = 0
                if exon1['loc_region'] == exon2['loc_region']:
                    overlap_score = cls.compute_overlap(exon1['loc_start'], exon1['loc_end'], exon2['loc_start'], exon2['loc_end'])
                    if overlap_score > 0:
                        print("====found overlap between ==== " + str(exon1['exon_order'])  + "  and " + str(exon2['exon_order']) )
                        print(overlap_score)
                        cumulative_overlap_score = cumulative_overlap_score + 1
                        current_compare_result['overlapping_exon'] = exon2
                        #current_compare_result['overlapping_exon_order'] = exon2['exon_order']
                        current_compare_result['loc_checksum'] = exon1['loc_checksum'] == exon2['loc_checksum']
                        current_compare_result['seq_checksum'] = exon1['seq_checksum'] == exon2['seq_checksum']

                        matched_exons.append(current_compare_result)

            compare_results.append((cur_exon, matched_exons))

        compare_results.insert(0, ("cumulative_overlap_score", cumulative_overlap_score))

        print("==================compare_results============")
        print(compare_results)
        print("==================compare_results============")
        return compare_results

    @classmethod
    def compare_exon_sets(cls, exonset1, exonset2):

        compare_results = []

        for exon1 in exonset1:
            match_exists = False
            for exon2 in exonset2:
                if exon1['loc_checksum'] == exon2['loc_checksum'] and exon1['seq_checksum'] == exon2['seq_checksum']:
                    compare_results.append([exon1['exon_order'], exon2['exon_order']])
                    match_exists = True
                    break

            if not match_exists:
                compare_results.append([exon1['exon_order'], 0])

        if(len(exonset2) > len(exonset1)):
            index = 0
            for exon2 in exonset2:
                if index >= len(exonset1):
                    compare_results.append([0, exon2['exon_order']])
                index = index + 1

        print("==================compare_results============")
        print(compare_results)
        print("==================compare_results============")
        return compare_results

    @classmethod
    def compute_overlap(cls, start1, end1, start2, end2):
        x = range(start1, end1)
        y = range(start2, end2)
        xs = set(x)
        overlap = xs.intersection(y)
        return len(overlap)
