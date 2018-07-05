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


class ExonUtils(object):

    @classmethod
    def exon_set_compare(cls, exonset1, exonset2):
        print("******====FROM exon_set_compare set1===========")
        print(exonset1)
        print("*******===FROM exon_set_compare===========")

        print("******====FROM exon_set_compare set2===========")
        print(exonset2)
        print("*******===FROM exon_set_compare===========")

        compare_result = {}

        for exon1 in exonset1:
            for exon2 in exonset2:
                if exon1["loc_start"] >= exon2["loc_start"] and exon1["loc_start"] <= exon2["loc_end"] or \
                        exon1["loc_end"] >= exon2["loc_start"] and exon1["loc_end"] <= exon2["loc_end"]:
                    compare_result[exon1["exon_order"]] = exon2["exon_order"]
                    break

        print(compare_result)

        # check compare_result and add the missing match
        list_set1 = []
        list_set2 = []
        if len(exonset1) >= len(exonset2):
            for exon1 in exonset1:
                if exon1["exon_order"] in compare_result.keys():
                    list_set1.append(exon1["exon_order"])
                    list_set2.append(compare_result[exon1["exon_order"]])
                else:
                    list_set1.append(exon1["exon_order"])
                    list_set2.append(0)
        else:
            for exon2 in exonset2:
                if exon2["exon_order"] in compare_result.values():
                    if exon2["exon_order"] in compare_result:
                        list_set1.append(exon2["exon_order"])
                        list_set2.append(compare_result[exon2["exon_order"]])
                else:
                    list_set1.append(0)
                    list_set2.append(exon2["exon_order"])


        compare_result_list = [list_set1, list_set2]

        print(list_set1)
        print(list_set2)
        print(compare_result_list)

        return compare_result_list

