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
from session.models import Session


class GeneNames(auto_prefetch.Model):
    gene_names_id = models.AutoField(primary_key=True)
    external_id = models.CharField(max_length=32, blank=True, null=True, db_index=True)
    name = models.CharField(max_length=32, blank=True, null=True)
    source = models.CharField(max_length=32, blank=True, null=True)
    primary_id = models.IntegerField(blank=True, null=True)
    session = auto_prefetch.ForeignKey(Session, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gene_names'
