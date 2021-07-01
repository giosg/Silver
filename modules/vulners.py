import json

from core.requester import requester
from core.utils import reader, write_json


class VulnersExplorer:
    def __init__(self, cache_file_path):
        self.cache_file_path = cache_file_path
        self.database = json.loads(reader(self.cache_file_path))


    def vulners(self, software, version, cpe=False):
        if software and version:
            pass
        else:
            return False
        cached = self.__query_cache(software, version, cpe)
        if cached:
            if cached == 'vulnerable':
                return True
            else:
                return False
        kind = 'software'
        if cpe:
            kind = 'cpe'
        data = '{"software": "%s", "version": "%s", "type" : "%s", "maxVulnerabilities" : %i}' % (software, version, kind, 1)
        response = requester('https://vulners.com/api/v3/burp/software/', get=False, data=data).text
        self.__cache(software, version, response, cpe)
        if 'Nothing found for Burpsuite search request' in response:
            return False
        return True

    def __query_cache(self, software, version, cpe):
        if cpe:
            if software in self.database['by_cpe']:
                if self.database['by_cpe'][software] == True:
                    return 'vulnerable'
                else:
                    return 'not-vulerable'
                return False
        else:
            if software in self.database['by_version']:
                if version in self.database['by_version'][software]:
                    if self.database['by_version'][software][version] == True:
                        return 'vulnerable'
                    else:
                        return 'not-vulerable'
                return False
        return False

    def __cache(self, software, version, response, cpe):
        vulnerable = True
        if 'Nothing found for Burpsuite search request' in response:
            vulnerable = False
        if cpe:
            if software not in self.database['by_cpe']:
                self.database['by_cpe'][software] = vulnerable
        else:
            if software not in cache_db['by_version']:
                self.database['by_version'][software] = {}
            if version not in database['by_version'][software]:
                self.database['by_version'][software][version] = vulnerable
        write_json(self.cache_file_path, self.database)
