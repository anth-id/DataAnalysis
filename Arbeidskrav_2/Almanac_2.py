import keyring
from Arbeidskrav_2.API_classes.SolarDataApi import SolarDataApi
from Arbeidskrav_2.API_classes.GeoDataApi import GeoDataApi
from Arbeidskrav_2.Models.GeoData import GeoData
from Arbeidskrav_2.Models.SolarData import SolarData


#Saving api-key to openweathermap as apikey, raises systemexit if it cant retrieve the api key
apikey:str = str(keyring.get_password("openweathermap", "api-key"))
if apikey == 'None':
    raise SystemExit("Failed to retrieve API Key from Python Keyring")


#saving api base url as string variables
sunset_sunrise_api:str = "https://api.sunrise-sunset.org/v2"
openweathermap_api:str = "https://api.openweathermap.org/geo/1.0/direct"

#Saving user input as city and countrycode (q paramater used in get_cityinfo())
location_input:str = input('In which city do you want to see moon and sun information?\n')
startday_input:str = input('Enter your start date\n')
endday_input:str = input('Enter your end date\n')

geo_params:dict = {
            "q": location_input,
            "limit" : 1, 
            "appid": apikey
            }
geoApi:GeoDataApi = GeoDataApi(openweathermap_api, geo_params)
gdata:list[GeoData] = geoApi.getresults()


solar_params = {
    "lat": gdata[0].lat,
    "lng": gdata[0].lon,
    "date_start": startday_input,
    "date_end": endday_input
    }
solarApi:SolarDataApi = SolarDataApi(sunset_sunrise_api,solar_params)
wdata = solarApi.getresults()


for g in gdata:
    print(g)

for w in wdata:
    print(w)



