# Almanac
Python script that takes user input as a city and country code. Looks up the coordinates and uses them to retrieve moonphase, moon illumination, sunrise and sunset for the specific city at todays date.

## How it works

1. Takes user input as *cityname, countrycode*.
2. OpenWeatherMap API gives us longitude and latitude of the city. (Needs an account)
3. Sunrise-Sunset API returns sun and moon data for those coordinates. (Doesnt need an account or API key, but has usage limits )
4. The script prints the results.

## Requirements
* Python
* OpenweatherMap API Key (Free)
* The packages *requests* and *keyring* (in requirements.txt)

```bash 
pip install requests keyring
```
or
``` bash
pip install -r requirements.txt
```
## How to set it up
1. Get your API key from [OpenWeatherMap](https://openweathermap.org/api)
2. Store your API Key with Python Keyring with the following command. Then paste your key in the terminal.
```
keyring set openweathermap api-key
```
## How to run 
Create a new folder and clone the repository in there. Then enter the folder arbeidskrav_1.

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
python Almanac.py
```

## Usage
When starting the program it will ask for input:
```text
In which city do you want to see moon and sun information? Format:(City,Countrycode)
```
User input:
```
Oslo, NO
```

Example output:
```text
Here is some information of Oslo as of 2026-10-04:
Moonphase: Waxing Gibbous
Moonillumination: 78.4 %
Sunrise: 07:41:12
Sunset: 18:02:37
```

