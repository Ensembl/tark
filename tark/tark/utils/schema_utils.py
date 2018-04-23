'''
Copyright [1999-2015] Wellcome Trust Sanger Institute and the EMBL-European Bioinformatics Institute
Copyright [2016-2018] EMBL-European Bioinformatics Institute

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

from django.apps import apps


class SchemaUtils(object):

    @classmethod
    def get_field_names(cls, app_name=None, model_name=None, exclude_pk=False):

        model = apps.get_model(app_name, model_name)
        field_names = []

        if exclude_pk is True:
            field_names = [field.name for field in model._meta.get_fields(include_parents=False, include_hidden=False)
                           if (field.related_model is None and field.primary_key is False)]
        else:
            field_names = [field.name for field in model._meta.get_fields(include_parents=False, include_hidden=False)
                           if (field.related_model is None)]

        return field_names

    @classmethod
    def get_app_model_mappings(cls):
        mappings = {}
        for app in apps.get_app_configs():
            for model in app.get_models():
                mappings[model.__name__.lower()] = app.verbose_name.lower()

        return mappings
