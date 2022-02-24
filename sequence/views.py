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

from __future__ import unicode_literals
from sequence.models import Sequence
from sequence.drf.serializers import SequenceSerializer
from rest_framework import generics
from sequence.drf.filters import SequenceFilterBackend
from django.shortcuts import render  # @UnusedImport
from tark_web.utils.sequtils import TarkSeqUtils
import urllib
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from setuptools.dist import sequence
import io


# Create your views here.
def align_sequence(request, feature_type, stable_id_a, stable_id_version_a, stable_id_b, stable_id_version_b,
                   input_type, outut_format='pair'):

    sequence_a = TarkSeqUtils.fetch_fasta_sequence(request, feature_type, stable_id_a, stable_id_version_a)
    sequence_b = TarkSeqUtils.fetch_fasta_sequence(request, feature_type, stable_id_b, stable_id_version_b)

    pay_load = {'asequence': sequence_a, 'bsequence': sequence_b,
                'format': outut_format, 'stype': input_type, 'email': 'prem@ebi.ac.uk'}

    encoded_pay_load = urllib.parse.urlencode(pay_load).encode("utf-8")
#     print(encoded_pay_load)
#
    jobId = TarkSeqUtils.serviceRun(encoded_pay_load)
    # jobId = "emboss_needle-I20190401-145945-0054-27249118-p2m"

    if jobId:
        status = TarkSeqUtils.serviceGetStatus(jobId)

    return render(request, 'alignment_viewer.html', context={'status': status,
                                                             'jobId': jobId,
                                                             })


# Create your views here.
@csrf_exempt
def call_align_sequence_clustal(request):

    if request.method == "POST":
        data = request.body
        body_unicode = data.decode('utf-8')

        body = json.loads(body_unicode)
        transcript_list = body['payload_data_list']
        first_transcript = transcript_list.pop(0)
        (first_tr_stable_id, first_tr_stable_id_version) = first_transcript['transcript1_stable_id'].split('.')

        sequence_tr1 = TarkSeqUtils.fetch_fasta_sequence(request, "transcript", first_tr_stable_id,
                                                         first_tr_stable_id_version,
                                                         release_short_name=first_transcript['transcript1_release'],
                                                         assembly_name=first_transcript['transcript1_assembly'],
                                                         source_name=first_transcript['transcript1_source'])

        output = io.StringIO()
        output.write(sequence_tr1)
        for transcript in transcript_list:
            (tr_stable_id, tr_stable_id_version) = transcript['transcript2_stable_id'].split('.')
            sequence_tr = TarkSeqUtils.fetch_fasta_sequence(request, "transcript", tr_stable_id,
                                                            tr_stable_id_version,
                                                            release_short_name=transcript['transcript2_release'],
                                                            assembly_name=transcript['transcript2_assembly'],
                                                            source_name=transcript['transcript2_source'])
            print(sequence_tr, file=output, end="")

        seq_data = output.getvalue()

        pay_load = {'sequence': seq_data,
                    'outfmt': 'clustal', 'stype': 'dna', 'email': 'prem@ebi.ac.uk',
                    'title': "Results from Clustal Multiple Sequence alignment"}

        encoded_pay_load = urllib.parse.urlencode(pay_load).encode("utf-8")
        jobId = TarkSeqUtils.serviceRunClustal(encoded_pay_load)

        # jobId= "clustalo-R20191210-155816-0727-14316613-p1m"
        if jobId:
            status = TarkSeqUtils.serviceGetStatus(jobId)

        data = {'status': status, 'jobId': jobId}
        return JsonResponse(data)


def align_cds_sequence(request, feature_type,
                       stable_id_a, stable_id_version_a, release_short_name_a, assembly_name_a, source_name_a,
                       stable_id_b, stable_id_version_b, release_short_name_b, assembly_name_b, source_name_b,
                       cds_type="cds", output_format="raw"):

    sequence_a = TarkSeqUtils.fetch_cds_sequence(request, feature_type, stable_id_a, stable_id_version_a,
                                                 release_short_name_a, assembly_name_a, source_name_a,
                                                 cds_type, output_format)

    sequence_b = TarkSeqUtils.fetch_cds_sequence(request, feature_type, stable_id_b, stable_id_version_b,
                                                 release_short_name_b, assembly_name_b, source_name_b,
                                                 cds_type, output_format)

    if len(sequence_a) == 0 or len(sequence_b) == 0:
        return render(request, 'alignment_viewer.html', context={'error_msg': "Alignment Error...One of the sequence is not available, please check!",
                                                                 })
    pay_load = {'asequence': sequence_a, 'bsequence': sequence_b,
                'format': "pair", 'stype': "dna", 'email': 'prem@ebi.ac.uk'}

    encoded_pay_load = urllib.parse.urlencode(pay_load).encode("utf-8")
#     print(encoded_pay_load)
# # #
    jobId = TarkSeqUtils.serviceRun(encoded_pay_load)
    # jobId = "emboss_needle-R20190607-121522-0390-94599336-p2m"

    if jobId:
        status = TarkSeqUtils.serviceGetStatus(jobId)

    return render(request, 'alignment_viewer.html', context={'status': status,
                                                             'jobId': jobId,
                                                             })


def check_service_status(request, job_id):

    if job_id:
        status = TarkSeqUtils.serviceGetStatus(job_id)
    return JsonResponse({"status": status})

class SequenceList(generics.ListAPIView):
    queryset = Sequence.objects.all()
    serializer_class = SequenceSerializer
    filter_backends = (SequenceFilterBackend,)
