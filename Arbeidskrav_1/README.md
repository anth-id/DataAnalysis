# Almanac
Python script that takes user input as a city and country code. Looks up the coordinates and uses them to retrieve moonphase, moon illumination, sunrise and sunset for the specifik city.

## How it works

1. Takes user input as *cityname, countrycode*.
2. OpenWeatheMap API gives us longitude and latitude of the city.
3. Sunrise-Sunset API returns sun and moon data for those coordinates.
4. The script prints the results.

## Requirements
* OpenweatherMap API Key (Free)
* The packages *requests* and *keyring* (in requirements.txt)

```python
pip install requests keyring
```
or
```
pip install -r requirements.txt
```

Vises som:
print("Hei, verden!")
Tabell
| Name | Age |
|------|-----|
| John | 30 |
| Jane | 25 |