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

from rest_framework import serializers
from tark_drf.utils.drf_mixin import SerializerMixin
from assembly.drf.serializers import AssemblySerializer
from release.drf.serializers import ReleaseSetSerializer

from tark_drf.utils.drf_fields import AssemblyField, CommonFields,\
    TranscriptFieldEns, TranscriptFieldRefSeq, TranscriptFieldRelationshipType
from release.models import TranscriptReleaseTag,\
    TranscriptReleaseTagRelationship
from transcript.models import Transcript
from sequence.drf.serializers import SequenceSerializer
from gene.drf.serializers import GeneSerializer
from exon.drf.serializers import ExonTranscriptSerializer
from translation.drf.serializers import TranslationSerializer


class HgncNameField(serializers.RelatedField):
    def to_representation(self, value):
        if value is not None:
            return value.name
        return None


class TranscriptReleaseTagRelationshipSerializer(SerializerMixin, serializers.ModelSerializer):

    transcript_release_object = TranscriptFieldEns(read_only=True)
    transcript_release_subject = TranscriptFieldRefSeq(read_only=True)
    relationship_type = TranscriptFieldRelationshipType(read_only=True)

    class Meta:
        model = TranscriptReleaseTagRelationship
        fields = '__all__'


class TranscriptReleaseTagSerializer(serializers.ModelSerializer):

    ONE2MANY_SERIALIZER = {TranscriptReleaseTag.ONE2MANY_RELATED['TRANSCRIPTRELEASETAGRELATIONSHIP']:
                           TranscriptReleaseTagRelationshipSerializer}

    class Meta:
        model = TranscriptReleaseTag
        fields = '__all__'


class TranscriptSerializer(SerializerMixin, serializers.ModelSerializer):

    MANY2ONE_SERIALIZER = {Transcript.MANY2ONE_RELATED['SEQUENCE']: SequenceSerializer,
                           Transcript.MANY2ONE_RELATED['ASSEMBLY']: AssemblySerializer}
    ONE2MANY_SERIALIZER = {Transcript.ONE2MANY_RELATED['RELEASE_SET']: ReleaseSetSerializer,
                           Transcript.ONE2MANY_RELATED['GENE']: GeneSerializer,
                           Transcript.ONE2MANY_RELATED['TRANSLATION']: TranslationSerializer,
                           Transcript.ONE2MANY_RELATED['EXONTRANSCRIPT']: ExonTranscriptSerializer,
                           }

    assembly = AssemblyField(read_only=True)
    mane_transcript = serializers.SerializerMethodField()
    mane_transcript_type = serializers.SerializerMethodField()

    def get_mane_transcript_type(self, obj):

        transcript = Transcript.objects.get(pk=obj.pk)
        source = "Ensembl"
        if transcript is not None:
            try:
                source = transcript.transcript_release_set.all()[:1].get().source.shortname
            except Exception as e:
                print("Exception from  get_mane_transcript " + e)

        if "Ensembl" in source:
            raw_sql = "SELECT \
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
                        transcript_release_tag_relationship.relationship_type_id=relationship_type.relationship_type_id\
                        WHERE \
                        t1.transcript_id=%s limit 1"
        else:
            raw_sql = "SELECT \
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
                        transcript_release_tag_relationship.relationship_type_id=relationship_type.relationship_type_id\
                        WHERE \
                        t1.transcript_id=%s limit 1"

        mane_transcripts = Transcript.objects.raw(raw_sql, [obj.pk])
        if mane_transcripts is not None:
            manes = []
            for mane in mane_transcripts:
                mane_string = mane.mane_type
                manes.append(mane_string)

            return ','.join(manes)
        else:
            return "-"

    def get_mane_transcript(self, obj):

        transcript = Transcript.objects.get(pk=obj.pk)
        source = "Ensembl"
        if transcript is not None:
            try:
                source = transcript.transcript_release_set.all()[:1].get().source.shortname
            except Exception as e:
                print("Exception from  get_mane_transcript " + e)

        if "Ensembl" in source:
            raw_sql = "SELECT \
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
                        transcript_release_tag_relationship.relationship_type_id=relationship_type.relationship_type_id\
                        WHERE \
                        t1.transcript_id=%s limit 1"
        else:
            raw_sql = "SELECT \
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
                        transcript_release_tag_relationship.relationship_type_id=relationship_type.relationship_type_id\
                        WHERE \
                        t1.transcript_id=%s limit 1"
        mane_transcripts = Transcript.objects.raw(raw_sql, [obj.pk])
        if mane_transcripts is not None:
            manes = []
            for mane in mane_transcripts:
                mane_string = mane.refseq_stable_id + '.' + str(mane.refseq_stable_id_version)
                manes.append(mane_string)

            return ','.join(manes)
        else:
            return "-"

    class Meta:
        model = Transcript
        fields = CommonFields.COMMON_FIELD_SET + ('exon_set_checksum', 'transcript_checksum',
                                                  'sequence', 'mane_transcript', 'mane_transcript_type')

    def __init__(self, *args, **kwargs):
        super(TranscriptSerializer, self).__init__(*args, **kwargs)
        self.set_related_fields(TranscriptSerializer, **kwargs)


class TranscriptDataTableSerializer(TranscriptSerializer):

    genes = serializers.SerializerMethodField(read_only=True)

    def get_genes(self, obj):
        gene_names = ""
        for gene in obj.genes.all():
            if gene.hgnc:
                return gene.hgnc.name

        return gene_names

    class Meta:
        model = Transcript
        fields = CommonFields.COMMON_FIELD_SET + ('genes', )


class TranscriptDiffSerializer(TranscriptSerializer):

    def __init__(self, *args, **kwargs):
        super(TranscriptDiffSerializer, self).__init__(*args, **kwargs)
        self.set_related_fields(TranscriptDiffSerializer, **kwargs)


class TranscriptSearchSerializer(TranscriptSerializer):

    def __init__(self, *args, **kwargs):
        super(TranscriptSearchSerializer, self).__init__(*args, **kwargs)
        self.set_related_fields(TranscriptSearchSerializer, **kwargs)
