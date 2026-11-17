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
SUNSET_SUNRISE_URL:str = "https://api.sunrise-sunset.org/v2"
OPENWEATHERMAP_URL:str = "https://api.openweathermap.org/geo/1.0/direct"



'''
1. Saving user input as city. (City is used as q parameter in geo_params dict)
2. Using list comprehension to first split userinput into separate strings and then strip blankspaces. Saving each city into cities list.
3. Creating a dataframe list used to save each city df into one.
'''
location_input:str = input('Enter your city/cities, separated with commas.\n')
cities = [l.strip() for l in location_input.split(",")]
dfs:list[pd.DataFrame] = []

'''
1. Creating a credentials variable (cred) for setting up postgreSQL connection.
2. If failed to retrieve credentials, then raise SystemExit.
3. Creating a SolarDataDB object that connects to the database. 

'''
cred = keyring.get_credential("PostgreSQL", "postgres")
if cred is None:
    raise SystemExit("Failed to retreieve database credentials.")
db:SolarDataDb = SolarDataDb(f"host=localhost dbname=dataanalytiker_FSV user={cred.username} password={cred.password}")

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
                "date_start": '2026-01-01',
                "date_end": '2026-12-31'
                }
            solarApi:SolarDataApi = SolarDataApi(SUNSET_SUNRISE_URL,solar_params)
            sdata:list[SolarData] = solarApi.getresults()
            print(f"Trying to retrieve information for {city}.")

            city_id:int = db.getcity(gdata[0])
            for day in sdata:
                db.insert(city_id,day)
            print(f"Information {city} inserted into the database. \n")
            

        except Exception as e :
            raise SystemExit(f"An error has occured for {city} ({e})")

        #Sorting on Solar altiude (maximum angle of the sun above the horizon)
        data:list[SolarData] = sorted(sdata, key=lambda SolarData: SolarData.solar_noon_altitude, reverse=True)
        solar_noon_sorted = data[0]
        print(f"In {city} the date with where the sun is at its maximum angle above the horizon is {solar_noon_sorted.date} ")
        #Sorting on date, creating a dataframe, adding a city column and then appending to a list with dataframes.
        
        days:list[SolarData] = sorted(sdata, key=lambda SolarData: SolarData.date)
        df = pd.DataFrame(d.__dict__ for d in days)
        df["city"] = city
        dfs.append(df)


finally:
    db.close()



#Continue on a seperate file that makes the calculations. 
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



