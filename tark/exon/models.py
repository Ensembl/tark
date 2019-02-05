from django.db import models
from assembly.models import Assembly
from sequence.models import Sequence
from session.models import Session
from transcript.models import Transcript
from tark.fields import ChecksumField


# Create your models here.


class Exon(models.Model):

    MANY2ONE_RELATED = {'SEQUENCE': 'sequence', 'SESSION': 'session', 'ASSEMBLY': 'assembly'}
    ONE2MANY_RELATED = {'RELEASE_SET': 'exon_release_set', 'EXON_TRANSCRIPT': 'transcript'}

    exon_id = models.AutoField(primary_key=True)
    stable_id = models.CharField(max_length=64)
    stable_id_version = models.PositiveIntegerField()
    assembly = models.ForeignKey(Assembly, models.DO_NOTHING, blank=True, null=True)
    loc_start = models.PositiveIntegerField(blank=True, null=True)
    loc_end = models.PositiveIntegerField(blank=True, null=True)
    loc_strand = models.IntegerField(blank=True, null=True)
    loc_region = models.CharField(max_length=42, blank=True, null=True)
    loc_checksum = ChecksumField(max_length=20, blank=True, null=True)
    exon_checksum = ChecksumField(unique=True, max_length=20, blank=True, null=True)
    # seq_checksum = ChecksumField(unique=True, max_length=20, blank=True, null=True)
    sequence = models.ForeignKey(Sequence, models.DO_NOTHING, db_column='seq_checksum', blank=True, null=True)
    session = models.ForeignKey(Session, models.DO_NOTHING, blank=True, null=True)
    exon_release_set = models.ManyToManyField('release.ReleaseSet', through='release.ExonReleaseTag',
                                              related_name='exon_release_set')
    transcripts = models.ManyToManyField('transcript.Transcript', through='exon.ExonTranscript')

    class Meta:
        managed = False
        db_table = 'exon'


class ExonTranscript(models.Model):
    exon_transcript_id = models.AutoField(primary_key=True)
    transcript = models.ForeignKey(Transcript, models.DO_NOTHING, blank=True, null=True)
    exon = models.ForeignKey(Exon, models.DO_NOTHING, blank=True, null=True)
    exon_order = models.PositiveSmallIntegerField(blank=True, null=True)
    session = models.ForeignKey(Session, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'exon_transcript'
        unique_together = (('transcript', 'exon'),)
        ordering = ['exon_order']
