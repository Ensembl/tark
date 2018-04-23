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

from django import forms
from release.utils.release_utils import ReleaseUtils


class DiffForm(forms.Form):

    SPECIES = (
        ('homo_sapiens', 'Homo sapiens'),
    )

    ASSEMBLY = (
        ('GRCh38', 'GRCh38'),
        ('GRCh37', 'GRCh37'),
    )

#     RELEASE = (
#         ('84', '84'),
#         ('85', '85'),
#         ('87', '87'),
#     )

    RELEASE = (
        ('88', '88'),
        ('89', '89'),
        ('90', '90'),
        ('91', '91'),
        ('92', '92'),
    )
    current_release = ReleaseUtils.get_latest_release()

    species = forms.CharField(widget=forms.Select(choices=SPECIES))
    stable_id = forms.CharField(max_length=30, help_text='Please enter Transcript Stable ID')
    diff_me_assembly = forms.CharField(widget=forms.Select(choices=ASSEMBLY))
    diff_me_release = forms.CharField(widget=forms.Select(choices=RELEASE))
    diff_with_assembly = forms.CharField(widget=forms.Select(choices=ASSEMBLY))
    diff_with_release = forms.CharField(initial=current_release, widget=forms.Select(choices=RELEASE))


class SearchForm(forms.Form):

    SPECIES = (
        ('homo_sapiens', 'Homo sapiens'),
    )

    ASSEMBLY = (
        (' ', ' '),
        ('GRCh38', 'GRCh38'),
        ('GRCh37', 'GRCh37'),
    )

#     RELEASE = (
#         (' ', ' '),
#         ('84', '84'),
#         ('85', '85'),
#         ('87', '87'),
#     )

    RELEASE = (
        (' ', ' '),
        ('88', '88'),
        ('89', '89'),
        ('90', '90'),
        ('91', '91'),
        ('92', '92'),
    )

    current_release = ReleaseUtils.get_latest_release()

    species = forms.CharField(widget=forms.Select(choices=SPECIES))
    search_identifier = forms.CharField(max_length=30, help_text='Please enter valid identifiers')
    search_assembly = forms.CharField(widget=forms.Select(choices=ASSEMBLY), required=False)
    search_release = forms.CharField(widget=forms.Select(choices=RELEASE), required=False)
