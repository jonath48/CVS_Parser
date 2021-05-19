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

# user_location = "(" + loc + ")"
# print(user_location)

# print(loc)

x = loc.split(",")

# print(x[0])
lat = x[0]
lng = x[1]
# print(type(lat))
lat_int = float(lat)
lng_int = float(lng)
userCoor = (lat_int, lng_int)
# print(userCoor)


CVS_results = gmaps.places_nearby(
    location=loc,
    radius=160934,
    open_now=False,
    name="CVS Pharmacy",
    type="pharmacy",
)

# print(CVS_results)

# place_json = CVS_results.json
# lat = place_json["lat"]
# lng = place_json["lng"]
# print(lat)
# print(lng)

num_result = 0

places = CVS_results["results"]
place_num = places[num_result]
# print(place_num)
geom = place_num["geometry"]
locate = geom["location"]
lat = locate["lat"]
lng = locate["lng"]
# print(lat)
# print(lng)

# print("Pick a store to get directions to:")

# store_num = "[{num_store}] "

# num = 0

# print(CVS_results)

# import numpy as np

# storeCoor = np.zeros(len(CVS_results["results"]))
# # storeCoor = np.zeros(0)
# storeNames = np.zeros(len(CVS_results["results"]))
import array

storeCoor = []
storeNames = []

listLength = len(CVS_results["results"])

for place in CVS_results["results"]:
    curr_place_id = place["place_id"]
    # curr_loc = place["geometry/location"]
    # for geom in place["geometry"]:
    #     for locate in geom["location"]:
    #         lat = locate["lat"]
    #         lng = locate["lng"]
    curr_store_name = place["name"]
    curr_store_vicinity = place["vicinity"]
    geoStore = place["geometry"]
    locationStore = geoStore["location"]
    latStore = locationStore["lat"]
    lngStore = locationStore["lng"]
    # storeCoor = (latStore, lngStore)
    # print(locationStore)
    storeCoordinates = "(" + str(latStore) + "," + str(lngStore) + ")"
    # print(storeCoordinates)
    stoCoor = (latStore, lngStore)
    # print(stoCoor)
    storeCoor.append(stoCoor)
    # print(stoCoor)
    # curr_store_number = place["phone_number"]
    # print(curr_store_number)
    storesStr = curr_store_name + "--" + curr_store_vicinity
    storeNames.append(storesStr)
    # print(storesStr)
    # print(curr_store_name + " " + curr_store_vicinity)
    # print(curr_store_vicinity)
    curr_fields = ["name", "formatted_phone_number", "type", "geometry/location"]
    place_details = gmaps.place(
        place_id=curr_place_id,
        fields=curr_fields,
    )
    # index += 1
    # print(curr_place_id)
    # print(place_details)
    # store_num = "[{num_store:.0f}] " + str(place_details)
    # print(store_num.format(num_store=num))
    # num += 1

# for stores in storeCoor:
#     print(stores)

print("Pick a store to get directions to: ")

for index in range(0, listLength):
    print(str(index) + ": " + storeNames[index])


selection = input()

dirLocation = storeCoor[int(selection)]

destLocation = gmaps.reverse_geocode(dirLocation)

from datetime import datetime, timedelta

results = gmaps.directions(
    user_location[0]["formatted_address"],
    destLocation[0]["formatted_address"],
    arrival_time=datetime.now() + timedelta(minutes=0.5),
)

locations = [
    user_location[0]["formatted_address"],
    destLocation[0]["formatted_address"],
]

markers = [
    "color:blue|size:mid|label:" + chr(65 + i) + "|" + r
    for i, r in enumerate(locations)
]

result_map = gmaps.static_map(
    center=destLocation[0]["formatted_address"],
    scale=5,
    zoom=1,
    size=[1200, 1200],
    format="jpg",
    maptype="roadmap",
    markers=markers,
    path="color:0x0000ff|weight:2|" + "|".join(locations),
)

marker_points = []
waypoints = []

# extract the location points from the previous directions function

for leg in results[0]["legs"]:
    leg_start_loc = leg["start_location"]
    marker_points.append(f'{leg_start_loc["lat"]},{leg_start_loc["lng"]}')
    for step in leg["steps"]:
        end_loc = step["end_location"]
        waypoints.append(f'{end_loc["lat"]},{end_loc["lng"]}')
last_stop = results[0]["legs"][-1]["end_location"]
marker_points.append(f'{last_stop["lat"]},{last_stop["lng"]}')

markers = [
    "color:blue|size:mid|label:" + chr(65 + i) + "|" + r
    for i, r in enumerate(marker_points)
]
result_map = gmaps.static_map(
    center=waypoints[0],
    scale=2,
    zoom=13,
    size=[640, 640],
    format="jpg",
    maptype="roadmap",
    markers=markers,
    path="color:0x0000ff|weight:2|" + "|".join(waypoints),
)

with open("driving_route_map.jpg", "wb") as img:
    for chunk in result_map:
        img.write(chunk)

# import gmaps

# gmaps.figure(center=userCoor, zoom_level=12, map_type="TERRAIN")
# fig = gmaps.figure()
# # print(userCoor)
# # print(dirLocation)
# layer = gmaps.directions.Directions(userCoor, dirLocation)
# fig.add_layer(layer)

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
