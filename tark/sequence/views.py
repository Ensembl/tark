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


from django.shortcuts import render  # @UnusedImport
from tark_web.utils.sequtils import TarkSeqUtils
import urllib
from django.http.response import JsonResponse


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


def align_cds_sequence(request, sequence_a, sequence_b, stable_id_a,
                       stable_id_version_a, stable_id_b, stable_id_version_b,
                       input_type, outut_format='pair'):

    # sequence_a = TarkSeqUtils.fetch_fasta_sequence(request, feature_type, stable_id_a, stable_id_version_a)
    # sequence_b = TarkSeqUtils.fetch_fasta_sequence(request, feature_type, stable_id_b, stable_id_version_b)
    sequence_a = TarkSeqUtils.format_fasta(sequence_a, id_=stable_id_a + '.' + str(stable_id_version_a))
    sequence_b = TarkSeqUtils.format_fasta(sequence_b, id_=stable_id_b + '.' + str(stable_id_version_b))

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



def check_service_status(request, job_id):

    if job_id:
        status = TarkSeqUtils.serviceGetStatus(job_id)
    return JsonResponse({"status": status})
