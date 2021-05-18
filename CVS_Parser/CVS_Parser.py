import googlemaps
import argparse
import requests
from os import name
from datetime import datetime
from requests import get

key_parser = argparse.ArgumentParser(
    description="Finds the nearest CVS and gives you directions to it. Requires a Google API key."
)
key_parser.add_argument("API_key", help="Enter Google API Key here.")
args = key_parser.parse_args()

API_KEY = args.API_key
gmaps = googlemaps.Client(key=API_KEY)

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

user_location = gmaps.reverse_geocode(loc)

CVS_results = gmaps.places_nearby(
    location=loc,
    radius=160934,
    open_now=False,
    name="CVS Pharmacy",
    type="pharmacy",
)
<<<<<<< HEAD
=======

# print(CVS_results)

# place_json = CVS_results.json
# lat = place_json["lat"]
# lng = place_json["lng"]
# print(lat)
# print(lng)

num_result = 0

places = CVS_results["results"]
place_num = places[num_result]
print(place_num)
geom = place_num["geometry"]
locate = geom["location"]
lat = locate["lat"]
lng = locate["lng"]
print(lat)
print(lng)


for place in CVS_results["results"]:
    curr_place_id = place["place_id"]
    curr_loc = place["geometry"]
    # for geom in place["geometry"]:
    # for lat
    curr_fields = ["name", "formatted_phone_number", "type"]
    place_details = gmaps.place(place_id=curr_place_id, fields=curr_fields)
    print(curr_loc)
    print(place_details)

# print(CVS_results)

# import time

# time.sleep(5)

# CVS_results = gmaps.places_nearby(page_token=CVS_results["next_page_token"])

# Geocoding an address
# geocode_result = gmaps.geocode("1600 Amphitheatre Parkway, Mountain View, CA")

# Look up an address with reverse geocoding
# reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# Request directions via public transit
# now = datetime.now()
# directions_result = gmaps.directions(
#     "Sydney Town Hall", "Parramatta, NSW", mode="transit", departure_time=now
# )
>>>>>>> dbfea056c5574eb29f433b80fe0e98774ba8bc56
