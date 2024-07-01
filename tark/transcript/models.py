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

from tark.fields import ChecksumField
from sequence.models import Sequence
from gene.models import Gene
from session.models import Session

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class Transcript(auto_prefetch.Model):
    MANY2ONE_RELATED = {'SEQUENCE': 'sequence', 'SESSION': 'session', 'ASSEMBLY': 'assembly'}
    ONE2MANY_RELATED = {'RELEASE_SET': 'transcript_release_set', 'GENE': 'genes',
                        'TRANSLATION': "translations", "EXONTRANSCRIPT": "exons"
                        }

    # You'll normally want to ensure that you've set an appropriate related_name argument on the relationship,
    # that you can use as the field name.

    transcript_id = models.AutoField(primary_key=True)
    stable_id = models.CharField(max_length=64)
    stable_id_version = models.PositiveIntegerField()
    assembly = auto_prefetch.ForeignKey(Assembly, models.DO_NOTHING, blank=True, null=True)
    loc_start = models.PositiveIntegerField(blank=True, null=True)
    loc_end = models.PositiveIntegerField(blank=True, null=True)
    loc_strand = models.IntegerField(blank=True, null=True)
    loc_region = models.CharField(max_length=42, blank=True, null=True)
    loc_checksum = ChecksumField(unique=True, max_length=20, blank=True, null=True)
    exon_set_checksum = ChecksumField(unique=True, max_length=20, blank=True, null=True)
    transcript_checksum = ChecksumField(unique=True, max_length=20, blank=True, null=True)
    sequence = auto_prefetch.ForeignKey(Sequence, models.DO_NOTHING, db_column='seq_checksum', blank=True, null=True)
    session = auto_prefetch.ForeignKey(Session, models.DO_NOTHING, blank=True, null=True)
    transcript_release_set = models.ManyToManyField('release.ReleaseSet', through='release.TranscriptReleaseTag',
                                                    related_name='transcript_release_set')
    biotype = models.CharField(max_length=40, blank=True, null=True)
    genes = models.ManyToManyField('gene.Gene', through='transcript.TranscriptGene', related_name='transcripts')
    exons = models.ManyToManyField('exon.Exon', through='exon.ExonTranscript')
    translations = models.ManyToManyField('translation.Translation', through='translation.TranslationTranscript')

    three_prime_utr_start = models.PositiveIntegerField(blank=True, null=True)
    three_prime_utr_end = models.PositiveIntegerField(blank=True, null=True)
    three_prime_utr_seq = models.TextField(blank=True, null=True)
    three_prime_utr_checksum = ChecksumField(unique=True, max_length=20, blank=True, null=True)
    five_prime_utr_start = models.PositiveIntegerField(blank=True, null=True)
    five_prime_utr_end = models.PositiveIntegerField(blank=True, null=True)
    five_prime_utr_seq = models.TextField(blank=True, null=True)
    five_prime_utr_checksum = ChecksumField(unique=True, max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transcript'

    @classmethod
    def fetch_mane_transcript_and_type(cls, transcript_id=None):

        transcript = None
        source = "Ensembl"
        if transcript_id is not None:
            transcript = Transcript.objects.get(pk=transcript_id)

        if transcript is not None:
            try:
                source = transcript.transcript_release_set.all()[:1].get().source.shortname
            except Exception as e:
                logger.error("Exception from  get_mane_transcript " + str(e))

        if "Ensembl" in source:
            raw_sql = "SELECT DISTINCT\
                        t1.transcript_id, t1.stable_id as ens_stable_id, t1.stable_id_version as ens_stable_id_version,\
                        relationship_type.shortname as mane_type,\
                        t2.stable_id as refseq_stable_id, t2.stable_id_version as refseq_stable_id_version \
                        FROM \
                        transcript t1 \
                        JOIN transcript_release_tag trt1 ON t1.transcript_id=trt1.feature_id \
                        JOIN transcript_release_tag_relationship ON \
                        trt1.transcript_release_id=transcript_release_tag_relationship.transcript_release_object_id \
                        JOIN transcript_release_tag trt2 ON \
                        transcript_release_tag_relationship.transcript_release_subject_id=trt2.transcript_release_id \
                        JOIN transcript t2 ON trt2.feature_id=t2.transcript_id \
                        JOIN relationship_type ON \
                        transcript_release_tag_relationship.relationship_type_id=relationship_type.relationship_type_id"
        else:
            raw_sql = "SELECT DISTINCT\
                        t1.transcript_id, t1.stable_id as ens_stable_id, t1.stable_id_version as ens_stable_id_version,\
                        relationship_type.shortname as mane_type,\
                        t2.stable_id as refseq_stable_id, t2.stable_id_version as refseq_stable_id_version \
                        FROM \
                        transcript t1 \
                        JOIN transcript_release_tag trt1 ON t1.transcript_id=trt1.feature_id \
                        JOIN transcript_release_tag_relationship ON \
                        trt1.transcript_release_id=transcript_release_tag_relationship.transcript_release_subject_id \
                        JOIN transcript_release_tag trt2 ON \
                        transcript_release_tag_relationship.transcript_release_object_id=trt2.transcript_release_id \
                        JOIN transcript t2 ON trt2.feature_id=t2.transcript_id \
                        JOIN relationship_type ON \
                        transcript_release_tag_relationship.relationship_type_id=relationship_type.relationship_type_id"

        if transcript_id is not None:
            raw_sql = raw_sql + " WHERE t1.transcript_id=%s limit 1"
            mane_transcripts = Transcript.objects.raw(raw_sql, [transcript_id])
            mane_transcript_dict = {}
            if mane_transcripts is not None and len(list(mane_transcripts)) > 0:
                mane_transcript = mane_transcripts[0]
                mane_transcript_dict = {"mane_transcript_stableid":
                                            "{}.{}".format(mane_transcript.refseq_stable_id,
                                                           mane_transcript.refseq_stable_id_version),
                                        "mane_transcript_type": mane_transcript.mane_type}

                return mane_transcript_dict
        else:
            raw_sql = "SELECT DISTINCT\
                        t1.transcript_id, t1.stable_id as ens_stable_id, t1.stable_id_version as ens_stable_id_version,\
                        relationship_type.shortname as mane_type,\
                        t2.stable_id as refseq_stable_id, t2.stable_id_version as refseq_stable_id_version,\
                        gn1.name as ens_gene_name \
                        FROM \
                        transcript t1 \
                        JOIN transcript_release_tag trt1 ON t1.transcript_id=trt1.feature_id \
                        JOIN transcript_release_tag_relationship ON \
                        trt1.transcript_release_id=transcript_release_tag_relationship.transcript_release_object_id \
                        JOIN transcript_release_tag trt2 ON \
                        transcript_release_tag_relationship.transcript_release_subject_id=trt2.transcript_release_id \
                        JOIN transcript t2 ON trt2.feature_id=t2.transcript_id \
                        JOIN relationship_type ON \
                        transcript_release_tag_relationship.relationship_type_id=relationship_type.relationship_type_id\
                         JOIN transcript_gene tg1 ON \
                        t1.transcript_id=tg1.transcript_id \
                        JOIN gene gene1 ON \
                        tg1.gene_id=gene1.gene_id \
                        JOIN gene_names gn1 ON \
                        gene1.name_id=gn1.external_id \
                        where gn1.primary_id=1"
            mane_transcripts = Transcript.objects.raw(raw_sql)
            return mane_transcripts


class TranscriptGene(auto_prefetch.Model):
    gene_transcript_id = models.AutoField(primary_key=True)
    gene = auto_prefetch.ForeignKey(Gene, models.DO_NOTHING, blank=True, null=True)
    transcript = auto_prefetch.ForeignKey(Transcript, models.DO_NOTHING, blank=True, null=True)
    session = auto_prefetch.ForeignKey(Session, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transcript_gene'
        unique_together = (('gene', 'transcript'),)
