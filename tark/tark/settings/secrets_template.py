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

import tark.settings.env

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'bydgsk0!l&7!c5@s5tz9^*)*+@2%hhw6eugyak=31t$fhm0vw7'

if tark.settings.env.TEST_ENV:
    DATABASE_NAME = 'xxx'
    DATABASE_USER = 'xxx'
    DATABASE_PASSWORD = 'xxx'
    DATABASE_HOST = 'localhost'
    DATABASE_PORT = '3306'
else:
    DATABASE_NAME = 'xxx'
    DATABASE_USER = 'xxx'
    DATABASE_PASSWORD = 'xxx'
    DATABASE_HOST = 'localhost'
    DATABASE_PORT = '3306'
