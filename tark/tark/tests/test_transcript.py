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

from rest_framework.test import APITestCase
from transcript.models import Transcript
from django.urls.base import reverse
from rest_framework import status
import json


# ./manage.py test tark.tests.test_transcript --settings=tark.settings.test


class TranscriptTest(APITestCase):
    fixtures = ['transcript']

    # multi_db = True

    def test_transcript(self):
        """
        Ensure we get all the fields we need
        """
        url = reverse('transcript_list')
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Transcript.objects.count(), 7)

        data = {'stable_id': 'ENST00000380152'}
        response = self.client.get(url, data, format='json')
        transcript_152 = json.loads(json.dumps(response.data))
        self.assertEqual(transcript_152["count"], 1)
        current_transcript = transcript_152['results'][0]
        self.assertEqual(current_transcript['stable_id'], 'ENST00000380152')
        self.assertEqual(current_transcript['stable_id_version'], 7)
