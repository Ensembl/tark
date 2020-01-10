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


from django.test.testcases import TestCase
from transcript.utils.search_utils import SearchUtils


# ./manage.py test transcript.tests.test_search_utils --settings=tark.settings.test
class SearchUtilsTest(TestCase):

    def test_get_seq_region_from_refseq_accession(self):
        (loc_region, loc_assembly) = SearchUtils.get_seq_region_from_refseq_accession("NC_000006.12")
        self.assertEqual(loc_region, '6', 'Got the right loc_region 6')
        self.assertEqual(loc_assembly, 'GRCh38', 'Got the right loc_assembly GRCh38')

        (loc_region, loc_assembly) = SearchUtils.get_seq_region_from_refseq_accession("NC_000006.11")
        self.assertEqual(loc_region, '6', 'Got the right loc_region 6')
        self.assertEqual(loc_assembly, 'GRCh37', 'Got the right loc_assembly GRCh37')

    def test_parse_location_string(self):
        loc_string = "5: 62797383 - 63627669 "
        (loc_region, loc_start, loc_end) = SearchUtils.parse_location_string(loc_string)
        self.assertEqual(loc_region, "5", "Loc region is ok")
        self.assertEqual(loc_start, "62797383", "Loc start is ok")
        self.assertEqual(loc_end, "63627669", "Loc end is ok")

    def test_parse_hgvs_genomic_location_string(self):
        loc_string = "NC_000023.11:g.32389644G>A"
        (loc_region, loc_start, loc_end, loc_assembly) = SearchUtils.parse_hgvs_genomic_location_string(loc_string)
        self.assertEqual(loc_region, "X", "Loc region is ok")
        self.assertEqual(loc_start, "32389644", "Loc start is ok")
        self.assertEqual(loc_end, "32389644", "Loc end is ok")
        self.assertEqual(loc_assembly, "GRCh38", "Loc assembly is ok")

    def test_get_identifier_type(self):
        self.assertEqual(SearchUtils.get_identifier_type("ENST00000252934.10"),
                         SearchUtils.ENSEMBL_TRANSCRIPT, "Got the right id_type for " +
                         SearchUtils.ENSEMBL_TRANSCRIPT)

        self.assertEqual(SearchUtils.get_identifier_type("ENSG00000130638.17"),
                         SearchUtils.ENSEMBL_GENE, "Got the right id_type for " + SearchUtils.ENSEMBL_GENE)

        self.assertEqual(SearchUtils.get_identifier_type("NC_000023.11:g.32389644G>A"),
                         SearchUtils.HGVS_GENOMIC_REF, "Got the right id_type for " + SearchUtils.HGVS_GENOMIC_REF)

        self.assertEqual(SearchUtils.get_identifier_type("NM_004006.2:c.4375C>T"),
                         SearchUtils.HGVS_REFSEQ_CDS, "Got the right id_type for " + SearchUtils.HGVS_REFSEQ_CDS)

        self.assertEqual(SearchUtils.get_identifier_type("BRCA2"),
                         SearchUtils.HGNC_SYMBOL, "Got the right id_type for " + SearchUtils.HGNC_SYMBOL)

        self.assertEqual(SearchUtils.get_identifier_type("LRG_1"),
                         SearchUtils.LRG_GENE, "Got the right id_type for " + SearchUtils.LRG_GENE)

        self.assertEqual(SearchUtils.get_identifier_type("LRG_59t1"),
                         SearchUtils.LRG_TRANSCRIPT, "Got the right id_type for " + SearchUtils.LRG_TRANSCRIPT)

        self.assertEqual(SearchUtils.get_identifier_type("NM_000109.4"),
                         SearchUtils.REFSEQ_TRANSCRIPT, "Got the right id_type for " + SearchUtils.REFSEQ_TRANSCRIPT)

        self.assertEqual(SearchUtils.get_identifier_type("XM_017029329"),
                         SearchUtils.REFSEQ_TRANSCRIPT, "Got the right id_type for " + SearchUtils.REFSEQ_TRANSCRIPT)

        self.assertEqual(SearchUtils.get_identifier_type("NR_000005"),
                         SearchUtils.REFSEQ_TRANSCRIPT, "Got the right id_type for " + SearchUtils.REFSEQ_TRANSCRIPT)

        self.assertEqual(SearchUtils.get_identifier_type("13: 32315474-32400266"),
                         SearchUtils.GENOMIC_LOCATION, "Got the right id_type for " + SearchUtils.GENOMIC_LOCATION)

    def test_get_lrg_id_from_hgnc_name(self):
        self.assertEqual(SearchUtils.get_lrg_id_from_hgnc_name("COL1A1"), "LRG_1", "Got the right LRG id back")
