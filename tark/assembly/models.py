from django.db import models
from genome.models import Genome
from session.models import Session

# Create your models here.


class Assembly(models.Model):
    assembly_id = models.AutoField(primary_key=True)
    genome = models.ForeignKey(Genome, models.DO_NOTHING, blank=True, null=True)
    assembly_name = models.CharField(unique=True, max_length=128, blank=True, null=True)
    session = models.ForeignKey(Session, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'assembly'


class AssemblyAlias(models.Model):
    assembly_alias_id = models.AutoField(primary_key=True)
    alias = models.CharField(unique=True, max_length=64, blank=True, null=True)
    genome = models.ForeignKey(Genome, models.DO_NOTHING, blank=True, null=True)
    assembly = models.ForeignKey(Assembly, models.DO_NOTHING, blank=True, null=True)
    session = models.ForeignKey(Session, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'assembly_alias'
