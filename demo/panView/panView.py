#!/usr/bin/python

from bottle import route, run, template, request
from jsonrpclib import Server
import collections
import time
import socket
import json

username = "eapi"  #"fredlhsu"
password = "eapi"  #"arista"
SWITCH = "172.22.28.95"
DEMO_SWITCH_IP= SWITCH    
commandApiUrl = "http://{}:{}@{}/command-api".format(username, password, DEMO_SWITCH_IP)

def jsonp(request, dictionary):
    if (request.query.callback):
        dictionary = convert(eApiShowInterfaces())
        interfaces = []
        for i in range(1,5):
            name = "Ethernet{}".format(i)
            intf = {"name":name, "stats":dictionary["interfaces"][name]["interfaceStatistics"]}
            interfaces.append(intf)

        response = "%s(%s)" % (request.query.callback, interfaces)
        return response
    return dictionary

def directFlowJsonp(request):
    response = ""
    if (request.query.callback):
        flows = json.dumps(eApiDirectFlow(), indent=4, sort_keys=True)
        response = "%s(%s)" % (request.query.callback, flows)
    return response


@route('/something')
def something():
    return jsonp(request, dict(success="It worked"))


@route('/show/directflow/flows')
def showdirectflowflows():
    if (request.query.callback):
        return directFlowJsonp(request)
    else:
        return json.dumps(eApiDirectFlow(), indent=4, sort_keys=True)

@route('/showinterfaces')
def showinterface():
    dictionary = convert(eApiShowInterfaces())
    return dictionary

def eApiShowInterfaces():
    switch = Server(commandApiUrl)
    response = switch.runCmds( 1, ["show interfaces"])
    return response[0]

def eApiDirectFlow():
    switch = Server(commandApiUrl)
    response = switch.runCmds( 1, ["show directflow flows"] )
    return response[0]['flows']

def eApiIntfDirectFlow():
    switch = Server(commandApiUrl)
    response = switch.runCmds( 1, ["show interfaces", "show directflow flows"] )
    return response

@route('/dfa/pause')
def dfapause():
    print "Pause pressed"
    pause_processing()

@route('/dfa/resume')
def dfaresume():
    print "Resume pressed"
    resume_processing()

@route('/dfa/delete')
def dfadelete():
    print "delete preseed"
    delete_directflow_entries()

def convert(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data


# -------------------
# Controls for DFA
# -------------------

DEMO_CTRL_UDP_PORT= 9515 


def pause_processing():            # stop processing new syslog messages
   send_datagram('DFA_CMD_PAUSE')

def resume_processing():           # resume processing new syslog messages
   send_datagram('DFA_CMD_RESUME')

def delete_directflow_entries():   # delete existing DROP and BYPASS flow entries
   send_datagram('DFA_CMD_DELETE_FLOWS')

def send_datagram( msg ):
   udp_socket= socket.socket( socket.AF_INET, 
                              socket.SOCK_DGRAM, 
                              socket.IPPROTO_UDP )
   print 'sending msg: %s to %s on UDP port %d' % ( msg, DEMO_SWITCH_IP, 
                                                    DEMO_CTRL_UDP_PORT )
   udp_socket.sendto( msg, (DEMO_SWITCH_IP, DEMO_CTRL_UDP_PORT) )
   udp_socket.close()


run(host='172.22.28.143', port=8090)
