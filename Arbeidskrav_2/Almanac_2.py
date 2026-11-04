import keyring
import pandas as pd
from API_classes.SolarDataApi import SolarDataApi
from API_classes.GeoDataApi import GeoDataApi
from Models.GeoData import GeoData
from Models.SolarData import SolarData
import matplotlib.pyplot as plt


#Saving api-key to openweathermap as apikey, raises systemexit if it cant retrieve the api key
apikey:str = str(keyring.get_password("openweathermap", "api-key"))
if apikey == 'None':
    raise SystemExit("Failed to retrieve API Key from Python Keyring")


#saving api base url as string variables
sunset_sunrise_api:str = "https://api.sunrise-sunset.org/v2"
openweathermap_api:str = "https://api.openweathermap.org/geo/1.0/direct"

#Saving user input as city and countrycode (q paramater used in get_cityinfo())
location_input:str = input('In which city do you want to see moon and sun information?\n')
# startday_input:str = input('Enter your start date\n')
# endday_input:str = input('Enter your end date\n')

geo_params:dict = {
            "q": location_input,
            "limit" : 1, 
            "appid": apikey
            }
geoApi:GeoDataApi = GeoDataApi(openweathermap_api, geo_params)
gdata:list[GeoData] = geoApi.getresults()
try: 
    solar_params = {
        "lat": gdata[0].lat,
        "lng": gdata[0].lon,
        "date_start": '2026-01-01',#startday_input,
        "date_end": '2026-12-31'#endday_input
        }
    solarApi:SolarDataApi = SolarDataApi(sunset_sunrise_api,solar_params)
    sdata = solarApi.getresults()
except Exception:
    raise SystemExit("Are you sure that is a real city?")



for g in gdata:
    print(g)

# for s in sdata:
#     print(s)

days:list[SolarData] = sorted(sdata, key=lambda day: day.sunset)

df = pd.json_normalize(d.__dict__ for d in days)
df.plot.line(
    title="Solar Altitude",
    x="date",
    y="solar_noon_altitude"
)
plt.xlabel("Date")
plt.ylabel("Degrees over horizon")
plt.show()


