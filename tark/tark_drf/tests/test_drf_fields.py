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

from django.test.testcases import TestCase
from transcript.models import Transcript
from tark_drf.utils.drf_fields import DrfFields, CommonFields
from coreapi.document import Field


# ./manage.py test tark_drf.tests.test_drf_fields --settings=tark.settings.test
class DrfFieldsTest(TestCase):

    def test_get_expand_field(self):
        expected_field = Field(name='expand',
                               required=False,
                               location='query', schema=None,
                               description='comma separated list of objects to expand (eg:<br/> ' \
                                           'sequence,session,assembly,transcript_release_set,genes,translations,<br/>exons,)',
                               type='string', example=None)
        expanded_field = DrfFields.get_expand_field(Transcript)
        self.assertEqual(expected_field, expanded_field)

        exptected_expand_all_field = Field(name='expand_all', required=False,
                                           location='query', schema=None,
                                           description='selecting true will expand all the related fields, ' \
                                                       'to selectively expand, use expand above',
                                           type='boolean', example=None)
        expanded_all_field = DrfFields.get_expand_all_field()
        self.assertEqual(exptected_expand_all_field, expanded_all_field)

        common_query_set_fields = CommonFields.get_common_query_set(Transcript)
        self.assertIsNotNone(common_query_set_fields)

        query_set_fields = CommonFields.get_expand_query_set(Transcript)
        self.assertIsNotNone(query_set_fields)

        expand_all_mandatory_query_set_fields = CommonFields.get_expand_all_mandatory_query_set(Transcript)
        self.assertIsNotNone(expand_all_mandatory_query_set_fields)
