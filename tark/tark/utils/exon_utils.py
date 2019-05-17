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


class ExonUtils(object):

    # this is the current one
    @classmethod
    def diff_exon_sets(cls, exonset1, exonset2):

        compare_results = []
        cumulative_overlap_score = 0

        for exon1 in exonset1:
            cur_exon = exon1
            matched_exons = []
            exon1_stable_id_version = str(exon1['stable_id']) + '.' + str(exon1['stable_id_version'])  # @UnusedVariable

            for exon2 in exonset2:
                exon2_stable_id_version = str(exon2['stable_id']) + '.' + str(exon2['stable_id_version'])  # @UnusedVariable

                # check if exon from exonset1 overlaps with any exon in exonset2
                current_compare_result = {}
                overlap_score = 0
                if exon1['loc_region'] == exon2['loc_region']:
                    overlap_score = cls.compute_overlap(exon1['loc_start'], exon1['loc_end'], exon2['loc_start'],
                                                        exon2['loc_end'])
                    if overlap_score > 0:

                        cumulative_overlap_score = cumulative_overlap_score + 1
                        current_compare_result['overlapping_exon'] = exon2

                        current_compare_result['loc_checksum'] = exon1['loc_checksum'] == exon2['loc_checksum']
                        current_compare_result['seq_checksum'] = exon1['seq_checksum'] == exon2['seq_checksum']

                        matched_exons.append(current_compare_result)

            compare_results.append((cur_exon, matched_exons))

        compare_results.insert(0, ("cumulative_overlap_score", cumulative_overlap_score))
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
        return compare_results

    @classmethod
    def compute_overlap(cls, start1, end1, start2, end2):
        x = range(start1, end1)
        y = range(start2, end2)
        xs = set(x)
        overlap = xs.intersection(y)
        return len(overlap)

    @classmethod
    def compute_cds_sequence(cls, transcript):
        cds_info = cls.fetch_cds_info(transcript)

        if 'cds_seq' in cds_info:
            return cds_info['cds_seq']

        return ""

    @classmethod
    def fetch_cds_info(cls, transcript):

        cds_info = {}

        five_prime_utr_seq = ""
        three_prime_utr_seq = ""
        if "translations" in transcript:
            translation = transcript['translations']
            translation_start = translation['loc_start']
            translation_end = translation['loc_end']

            cds_info['translation_start'] = translation_start
            cds_info['translation_end'] = translation_end
            cds_info['five_prime_utr_end'] = translation_start - 1
            cds_info['three_prime_utr_start'] = translation_end + 1

            if 'exons' in transcript:
                exons = transcript['exons']

                first_exon = exons[0]
                cds_info['five_prime_utr_start'] = first_exon['loc_start']
                cds_info['loc_region'] = first_exon['loc_region']

                start_exon = None
                end_exon = None
                # Find start exon
                for exon in exons:
                    exon_start = exon['loc_start']
                    exon_end = exon['loc_end']
                    overlap_score = ExonUtils.compute_overlap(exon_start, exon_end, translation_start, translation_end)
                    if overlap_score > 0:
                        start_exon = exon
                        break
#
#                 #  collect all the previous exons to calculate the five prime utr length
#                 #  Work here tomorrow
                five_prime_exon_iterator = iter(exons)
                current_exon = next(five_prime_exon_iterator)
                start_exon_order = start_exon['exon_order']

                # print('Start exon order ' + str(start_exon_order))
                while(current_exon['exon_order'] < start_exon_order):
                    # print(' 5 prime UTR exon %d' %current_exon['exon_order'])
                    five_prime_utr_seq = five_prime_utr_seq + current_exon['sequence']
                    current_exon = next(five_prime_exon_iterator)

                # Now add the overlapping bit
                start_exon_utr_len = translation_start - start_exon['loc_start']
#                 print(" start_exon_utr_len " + str(start_exon_utr_len))
#                 print("  start exon sequence " + start_exon['sequence'][:start_exon_utr_len])
                five_prime_utr_seq = five_prime_utr_seq + start_exon['sequence'][:start_exon_utr_len]

                # Find end exon
                exons_copy = exons.copy()
                exons_copy.reverse()
                for exon in exons_copy:
                    exon_start = exon['loc_start']
                    exon_end = exon['loc_end']
                    overlap_score = ExonUtils.compute_overlap(exon_start, exon_end, translation_start, translation_end)
                    if overlap_score > 0:
                        end_exon = exon
                        break
#
#                 #  collect all the previous exons to calculate the three prime utr length
#                 #  Work here tomorrow
                three_prime_exon_iterator = iter(exons_copy)
                current_exon = next(three_prime_exon_iterator)
                end_exon_order = end_exon['exon_order']

                # print('End exon order ' + str(end_exon_order))
                while(current_exon['exon_order'] > end_exon_order):
                    # print(' 3 prime UTR exon %d' %current_exon['exon_order'])
                    three_prime_utr_seq = current_exon['sequence'] + three_prime_utr_seq
                    current_exon = next(three_prime_exon_iterator)

                # Now add the overlapping bit for the 3 prime
                end_exon_utr_len = end_exon['loc_end'] - translation_end
#                 print(" end_exon_utr_len " + str(end_exon_utr_len))
#                 print("  end exon sequence " + end_exon['sequence'][-end_exon_utr_len:])
                three_prime_utr_seq = end_exon['sequence'][-end_exon_utr_len:] + three_prime_utr_seq

            cds_start_len = translation_start - start_exon['loc_start']

            cds_seq = start_exon['sequence'][cds_start_len:]
            exon_iterator = iter(exons)
            cur_exon = next(exon_iterator)
            while(end_exon['exon_order'] != cur_exon['exon_order']):
                if(cur_exon['exon_order'] > start_exon['exon_order']):
                    cds_seq = cds_seq + cur_exon['sequence']
                cur_exon = next(exon_iterator)

            last_exon = exons[-1]
            cds_info['three_prime_utr_end'] = last_exon['loc_end']

            cds_end_len = (translation_end - end_exon['loc_start']) + 1
            cds_seq = cds_seq + end_exon['sequence'][:cds_end_len]
            cds_info['cds_seq'] = cds_seq

            cds_info['five_prime_utr_seq'] = five_prime_utr_seq
            cds_info['five_prime_utr_length'] = len(five_prime_utr_seq)
            cds_info['three_prime_utr_seq'] = three_prime_utr_seq
            cds_info['three_prime_utr_length'] = len(three_prime_utr_seq)

        # print(cds_info)
        return cds_info
