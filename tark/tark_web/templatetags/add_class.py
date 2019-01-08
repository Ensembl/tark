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

from django import template
register = template.Library()


@register.filter
def add_class(field, css_class):
    class_old = field.field.widget.attrs.get('class', None)
    class_new = class_old + ' ' + css_class if class_old else css_class
    return field.as_widget(attrs={"class": class_new})


@register.filter
def add_location(transcript):
    location = None
    if len(transcript) > 0:
        location = str(transcript['loc_region']) + " : " + str(transcript['loc_start']) + " - " + \
            str(transcript['loc_end']) + \
            " : " + str(transcript['loc_strand'])
    return location
