#!/usr/bin/python

from bottle import route, run, template, request
from jsonrpclib import Server
import collections
import time
import socket
import json

username = "admin"  #"Fernando"
password = "admin"  #"password"
SWITCH = "172.28.169.125"
DEMO_SWITCH_IP= SWITCH
commandApiUrl = "http://{}:{}@{}/command-api".format(username, password, DEMO_SWITCH_IP)
new_user = "fernando"
new_passwd = "admin"

commandApiUrl.runCmds(1, ["enable", "configure terminal", + new_user, + new_passwd, "end" ])




