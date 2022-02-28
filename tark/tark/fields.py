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

from django.db import models
from Bio.Seq import Seq
from Bio.Alphabet import IUPAC
from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor
import binascii

ALPHABETS = {
    'gene': IUPAC.ambiguous_dna,
    'transcript': IUPAC.ambiguous_dna,
    'exon': IUPAC.ambiguous_dna,
    'translation': IUPAC.extended_protein
}


class ChecksumField(models.CharField):
    '''
    https://docs.djangoproject.com/en/2.0/howto/custom-model-fields/
    '''
    description = "Allow retrieval of binary mysql fields"

    # called by Django when the framework constructs the CREATE TABLE statements
    def db_type(self, connection):
        return 'binary(20)'

    # will be called in all circumstances when the data is loaded from the database,
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return binascii.hexlify(value).decode('ascii').upper()


class GeneSetField(models.CharField):
    description = "Allows retrieval of abstract field type containing a grouping of genes"

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        decoded_genes = []
        genes = value.split('#!#!#')

        for gene in genes:
            pieces = gene.split(',', 3)
            if len(pieces) >= 3:
                pieces[3] = ''.join(["%02X" % ord(x) for x in pieces[3]]).strip()

                decoded_genes.append(pieces)

        return decoded_genes

    def to_python(self, value):
        return value


class SequenceField(models.TextField):
    @classmethod
    def alphabet_type(cls, feature_type):
        return ALPHABETS.get(feature_type, IUPAC.Alphabet)

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return Seq('')
        return Seq(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)

    def to_python(self, value):
        return str(value)

    def get_prep_value(self, value):
        if value is None:
            return None
        return str(value)

    def get_prep_lookup(self, lookup_type, value):
        if value is None:
            return None

        if lookup_type == 'isnull' and value in (True, False):
            return value

        if isinstance(value, (list, set)):
            return [self.item_field_type.to_python(x) for x in value]
        return self.item_field_type.to_python(value)


class HGNCForwardManyToOneDescription(ForwardManyToOneDescriptor):
    """
    We need to address what occurs when a lookup in the gene_name table
    fails because the HGNC column is NULL. There might be a more eligant
    way to handle this in django, I just haven't found it. So we're
    overloading the relationship manager such that when a __get__ is
    done, if the related column in gene_name fails we return none
    rather than letting the exception bubble up.
    """

    def __get__(self, instance, cls=None):
        try:
            rel_obj = super(HGNCForwardManyToOneDescription, self).__get__(instance, cls)
        except Exception:
            return None

        return rel_obj


class HGNCField(models.ForeignKey):
    """
    Derived class from ForeignKey, adding the restriction when following the
    froreign key to HGNC names, we only want the primary name from source type
    HGNC. Overloading get_extra_descriptor_filter just returns extra join
    conditions when looking up in the gene_names table.
    """
    requires_unique_target = False

    def get_extra_descriptor_filter(self, instance):
        return {'primary_id': 1, 'source': 'HGNC'}

    def contribute_to_class(self, cls, name, private_only=False, **kwargs):
        '''
        Override the relationship manager used for our HGNCField, see HGNCForwardManyToOneDescription
        above for more details.
        '''
        super(HGNCField, self).contribute_to_class(cls, name, private_only, **kwargs)

        setattr(cls, self.name, HGNCForwardManyToOneDescription(self))
