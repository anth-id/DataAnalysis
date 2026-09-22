from urllib import response

import keyring
import requests
import json

#API keyring
apikey:str = str(keyring.get_password("openweathermap", "api-key"))




base_url:str = "http://api.openweathermap.org/geo/1.0/direct"
limit:int = 1

#q par cityn name, statecode (US) and countrycode divided by comma
cities:list [str] = ["Kongsberg,NO", "Gothenburg,SE", "Madrid,ES"] 
def citylist(q):
    for city in cities:
        url:str = f"{base_url}?q={city}&limit={limit}&appid={apikey}"

        response = requests.get(url)
        if response.status_code !=200:
            print(f"failed to retrieve data. Status code {response.status_code}")
        else:
            data:str = response.text

        parser = json.loads(data)
        for rec in parser:
            rcity:str = rec['name']
            lat:str = rec['lat']
            lon:str = rec['lon']
            country:str = rec['country']
            print(f"[{rcity}, {country} coordinates: {lat},{lon}]")
          






citylist(cities)




