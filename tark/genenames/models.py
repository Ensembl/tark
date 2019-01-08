'''
Copyright [1999-2015] Wellcome Trust Sanger Institute and the EMBL-European Bioinformatics Institute
Copyright [2016-2019] EMBL-European Bioinformatics Institute

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
from session.models import Session


class GeneNames(models.Model):
    gene_names_id = models.AutoField(primary_key=True)
    external_id = models.PositiveIntegerField(blank=True, null=True, db_index=True)
    name = models.CharField(max_length=32, blank=True, null=True)
    source = models.CharField(max_length=32, blank=True, null=True)
    primary_id = models.IntegerField(blank=True, null=True)
    session = models.ForeignKey(Session, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gene_names'
