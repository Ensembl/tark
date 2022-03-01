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

from release.utils.release_utils import ReleaseUtils


class RequestUtils(object):

    @classmethod
    def get_query_params(cls, request, diff_type=None):
        params_diff = {}
        stable_id_cur = request.query_params.get(diff_type + '_stable_id', None)
        if '.' in stable_id_cur:
            stable_id, stable_id_version = stable_id_cur.split('.')
            params_diff['stable_id'] = stable_id
            params_diff['stable_id_version'] = stable_id_version
        else:
            params_diff['stable_id'] = request.query_params.get(diff_type + '_stable_id', None)

        params_diff['release_short_name'] = request.query_params.get(diff_type + '_release',
                                                                     ReleaseUtils.get_latest_release())
        params_diff['assembly_name'] = request.query_params.get(diff_type + '_assembly',
                                                                ReleaseUtils.get_latest_assembly())
        params_diff['source_name'] = request.query_params.get(diff_type + '_source',
                                                              ReleaseUtils.get_default_source())
        # params_diff['expand'] = request.query_params.get('expand', "transcript_release_set,translations, sequence")
        params_diff['expand_all'] = request.query_params.get('expand_all', "true")

        return params_diff

    @classmethod
    def get_query_param_string(self, params):
        param_string = ""
        for key, value in params.items():  # @IgnorePep8

            if value is not None and len(value) > 0:
                param_string = param_string + key + "=" + value + "&"

        if len(param_string) > 0:
            param_string = param_string.rstrip('&')

        return param_string
