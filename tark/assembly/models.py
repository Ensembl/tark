"""
   See the NOTICE file distributed with this work for additional information
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
from genome.models import Genome
from session.models import Session


class Assembly(auto_prefetch.Model):
    """Model class for assembly table"""
    assembly_id = models.AutoField(primary_key=True)
    genome = auto_prefetch.ForeignKey(Genome, models.DO_NOTHING, blank=True, null=True)
    assembly_name = models.CharField(unique=True, max_length=128, blank=True, null=True)
    session = auto_prefetch.ForeignKey(Session, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'assembly'


class AssemblyAlias(auto_prefetch.Model):
    """Model class for assembly_alias table"""
    assembly_alias_id = models.AutoField(primary_key=True)
    alias = models.CharField(unique=True, max_length=64, blank=True, null=True)
    genome = auto_prefetch.ForeignKey(Genome, models.DO_NOTHING, blank=True, null=True)
    assembly = auto_prefetch.ForeignKey(Assembly, models.DO_NOTHING, blank=True, null=True)
    session = auto_prefetch.ForeignKey(Session, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'assembly_alias'
