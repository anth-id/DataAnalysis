from typing import final

import keyring
import psycopg2
import pandas as pd
from API_classes.SolarDataApi import SolarDataApi
from API_classes.GeoDataApi import GeoDataApi
from Models.GeoData import GeoData
from Models.SolarData import SolarData
import matplotlib.pyplot as plt
from postgreSQL.SolarDataDB import SolarDataDb

#Saving api-key to openweathermap as apikey, raises systemexit if it cant retrieve the api key
apikey:str = str(keyring.get_password("openweathermap", "api-key"))
if apikey == 'None':
    raise SystemExit("Failed to retrieve API Key from Python Keyring")


#saving api base url as string variables
sunset_sunrise_api:str = "https://api.sunrise-sunset.org/v2"
openweathermap_api:str = "https://api.openweathermap.org/geo/1.0/direct"



#Saving user input as city and countrycode (q paramater used in get_cityinfo())
location_input:str = input('Enter your cities, separated with commas.\n')
cities = [l.strip() for l in location_input.split(",")]
dfs:list[pd.DataFrame] = []
# startday_input:str = input('Enter your start date\n')
# endday_input:str = input('Enter your end date\n')
cred = keyring.get_credential("PostgreSQL", "postgres")
if cred is None:
    raise SystemExit("Failed to retreieve database credentials.")
db:SolarDataDb = SolarDataDb(f"host=localhost dbname=dataanalytiker_FSV user={cred.username} password={cred.password}")
try:
    for city in cities:
        geo_params:dict = {
                    "q": city,
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
            print(f"Trying to retrieve information for {city}.")

            city_id:int = db.getcity(gdata[0])
            for day in sdata:
                db.insert(city_id,day)
            print(f"Information {city} inserted into the database.")

        except Exception as e :
            raise SystemExit(f"An error has occured for {city} ({e})")

        #Sorting on date
        days:list[SolarData] = sorted(sdata, key=lambda SolarData: SolarData.date)

        df = pd.DataFrame(d.__dict__ for d in days)
        df["city"] = city
        dfs.append(df)
finally:
    db.close()


    dfcombined = pd.concat(dfs, ignore_index=True)
plot_data = dfcombined.pivot(
    columns="city",
    index="date",
    values="solar_noon_altitude"
)

plot_data.plot.line(title="Solar Altidude", xlabel = "Date", ylabel="Azimuth")
plt.xlabel("Date")
plt.ylabel("Degrees over horizon")
plt.show()


dfcombined = pd.concat(dfs, ignore_index=True)
plot_data = dfcombined.pivot(
    columns="city",
    index="date",
    values="daylen_hours"
)

plot_data.plot.line(title="Day length")
plt.xlabel("Date")
plt.ylabel("Day length")
plt.show()
