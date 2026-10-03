from datetime import datetime
import keyring
import requests
import json
from typing import Any

#Saving api-key to openweathermap as apikey, raises systemexit if it cant retrieve the api key
apikey:str = str(keyring.get_password("openweathermap", "api-key"))
if apikey is None:
    raise SystemExit("Failed to retrieve API Key from Python Keyring")



#saving api base url as string variables
sunset_sunrise_api:str = "https://api.sunrise-sunset.org/v2"
openweathermap_api:str = "http://api.openweathermap.org/geo/1.0/direct"
#limit number of locations in the api response. Used in function getcoordinates()
limit:int = 1

#Creating a function to call api and save to a python readable JSON file. Since this is a general function to call the API. We set the return type annotation to Any.
def getrequest(url:str, args:dict = {}) -> Any:
    response = requests.get(url, args)
    if response.status_code == 200:
        data:str = response.text
        return json.loads(data)
    else:
        raise SystemError (f"Failed to retrieve data. Status code {response.status_code}")
#----------
def get_cityinfo(city:str) -> dict:
    args:dict = {
            "q": city,
            "limit" : limit, 
            "appid": apikey
            }
    parser:dict = getrequest(openweathermap_api, args)
    if not parser:
        raise SystemError(f"{city}: was not found")
    return parser[0]
#----
def sun_today(lat:float, lon:float) -> dict:
    args:dict = {
        "lat": lat,
        "lng": lon}
    return getrequest(sunset_sunrise_api, args)
#-----

location_input:str = input('Where do you want to see the weather? Format:(City,Countrycode)\n')

place:dict = get_cityinfo(location_input)
today = sun_today(place["lat"], place["lon"])



moonphase:str = today['moon_phase']
moonillumination:float = today['moon_illumination']
sunrise = datetime.fromisoformat(today['sunrise'])
sunset = datetime.fromisoformat(today['sunset'])
print(f"Here is some information of {place['name']} as of {today['date']}:\nMoonphase: {moonphase}\nMoonillumination: {moonillumination} %\nSunrise: {sunrise:%H:%M:%S}\nSunset: {sunset:%H:%M:%S}")

