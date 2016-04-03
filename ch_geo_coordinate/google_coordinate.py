#-*- coding: utf8 -*-
import urllib
import json
import socket
import socks
googleGeocodeUrl = 'http://maps.googleapis.com/maps/api/geocode/json?'

def get_coordinates(query, from_sensor=False):
    if isinstance(query,unicode):
        query=query.encode("utf-8")
    # query = query.encode('utf-8')
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 1080)
    socket.socket = socks.socksocket
    params = {
        'address': query,
        'sensor': "true" if from_sensor else "false"
    }
    url = googleGeocodeUrl + urllib.urlencode(params)
    count_number=5
    while count_number:
        try:
            json_response = urllib.urlopen(url)
            response = json.loads(json_response.read())
            count_number=0
        except:
            count_number-=1
    if response['results']:
        location = response['results'][0]['geometry']['location']
        latitude, longitude = location['lat'], location['lng']
        print query, latitude, longitude
    else:
        latitude, longitude = None, None
        print query, "<no results>"
    return latitude, longitude

if __name__ == '__main__':

    a=u'39.159267'
    print(a.__class__)
    b=str(a)
    sql="select * from a=%s where" % 'baba'
    print(sql)
    print(unicode(b,'utf-8'),b.__class__)
    print(float(unicode(b,'utf-8')))
    print get_coordinates(a)[0].__class__
    a="三沙"
    print get_coordinates(a)

