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

from tark_drf.utils.decorators import setup_eager_loading

from gene.drf.serializers import GeneSerializer
from gene.drf.filters import GeneFilterBackend


class GeneList(generics.ListAPIView):
    queryset = Gene.objects.all()
    serializer_class = GeneSerializer
    filter_backends = (GeneFilterBackend,)

    @setup_eager_loading(GeneSerializer)
    def get_queryset(self):
        queryset = Gene.objects.order_by('pk')
        return queryset


class GeneDetail(generics.RetrieveAPIView):
    queryset = Gene.objects.all()
    serializer_class = GeneSerializer
