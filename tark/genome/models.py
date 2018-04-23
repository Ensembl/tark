from django.db import models
from session.models import Session

# Create your models here.


class Genome(models.Model):
    genome_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    tax_id = models.PositiveIntegerField(blank=True, null=True)
    session = models.ForeignKey(Session, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'genome'
        unique_together = (('name', 'tax_id'),)
