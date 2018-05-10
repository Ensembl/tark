'''
Copyright [1999-2015] Wellcome Trust Sanger Institute and the EMBL-European Bioinformatics Institute
Copyright [2016-2018] EMBL-European Bioinformatics Institute

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''


from django.db import models
from assembly.models import Assembly
from django.contrib.sessions.models import Session
from tark.fields import ChecksumField
from sequence.models import Sequence
from gene.models import Gene


class Transcript(models.Model):

    MANY2ONE_RELATED = {'SEQUENCE': 'sequence', 'SESSION': 'session', 'ASSEMBLY': 'assembly'}
    ONE2MANY_RELATED = {'RELEASE_SET': 'transcript_release_set', 'GENE': 'genes',
                        'TRANSLATION': "translations", "EXONTRANSCRIPT": "exons"
                        }
    #                   'TRANSCRIPT_EXON': 'exons'

    # You'll normally want to ensure that you've set an appropriate related_name argument on the relationship, that you can use as the field name.

    transcript_id = models.AutoField(primary_key=True)
    stable_id = models.CharField(max_length=64)
    stable_id_version = models.PositiveIntegerField()
    assembly = models.ForeignKey(Assembly, models.DO_NOTHING, blank=True, null=True)
    loc_start = models.PositiveIntegerField(blank=True, null=True)
    loc_end = models.PositiveIntegerField(blank=True, null=True)
    loc_strand = models.IntegerField(blank=True, null=True)
    loc_region = models.CharField(max_length=42, blank=True, null=True)
    loc_checksum = ChecksumField(unique=True, max_length=20, blank=True, null=True)
    exon_set_checksum = ChecksumField(unique=True, max_length=20, blank=True, null=True)
    transcript_checksum = ChecksumField(unique=True, max_length=20, blank=True, null=True)
    sequence = models.ForeignKey(Sequence, models.DO_NOTHING, db_column='seq_checksum', blank=True, null=True)
    session = models.ForeignKey(Session, models.DO_NOTHING, blank=True, null=True)
    transcript_release_set = models.ManyToManyField('release.ReleaseSet', through='release.TranscriptReleaseTag',
                                                    related_name='transcript_release_set')
    genes = models.ManyToManyField('gene.Gene', through='transcript.TranscriptGene')
    exons = models.ManyToManyField('exon.Exon', through='exon.ExonTranscript')
    translations = models.ManyToManyField('translation.Translation', through='translation.TranslationTranscript')

    class Meta:
        managed = False
        db_table = 'transcript'


class TranscriptGene(models.Model):
    gene_transcript_id = models.AutoField(primary_key=True)
    gene = models.ForeignKey(Gene, models.DO_NOTHING, blank=True, null=True)
    transcript = models.ForeignKey(Transcript, models.DO_NOTHING, blank=True, null=True)
    session = models.ForeignKey(Session, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transcript_gene'
        unique_together = (('gene', 'transcript'),)




