##########################################################################
## ReverseGeoCoding.py v0.1
##
## Get the location details given a latitude and longitude
##
## Team Name: ANA
## Team Members : Anandh Varadarajan, Nithish Kolli, Abhiram Karri
##########################################################################

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="specify_your_app_name_here")
location = geolocator.reverse(51.588309,-0.070731)
print(location.raw)
print(location.address)
print((location.raw['address']['city']))