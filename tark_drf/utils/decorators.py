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


import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class setup_eager_loading(object):
    '''
    Decorator to select/prefetch related entries
    '''

    def __init__(self, serializer):
        self.serializer = serializer

    def __call__(self, f):
        def wrapped_f(*args):
            view = args[0]
            queryset = f(*args)
            query_params = view.request.query_params
            entries = []
            many2one = getattr(self.serializer, 'MANY2ONE_SERIALIZER', None)
            one2many = getattr(self.serializer, 'ONE2MANY_SERIALIZER', None)

            if 'expand' in query_params:
                entry = query_params['expand']
                entries = entry.split(',') if entry else None
            elif 'expand_all' in query_params and query_params['expand_all'] == 'true':
                if many2one is not None:
                    entries.extend(list(many2one.keys()))
                if one2many is not None:
                    entries.extend(list(one2many.keys()))

            for entry in entries:
                entry = entry.strip()
                if many2one is not None and entry in many2one.keys():
                    logger.info('many2one entry from eager loading select_related:' + str(entry))
                    queryset = queryset.select_related(entry)
                if one2many is not None and entry in one2many.keys():
                    logger.info('one2many entry from eager loading prefetch_related: ' + str(entry))
                    if "translations" == entry:
                        queryset = queryset.prefetch_related(entry)

            return queryset
        return wrapped_f


class expand_all_related(object):
    '''
    Decorator to select/prefetch related entries
    '''

    def __init__(self, serializer):
        self.serializer = serializer

    def __call__(self, f):
        def wrapped_f(*args):
            queryset = f(*args)
            entries = []
            many2one = getattr(self.serializer, 'MANY2ONE_SERIALIZER', None)
            one2many = getattr(self.serializer, 'ONE2MANY_SERIALIZER', None)

            if many2one is not None:
                entries.extend(list(many2one.keys()))
            if one2many is not None:
                entries.extend(list(one2many.keys()))

            for entry in entries:
                entry = entry.strip()
                if many2one is not None and entry in many2one.keys():
                    queryset = queryset.select_related(entry)
                if one2many is not None and entry in one2many.keys():
                    queryset = queryset.prefetch_related(entry)

            return queryset
        return wrapped_f
