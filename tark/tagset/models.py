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
import auto_prefetch
from django.db import models
from session.models import Session
from transcript.models import Transcript


# Create your models here.


class Tagset(auto_prefetch.Model):
    tagset_id = models.AutoField(primary_key=True)
    shortname = models.CharField(max_length=45, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    version = models.CharField(max_length=20, blank=True, null=True)
    is_current = models.IntegerField(blank=True, null=True)
    session = auto_prefetch.ForeignKey(Session, models.DO_NOTHING, blank=True, null=True)
    tagset_checksum = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tagset'
        unique_together = (('shortname', 'version'),)


class Tag(auto_prefetch.Model):
    transcript = auto_prefetch.ForeignKey(Transcript, models.DO_NOTHING)
    tagset = auto_prefetch.ForeignKey(Tagset, models.DO_NOTHING)
    session = auto_prefetch.ForeignKey(Session, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tag'
        unique_together = (('transcript', 'tagset'),)
