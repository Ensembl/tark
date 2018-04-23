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
import collections
import requests
from exon.models import ExonTranscript


class DiffUtils(object):

    @classmethod
    def get_diff_dict(cls, request, result_dict, params):

        result_data = result_dict.data
        count = result_data['count']
        results = result_data['results']
        diff_dict = collections.OrderedDict()

        (first_object_, second_object_) = cls.get_compare_objects(result_dict, params)

        print("COUNT ==================  " + str(count))

        if first_object_ is not None and second_object_ is not None:
            diff_set = DiffSet(first_object=first_object_, second_object=second_object_)
            diff_dict = diff_set.compare_objects()
            result_data['results'] = diff_dict
            result_data['count'] = 1  # for output
        else:
            result_data['results'] = diff_dict
            result_data['count'] = 0  # for output

        # add params
        print(params)
        for param_key, param_value in params.items():
            if "expand" not in param_key:
                result_data[param_key] = param_value

        # get host url - move to utils
        hostname = request.get_host()
        http_protocal = 'https' if request.is_secure() else 'http'
        print('hostname ' + hostname)
        print('http_protocal ' + http_protocal)

        host_url = http_protocal + '://' + hostname

        # get diff me
        query_url_diff_me = "/api/transcript/?stable_id=" + params['stable_id'] + "&assembly_name=" + \
                            params['diff_me_assembly'] + "&release_short_name=" + params['diff_me_release'] + \
                            "&expand_all=true"

        response_diff_me = requests.get(host_url + query_url_diff_me)
        print(response_diff_me.status_code)

        if response_diff_me.status_code == 200:
            diff_me_result = response_diff_me.json()
            print("===diff_me_result===========")
            print(diff_me_result)
            print("=============================")
            result_data['diff_me_transcript'] = diff_me_result

        # get diff with
        query_url_diff_with = "/api/transcript/?stable_id=" + params['stable_id'] + "&assembly_name=" + \
            params['diff_with_assembly'] + "&release_short_name=" + params['diff_with_release'] + \
            "&expand_all=true"

        response_diff_with = requests.get(host_url + query_url_diff_with)
        print(response_diff_with.status_code)

        if response_diff_with.status_code == 200:
            diff_with_result = response_diff_with.json()
            result_data['diff_with_transcript'] = diff_with_result

        result_dict.data = result_data
        return result_dict

    @classmethod
    def get_compare_objects(cls, result_dict, params):
        result_data = result_dict.data
        count = result_data['count']
        results = result_data['results']
        print("Count from get_compare_objects " + str(count))
        first_object = None
        second_object = None
        tr_in_diff_me_release = False
        tr_in_diff_with_release = False
#         tr_in_diff_me_assembly = False
#         tr_in_diff_with_assembly = False
        # no results, both objects None
        if count == 0:
            return (first_object, second_object)
        elif count == 1:
            # we can reach here if the object is not changed between releases
            # or the object is available only for one release and not other
            first_object = results[0]
            # check if in assembly
            if params['diff_me_assembly'] == first_object['assembly'] and \
                    params['diff_with_assembly'] == first_object['assembly']:

                if 'transcript_release_set' in first_object:
                    tr_release_sets = first_object['transcript_release_set']
                    for release in tr_release_sets:
                        if params['diff_me_release'] in release["shortname"]:
                            tr_in_diff_me_release = True
                        if params['diff_with_release'] in release["shortname"]:
                            tr_in_diff_with_release = True

                if tr_in_diff_me_release and tr_in_diff_with_release:
                    # both objects are same
                    second_object = first_object
                    return (first_object, second_object)
        elif count == 2:
            print("Reached cound 2")
            first_object = results[0]
            second_object = results[1]
            return (first_object, second_object)
        else:
            print("Something is seriously wrong\n")

        return (first_object, second_object)


class DiffSet(object):

    def __init__(self, first_object, second_object):
        self.first_object = first_object
        self.second_object = second_object

    def compare_objects(self):
        first_object = self.first_object
        second_object = self.second_object

        diff_dict = collections.OrderedDict()
        diff_dict['stable_id'] = None
        if first_object['stable_id'] == second_object['stable_id']:
            diff_dict['stable_id'] = first_object['stable_id']

        diff_dict['has_location_changed'] = self.has_location_changed()
        diff_dict['has_exon_set_changed'] = self.has_exon_set_changed()
        diff_dict['has_transcript_changed'] = self.has_transcript_changed()
        diff_dict['has_seq_changed'] = self.has_seq_changed()

#         print("=======FIRST==========")
#         print(first_object)
#         print("=======SECOND==========")
#         print(second_object)
#         print("=================")
        return diff_dict

    def has_location_changed(self):
        return not (self.first_object['loc_checksum'] == self.second_object['loc_checksum'])

    def has_exon_set_changed(self):
        return not (self.first_object['exon_set_checksum'] == self.second_object['exon_set_checksum'])

    def has_transcript_changed(self):
        return not (self.first_object['transcript_checksum'] == self.second_object['transcript_checksum'])

    def has_seq_changed(self):
        # when sequence is expanded
        if 'seq_checksum' in self.first_object['sequence'] and 'seq_checksum' in self.second_object['sequence']:
            return not(self.first_object['sequence']['seq_checksum'] == self.second_object['sequence']['seq_checksum'])

        return not(self.first_object['sequence'] == self.second_object['sequence'])
