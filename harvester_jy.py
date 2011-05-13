#!/usr/bin/env jython
# -*- coding: utf-8 -*-

from sys import path
from glob import glob
from os.path import exists
import settings
from com.xhaus.jyson import JysonCodec as json

libDir='/home/rafael/aplicacoes/oai-pmh/java/lib/harvester2-0.1.12'

for jar in glob(libDir+'/*.jar'):
    path.append(jar)

from ORG.oclc.oai.harvester2.verb import GetRecord
from ORG.oclc.oai.harvester2.verb import ListRecords

def listRecords(url, provider, from_date='', until_date='', setSpec='', prefix='', token=''):
    content = ''
    loop = 0
    if token == None:
        records = ListRecords(url, from_date, until_date, setSpec, prefix)
    else:
        records = ListRecords(url, token)
    while records:
        #import pdb; pdb.set_trace()
        loop += 1
        content += records.toString() + "\n"
        errors = records.getErrors().toString()
        token = records.getResumptionToken()
        if errors != None or errors.length > 0:
            #writeErrorLog(errors + "\n")
            pass            
        if token == None or len(token) == 0:
            content=''
            break
        elif (token != None or len(token) != 0) and loop >= settings.LIMIT_TO_CALLS:
            saveResumptionToken(provider, token)
            break
        else:
            records = ListRecords(url, token)
    return content


def writeXMLFile(provider, content):
    fileName = provider+'.xml'
    if exists(fileName):
        xmlFile = open(fileName, 'a')
    else:
        xmlFile = open(fileName, 'w')
    xmlFile.write(content.encode('utf-8') + "\n")
    xmlFile.close()

def writeErrorLog(content):
    errorLog = open('ErrorLog.xml', 'a+')
    errorLog.write(content)
    errorLog.close()
    
def saveResumptionToken(provider, token):
    tf = open('token.json', 'r')
    tokenDict = json.loads(tf.read())
    tf.close()
    
    tokenDict[provider]['token'] = token
    
    tf = open('token.json', 'w')
    tf.write(json.dumps(tokenDict))
    tf.close()

def loadResumptionToken(provider):
    tf = open('token.json', 'r')
    res = json.loads(tf.read())
    tf.close()
    
    return res[provider]['token']

def doHarvest():
    for provider in settings.PROVIDERS:
        name = provider[0]
        url = provider[1]
        token = loadResumptionToken(name)
        content = listRecords(url, name, 'oai_dc')
        writeXMLFile(name, content)
        print "Harvest done for %s provider" % name
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
