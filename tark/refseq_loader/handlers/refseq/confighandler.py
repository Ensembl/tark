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

import configparser
from django.conf import settings


class ConfigHandler(object):

    def __init__(self, ini_file=None):
        if ini_file is None:
            # get the default ini file from settings
            self.ini_file = settings.INI_FILE
        else:
            self.ini_file = ini_file

        print("Loading ini_file...please wait..." + self.ini_file)
        config = configparser.ConfigParser()
        config.read(self.ini_file)
        self.config = config

    def get_section_config(self, section_name=None):
        if section_name is None:
            config = self.config['DEFAULT']
        else:
            config = self.config[section_name]
        return config
