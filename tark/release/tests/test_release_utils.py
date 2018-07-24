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


from django.test.testcases import TestCase
from release.utils.release_utils import ReleaseUtils
from django.conf import settings


class ReleaseUtilsTest(TestCase):
    fixtures = ['assembly', 'release_set']
    #multi_db = True

    def test_get_latest_release(self):
        latest_release = ReleaseUtils.get_latest_release()
        current_release = getattr(settings, "CURRENT_RELEASE", "92")
        self.assertEquals(latest_release, current_release, "Got the correct latest release " + latest_release)

    def test_get_latest_assembly(self):
        latest_assembly = ReleaseUtils.get_latest_assembly()
        current_assembly = getattr(settings, "CURRENT_ASSEMBLY", "GRCh38")
        self.assertEquals(latest_assembly, current_assembly, "Got the correct latest assembly " + latest_assembly)

    def test_get_all_releases(self):
        all_releases = ReleaseUtils.get_all_releases()
        self.assertEqual(len(all_releases), 3, "Release list match for current release")

        all_releases = ReleaseUtils.get_all_releases(assembly_name="GRCh37")
        self.assertEqual(len(all_releases), 1, "Release list match for GRCh37")

    def test_get_all_release_short_names(self):
        all_release_short_names = ReleaseUtils.get_all_release_short_names()
        expected_releases = ['92', '91']
        self.assertListEqual(all_release_short_names, expected_releases, "Release list match for current release")

        all_release_short_names = ReleaseUtils.get_all_release_short_names(assembly_name="GRCh37")
        expected_releases = ['92']
        self.assertListEqual(all_release_short_names, expected_releases, "Release list match for GRCh37")

    def test_get_all_assemblies(self):
        all_assemblies = ReleaseUtils.get_all_assemblies()
        self.assertEqual(len(all_assemblies), 2, "Got right assemblies")

    def test_get_all_assembly_names(self):
        all_assemblies = ReleaseUtils.get_all_assembly_names()
        expected_list = ['GRCh37', 'GRCh38']
        self.assertListEqual(all_assemblies, expected_list, "Got the right assembly list")

    def test_get_all_assembly_releases(self):
        all_assembly_releases = ReleaseUtils.get_all_assembly_releases()
        expected_result = {'GRCh37': ['92'], 'GRCh38': ['92', '91']}
        self.assertDictEqual(all_assembly_releases, expected_result, "Got the right assembly_releases")

        all_assembly_releases_refseq = ReleaseUtils.get_all_assembly_releases(source_name="RefSeq")
        expected_result_refseq = {'GRCh37': [], 'GRCh38': ['92']}
        self.assertDictEqual(all_assembly_releases_refseq, expected_result_refseq, "Got the expected result for RefSeq")

    def test_get_all_release_sources(self):
        all_release_sources = ReleaseUtils.get_all_release_sources()
        expected_result = ['Ensembl', 'RefSeq']
        self.assertListEqual(expected_result, all_release_sources, "Got the right sources")
