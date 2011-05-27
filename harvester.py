#!/usr/bin/env python
# -*- coding: utf-8 -*-


from customclient import CustomClient
from oaipmh.metadata import MetadataRegistry, oai_dc_reader
from oaipmh.server import oai_dc_writer
from os.path import exists
from datetime import datetime
from os import makedirs
import argparse
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
            

    def doMultHarvest(self, providers):
        for provider in providers:
            date = self.getFromDate(provider)
            iterator = provider.listRecords(metadataPrefix='oai_dc', from_=date)
            for rec in iterator:
                provider.save()
                
    def doHarvest(self, provider, metadata, from_, until):
        import pdb; pdb.set_trace()
        iterator = provider.listRecords(metadataPrefix=metadata, 
                                        from_=from_, until=until)
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
    
    parser = argparse.ArgumentParser(
        description='Make harvest from any repositories and save the metadata in file system')
        
    parser.add_argument(
        '-u', '--url', type=str, default=None,
        help='an alternative URL for harvesting. Ignore settings file')   
    
    parser.add_argument(
        '-f', '--from_', type=str, default=None,
        help='an initial date to harvest')
        
    parser.add_argument(
        '-t', '--to', type=str, default=None,
        help='a final date to harvest')
        
    parser.add_argument(
        '-m', '--metadata', type=str, default='oai_dc',
        help='specify the metadataPrefix for OAI protocol')
        
    parser.add_argument(
        '-g', '--go', action='store_true', 
        help='makes harvest from a default providers list')
        
    args = parser.parse_args()
    if args.go:
        providers = harv.getProvidersIterator()
        harv.doMultHarvest(providers)
    else:
        from_=datetime.strptime(args.from_, '%Y-%m-%d')
        until=datetime.strptime(args.to, '%Y-%m-%d')
        provider = CustomClient(args.url, BASE_PATH, harv._registry)
        harv.doHarvest(provider, args.metadata, from_=from_, until=until)
        
    
    
    
    
    



























