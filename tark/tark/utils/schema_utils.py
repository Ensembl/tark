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

from django.apps import apps
from django.urls.conf import include


class SchemaUtils(object):

    @classmethod
    def get_field_names(cls, app_name=None, model_name=None, exclude_pk=False, include_parents_=False,
                        exclude_fields=None, include_fields=None):

        model = apps.get_model(app_name, model_name)
        field_names = []

        if exclude_pk is True:
            field_names = [field.name for field in model._meta.get_fields(include_parents=include_parents_,
                                                                          include_hidden=False)
                           if (field.related_model is None and field.primary_key is False)]
        else:
            field_names = [field.name for field in model._meta.get_fields(include_parents=include_parents_,
                                                                          include_hidden=False)
                           if (field.related_model is None)]

        if exclude_fields is not None:
            field_names = [field for field in field_names if field not in exclude_fields]

        if include_fields is not None:
            field_names = field_names + include_fields

        return field_names

    @classmethod
    def get_app_model_mappings(cls):
        mappings = {}
        for app in apps.get_app_configs():
            for model in app.get_models():
                mappings[model.__name__.lower()] = app.verbose_name.lower()

        return mappings
