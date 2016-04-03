#-*- coding: utf8 -*-
__author__ = 'usr'
import socket
import socks
import datetime
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 1080)
socket.socket = socks.socksocket
api_key='AIzaSyAZvxdvjusRu-hTXKoR7MdIoe6lyWwF0kw'
import googlemaps
gmaps = googlemaps.Client(key='AIzaSyAZvxdvjusRu-hTXKoR7MdIoe6lyWwF0kw')
a="湖北省武汉市硚口区"

geocode_result = gmaps.geocode(a)
print geocode_result
for i in geocode_result[0]:
    print i,geocode_result[0][i]
a= geocode_result[0]['geometry']['location']
print a['lat'],a['lng']
# reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))
# address = 'Constitution Ave NW & 10th St NW, Washington, DC'
# lat, lng = gmaps.

# now = datetime.now()
now = datetime.datetime.now()
# directions_result = gmaps.directions("Sydney Town Hall",
#                                      "Parramatta, NSW",
#                                      mode="transit",
#                                      departure_time=now)
