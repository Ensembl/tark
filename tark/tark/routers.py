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


class TarkRouter(object):
    """
    A router to control all database operations on models in the tark
    """
    TARK_APPS = ('assembly', 'exon', 'genenames', 'gene', 'genome', 'operon', 'release', 'sequence', 'session',
                 'tagset', 'tark', 'tark_drf', 'tark_web', 'transcript', 'translation')

    def db_for_read(self, model, **hints):
        if model._meta.app_label in TarkRouter.TARK_APPS:
            # print(" Appl label " + str(model._meta.app_label))
            return 'tark'
        return 'default'

    def db_for_write(self, model, **hints):
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label in TarkRouter.TARK_APPS or \
           obj2._meta.app_label in TarkRouter.TARK_APPS:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True
