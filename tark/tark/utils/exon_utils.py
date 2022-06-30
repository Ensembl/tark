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
                exon2_stable_id_version = str(exon2['stable_id']) + '.' + str(
                    exon2['stable_id_version'])  # @UnusedVariable

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

        if "translations" in transcript and len(transcript['translations']) > 0:

            translations = transcript["translations"]
            if type(translations) is list and len(translations) > 0:
                translation = translations[0]
            else:
                translation = translations

            cds_info["translation_start"] = translation["loc_start"]
            cds_info["translation_end"] = translation["loc_end"]
            cds_info["three_prime_utr_start"] = ExonUtils.get_or_default(transcript, "three_prime_utr_start", 0)
            cds_info["three_prime_utr_end"] = ExonUtils.get_or_default(transcript, "three_prime_utr_end", 0)
            three_prime_utr_seq = ExonUtils.get_or_default(transcript, "three_prime_utr_seq", "")
            cds_info["three_prime_utr_seq"] = three_prime_utr_seq
            cds_info["three_prime_utr_length"] = len(three_prime_utr_seq)
            cds_info["five_prime_utr_start"] = ExonUtils.get_or_default(transcript, "five_prime_utr_start", 0)
            cds_info["five_prime_utr_end"] = ExonUtils.get_or_default(transcript, "five_prime_utr_end", 0)
            five_prime_utr_seq = ExonUtils.get_or_default(transcript, "five_prime_utr_seq", "")
            cds_info["five_prime_utr_seq"] = five_prime_utr_seq
            cds_info["five_prime_utr_length"] = len(five_prime_utr_seq)
            cds_info["loc_region"] = transcript["loc_region"]
            cds_info["loc_strand"] = transcript["loc_strand"]

            cds_info['cds_seq'] = None

            if 'sequence' in transcript and 'sequence' in transcript['sequence']:
                last_exon = sorted(transcript["exons"], key=lambda e: e["exon_order"])[-1]
                transcript['sequence']['sequence'] = (
                    cls.remove_polyA_tail(transcript['sequence']['sequence'], last_exon['sequence']))
                cds_seq = cls.get_cds_sequence(transcript['sequence']['sequence'],
                                               len(cds_info['five_prime_utr_seq']),
                                               len(cds_info['three_prime_utr_seq']))
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

    @staticmethod
    def get_or_default(feature, field, default_value):
        if field in feature and feature[field] is not None:
            return feature[field]
        return default_value
