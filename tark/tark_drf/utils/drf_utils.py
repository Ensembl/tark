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


class DrfUtils(object):

    @classmethod
    def get_related_entities(cls, model, cardinality=None):
        entities = []
        many2one = getattr(model, 'MANY2ONE_RELATED', None)
        one2many = getattr(model, 'ONE2MANY_RELATED', None)

        if(cardinality is None):
            if many2one is not None:
                entities.extend(list(many2one.values()))
            if one2many is not None:
                entities.extend(list(one2many.values()))
        elif (cardinality == 'many2one' or cardinality == 'many2many'):
            if many2one is not None:
                entities.extend(list(many2one.values()))
        elif (cardinality == 'one2many'):
            if one2many is not None:
                entities.extend(list(one2many.values()))
        print("======RELATED entities from get_related_entities")
        print(entities)
        return entities
