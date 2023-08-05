import logging
import re

import pandas as pd
from requests import HTTPError

from ..util.nopcache import NopCache
from ..util.webcache import fetchjson


_logger = logging.getLogger(__name__)


foo = None


class CensusDataEndpoint(object):
    """A single census endpoint, with metadata about queryable variables
    and geography
    """

    def __init__(self, key, ds, cache, session, variableindex):
        """Initialize a Census API endpoint wrapper.

        Arguments:
          * key: user's API key.
          * ds: census dataset descriptor metadata.
          * cache: cache in which to look up/store metadata.
          * session: requests.Session to use for retrieving data.
          * variableindex: the Index in which to store variable data
        """
        self.key = key                         # API key
        self.session = session                 # requests.Session
        self.title = ds['title']               # title
        self.description = ds['description']   # long description
        self.__doc__ = self.description
        # dataset descriptors, (general to specific)
        self.dataset = tuple(ds['c_dataset'])
        # vintage, if dataset is year-specific
        self.vintage = ds.get('c_vintage')
        # API endpoint URL
        for distribution in ds.get('distribution') or []:
            if distribution.get('format') == 'API':
                self.endpoint = distribution['accessURL']
        # short ID
        self.id = self.endpoint.replace('https://api.census.gov/data/', '')
        # list of valid geographies
        self.geographies_ = (
            fetchjson(ds['c_geographyLink'], cache,
                      self.session) or
            {}
        )
        geo_cols = [
            'scheme',
            'name',
            'predicate_type',
            'referenceDate',
            'requires',
            'optionalWithWCFor',
            'wildcard']
        self.geographies = pd.DataFrame([], columns=geo_cols)
        for scheme in self.geographies_:
            tmp = pd.DataFrame(
                self.geographies_[scheme], columns=geo_cols)
            tmp['scheme'] = scheme
            self.geographies.append(tmp)

        # list of valid variables
        self.variables_ = (
            fetchjson(ds['c_variablesLink'], cache,
                      self.session)['variables'] or
            {}
        )
        global foo
        foo = self
        self.variables = pd.DataFrame(
            self.variables_, index=[
                'label', 'concept', 'predicateType', 'group',
                'limit', 'predicateOnly', 'attributes',
            ]).T
        # index the variables
        self.variableindex = variableindex
        self.variableindex.add(self._generateVariableRows())

        # keep track of concepts for indexing
        self.concepts = set(self.variables['concept']
                            .dropna().sort_values().values)

        # list of keywords
        self.keywords = ds.get('keyword', [])
        # list of tags
        self.tags = []
        if 'c_tagsLink' in ds:
            # list of tags
            # Note: as of 2021-04-12, these are all broken
            try:
                self.tags = fetchjson(ds['c_tagsLink'], cache,
                                      self.session)['tags']
            except HTTPError as e:
                _logger.warn(f"Unable to fetch {ds['c_tagsLink']}: {e}")

        # list of groups
        self.groups_ = {}
        if 'c_groupsLink' in ds:
            # list of groups
            for row in fetchjson(ds['c_groupsLink'], cache,
                                 self.session)['groups']:
                self.groups_[row['name']] = {'descriptions': row['description']}
                if row['variables']:
                    self.groups_[row['name']]['variables'] = list(
                        fetchjson(row['variables'], cache,
                                  self.session)['variables'].keys())
        self.groups = pd.DataFrame(self.groups_).T

    def searchVariables(self, query, **constraints):
        """Return for variables matching a query string.

        Keywords are `variable` (ID), `label` (name) and `concept`
        (grouping of variables).

        """
        return pd.DataFrame(
            self.variableindex.query(
                query,
                api_id=self.id,
                **constraints),
            columns=['score'] + list(self.variableindex.fields)
        ).drop('api_id', axis=1)

    @staticmethod
    def _geo2str(geo):
        """Format geography dict as string for query"""
        return ' '.join(f'{k}:{v}' for k, v in geo.items())

    def __call__(self, fields, geo_for, *, geo_in=None, cache=NopCache(),
                 groups=[]):
        """Special method to make API object invocable.

        Arguments:
          * fields: list of variables to return.
          * geo_* fields must be given as dictionaries, eg:
            `{'county': '*'}`
          * cache: cache in which to store results. Not cached by default.
          * groups: variable groups to retrieve
        """
        params = {
            'get': ','.join(fields + [f'group({group})'
                                      for group in groups]),
            'key': self.key,
            'for': self._geo2str(geo_for),
        }
        if geo_in:
            params['in'] = self._geo2str(geo_in)

        j = fetchjson(self.endpoint, cache, self.session, params=params)
        ret = pd.DataFrame(data=j[1:], columns=j[0])
        for group in groups:
            if group in self.groups.index:
                fields += self.groups.loc[group, 'variables']
        for field in fields:
            basefield = re.sub(r'(?<=\d)[EM]A?$', 'E', field)
            if self.variables.loc[basefield, 'predicateType'] in ('int', 'float'):
                ret[field] = pd.to_numeric(ret[field])
        return ret

    def _generateVariableRows(self):
        for k, v in self.variables_.items():
            yield dict(
                api_id=self.id,
                variable=k,
                group=v.get('group', ''),
                label=v.get('label', ''),
                concept=v.get('concept', ''),
            )

    def __repr__(self):
        """Represent API endpoint by its title"""
        return self.title
