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
from tark.fields import ChecksumField, HGNCField
from genenames.models import GeneNames


class Gene(auto_prefetch.Model):
    MANY2ONE_RELATED = {'SESSION': 'session', 'ASSEMBLY': 'assembly', 'HGNC': 'name'}
    ONE2MANY_RELATED = {'RELEASE_SET': 'gene_release_set', 'GENE_TRANSCRIPT': 'transcripts'}

    gene_id = models.AutoField(primary_key=True)
    stable_id = models.CharField(max_length=64)
    stable_id_version = models.PositiveIntegerField()
    assembly = auto_prefetch.ForeignKey(Assembly, models.DO_NOTHING, blank=True, null=True)
    loc_start = models.PositiveIntegerField(blank=True, null=True)
    loc_end = models.PositiveIntegerField(blank=True, null=True)
    loc_strand = models.IntegerField(blank=True, null=True)
    loc_region = models.CharField(max_length=42, blank=True, null=True)
    loc_checksum = ChecksumField(unique=True, max_length=20, blank=True, null=True)
    name = HGNCField(GeneNames, models.DO_NOTHING, to_field='external_id', blank=True, null=True)
    gene_checksum = ChecksumField(unique=True, max_length=20, blank=True, null=True)
    session = auto_prefetch.ForeignKey(Session, models.DO_NOTHING, blank=True, null=True)
    gene_release_set = models.ManyToManyField('release.ReleaseSet', through='release.GeneReleaseTag',
                                              related_name='gene_release_set')

    class Meta:
        managed = False
        db_table = 'gene'
