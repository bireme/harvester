from customclient import CustomClient
from oaipmh.metadata import MetadataRegistry, oai_dc_reader
from oaipmh.server import oai_dc_writer
from os.path import exists
from datetime import datetime
from os import makedirs
import settings
import json

BASE_PATH = '/home/rafael/aplicacoes/oai-pmh/script/tmp/'


registry = MetadataRegistry()
registry.registerReader('oai_dc', oai_dc_reader)
registry.registerWriter('oai_dc', oai_dc_writer)

def getProvidersIterator():
    for provider in settings.PROVIDERS:
        providerDir = BASE_PATH+provider[0]
        if not exists(providerDir):
            makedirs(providerDir)
        yield CustomClient(provider[1], providerDir, registry)
        

def doHarvest():
    for provider in getProvidersIterator():
        iterator = provider.listRecords(metadataPrefix='oai_dc')
        for rec in iterator:
            provider.save()

def getInitDate(provider):
    about = provider.identify()
    return about.earliestDatestamp()
    
def saveLastDate(provider, date):
    repoName = provider[0]
    entry = {}
    entry[repoName] = {}
    entry[repoName]['year'] = date.year
    entry[repoName]['month'] = date.month
    entry[repoName]['day'] = date.day
    
    with open('teste.json', mode='a+') as f:
        json.dump(entry, f, indent=2)

def loadLastDate(provider):
    with open('teste.json', mode='r') as f:
        entry = json.load(f)
        
    repoName = provider[0]
    lastDate = datetime(entry[repoName]['year'],
                        entry[repoName]['month'],
                        entry[repoName]['day']
                        )
    return lastDate
