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
from tark_drf.utils.drf_utils import DrfUtils
from transcript.models import Transcript
from gene.models import Gene
from exon.models import Exon
from release.models import TranscriptReleaseTag


# ./manage.py test tark_drf.tests.test_drf_utils --settings=tark.settings.test
class DrfUtilsTest(TestCase):

    def test_get_related_entities(self):
        expected_related_models = ['sequence', 'session', 'assembly',
                                   'transcript_release_set', 'genes', 'translations', 'exons']
        related_models = DrfUtils.get_related_entities(Transcript)
        self.assertListEqual(related_models, expected_related_models)

        expected_related_models = ['session', 'assembly', 'name', 'gene_release_set']
        related_models = DrfUtils.get_related_entities(Gene)
        self.assertListEqual(related_models, expected_related_models)

        expected_related_models = ['sequence', 'session', 'assembly', 'exon_release_set', 'transcript']
        related_models = DrfUtils.get_related_entities(Exon)
        self.assertListEqual(related_models, expected_related_models)

        expected_related_models = ['transcript_release_tag_relationship']
        related_models = DrfUtils.get_related_entities(TranscriptReleaseTag)
        self.assertListEqual(related_models, expected_related_models)
