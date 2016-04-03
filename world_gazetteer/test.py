#__author__ = 'Administrator'
# -*- coding: utf-8 -*-

import socket
import socks

import goslate

socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 1080)
socket.socket = socks.socksocket


# print a.strip('`')
# a=unicode('·','utf-8')
# a=u'`‘“结果`‘“'
# print(a)
# a=a.encode('gb2312')
# # a=a.encode('utf-8')
# print(a.__class__)
# print(a)
# a = a.strip('`‘“')
# print('\x9e')
# b=a.decode('gb2312')
# print(b)
# print(b.__class__)
# print(a.__class__)
# print(unicode(a,'utf-8'))
# print
# gs = goslate.Goslate()
# a= gs.lookup_dictionary('ABDESMAYA', 'zh-CN')
# print(a)

gs = goslate.Goslate()
print gs.lookup_dictionary('hello world', 'zh-CN')
# print gs.translate('hellpw world','zh-CN')

