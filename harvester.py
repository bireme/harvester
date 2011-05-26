from customclient import CustomClient
from oaipmh.metadata import MetadataRegistry, oai_dc_reader
from oaipmh.server import oai_dc_writer
from os.path import exists
from datetime import datetime
from os import makedirs
import settings
import json
import sys

BASE_PATH = '/home/rafael/aplicacoes/oai-pmh/script/tmp/'

class Harvester(object):
    '''A client to originally harvest DSpace repositories.
    Use the PyOAI API.
    '''

    def __init__(self, registry):
        self._registry = registry

    def getProvidersIterator(self):
        for provider in settings.PROVIDERS:
            providerDir = BASE_PATH+provider[0]
            if not exists(providerDir):
                makedirs(providerDir)
            yield CustomClient(provider[1], providerDir, self._registry)
            

    def doHarvest():
        for provider in getProvidersIterator():
            date = getFromDate(provider)
            iterator = provider.listRecords(metadataPrefix='oai_dc', from_=date)
            for rec in iterator:
                provider.save()

    def getFromDate(provider):
        pName = provider._name
        
        with open('teste.json', 'r') as f:
            entry = json.load(f)
        
        pDict = entry.get(pName)
        
        if pDict:
            date = datetime(pDict['year'],
                            pDict['month'],
                            pDict['day'])
        else:
            date = provider._earliestDate
        
        
    def saveLastDate(provider, date):
        pName = provider._name
        entry = {}
        entry[pName] = {}
        entry[pName]['year'] = date.year
        entry[pName]['month'] = date.month
        entry[pName]['day'] = date.day
        
        with open('teste.json', mode='a+') as f:
            json.dump(entry, f, indent=2)

    def loadLastDate(provider):
        with open('teste.json', mode='r') as f:
            entry = json.load(f)
            
        pName = provider._name
        lastDate = datetime(entry[pName]['year'],
                            entry[pName]['month'],
                            entry[pName]['day'])
                            
        return lastDate


if __name__ == '__main__':
    
    registry = MetadataRegistry()
    registry.registerReader('oai_dc', oai_dc_reader)
    registry.registerWriter('oai_dc', oai_dc_writer)
    
    harv = Harvester(registry)
    
    if len(sys.argv) == 1:
        #harv.doHarvest()
        pass
