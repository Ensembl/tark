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
from assembly.models import Assembly
from session.models import Session
from gene.models import Gene
from transcript.models import Transcript
from exon.models import Exon
from translation.models import Translation
from tark.fields import ChecksumField
from django.contrib import admin


class ReleaseSource(auto_prefetch.Model):
    ONE2MANY_RELATED = {'RELEASE_SET': 'release_set'}

    source_id = models.AutoField(primary_key=True)
    shortname = models.CharField(unique=True, max_length=24, blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'release_source'


class ReleaseSet(auto_prefetch.Model):
    MANY2ONE_RELATED = {'RELEASE_SOURCE': 'release_source'}
    ONE2MANY_RELATED = {'RELEASE_SET': 'release_set'}

    release_id = models.AutoField(primary_key=True)
    shortname = models.CharField(max_length=24, blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    assembly = auto_prefetch.ForeignKey(Assembly, models.DO_NOTHING, blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    session = auto_prefetch.ForeignKey(Session, models.DO_NOTHING, blank=True, null=True)
    release_checksum = ChecksumField(unique=True, max_length=20, blank=True, null=True)
    source = auto_prefetch.ForeignKey(ReleaseSource, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'release_set'
        unique_together = (('shortname', 'assembly', 'source'),)


class ReleaseStats(auto_prefetch.Model):
    release_stats_id = models.AutoField(primary_key=True)
    release = auto_prefetch.ForeignKey(
        ReleaseSet,
        models.DO_NOTHING,
        blank=True,
        null=True
    )
    json = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'release_stats'
        # unique_together = (('release'),)
        # display most recent release at top of the table
        ordering = ['-release_stats_id']


class GeneReleaseTag(auto_prefetch.Model):
    feature = auto_prefetch.ForeignKey(Gene, models.DO_NOTHING)
    release = auto_prefetch.ForeignKey(ReleaseSet, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'gene_release_tag'
        unique_together = (('feature', 'release'),)


class TranscriptReleaseTag(auto_prefetch.Model):
    ONE2MANY_RELATED = {'TRANSCRIPTRELEASETAGRELATIONSHIP': "transcript_release_tag_relationship"
                        }

    transcript_release_id = models.AutoField(primary_key=True)
    feature = auto_prefetch.ForeignKey(Transcript, models.DO_NOTHING)
    release = auto_prefetch.ForeignKey(ReleaseSet, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'transcript_release_tag'
        unique_together = (('feature', 'release'),)


class RelationshipType(auto_prefetch.Model):
    relationship_type_id = models.AutoField(primary_key=True)
    shortname = models.CharField(max_length=24, blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    version = models.CharField(max_length=32, blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'relationship_type'
        unique_together = (('shortname', 'version'),)


class TranscriptReleaseTagRelationshipAdmin(admin.ModelAdmin):
    search_fields = ["transcript_release_tag_relationship__transcript_release_object__transcript_release_tag",
                     "transcript_release_tag_relationship__transcript_release_subject__transcript_release_tag"]
    list_select_related = ('transcript_release_tag', 'transcript')


class TranscriptReleaseTagRelationship(auto_prefetch.Model):
    transcript_transcript_id = models.AutoField(primary_key=True)
    transcript_release_object = auto_prefetch.ForeignKey(TranscriptReleaseTag, models.DO_NOTHING,
                                                  related_name='ens_to_refseq')
    transcript_release_subject = auto_prefetch.ForeignKey(TranscriptReleaseTag, models.DO_NOTHING,
                                                   related_name='refseq_to_ens')
    relationship_type = auto_prefetch.ForeignKey(RelationshipType, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'transcript_release_tag_relationship'


class ExonReleaseTag(auto_prefetch.Model):
    feature = auto_prefetch.ForeignKey(Exon, models.DO_NOTHING)
    release = auto_prefetch.ForeignKey(ReleaseSet, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'exon_release_tag'
        unique_together = (('feature', 'release'),)


class TranslationReleaseTag(auto_prefetch.Model):
    feature = auto_prefetch.ForeignKey(Translation, models.DO_NOTHING)
    release = auto_prefetch.ForeignKey(ReleaseSet, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'translation_release_tag'
        unique_together = (('feature', 'release'),)
