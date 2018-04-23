from django.db import models
from session.models import Session
from tark.fields import ChecksumField


class Sequence(models.Model):

    seq_checksum = ChecksumField(max_length=20, blank=False, null=False, primary_key=True)
    sequence = models.TextField(blank=True, null=True)
    # sequence = SequenceField(blank=True, null=True)
    session = models.ForeignKey(Session, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sequence'
