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


from Bio.Alphabet import generic_dna
from Bio.SeqRecord import SeqRecord
from io import StringIO
from Bio.Seq import Seq
from Bio import SeqIO
import subprocess
import os
import re
import platform
import time
from tark_web.utils.apiutils import ApiUtils
import requests
from translation.models import Translation
from tark.utils.exon_utils import ExonUtils
from exon.models import Exon
try:
    from urllib.parse import urlparse, urlencode
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError
    from urllib.request import __version__ as urllib_version
except ImportError:
    from urlparse import urlparse
    from urllib import urlencode
    from urllib2 import urlopen, Request, HTTPError
    from urllib2 import __version__ as urllib_version

# allow unicode(str) to be used in python 3
try:
    unicode('')
except NameError:
    unicode = str

# Base URL for service
baseUrl = u'https://www.ebi.ac.uk/Tools/services/rest/emboss_needle'
version = u'2019-01-29 14:22'
# Set interval for checking status
pollFreq = 3


class TarkSeqUtils(object):

    @classmethod
    def fetch_fasta_sequence(cls, request, feature_type, stable_id, stable_id_version,
                             release_short_name=None, assembly_name=None, source_name=None, output_format="fasta"):

        if source_name is not None:
            source_name = source_name.lower()

        host_url = ApiUtils.get_host_url(request)
        query_url = ""
        if release_short_name is not None and assembly_name is not None and source_name is not None:
            query_url = "/api/" + feature_type.lower() + "/?stable_id=" + stable_id + \
                        "&stable_id_version=" + stable_id_version + \
                        "&release_short_name=" + release_short_name + \
                        "&assembly_name=" + assembly_name + \
                        "&source_name=" + source_name + \
                        "&expand=sequence"
        else:
            query_url = "/api/" + feature_type.lower() + "/?stable_id=" + stable_id + \
                        "&stable_id_version=" + stable_id_version + \
                        "&expand=sequence"

        sequence = None
        response = requests.get(host_url + query_url)
        if response.status_code == 200:
            response_result = response.json()
            if "results" in response_result and len(response_result["results"]) > 0:
                sequence_result = response_result["results"][0]
                sequence = sequence_result["sequence"]["sequence"]

            if sequence and "fasta" in output_format:
                id_a = stable_id + '.' + stable_id_version
                formatted_seq = cls.format_fasta(sequence, id_=id_a)
                return formatted_seq
            elif sequence and "raw" in output_format:
                return sequence

        return sequence

    @classmethod
    def fetch_cds_sequence(cls, request, feature_type, stable_id, stable_id_version,
                           release_short_name=None, assembly_name=None, source_name=None,
                           seq_type="cds", output_format="raw"):

        if source_name is not None:
            source_name = source_name.lower()

        host_url = ApiUtils.get_host_url(request)
        query_url = ""
        if release_short_name is not None and assembly_name is not None and source_name is not None:
            query_url = "/api/" + feature_type.lower() + "/?stable_id=" + stable_id + \
                        "&stable_id_version=" + stable_id_version + \
                        "&release_short_name=" + release_short_name + \
                        "&assembly_name=" + assembly_name + \
                        "&source_name=" + source_name + "&expand_all=true"
        else:
            query_url = "/api/" + feature_type.lower() + "/?stable_id=" + stable_id + \
            "&stable_id_version=" + stable_id_version + \
            "&expand_all=true"

        sequence = None
        response = requests.get(host_url + query_url)
        if response.status_code == 200:
            response_result = response.json()
            if "results" in response_result and len(response_result["results"]) > 0:
                transcript_result = response_result["results"][0]
                if "translations" in transcript_result and len(transcript_result["translations"]) > 0:
                    translation = transcript_result["translations"][0]

                    if "translation_id" in translation:
                        tl_translation_id = translation["translation_id"]
                        tl_query_set = Translation.objects.filter(translation_id=tl_translation_id).select_related('sequence')
                        if tl_query_set is not None and len(tl_query_set) == 1:
                            tl_obj = tl_query_set[0]
                            translation["sequence"] = tl_obj.sequence.sequence
                            translation["seq_checksum"] = tl_obj.sequence.seq_checksum
                            transcript_result["translations"] = translation

                            if "exons" in transcript_result:
                                all_exons = transcript_result["exons"]
                                new_exons = []
                                for exon in all_exons:
                                    if "exon_id" in exon:
                                        current_exon_query_set = Exon.objects.filter(exon_id=exon["exon_id"]).select_related('sequence')  # @IgnorePep8

                                        if current_exon_query_set is not None and len(current_exon_query_set) == 1:
                                            current_exon_with_sequence = current_exon_query_set[0]
                                            exon["sequence"] = current_exon_with_sequence.sequence.sequence
                                            exon["seq_checksum"] = current_exon_with_sequence.sequence.seq_checksum
                                            new_exons.append(exon)

                                if len(new_exons) > 0:
                                    transcript_result["exons"] = new_exons

                            cds_info = ExonUtils.fetch_cds_info(transcript_result)

                            if cds_info:
                                if seq_type == "cds":
                                    if "cds_seq" in cds_info:
                                        sequence = cds_info['cds_seq']
                                elif seq_type == "five_prime":
                                    if "five_prime_utr_seq" in cds_info:
                                        sequence = cds_info['five_prime_utr_seq']
                                elif seq_type == "three_prime":
                                    if "three_prime_utr_seq" in cds_info:
                                        sequence = cds_info['three_prime_utr_seq']

        if output_format == "raw":
            return sequence
        elif output_format == "fasta":
            id_version = stable_id + '.' + stable_id_version
            formatted_seq = cls.format_fasta(sequence, id_=id_version)
            return formatted_seq

        return sequence

    # Submit job
    @classmethod
    def serviceRun(cls, requestData):
        # Errors are indicated by HTTP status codes.
        try:
            requestUrl = baseUrl + u'/run/'
            # Set the HTTP User-agent.
            user_agent = cls.getUserAgent()
            http_headers = {u'User-Agent': user_agent}
            req = Request(requestUrl, None, http_headers)
            # Make the submission (HTTP POST).
            reqH = urlopen(req, requestData)
            jobId = unicode(reqH.read(), u'utf-8')
            reqH.close()
        except HTTPError as ex:
            print(ex)

        return jobId

    # Get job status
    @classmethod
    def serviceGetStatus(cls, jobId):
        requestUrl = baseUrl + u'/status/' + jobId
        status = cls.restRequest(requestUrl)
        return status

# Client-side poll
    @classmethod
    def clientPoll(cls, jobId):
        result = u'PENDING'
        while result == u'RUNNING' or result == u'PENDING':
            result = cls.serviceGetStatus(jobId)
            if result == u'RUNNING' or result == u'PENDING':
                time.sleep(pollFreq)

        return result

    # Wrapper for a REST (HTTP GET) request
    @classmethod
    def restRequest(cls, url):
        try:
            # Set the User-agent.
            user_agent = cls.getUserAgent()
            http_headers = {u'User-Agent': user_agent}
            req = Request(url, None, http_headers)
            # Make the request (HTTP GET).
            reqH = urlopen(req)
            resp = reqH.read()
            contenttype = reqH.info()

            if (len(resp) > 0 and contenttype != u"image/png;charset=UTF-8"
                    and contenttype != u"image/jpeg;charset=UTF-8" and contenttype != u"application/gzip;charset=UTF-8"):
                try:
                    result = unicode(resp, u'utf-8')
                except UnicodeDecodeError:
                    result = resp
            else:
                result = resp
            reqH.close()
        # Errors are indicated by HTTP status codes.
        except HTTPError as ex:
            print(ex)
            quit()

        return result

    # User-agent for request (see RFC2616).
    @classmethod
    def getUserAgent(cls):
        # Agent string for urllib2 library.
        urllib_agent = u'Python-urllib/%s' % urllib_version
        clientRevision = version
        # Prepend client specific agent string.
        try:
            pythonversion = platform.python_version()
            pythonsys = platform.system()
        except ValueError:
            pythonversion, pythonsys = "Unknown", "Unknown"
        user_agent = u'EBI-Sample-Client/%s (%s; Python %s; %s) %s' % (
            clientRevision, os.path.basename(__file__),
            pythonversion, pythonsys, urllib_agent)

        return user_agent

    @classmethod
    def format_fasta(cls, sequence, id_="ID_", name_="", description_=""):
        record = SeqRecord(Seq(sequence, generic_dna),
                           id=id_, name=name_, description=description_)

        sequences = [record]
        fh = StringIO()
        SeqIO.write(sequences, fh, "fasta")
        return fh.getvalue()

    @classmethod
    def align_sequences(cls, query_fasta, target_fasta):
        if os.path.isfile(query_fasta) and os.path.isfile(target_fasta):
            p = subprocess.Popen(["exonerate", query_fasta, target_fasta], stdout=subprocess.PIPE)
            (output, err) = p.communicate()  # @UnusedVariable
            return output

    @classmethod
    def parse_location_string(cls, loc_string):
        loc_string = loc_string.replace(" ", "")
        matchloc = re.search(r'(\w+):(\d+)-(\d+)', loc_string)
        loc_region = matchloc.group(1)
        loc_start = matchloc.group(2)
        loc_end = matchloc.group(3)
        return (loc_region, loc_start, loc_end)

    @classmethod
    def difference_transcript_set(cls, release1, release2):
        pass
