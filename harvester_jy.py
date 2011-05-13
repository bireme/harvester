#!/usr/bin/env jython
# -*- coding: utf-8 -*-

from sys import path
from glob import glob
from os.path import exists
import settings
import json


libDir='/home/rafael/aplicacoes/oai-pmh/java/lib/harvester2-0.1.12'

for jar in glob(libDir+'/*.jar'):
    path.append(jar)

from ORG.oclc.oai.harvester2.verb import GetRecord
from ORG.oclc.oai.harvester2.verb import ListRecords

def listRecords(url, from_date='', until_date='', setSpec='', prefix=''):
    content = ''
    loop = 0
    res = loadResumptionToken('scielo')
    if res == None:
        records = ListRecords(url, from_date, until_date, setSpec, prefix)
    else:
        records = ListRecords(url, res)
    while records:
        #import pdb; pdb.set_trace()
        loop += 1
        content += records.toString() + "\n"
        errors = records.getErrors()
        res = records.getResumptionToken()
        if errors != None or errors.length > 0:
            writeErrorLog(res + "\n")            
        if res == None or len(res) == 0:
            content=''
            break
        elif (res != None or len(res) != 0) and loop >= LIMIT_TO_CALLS:
            saveResumptionToken('scielo', res)
            break
        else:
            records = ListRecords(url, res)
    return content


def writeXMLFile(content):
    if exists('oai.xml'):
        xmlFile = open('oai.xml', 'a')
    else:
        xmlFile = open('oai.xml', 'w')
    xmlFile.write(content.encode('utf-8') + "\n")
    xmlFile.close()

def writeErrorLog(content):
    errorLog = open('ErrorLog.xml', 'a+')
    errorLog.write(content)
    errorLog.close()
    
def saveResumptionToken(provider, token):
    tf = open('token.json', 'r')
    tokenDict = json.load(tf)
    tf.close()
    
    tokenDict[provider]['token'] = token
    
    with open('token.json', 'w') as tf:
        json.dump(tokenDict, tf, indent=2)

def loadResumptionToken(provider):
    with open('token.json', 'r') as tf:
        res = json.load(tf)
    
    return res[provider]['token']


