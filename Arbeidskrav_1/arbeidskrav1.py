from datetime import date, datetime
from re import S
from typing import Any

import keyring
import requests
import json

#API keyring
apikey:str = str(keyring.get_password("openweathermap", "api-key"))



sunset_sunrise_api:str = "https://api.sunrise-sunset.org/v2"
openweathermap_api:str = "http://api.openweathermap.org/geo/1.0/direct"
limit:int = 1

#q par cityn name, statecode (US) and countrycode divided by comma
cities:list [str] = ["Kongsberg,NO", "Gothenburg,SE", "Madrid,ES"] 
def getrequest(url:str, args:dict = {}) -> Any:
    #requests.get(url, args) bygger vår url. "url"?q=Gothenburg,SE&limit=1 och sparar GET requesten i en variabel.
    response = requests.get(url, args)
    if response.status_code == 200:
        #sparar JSON som kommer tillbaka som en sträng i en variabel som heter data
        data:str = response.text
        # returnerar och konverterar långa json strängen till en python dict. Detta gör så att vi kan parsea
        return json.loads(data)
    else:
        raise SystemError (f"Failed to retrieve data. Status code {response.status_code}")
#----------
# can use timedelta function here instead.,
def formattime(secs:int) -> str:
    # // floor division and returns integer instead of float
    # % whats left of x. Takes whats left of 3600 and divides by 60.
    hours = secs // 3600
    minutes = (secs % 3600) // 60
    seconds:int = secs % 60
    return f"{sunrise.date()} : {hours}:{minutes}:{seconds}"

def get_coordinates(city:str) -> dict:
    args:dict = {
            "q": city,
            "limit" : limit, 
            "appid": apikey
            }
    parser = getrequest(openweathermap_api, args)
    if not parser:
        raise SystemError(f"{city}: was not found")
    return parser[0]
#-----
#set standard parameter "today" since the API documentations says this.
def sun_up_down(lat:float, lon:float, date:str = "today") -> dict:
    args:dict = {
        "lat": lat,
        "lng": lon,
        "date": date}
    return getrequest(sunset_sunrise_api, args)


place =  get_coordinates('Oslo,NO')
sun = sun_up_down(place["lat"], place["lon"])

#Lagrar formatteringen av datetime från API callet. 
sunrise = datetime.fromisoformat(sun["sunrise"])
sunset = datetime.fromisoformat(sun["sunset"])


#Formatterar till H=Hours, M=Minutes, S=Seconds
print(f"In {place['name']} the sun goes up: {sunrise:%H:%M:%S}, and down: {sunset:%H:%M:%S}")

       








