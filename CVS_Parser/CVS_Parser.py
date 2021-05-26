import googlemaps
import argparse
import requests
import array
from os import name
from datetime import datetime
from requests import get

key_parser = argparse.ArgumentParser(
    description="Finds the nearest CVS and gives you directions to it. Requires a Google API key."
)
key_parser.add_argument("API_key", help="Enter Google API Key here.")
key_parser.add_argument("-r", "--range", type=int, default=100, help="The range in miles in which to parser for CVS (default: 100 miles)")
args = key_parser.parse_args()

API_KEY = args.API_key
CVS_RANGE = args.range
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
x = loc.split(",")
lat = x[0]
lng = x[1]
lat_int = float(lat)
lng_int = float(lng)
userCoor = (lat_int, lng_int)


CVS_results = gmaps.places_nearby(
    location=loc,
    radius=1609.34 * CVS_RANGE,
    open_now=False,
    name="CVS Pharmacy",
    type="pharmacy",
)

num_result = 0

places = CVS_results["results"]
place_num = places[num_result]
geom = place_num["geometry"]
locate = geom["location"]
lat = locate["lat"]
lng = locate["lng"]

storeCoor = []
storeNames = []

listLength = len(CVS_results["results"])

for place in CVS_results["results"]:
    curr_place_id = place["place_id"]
    curr_store_name = place["name"]
    curr_store_vicinity = place["vicinity"]
    geoStore = place["geometry"]
    locationStore = geoStore["location"]
    latStore = locationStore["lat"]
    lngStore = locationStore["lng"]
    storeCoordinates = "(" + str(latStore) + "," + str(lngStore) + ")"
    stoCoor = (latStore, lngStore)
    storeCoor.append(stoCoor)
    storesStr = curr_store_name + "--" + curr_store_vicinity
    storeNames.append(storesStr)
    curr_fields = ["name", "formatted_phone_number", "type", "geometry/location"]
    place_details = gmaps.place(
        place_id=curr_place_id,
        fields=curr_fields,
    )

print("Pick a store to get directions to: ")

for index in range(0, listLength):
    print(str(index) + ": " + storeNames[index])


selection = input()

dirLocation = storeCoor[int(selection)]

destLocation = gmaps.reverse_geocode(dirLocation)

# from codefurther.directions import GetDirections


# direct = GetDirections(
#     user_location[0]["formatted_address"],
#     destLocation[0]["formatted_address"],
#     mode="walking",
# )
# direct.footer

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
    center=markers[0],  # waypoints[0],
    scale=10,
    zoom=10,
    size=[1280, 1280],
    format="jpg",
    maptype="roadmap",
    markers=markers,
    path="color:0x0000ff|weight:2|" + "|".join(waypoints),
)

with open("driving_route_map.jpg", "wb") as img:
    for chunk in result_map:
        img.write(chunk)
