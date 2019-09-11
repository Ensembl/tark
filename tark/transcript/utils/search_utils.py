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
import re


class SearchUtils(object):

    ENSEMBL_TRANSCRIPT = "ENSEMBL_TRANSCRIPT"
    ENSEMBL_GENE = "ENSEMBL_GENE"
    ENSEMBL_PROTEIN = "ENSEMBL_PROTEIN"

    REFSEQ_TRANSCRIPT = "REFSEQ_TRANSCRIPT"
    REFSEQ_PROTEIN = "REFSEQ_PROTEIN"

    LRG_TRANSCRIPT = "LRG_TRANSCRIPT"
    LRG_GENE = "LRG_GENE"

    HGVS_GENOMIC_REF = "HGVS_GENOMIC_REF"

    HGVS_REFSEQ_REF = "HGVS_REFSEQ_REF"

    HGNC_SYMBOL = "HGNC_SYMBOL"

    GENOMIC_LOCATION = "GENOMIC_LOCATION"

    @classmethod
    def get_seq_region_from_refseq_accession(cls, refseq_accession):

        GRCh38 = {
            'NC_000001.11': '1',
            'NC_000002.12': '2',
            'NC_000003.12': '3',
            'NC_000004.12': '4',
            'NC_000005.10': '5',
            'NC_000006.12': '6',
            'NC_000007.14': '7',
            'NC_000008.11': '8',
            'NC_000009.12': '9',
            'NC_000010.11': '10',
            'NC_000011.10': '11',
            'NC_000012.12': '12',
            'NC_000013.11': '13',
            'NC_000014.9': '14',
            'NC_000015.10': '15',
            'NC_000016.10': '16',
            'NC_000017.11': '17',
            'NC_000018.10': '18',
            'NC_000019.10': '19',
            'NC_000020.11': '20',
            'NC_000021.9': '21',
            'NC_000022.11': '22',
            'NC_000023.11': 'X',
            'NC_000024.10': 'Y',
            'NC_012920.1': 'MT'
        }

        GRCh37 = {
            'NC_000001.10': '1',
            'NC_000002.11': '2',
            'NC_000003.11': '3',
            'NC_000004.11': '4',
            'NC_000005.9': '5',
            'NC_000006.11': '6',
            'NC_000007.13': '7',
            'NC_000008.10': '8',
            'NC_000009.11': '9',
            'NC_000010.10': '10',
            'NC_000011.9': '11',
            'NC_000012.11': '12',
            'NC_000013.10': '13',
            'NC_000014.8': '14',
            'NC_000015.9': '15',
            'NC_000016.9': '16',
            'NC_000017.10': '17',
            'NC_000018.9': '18',
            'NC_000019.9': '19',
            'NC_000020.10': '20',
            'NC_000021.8': '21',
            'NC_000022.10': '22',
            'NC_000023.10': 'X',
            'NC_000024.9': 'Y',
        }

        if refseq_accession in GRCh38:
            return (GRCh38[refseq_accession], "GRCh38")
        elif refseq_accession in GRCh37:
            return (GRCh37[refseq_accession], "GRCh37")
        else:
            return None

    @classmethod
    def parse_location_string(cls, loc_string):
        loc_string = loc_string.replace(" ", "")
        loc_string = loc_string.replace(",", "")
        matchloc = re.search(r'(\w+):(\d+)-(\d+)', loc_string)
        loc_region = matchloc.group(1)
        loc_start = matchloc.group(2)
        loc_end = matchloc.group(3)
        return (loc_region, loc_start, loc_end)

    @classmethod
    def parse_hgvs_genomic_location_string(cls, hgvs_string):
        matchloc = re.search(r'(NC_\d+\.\d+):g\.(\d+)(\w\>\w)', hgvs_string)
        refseq_accession = matchloc.group(1)
        (loc_region, loc_assemby) = cls.get_seq_region_from_refseq_accession(refseq_accession)
        loc_start = matchloc.group(2)
        loc_end = loc_start
        return (loc_region, loc_start, loc_end, loc_assemby)

    @classmethod
    def parse_hgvs_refseq_string(cls, hgvs_string):
        matchloc = re.search(r'(NM_\d+\.\d+):c\.(\d+)(\w\>\w)', hgvs_string)
        refseq_accession = matchloc.group(1)
        return (refseq_accession)

    @classmethod
    def get_identifier_type(cls, identifier):

        # replace white space
        identifier = identifier.replace(" ", "")

        # ensembl transcript
        if re.compile('^ENST\d+').match(identifier):
            return cls.ENSEMBL_TRANSCRIPT

        # ensembl gene
        if re.compile('^ENSG\d+').match(identifier):
            return cls.ENSEMBL_GENE

        # ensembl protein
        if re.compile('^ENSP\d+').match(identifier):
            return cls.ENSEMBL_PROTEIN

        # refseq protein
        if re.compile('^NP_\d+').match(identifier):
            return cls.REFSEQ_PROTEIN

        # hgvs genomic eg:  NC_000023.11:g.32389644G>A
        if re.compile(r'NC_\d+\.\d+:g\.\d+\w\>\w').match(identifier):
            return cls.HGVS_GENOMIC_REF

        # hgvs refesq eg:  NM_004006.2:c.4375C>T
        if re.compile(r'NM_\d+\.\d+:c\.\d+\w\>\w').match(identifier):
            return cls.HGVS_REFSEQ_REF

        # refseq trasncript
        if re.compile('(^NM_|NR_|XM_|XR_).*').match(identifier):
            return cls.REFSEQ_TRANSCRIPT

        # lrg transcript
        if re.compile('^LRG_\d+t\d+').match(identifier):
            return cls.LRG_TRANSCRIPT

        # lrg gene
        if re.compile('^LRG_\d+').match(identifier):
            return cls.LRG_GENE

        # genomic location eg:  13:32315474-32400266 )
        if re.compile(r'(\w+):(\d+)-(\d+)').match(identifier):
            return cls.GENOMIC_LOCATION

        # default
        return cls.HGNC_SYMBOL
