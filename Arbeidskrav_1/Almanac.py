from datetime import datetime
import keyring
import requests
import json
from typing import Any

#Saving api-key to openweathermap as apikey, raises systemexit if it cant retrieve the api key
apikey:str = str(keyring.get_password("openweathermap", "api-key"))
if apikey == 'None':
    raise SystemExit("Failed to retrieve API Key from Python Keyring")



#saving api base url as string variables
sunset_sunrise_api:str = "https://api.sunrise-sunset.org/v2"
openweathermap_api:str = "https://api.openweathermap.org/geo/1.0/direct"
#limit number of locations in the api response. Used in function get_cityinfo()
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
#Function to retrieve information about a city. Used to retrieve coordinates for sunrise-sunset API.
def get_cityinfo(city:str) -> dict:
    args:dict = {
            "q": city,
            "limit" : limit, 
            "appid": apikey
            }
    information:dict = getrequest(openweathermap_api, args)
    if not information:
        raise SystemError(f"{city}: was not found")
    #OpenWeathermap returns a list of cities, even though we set limit=1 the output will be a list with where we need to pull out the first dict.
    return information[0]
#----
#Function to retrieve sun, and moon information from the sunrise-sunrise api. Using latitude and longituded from openweathermap api. Using the API default of showing todays information.
def sun_today(lat:float, lon:float) -> dict:
    args:dict = {
        "lat": lat,
        "lng": lon}
    return getrequest(sunset_sunrise_api, args)
#-----

#Saving user input as city and countrycode (q paramater used in get_cityinfo())
location_input:str = input('In which city do you want to see moon and sun information? Format:(City,Countrycode)\n')
#saving cityinformation into a place variable.
place:dict = get_cityinfo(location_input)
#Saving todays suninfo into a dict using latidude and longitude of the city.
suninformation:dict = sun_today(place["lat"], place["lon"])



moonphase:str = suninformation['moon_phase']
moonillumination:float = suninformation['moon_illumination']
sunrise = datetime.fromisoformat(suninformation['sunrise'])
sunset = datetime.fromisoformat(suninformation['sunset'])
print(f"Here is some information of {place['name']} as of {suninformation['date']}:\nMoonphase: {moonphase}\nMoonillumination: {moonillumination} %\nSunrise: {sunrise:%H:%M:%S}\nSunset: {sunset:%H:%M:%S}")

