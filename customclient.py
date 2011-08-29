from oaipmh import client
from os import path, mkdir
from datetime import date
from urllib import urlencode
from string import zfill
            
class CustomClient(client.Client):
    def __init__(self, base_url, mapping_path, metadata_registry):
        client.Client.__init__(self, base_url, metadata_registry)
        self._mapping = {}
        self._mapping_path = mapping_path
        self._verbose = False
        about = self.identify()
        self._name = about.repositoryName()
        self._earliestDate = about.earliestDatestamp()
        self._day_granularity = True
        self._mapping.clear()
        
        
    def makeRequest(self, **kw):
        def getRequestKey(kw):
            """Create stable key for request dictionary to use in file.
            """
            items = kw.items()
            items.sort()
            return urlencode(items)
        if self._verbose:
            print kw
        text = client.Client.makeRequest(self, **kw)
        self._mapping[getRequestKey(kw)] = text
        return text

    def save(self, output):
        mapping_path = self._mapping_path
        output_dir = (output if output != None else self._name)
        if not path.exists(path.join(mapping_path, output_dir)):
            mkdir(path.join(mapping_path, output_dir))
        f = open(path.join(mapping_path, output_dir, 'mapping.txt'), 'w')
        i = 0
                
        for request, response in self._mapping.items():
            filename = zfill(str(i), 5) + '.xml'
            response_f = open(path.join(mapping_path, output_dir, filename), 'w')
            f.write(request)
            f.write('\n')
            response_f.write(response)
            response_f.close()
            i += 1

        f.close()
