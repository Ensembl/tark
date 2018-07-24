from django.db import models
from assembly.models import Assembly
from session.models import Session
from gene.models import Gene
from transcript.models import Transcript
from exon.models import Exon
from translation.models import Translation
from tark.fields import ChecksumField


class ReleaseSource(models.Model):
    source_id = models.AutoField(primary_key=True)
    shortname = models.CharField(unique=True, max_length=24, blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'release_source'


class ReleaseSet(models.Model):

    release_id = models.AutoField(primary_key=True)
    shortname = models.CharField(max_length=24, blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    assembly = models.ForeignKey(Assembly, models.DO_NOTHING, blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    session = models.ForeignKey(Session, models.DO_NOTHING, blank=True, null=True)
    release_checksum = ChecksumField(unique=True, max_length=20, blank=True, null=True)
    source = models.ForeignKey(ReleaseSource, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'release_set'
        unique_together = (('shortname', 'assembly', 'source'),)


class GeneReleaseTag(models.Model):
    feature = models.ForeignKey(Gene, models.DO_NOTHING)
    release = models.ForeignKey(ReleaseSet, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'gene_release_tag'
        unique_together = (('feature', 'release'),)


class TranscriptReleaseTag(models.Model):
    feature = models.ForeignKey(Transcript, models.DO_NOTHING)
    release = models.ForeignKey(ReleaseSet, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'transcript_release_tag'
        unique_together = (('feature', 'release'),)
        #ordering = ['release']


class ExonReleaseTag(models.Model):

    feature = models.ForeignKey(Exon, models.DO_NOTHING)
    release = models.ForeignKey(ReleaseSet, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'exon_release_tag'
        unique_together = (('feature', 'release'),)


class TranslationReleaseTag(models.Model):
    feature = models.ForeignKey(Translation, models.DO_NOTHING)
    release = models.ForeignKey(ReleaseSet, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'translation_release_tag'
        unique_together = (('feature', 'release'),)
