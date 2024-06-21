'''
Copyright [1999-2015] Wellcome Trust Sanger Institute and the EMBL-European Bioinformatics Institute
Copyright [2016-2024] EMBL-European Bioinformatics Institute

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

from __future__ import unicode_literals
from rest_framework import generics
from rest_framework.exceptions import NotFound
from tark_drf.utils.decorators import setup_eager_loading
from translation.models import Translation
from translation.drf.serializers import TranslationSerializer, TranslationDetailSerializer
from translation.drf.filters import TranslationFilterBackend


class TranslationList(generics.ListAPIView):
    queryset = Translation.objects.all()
    serializer_class = TranslationSerializer
    filter_backends = (TranslationFilterBackend,)

    @setup_eager_loading(TranslationSerializer)
    def get_queryset(self):
        queryset = Translation.objects.order_by('pk')
        return queryset


class TranslationDetail(generics.RetrieveAPIView):
    queryset = Translation.objects.all()
    serializer_class = TranslationSerializer


class TranslationListByStableID(generics.ListAPIView):
    serializer_class = TranslationDetailSerializer

    def get_queryset(self):
        stable_id = self.kwargs.get('stable_id')
        if not stable_id:
            raise NotFound('No stable ID provided.')
        
        queryset = Translation.objects.filter(stable_id=stable_id).prefetch_related('translation_release_set').order_by('pk')
        if queryset.exists():
            return queryset
        else:
            raise NotFound('No translations found for the given stable ID.')