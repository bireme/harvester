#!/usr/bin/env python
# -*- coding: utf-8 -*-

from oaipmh.metadata import MetadataRegistry, oai_dc_reader
from metadatareaders import qdc_reader
from customclient import CustomClient
from oaipmh.server import oai_dc_writer
from os.path import exists
from datetime import datetime
from re import compile, match
from os import makedirs
from settings import *
import argparse
import json
import sys


class Harvester(object):
    '''A client to originally harvest DSpace repositories.
    Use the PyOAI API.
    '''

    def __init__(self, registry):
        self._registry = registry

    def getProvidersIterator(self):
        for provider in PROVIDERS:
            providerDir = BASE_PATH+provider[0]
            if not exists(providerDir):
                makedirs(providerDir)
            yield CustomClient(provider[1], providerDir, self._registry)
            

    def doMultHarvest(self, providers, metadata, verbose):
        for provider in providers:
            provider._verbose = verbose
            date = self.getFromDate(provider)
            lastDate = None
            iterator = provider.listRecords(metadataPrefix=metadata, from_=date)
            for header, metadata, about in iterator:
                provider.save()
                lastDate = header.datestamp()
                
            self.saveLastDate(provider, lastDate)
                
    def doHarvest(self, provider, metadata, setName, from_, until):
        
        iterator = provider.listRecords(metadataPrefix=metadata, set=setName,
                                        from_=from_, until=until)
        
        for header, metadata, about in iterator:
            provider.save()

    def getFromDate(self, provider):
        pName = provider._name
        
        with open('dates.json', 'r') as f:
            entry = json.load(f)
        
        pDict = entry.get(pName)
        
        if pDict:
            date = datetime(pDict['year'],
                            pDict['month'],
                            pDict['day'])
        else:
            date = provider._earliestDate
        return date
        
    def saveLastDate(self, provider, date):
        pName = provider._name
        entry = {}
        entry[pName] = {}
        entry[pName]['year'] = date.year
        entry[pName]['month'] = date.month
        entry[pName]['day'] = date.day
        
        with open('dates.json', mode='a+') as f:
            json.dump(entry, f, indent=2)
    
    def showSets(self, provider):
        iterator = provider.listSets()
        print "Provider Name: %s \n" % provider._name

        for header, metadata, about in iterator:
            print "setSpec: {:<30} \t setName: {}".format(header, metadata)


    
if __name__ == '__main__' :
    
    registry = MetadataRegistry()
    registry.registerReader('oai_dc', oai_dc_reader)
    registry.registerReader('qdc', qdc_reader)
    registry.registerWriter('oai_dc', oai_dc_writer)
    
    date_patern = compile(REGEX_DATE)
    
    if not exists(BASE_PATH):
        makedirs(BASE_PATH)
    
    harv = Harvester(registry)
    
    parser = argparse.ArgumentParser(
        description='Make harvest from any repositories and save the metadata in file system')
        
    group = parser.add_mutually_exclusive_group(required=True)
    
    group.add_argument(
        '-u', '--url', type=str, default=None, metavar='OAI provider URL',
        help='an alternative URL for harvesting. Ignore settings file')   
    
    parser.add_argument(
        '-i', '--initial', type=str, default=None,
        help='an initial date to harvest')
        
    parser.add_argument(
        '-f', '--final', type=str, default=None,
        help='a final date to harvest')
        
    parser.add_argument(
        '-s', '--set', type=str, default=None,
        help='defines a SET to harvest')
        
    parser.add_argument(
        '-m', '--metadata', type=str, default='oai_dc',
        help='specify the metadataPrefix for OAI protocol')
        
    parser.add_argument(
        '-v', '--verbose', action='store_true', 
        help='list each request information')

    parser.add_argument(
        '-l', '--list', action='store_true', 
        help='list each provider set')
        
    group.add_argument(
        '-g', '--go', action='store_true', 
        help='makes harvest from a default providers list')
        
    args = parser.parse_args()
    
    if args.go:
        providers = harv.getProvidersIterator()
        harv.doMultHarvest(providers, args.metadata, args.verbose)
    elif args.list:
        provider = CustomClient(args.url, BASE_PATH, harv._registry)
        harv.showSets(provider)
    else:
        if args.initial and date_patern.match(args.initial):
            initial=datetime.strptime(args.initial, STR_DATE)
        elif args.initial:
            print 'Invalid date fromat: Date must be like %s' % DATE_EX
            raise SystemExit
        else:
           initial=None
        
        if args.final and date_patern.match(args.final):
            final=datetime.strptime(args.final, STR_DATE)
        elif args.final:
            print 'Invalid date fromat: Date must be like %s' % DATE_EX
            raise SystemExit
        else:
            final=None
            
        if initial > final:
            print 'Invalid date parameters: Final date must be greater than Initial date'
            raise SystemExit
        
        provider = CustomClient(args.url, BASE_PATH, harv._registry)
        provider._verbose=args.verbose
        harv.doHarvest(provider, args.metadata, args.set,
                       from_=initial, until=final)
