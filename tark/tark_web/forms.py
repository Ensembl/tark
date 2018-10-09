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


class FormUtils(object):

    @classmethod
    def get_all_assembly_name_tuples(cls):
        assembly_list = []

        for assembly in ReleaseUtils.get_all_assembly_names():
            assembly_list.append((assembly, assembly))

        return assembly_list

    @classmethod
    def get_all_release_name_tuples(cls, assembly_name=None, source_name="Ensembl"):
        release_list = []

        for release in ReleaseUtils.get_all_release_short_names(assembly_name, source_name):
            release_list.append((release, release))

        return release_list

    @classmethod
    def get_all_species_name_tuples(cls):
        species_list = []
        species_list.append(('homo_sapiens', 'Homo sapiens'))

        return species_list

    @classmethod
    def get_all_sources_tuples(cls):
        source_list = []

        for source in ReleaseUtils.get_all_release_sources():
            source_list.append((source, source))

        return source_list


class CompareSetForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(CompareSetForm, self).__init__(*args, **kwargs)
        current_release = ReleaseUtils.get_latest_release()
        current_assembly = ReleaseUtils.get_latest_assembly()
        current_source = ReleaseUtils.get_default_source()

        self.fields['diff_current_assembly'] = forms.CharField(initial=current_assembly,
                                                            widget=forms.Select(choices=FormUtils.get_all_assembly_name_tuples()))  # @IgnorePep8
        self.fields['diff_current_release'] = forms.CharField(initial=int(current_release),
                                                           widget=forms.Select(choices=FormUtils.get_all_release_name_tuples()))  # @IgnorePep8
        self.fields['diff_current_source'] = forms.CharField(initial=current_source,
                                                           widget=forms.Select(choices=FormUtils.get_all_sources_tuples()))  # @IgnorePep8

        self.fields['diff_compare_assembly'] = forms.CharField(initial=current_assembly,
                                                            widget=forms.Select(choices=FormUtils.get_all_assembly_name_tuples()))  # @IgnorePep8
        self.fields['diff_compare_release'] = forms.CharField(initial=int(current_release)-1,
                                                           widget=forms.Select(choices=FormUtils.get_all_release_name_tuples()))  # @IgnorePep8
        self.fields['diff_compare_source'] = forms.CharField(initial=current_source,
                                                           widget=forms.Select(choices=FormUtils.get_all_sources_tuples()))  # @IgnorePep8


class DiffForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(DiffForm, self).__init__(*args, **kwargs)
        current_release = ReleaseUtils.get_latest_release()
        current_assembly = ReleaseUtils.get_latest_assembly()
        default_source = ReleaseUtils.get_default_source()

        self.fields['species'] = forms.CharField(widget=forms.Select(choices=FormUtils.get_all_species_name_tuples()), required=False)
        self.fields['diff_me_stable_id'] = forms.CharField(max_length=30, help_text='Please enter Transcript Stable ID')
        self.fields['diff_with_stable_id'] = forms.CharField(max_length=30, help_text='Please enter Transcript Stable ID')
        self.fields['diff_me_assembly'] = forms.CharField(initial=current_assembly,
                                                          widget=forms.Select(choices=FormUtils.get_all_assembly_name_tuples()))  # @IgnorePep8
        self.fields['diff_me_release'] = forms.CharField(initial=current_release,
                                                         widget=forms.Select(choices=FormUtils.get_all_release_name_tuples()))  # @IgnorePep8
        self.fields['diff_with_assembly'] = forms.CharField(initial=current_assembly,
                                                            widget=forms.Select(choices=FormUtils.get_all_assembly_name_tuples()))  # @IgnorePep8
        self.fields['diff_with_release'] = forms.CharField(initial=int(current_release)-1,
                                                           widget=forms.Select(choices=FormUtils.get_all_release_name_tuples()))  # @IgnorePep8

        self.fields['diff_with_source'] = forms.CharField(initial=default_source,
                                                           widget=forms.Select(choices=FormUtils.get_all_sources_tuples()))  # @IgnorePep8
        self.fields['diff_me_source'] = forms.CharField(initial=default_source,
                                                           widget=forms.Select(choices=FormUtils.get_all_sources_tuples()))  # @IgnorePep8

    def get_cleaned_data(self):
        diff_me_stable_id = self.cleaned_data['diff_me_stable_id']
        diff_me_stable_id_version = '0'
        diff_me_source = self.cleaned_data['diff_me_source']

        diff_with_stable_id = self.cleaned_data['diff_with_stable_id']
        diff_with_stable_id_version = '0'
        diff_with_source = self.cleaned_data['diff_with_source']

        diff_form_data_dict = {}
        diff_form_data_dict['diff_me_stable_id'] = diff_me_stable_id

        if diff_me_source.lower() == "ensembl" and '.' in diff_me_stable_id:
                (stable_id, version) = diff_me_stable_id.split('.')
                diff_me_stable_id = stable_id
                diff_me_stable_id_version = version
        diff_form_data_dict['diff_me_stable_id_version'] = diff_me_stable_id_version

        diff_form_data_dict['diff_me_assembly'] = self.cleaned_data['diff_me_assembly']
        diff_form_data_dict['diff_me_release'] = self.cleaned_data['diff_me_release']
        diff_form_data_dict['diff_me_source'] = diff_me_source

        diff_form_data_dict['diff_with_stable_id'] = diff_with_stable_id
        if diff_with_source.lower() == "ensembl" and '.' in diff_with_stable_id:
                (stable_id, version) = diff_with_stable_id.split('.')
                diff_with_stable_id = stable_id
                diff_with_stable_id_version = version
        diff_form_data_dict['diff_with_stable_id_version'] = diff_with_stable_id_version

        diff_form_data_dict['diff_with_assembly'] = self.cleaned_data['diff_with_assembly']
        diff_form_data_dict['diff_with_release'] = self.cleaned_data['diff_with_release']
        diff_form_data_dict['diff_with_source'] = diff_with_source

        return diff_form_data_dict


class SearchForm(forms.Form):

#     current_release = ReleaseUtils.get_latest_release()
#     current_assembly = ReleaseUtils.get_latest_assembly()

#     species = forms.CharField(widget=forms.Select(choices=FormUtils.get_all_species_name_tuples()))
    search_identifier = forms.CharField(max_length=200, help_text='Please enter valid identifiers')
#     search_assembly = forms.CharField(widget=forms.Select(choices=FormUtils.get_all_assembly_name_tuples()), required=False)
#     search_release = forms.CharField(widget=forms.Select(choices=FormUtils.get_all_release_name_tuples()), required=False)
