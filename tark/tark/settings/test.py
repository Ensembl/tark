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


from tark.settings.base import *  # @UnusedWildImport
from django.test.runner import DiscoverRunner


class UnManagedModelTestRunner(DiscoverRunner):
    '''
    Test runner that automatically makes all unmanaged models in your Django
    project managed for the duration of the test run.
    Many thanks to the Caktus Group: http://bit.ly/1N8TcHW
    '''

    def setup_test_environment(self, *args, **kwargs):
        from django.apps import apps
        self.unmanaged_models = [m for m in apps.get_models() if not m._meta.managed]
        for m in self.unmanaged_models:
            m._meta.managed = True

        super(UnManagedModelTestRunner, self).setup_test_environment(*args, **kwargs)

    def teardown_test_environment(self, *args, **kwargs):
        super(UnManagedModelTestRunner, self).teardown_test_environment(*args, **kwargs)
        # reset unmanaged models
        for m in self.unmanaged_models:
            m._meta.managed = False


DATABASE_ROUTERS = []
#
# # Skip the migrations by setting "MIGRATION_MODULES"
# # to the DisableMigrations class defined above
# #
# MIGRATION_MODULES = DisableMigrations()


MIGRATION_MODULES = {
    'assembly': None,
    'exon': None,
    'genenames': None,
    'gene': None,
    'genome': None,
    'operon': None,
    'release': None,
    'sequence': None,
    'session': None,
    'tagset': None,
    'tark_drf': None,
    'transcript': None,
    'translation': None,
    'tark_web': None,
}


# Set Django's test runner to the custom class defined above
TEST_RUNNER = 'tark.settings.test.UnManagedModelTestRunner'
