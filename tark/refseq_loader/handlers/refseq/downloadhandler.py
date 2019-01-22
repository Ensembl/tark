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
import os
import wget


class DownloadHandler():

    @classmethod
    def download_files(cls, file_names, download_root_url, download_dir=None):
        download_dir = download_dir if download_dir else "tmp_refseq/"

        print('download_dir ' + download_dir)
        print('download_root_url ' + download_root_url)

        if not os.path.exists(download_dir):
            print("path doesn't exists. Creating dir at " + download_dir)
            os.makedirs(download_dir)

        print('Beginning refseq gff file download with wget module..........')
        downladed_files = {}
        for file_name in file_names:
            file_url = download_root_url + file_name
            print("File url :" + str(file_url))
            downloaded_file_url = download_dir + file_name
            base = os.path.basename(file_name)
            downloaded_file_url_unzipped = download_dir + os.path.splitext(base)[0]
            print(downloaded_file_url_unzipped)

            if "p12_genomic.gff" in file_name:
                file_key = "gff"
            elif "GRCh38.p12_rna.fna" in file_name:
                file_key = "fasta"
            elif "GRCh38.p12_protein.faa" in file_name:
                file_key = "protein"
            elif "p12_rna.gbff" in file_name:
                file_key = "gbff"

            downladed_files[file_key] = downloaded_file_url_unzipped

            if not os.path.exists(downloaded_file_url):
                print('File doesnt exists ' + downloaded_file_url + "\n About to download file " + file_url + '\n')
                sucess_file_name = wget.download(file_url, download_dir)
                print(" Success file name " + sucess_file_name)
                cls.unzip_file(downloaded_file_url)
            else:
                print("File already exists at " + downloaded_file_url)
                cls.unzip_file(downloaded_file_url)

        print('\nSuccessfully Downloaded refseq gff files to ' + download_dir + '\n')

        return downladed_files

    @classmethod
    def unzip_file(cls, file_path):
        print("calling unzip file " + file_path)
        if os.path.exists(file_path):
                    gff_status = os.system('gunzip ' + file_path)
                    if not gff_status == 0:
                        raise ValueError("Unzipped GFF file not found ")
