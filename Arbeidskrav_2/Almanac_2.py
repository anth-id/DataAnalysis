import keyring
import pandas as pd
from API_classes.SolarDataApi import SolarDataApi
from API_classes.GeoDataApi import GeoDataApi
from Calculations.SunCalc import SunCalc
from Models.GeoData import GeoData
from Models.SolarData import SolarData
import matplotlib.pyplot as plt
from postgreSQL.SolarDataDB import SolarDataDb
import os 
from dotenv import load_dotenv


#Saving api-key to openweathermap as apikey, raises systemexit if it cant retrieve the api key
apikey:str = str(keyring.get_password("openweathermap", "api-key"))
if apikey == 'None':
    raise SystemExit("Failed to retrieve API Key from Python Keyring")

#saving api base url as string variables
SUNSET_SUNRISE_URL:str = "https://api.sunrise-sunset.org/v2"
OPENWEATHERMAP_URL:str = "https://api.openweathermap.org/geo/1.0/direct"
START_DATE:str = "2026-01-01"
END_DATE:str = "2026-12-31"


'''
1. Saving user input as city. (City is used as q parameter in geo_params dict)
2. Using list comprehension to first split userinput into separate strings and then strip blankspaces. Saving each city into cities list.
3. Creating a dataframe list used to save each city df into one.
'''
location_input:str = input('Enter your city/cities, separated with commas.\n')
cities:list = [l.strip() for l in location_input.split(",")]
dfs:list[pd.DataFrame] = []

'''
1. Creating user, dbname and host variables to be able to configure .env file for the specific users database.
2. Creating a credentials variable (cred) for setting up postgreSQL connection.
3. If failed to retrieve credentials, then raise SystemExit.
4. Creating a SolarDataDB object that connects to the database. 

'''
load_dotenv()
user:str | None = os.getenv("PG_USER")
if user is None:
    raise SystemExit("No configured PG_USER in .env")

dbname: str | None = os.getenv("PG_DATABASE")
if dbname is None:
    raise SystemExit("No configured DB_NAME in .env")

host: str | None = os.getenv("PG_HOST")
if host is None:
    raise SystemExit("No configured PG_HOST in .env")


cred = keyring.get_credential("PostgreSQL", user)
if cred is None:
    raise SystemExit("Failed to retreieve database password.")
db:SolarDataDb = SolarDataDb(f"host={host} dbname={dbname} user={cred.username} password={cred.password}")

'''
1. Looping trough each city in cities list and assigns city to q parameter and uses api-key as app-id.
2. Creating a GeoDataApi object as geoApi with openweathermap api url and geo_params.
3. Creating a list called gdata which calls GeoDataApi getresults method to retreive and save GeoData from the api call (cityname, longitude and latitude).
4. Catch error if there is no records in gdata list. Then continues with the other cities.

'''
try:
    for city in cities:
        
        geo_params:dict = {
                    "q": city,
                    "limit" : 1, 
                    "appid": apikey
                    }
        geoApi:GeoDataApi = GeoDataApi(OPENWEATHERMAP_URL, geo_params)
        gdata:list[GeoData] = geoApi.getresults()
        if not gdata:
            print(f"{city} was not found.")
            continue
        
        '''
        1. Creating a SolarDataApi object as solarApi with sunset sunrise api url and solar_params. Using parameters from geodata.
        2. Creating a list called sdata which calls SolarDataApi get results method to retrieve and save SolarData from the api call. 
        3. Inserts the city, lon and lat into city table, db.getcity wil then return the city_id from the corresponding id in city table. 
        4. Inserts every record from sdata with the corresponding city_id from city table.
        
        '''

        try: 
            solar_params:dict = {
                "lat": gdata[0].lat,
                "lng": gdata[0].lon,
                "date_start": START_DATE,
                "date_end": END_DATE
                }
            solarApi:SolarDataApi = SolarDataApi(SUNSET_SUNRISE_URL,solar_params)
            sdata:list[SolarData] = solarApi.getresults()
            print(f"Trying to retrieve information for {city}.")

            city_id:int = db.getcity(gdata[0])
            for day in sdata:
                db.insert(city_id,day)
            print(f"Solar information was inserted into the database for: {city}\n")
            

        except Exception as e :
            raise SystemExit(f"An error has occured for {city} ({e})")
        
        retrievedata:pd.DataFrame = db.retrieve(cities)
  
finally:
    db.close()


calculations:SunCalc = SunCalc(retrievedata)
avg_monthly_sun:pd.DataFrame = calculations.avg_daylength_p_month()


avg_monthly_sun.plot.line(title="Average daylength per month", xlabel = "Month", ylabel= "Hours of daylight")
plt.xlabel("Month")
plt.ylabel("Hours of daylight")
plt.show()




