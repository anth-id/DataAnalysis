# Changes from Almanac_1

1. API Calls are moved to classes instead of functions in the main code. BaseApi is the parent class and GeoDataApi and SolarDataApi inherit the getrequest method. Also made two abstract methods in BaseApi so every child class needs a method to retrieve results.

2. API data is converted to objects in GeoData and SolarData. Since I only use getresults method every record is placed in a list regardless of one or multiple cities. 

3. Every record is saved into a PostgreSQL database. One table for GeoData and one table for SolarData. This is to make it easier to organize and do queries. Tried to use the normalization principles for relation databases. 

4. Made it possible to retrieve data for multiple cities with a loop.

5. Saves the solardata of every day in 2026 in a DF, and adding a city column into that. Then appending each df to a list of dataframes (dfs).

6. Using matplotlib to plot the dataframes together and shows the suns degrees over the horizons for every date in 2026.


# Almanac_2
Python script that takes user input as city/cities. Looks up the coordinates and uses them to retrieve moonphase, moon illumination, sunrise, sunset, sunrise azimuth, solar noon altitude, daylength in seconds and daylength in UTC format for the specific city at every date in a 2026.

The information retrieved is then loaded into DataFrames and made calculations on.

## How it works

1. Takes user input as *city name*.
2. OpenWeatherMap API gives us longitude and latitude of the city. (Needs an account)
3. Sunrise-Sunset API returns sun and moon data for those coordinates. (Doesnt need an account or API key, but has usage limits )


## Requirements



## How to set it up
1. Get your API key from [OpenWeatherMap](https://openweathermap.org/api)
2. Store your API Key with Python Keyring with the following command. Then paste your key in the terminal.
```
keyring set openweathermap api-key
```
3. Download PostgreSQL database and set it up. 
4. Set up your PostgreSQL database. Use keyring to store your PostgreSQL credentials. Then paste your password in the terminal.
```
keyring set PostgreSQL postgres
```

## How to run 
Create a new folder and clone the repository in there. Then enter the folder arbeidskrav_2.

```
git clone https://github.com/anth-id/DataAnalysis.git
```
Create and activate your virtual environment
```
python -m venv .venv
.venv\Scripts\activate
```

Install the packages and run the program
```
pip install -r requirements.txt
python Almanac_2.py
```

## Usage
When starting the program it will ask for input:
```text
Enter your city/cities, separated with commas.
```
User input:
```
Oslo, Madrid, Copenhagen


## Use of AI
I've used Brave AI search and claude to help me with syntaxes or make me understand concepts. 
Examples:

* How would you handle this if sunset, sunrise and daylen was None?

* How would you secure that my program never insert a new line into the database if there is already a city_id and date in it?
* Is it better to have cred = keyring in my main file or in the solardata class?