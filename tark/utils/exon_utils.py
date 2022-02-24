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
                if exon1['assembly'] == exon2['assembly'] and exon1['loc_region'] == exon2['loc_region']:
                    overlap_score = cls.compute_overlap(exon1['loc_start'], exon1['loc_end'], exon2['loc_start'],
                                                        exon2['loc_end'])
                    if overlap_score > 0:

                        cumulative_overlap_score = cumulative_overlap_score + 1
                        current_compare_result['overlapping_exon'] = exon2

                        current_compare_result['loc_checksum'] = exon1['loc_checksum'] == exon2['loc_checksum']
                        current_compare_result['seq_checksum'] = exon1['seq_checksum'] == exon2['seq_checksum']

                        matched_exons.append(current_compare_result)
                else:
                    # different assembly won't overlap, so check seq_checksum
                    if exon1['seq_checksum'] == exon2['seq_checksum']:

                        cumulative_overlap_score = cumulative_overlap_score + 1
                        current_compare_result['overlapping_exon'] = exon2

                        current_compare_result['loc_checksum'] = exon1['loc_checksum'] == exon2['loc_checksum']
                        current_compare_result['seq_checksum'] = exon1['seq_checksum'] == exon2['seq_checksum']

                        matched_exons.append(current_compare_result)

            compare_results.append((cur_exon, matched_exons))

        compare_results.insert(0, ("cumulative_overlap_score", cumulative_overlap_score))
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

        start_exon = None
        end_exon = None
        five_prime_utr_seq = ""
        three_prime_utr_seq = ""
        exons = None
        if "translations" in transcript and len(transcript['translations']) > 0:
            translations = transcript['translations']

            if type(translations) is list and len(translations) > 0:
                translation = translations[0]
            else:
                translation = translations
            translation_start = translation['loc_start']
            translation_end = translation['loc_end']

            cds_info['translation_start'] = translation_start
            cds_info['translation_end'] = translation_end
            cds_info['loc_strand'] = transcript['loc_strand']

            if transcript['loc_strand'] == -1:
                cds_info['three_prime_utr_start'] = translation_start - 1
                cds_info['five_prime_utr_end'] = translation_end + 1
            else:
                cds_info['five_prime_utr_end'] = translation_start - 1
                cds_info['three_prime_utr_start'] = translation_end + 1

            if 'exons' in transcript:
                exons = transcript['exons']

                first_exon = exons[0]
                if transcript['loc_strand'] == -1:
                    cds_info['five_prime_utr_start'] = first_exon['loc_end']
                else:
                    cds_info['five_prime_utr_start'] = first_exon['loc_start']

                cds_info['loc_region'] = first_exon['loc_region']


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
                if transcript['loc_strand'] == -1:
                    start_exon_utr_len = start_exon['loc_end'] - translation_end
                    five_prime_utr_seq = five_prime_utr_seq + start_exon['sequence'][:start_exon_utr_len]
                else:
                    start_exon_utr_len = translation_start - start_exon['loc_start']
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
                if transcript['loc_strand'] == -1:
                    end_exon_utr_len = translation_start - end_exon['loc_start']
                    if end_exon_utr_len > 0:
                        three_prime_utr_seq = end_exon['sequence'][-end_exon_utr_len:] + three_prime_utr_seq
                else:
                    end_exon_utr_len = end_exon['loc_end'] - translation_end
                    if end_exon_utr_len > 0:
                        three_prime_utr_seq = end_exon['sequence'][-end_exon_utr_len:] + three_prime_utr_seq

            if start_exon is not None:
                cds_start_len = translation_start - start_exon['loc_start']
                cds_seq = start_exon['sequence'][cds_start_len:]

            if exons is not None:
                last_exon = exons[-1]

                if transcript['loc_strand'] == -1:
                    if len(three_prime_utr_seq) > 0:
                        cds_info['three_prime_utr_end'] = last_exon['loc_start']
                    else:
                        cds_info['three_prime_utr_start'] = 0
                        cds_info['three_prime_utr_end'] = 0
                else:
                    if len(three_prime_utr_seq) > 0:
                        cds_info['three_prime_utr_end'] = last_exon['loc_end']
                    else:
                        cds_info['three_prime_utr_start'] = 0
                        cds_info['three_prime_utr_end'] = 0

            cds_info['five_prime_utr_seq'] = five_prime_utr_seq
            cds_info['five_prime_utr_length'] = len(five_prime_utr_seq)
            cds_info['three_prime_utr_seq'] = three_prime_utr_seq
            cds_info['three_prime_utr_length'] = len(three_prime_utr_seq)

            cds_info['cds_seq'] = None
            if 'sequence' in transcript and 'sequence' in transcript['sequence']:
                transcript['sequence']['sequence'] = (cls.remove_polyA_tail(transcript['sequence']['sequence'], last_exon['sequence']))
                cds_seq = cls.get_cds_sequence(transcript['sequence']['sequence'],
                                               cds_info['five_prime_utr_length'],
                                               cds_info['three_prime_utr_length'])
                cds_info['cds_seq'] = cds_seq

        return cds_info

    @classmethod
    def remove_polyA_tail(cls, transcript_sequence, last_exon_sequence):

        cdna_length = len(transcript_sequence)
        last_exon_length = len(last_exon_sequence)

        last_exon_seq_start_position = transcript_sequence.find(last_exon_sequence)

        polyA_tail_length = cdna_length - (last_exon_seq_start_position + last_exon_length)

        if polyA_tail_length > 0:
            polya_tail_truncated_seq = transcript_sequence[:-polyA_tail_length]
        else:
            polya_tail_truncated_seq = transcript_sequence

        return polya_tail_truncated_seq


    @classmethod
    def get_cds_sequence(cls, sequence_data, five_prime_utr_len=0, three_prime_utr_len=0):
        if int(five_prime_utr_len) > 0 and int(three_prime_utr_len) > 0:
            sequence_data = sequence_data[int(five_prime_utr_len):]
            sequence_data = sequence_data[:-int(three_prime_utr_len)]
        elif int(five_prime_utr_len) > 0:
            sequence_data = sequence_data[int(five_prime_utr_len):]
            # sequence_data = sequence_data[:int(five_prime_utr_len)]
        elif int(three_prime_utr_len) > 0:
            # sequence_data = sequence_data[-(int(three_prime_utr_len)):]
            sequence_data = sequence_data[:-int(three_prime_utr_len)]

        return sequence_data
