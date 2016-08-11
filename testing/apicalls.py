#!/usr/bin/pytho
from bottle import route, run, template, request
from jsonrpclib import Server
import collections
import time
import socket
import json

username = "admin" 
password = "admin"
SWITCH = "172.28.168.97"
DEMO_SWITCH_IP= SWITCH
commandApiUrl = "http://{}:{}@{}/command-api".format(username, password, DEMO_SWITCH_IP)

@route('/something')
def something():
    return jsonp(request, dict(success="It worked"))

def eApiShowInterfaces():
    switch = Server(commandApiUrl)
    response = switch.runCmds( 1, ["show interfaces"])
    if (request.query.callback):
        return directFlowJsonp(request)
    else:
        return json.dumps(eApiDirectFlow(), indent=4, sort_keys=True)

@route('/showinterfaces')
def showinterface():
    dictionary = convert(eApiShowInterfaces())
    return dictionary
