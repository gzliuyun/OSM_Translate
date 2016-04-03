__author__ = 'usr'

import socket
import urllib2
import re
true_socket = socket.socket

ipbind='60.207.237.21'
ip_to='http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013/'

def bound_socket(*a, **k):
    sock = true_socket(*a, **k)
    sock.bind((ipbind, 0))
    return sock

socket.socket = bound_socket

response = urllib2.urlopen(ip_to)
html = response.read()
ip=re.search(r'code.(.*?)..code',html)
print ip.group(1)