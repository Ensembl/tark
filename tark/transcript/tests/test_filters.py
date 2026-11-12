from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from assembly.models import Assembly
from release.models import ReleaseSet, ReleaseSource, TranscriptReleaseTag
from transcript.drf.filters import TranscriptFilterBackend
from transcript.models import Transcript


class TranscriptFilterBackendTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = Transcript.objects.create(stable_id='ENST00000252934', stable_id_version=10)
        cls.second = Transcript.objects.create(stable_id='ENST00000380152', stable_id_version=1)
        source = ReleaseSource.objects.create(shortname='Ensembl')
        grch37 = Assembly.objects.create(assembly_name='GRCh37')
        grch38 = Assembly.objects.create(assembly_name='GRCh38')
        for assembly, shortname in ((grch37, '116'), (grch38, '116'), (grch38, '117')):
            release = ReleaseSet.objects.create(assembly=assembly, shortname=shortname, source=source)
            TranscriptReleaseTag.objects.create(feature=cls.first, release=release)
            if shortname == '117':
                TranscriptReleaseTag.objects.create(feature=cls.second, release=release)

    def filter_transcripts(self, **params):
        request = Request(APIRequestFactory().get('/api/transcript/', params))
        return TranscriptFilterBackend().filter_queryset(
            request, Transcript.objects.order_by('pk'), None,
        )

    def test_unfiltered_pagination_count_avoids_distinct_subquery(self):
        with CaptureQueriesContext(connection) as queries:
            count = self.filter_transcripts().count()

        self.assertEqual(count, 2)
        self.assertEqual(len(queries), 1)
        self.assertNotIn('DISTINCT', queries[0]['sql'].upper())

    def test_stable_id_filter_returns_matching_transcript(self):
        transcripts = self.filter_transcripts(stable_id=self.first.stable_id, stable_id_version=10)
        self.assertEqual(list(transcripts), [self.first])

    def test_release_filter_returns_each_transcript_once_across_assemblies(self):
        transcripts = self.filter_transcripts(release_short_name='116')
        self.assertEqual(transcripts.count(), 1)
        self.assertEqual(list(transcripts), [self.first])

    def test_source_filter_returns_each_transcript_once_across_releases(self):
        transcripts = self.filter_transcripts(source_name='Ensembl')
        self.assertEqual(transcripts.count(), 2)
        self.assertEqual(list(transcripts), [self.first, self.second])

    def test_combined_release_and_source_filters_return_unique_transcripts(self):
        transcripts = self.filter_transcripts(release_short_name='116', source_name='Ensembl')
        self.assertEqual(transcripts.count(), 1)
        self.assertEqual(list(transcripts), [self.first])
