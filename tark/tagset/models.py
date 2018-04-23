from django.db import models
from session.models import Session
from transcript.models import Transcript

# Create your models here.


class Tagset(models.Model):
    tagset_id = models.AutoField(primary_key=True)
    shortname = models.CharField(max_length=45, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    version = models.CharField(max_length=20, blank=True, null=True)
    is_current = models.IntegerField(blank=True, null=True)
    session = models.ForeignKey(Session, models.DO_NOTHING, blank=True, null=True)
    tagset_checksum = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tagset'
        unique_together = (('shortname', 'version'),)


class Tag(models.Model):
    transcript = models.ForeignKey(Transcript, models.DO_NOTHING)
    tagset = models.ForeignKey(Tagset, models.DO_NOTHING)
    session = models.ForeignKey(Session, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tag'
        unique_together = (('transcript', 'tagset'),)
