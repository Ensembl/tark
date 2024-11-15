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

from rest_framework import generics
from gene.models import Gene
from release.models import ReleaseSet
from transcript.models import Transcript

from tark_drf.utils.decorators import setup_eager_loading

from gene.drf.serializers import GeneSerializer
from gene.drf.filters import GeneFilterBackend
from tark.views import DataTableListApi
from tark.utils.schema_utils import SchemaUtils
from django.db.models import Prefetch


class GeneDatatableView(DataTableListApi):
    serializer_class = GeneSerializer
    search_parameters = SchemaUtils.get_field_names(app_name='gene', model_name='gene', exclude_pk=True)
    default_order_by = 1
    queryset = Gene.objects.all()


class GeneList(generics.ListAPIView):
    queryset = Gene.objects.all()
    serializer_class = GeneSerializer
    filter_backends = (GeneFilterBackend,)

    @setup_eager_loading(GeneSerializer)
    def get_queryset(self):
        # Access and print the "HTTP_X_FORWARDED_PROTO" header from the request
        x_forwarded_proto = self.request.META.get("HTTP_X_FORWARDED_PROTO")
        print("HTTP_X_FORWARDED_PROTO:", x_forwarded_proto)

        headers = {key: value for key, value in self.request.META.items() if key.startswith("HTTP_")}
        print("Request Headers:", headers)

        # To reduce the number of queries sent to the database, several prefetch relationship objects are created below.

        # Create a prefetch object for gene_release_sets with nested prefetches
        gene_release_set_prefetch = Prefetch(
            'gene_release_set',
            queryset=ReleaseSet.objects.select_related('assembly', 'source').all()
        )

        # Prefetch for nested relationships within Transcript
        transcript_prefetch = Prefetch(
            'transcripts',
            queryset=Transcript.objects.select_related(
                'assembly', 'sequence', 'session'
            ).prefetch_related(
                'transcript_release_set',
                'exons',
                'translations'
            )
        )

        queryset = Gene.objects.prefetch_related(
            transcript_prefetch,
            gene_release_set_prefetch
        ).order_by('pk')

        return queryset


class GeneDetail(generics.RetrieveAPIView):
    queryset = Gene.objects.all()
    serializer_class = GeneSerializer
