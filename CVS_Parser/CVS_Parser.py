from os import name
import googlemaps
from datetime import datetime

# from GoogleMapsAPIKey import get_my_key

# API_KEY = get_my_key()
API_KEY = "key"

gmaps = googlemaps.Client(key=API_KEY)

import requests
from requests import get

# ip = get("https://api.ipify.org").text
# print("My public IP address is: {}".format(ip))
# print(type(ip))

url = "https://ipinfo.io/json"
r = requests.get(url)
js = r.json()
city = js["city"]
region = js["region"]
country = js["country"]
loc = js["loc"]
org = js["org"]
postal = js["postal"]
timezone = js["timezone"]
readme = js["readme"]
# js.items()
# print(city)

user_location = gmaps.reverse_geocode(loc)

CVS_results = gmaps.places_nearby(
    location=loc,
    radius=160934,
    open_now=False,
    name="CVS Pharmacy",
    type="pharmacy",
)

# print(CVS_results)

CVS_results = gmaps.places_nearby(page_token=CVS_results)

# Geocoding an address
# geocode_result = gmaps.geocode("1600 Amphitheatre Parkway, Mountain View, CA")

# Look up an address with reverse geocoding
# reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# Request directions via public transit
# now = datetime.now()
# directions_result = gmaps.directions(
#     "Sydney Town Hall", "Parramatta, NSW", mode="transit", departure_time=now
# )
