import geocoder
g = geocoder.ip('me')
print(type(g.latlng))