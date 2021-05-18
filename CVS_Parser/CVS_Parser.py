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
