'''
Copyright [1999-2015] Wellcome Trust Sanger Institute and the EMBL-European Bioinformatics Institute
Copyright [2016-2024] EMBL-European Bioinformatics Institute

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
import auto_prefetch
from django.db import models
from assembly.models import Assembly

from transcript.models import Transcript
from tark.fields import ChecksumField
from sequence.models import Sequence
from session.models import Session


class Translation(auto_prefetch.Model):
    MANY2ONE_RELATED = {'SEQUENCE': 'sequence', 'SESSION': 'session', 'ASSEMBLY': 'assembly'}
    ONE2MANY_RELATED = {'RELEASE_SET': 'translation_release_set', 'TRANSCRIPT': "transcripts"}

    translation_id = models.AutoField(primary_key=True)
    stable_id = models.CharField(max_length=64)
    stable_id_version = models.PositiveIntegerField()
    assembly = auto_prefetch.ForeignKey(Assembly, models.DO_NOTHING, blank=True, null=True)
    loc_start = models.PositiveIntegerField(blank=True, null=True)
    loc_end = models.PositiveIntegerField(blank=True, null=True)
    loc_strand = models.IntegerField(blank=True, null=True)
    loc_region = models.CharField(max_length=42, blank=True, null=True)
    loc_checksum = ChecksumField(unique=True, max_length=20, blank=True, null=True)
    translation_checksum = ChecksumField(unique=True, max_length=20, blank=True, null=True)
    sequence = auto_prefetch.ForeignKey(Sequence, models.DO_NOTHING, db_column='seq_checksum', blank=True, null=True)
    session = auto_prefetch.ForeignKey(Session, models.DO_NOTHING, blank=True, null=True)
    translation_release_set = models.ManyToManyField('release.ReleaseSet', through='release.TranslationReleaseTag',
                                                     related_name='translation_release_set')
    transcripts = models.ManyToManyField('transcript.Transcript', through='translation.TranslationTranscript')

    class Meta:
        managed = False
        db_table = 'translation'


class TranslationTranscript(auto_prefetch.Model):
    transcript_translation_id = models.AutoField(primary_key=True)
    transcript = auto_prefetch.ForeignKey(Transcript, models.DO_NOTHING, blank=True, null=True)
    translation = auto_prefetch.ForeignKey(Translation, models.DO_NOTHING, blank=True, null=True)
    session = auto_prefetch.ForeignKey(Session, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'translation_transcript'
        unique_together = (('transcript', 'translation'),)
