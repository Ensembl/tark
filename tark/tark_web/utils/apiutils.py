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


class ApiUtils(object):

    @classmethod
    def get_host_url(cls, request):
        hostname = request.get_host()
        http_protocal = 'https' if request.is_secure() else 'http'
        host_url = http_protocal + '://' + hostname
        return host_url

    @classmethod
    def get_feature_url(cls, request, feature_type, diff_type, diff_params):

        host_url = cls.get_host_url(request)
        query_url = "/api/" + feature_type + "/?"

        query_param = "stable_id=" + diff_params[diff_type + '_stable_id'] + "&assembly_name=" + \
                      diff_params[diff_type + '_assembly'] + "&release_short_name=" + diff_params[
                          diff_type + '_release'] + \
                      "&expand_all=true"

        return host_url + query_url + query_param

    @classmethod
    def get_release_set_url(cls, request):

        host_url = cls.get_host_url(request)
        query_url = "/api/release/nopagination"
        return host_url + query_url
