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

from release.utils.release_utils import ReleaseUtils
import json
from django.conf import settings
import logging

# Get an instance of a logger
from tark.settings.base import GOOGLE_ANALYTICS_ENABLED

logger = logging.getLogger(__name__)


def init_assembly_releases(request):
    # default is ensembl
    # The three queries below slows down all the pages on the app because they are
    # executes two or three times whenever a page is loaded, it is commented for now while
    # TODO: investigating why they were added (are they used somewhere?)
    # all_assembly_releases = json.dumps(ReleaseUtils.get_all_assembly_releases())
    # all_assembly_releases_refseq = json.dumps(ReleaseUtils.get_all_assembly_releases("RefSeq"))
    # all_assembly_releases_ensembl = json.dumps(ReleaseUtils.get_all_assembly_releases("Ensembl"))

    current_release = ReleaseUtils.get_latest_release()
    current_assembly = ReleaseUtils.get_latest_assembly()
    source_name = ReleaseUtils.get_default_source()
    software_release_tag = "1.0.0" if settings.SOFTWARE_RELEASE_TAG is None else settings.SOFTWARE_RELEASE_TAG

    init_hash = {
        # "all_assembly_releases": all_assembly_releases,
        # "all_assembly_releases_ensembl": all_assembly_releases_ensembl,
        # "all_assembly_releases_refseq": all_assembly_releases_refseq,
        "current_release": current_release,
        "current_assembly": current_assembly,
        "release_name": current_release,
        "assembly_name": current_assembly,
        'release_name_compare': int(current_release) - 1,
        'assembly_name_compare': current_assembly,
        'source_name': source_name,
        'software_release_tag': software_release_tag
    }

    return init_hash


def google_analytics_enabled(request):
    return {'GOOGLE_ANALYTICS_ENABLED': GOOGLE_ANALYTICS_ENABLED}
