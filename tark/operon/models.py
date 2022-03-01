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

from django.db import models
from assembly.models import Assembly
from sequence.models import Sequence
from session.models import Session
from transcript.models import Transcript


# Create your models here.


class Operon(models.Model):
    operon_id = models.AutoField(primary_key=True)
    stable_id = models.CharField(max_length=64, blank=True, null=True)
    stable_id_version = models.PositiveIntegerField(blank=True, null=True)
    assembly = models.ForeignKey(Assembly, models.DO_NOTHING, blank=True, null=True)
    loc_start = models.PositiveIntegerField(blank=True, null=True)
    loc_end = models.PositiveIntegerField(blank=True, null=True)
    loc_strand = models.IntegerField(blank=True, null=True)
    loc_region = models.CharField(max_length=42, blank=True, null=True)
    operon_checksum = models.CharField(max_length=20, blank=True, null=True)
    seq_checksum = models.ForeignKey(Sequence, models.DO_NOTHING, db_column='seq_checksum', blank=True, null=True)
    session = models.ForeignKey(Session, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'operon'


class OperonTranscript(models.Model):
    operon_transcript_id = models.AutoField(primary_key=True)
    stable_id = models.CharField(max_length=64, blank=True, null=True)
    stable_id_version = models.PositiveIntegerField(blank=True, null=True)
    operon = models.ForeignKey(Operon, models.DO_NOTHING, blank=True, null=True)
    transcript = models.ForeignKey(Transcript, models.DO_NOTHING, blank=True, null=True)
    session = models.ForeignKey(Session, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'operon_transcript'
        unique_together = (('operon', 'transcript'),)
