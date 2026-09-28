from datetime import datetime
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
def formattime(secs:int) -> str:
    # // floor division and returns integer instead of float
    # % whats left of x. Takes whats left of 3600 and divides by 60.
    hours = secs // 3600
    minutes = (secs % 3600) // 60
    seconds:int = secs % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

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
def sun_range(lat:float, lon:float, start:str, end:str) -> dict:
    args:dict = {
        "lat": lat,
        "lng": lon,
        "date_start": start,
        "date_end":end}
    return getrequest(sunset_sunrise_api, args)["days"]

place =  get_coordinates('Oslo,NO')
days = sun_range(place["lat"], place["lon"], "2026-09-01", "2026-09-30")
#Lagrar formatteringen av datetime från API callet. 
firstday = days[0]
lastday = days[-1]

# sunrise:datetime = datetime.fromisoformat(days["sunrise"])
# sunset:datetime = datetime.fromisoformat(days["sunset"])

#Formatterar till H=Hours, M=Minutes, S=Seconds
print(f"{firstday['date']} has a day length of {formattime(firstday['day_length'])} hours")
print(f"{lastday['date']} has a day length of {formattime(lastday['day_length'])} hours")
print(f"The differences is: {formattime(firstday['day_length']- lastday['day_length'])} hours")








