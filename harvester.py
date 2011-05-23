from customclient import CustomClient
from oaipmh.metadata import MetadataRegistry, oai_dc_reader
from oaipmh.server import oai_dc_writer
from os.path import exists
from os import makedirs
import settings

BASE_PATH = '/home/rafael/aplicacoes/oai-pmh/script/tmp/'


registry = MetadataRegistry()
registry.registerReader('oai_dc', oai_dc_reader)
registry.registerWriter('oai_dc', oai_dc_writer)

def getClientsIterator():
    for provider in settings.PROVIDERS:
        providerDir = BASE_PATH+provider[0]
        if not exists(providerDir):
            makedirs(providerDir)
        yield CustomClient(provider[1], providerDir, registry)
        

def doHarvest():
    for client in getClientsIterator():
        iterator = client.listRecords(metadataPrefix='oai_dc')
        for header, metadata, about in iterator:
            client.save()


