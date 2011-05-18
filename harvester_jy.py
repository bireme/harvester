#!/usr/bin/env jython
# -*- coding: utf-8 -*-

from sys import path
from glob import glob
from os.path import exists
import settings
from com.xhaus.jyson import JysonCodec as json
import xml.etree.ElementTree as etree


libDir='/home/rafael/aplicacoes/oai-pmh/java/lib/harvester2-0.1.12'

for jar in glob(libDir+'/*.jar'):
    path.append(jar)

from ORG.oclc.oai.harvester2.verb import Identify
from ORG.oclc.oai.harvester2.verb import ListRecords

def listRecords(url, provider, from_date='', until_date='', setSpec='', 
                prefix='', token=None):
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
        elif (token != None or len(token) != 0): #and loop >= settings.LIMIT_TO_CALLS:
            saveResumptionToken(provider, token)
            saveUntilDate()
            break
        else:
            records = ListRecords(url, token)
    return content
    
def identifyProvider(url):
    content = Identify(url)
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
    
def getFromDate(provider):
    tf = open('token.json', 'r')
    res = json.loads(tf.read())
    tf.close()
    
    providerName = provider[0]
    lastDate = res[providerName]['date']
    
    if lastDate:
        fromdate = lastDate
    else:
        fromDate = getInitDate(provider)
    return fromDate
    
def getInitDate(provider):
    url = provider[1]
    content = identifyProvider(url)
    root = etree.XML(content.toString())
    #FIXME: pegar a data do XML de um jeito correto
    return root[2][4].text
    

def doHarvest():
    for provider in settings.PROVIDERS:
        name = provider[0]
        url = provider[1]
        date = getFromDate(provider)
        token = loadResumptionToken(name)
        content = listRecords(url, name, date, prefix='oai_dc')
        writeXMLFile(name, content)
        print "Harvest done for %s provider" % name
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
