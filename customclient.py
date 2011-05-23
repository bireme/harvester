from oaipmh import client
import os.path
from datetime import date
from urllib import urlencode


def getRequestKey(kw):
    """Create stable key for request dictionary to use in file.
    """
    items = kw.items()
    items.sort()
    return urlencode(items)

class CustomClient(client.Client):
    def __init__(self, base_url, mapping_path, metadata_registry):
        client.Client.__init__(self, base_url, metadata_registry)
        self._mapping = {}
        self._mapping_path = mapping_path
        
    def makeRequest(self, **kw):
        print kw
        text = client.Client.makeRequest(self, **kw)
        self._mapping[getRequestKey(kw)] = text
        return text

    def save(self):
        mapping_path = self._mapping_path
        f = open(os.path.join(mapping_path, 'mapping.txt'), 'w')
        filename = date.today().strftime("%Y-%m-%d") + '.xml'
        response_f = open(os.path.join(mapping_path, filename), 'w')
        
        for request, response in self._mapping.items():
            f.write(request)
            f.write('\n')
            response_f.write(response)
            i += 1
        response_f.close()
        f.close()
  

