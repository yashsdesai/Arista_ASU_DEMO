#!/usr/bin/env python2.7
#
# Engineer:  Ben C. DeBolle, bdebolle@aristanetworks.com
# Copyright (c) 2014 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import socket
import time


DEMO_SWITCH_IP= 'bizdev-7050s.aristanetworks.com'    
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


def test():
   pause_processing()
   time.sleep(1)
   delete_directflow_entries()
   time.sleep(5)
   resume_processing()


if __name__ == '__main__':
   test()
