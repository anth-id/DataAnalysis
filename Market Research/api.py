from typing import Any
import requests
import json
import pandas as pd

#-------
#APIs used
#-------
#Documentation:
#https://data.brreg.no/enhetsregisteret/api/dokumentasjon/en/index.html
BASE_URL_BRREG_API = 'https://data.brreg.no/enhetsregisteret/api/underenheter'

#Documentation:
#https://ws.geonorge.no/adresser/v1/
BASE_URL_GEONORGE_API = 'https://ws.geonorge.no/adresser/v1/'

#-------
#Get API Function
#-------
def get_api(url:str, args:dict = {} ) -> Any:
    response = requests.get(url, args, timeout=10)
    if response.status_code == 200:
        data:str = response.text
        #print(data)
        return json.loads(data)
    else:
        raise SystemError (f"Failed to retrieve data. Status code {response.status_code}")

#-------
#Filters for BRREG API
#-------
Columns = [
    "beliggenhetsadresse.postnummer",
    "beliggenhetsadresse.adresse",
    #Business codes:
    # https://www.ssb.no/virksomheter-foretak-og-regnskap/_attachment/85512?_ts=13b2d1a6dc8
    "naeringskode1.kode", 
    "antallAnsatte", 
    "navn"
]

#-------
#Function to search units based on, takes parameters as postal code and businesscode(näringskode) and returns all units.
#-------
#Secure that the postalcode is 4 digits. If not raises ValueError and returns wrong input as quote.
def search_units(postalcode:str, businesscode:str) -> dict:
    if not (postalcode.isdigit() and len(postalcode) == 4):
        #"postalcode!r" will return the postalcode with " " this will show for example blankspaces. Maybe not needed further forward?
        raise ValueError (f"Postal code needs to be 4 digits, you wrote {postalcode!r}")

    args:dict = {
        "beliggenhetsadresse.postnummer": postalcode,
        "naeringskode" : businesscode,
        #use size to not cap to 20 returns.
        "size":1000

    }
    data =  get_api(BASE_URL_BRREG_API, args)
    units = data.get("_embedded", {}).get("underenheter", [])
    total_units = data.get("page", {}).get("totalElements", len(units))

    
    #Look more into this
    if total_units > len(units):
        print(f"{total_units} were found but only {len(units)} were shown.")

    return units


postalcode = input("Postalcode: ")
businesscode = input("Businesscode: ")

results_units = search_units(postalcode, businesscode)

#Exit program when search_units function returns an empty list.
if not results_units:
    print("No match was found.")
    raise SystemExit
#-------
#Geonorge API to retrieve lon and lat for the difference businesses.
#-------

def getcoordinates(adress:str, postalcode:str):
    #I will use adress from BRREG to retrieve lon and lat from geonorge
    # continue on this function to retrieve lon and lat
    args:dict = {
        "sok" : adress,
        "postnummer" : postalcode,
        "treffperside" : 1000, 

    }
    return get_api(BASE_URL_GEONORGE_API + "sok", args)




#Use columns only for me to show the most important thing for me. 
df = pd.json_normalize(results_units)[Columns]
print(df)


#Something is wrong here. I think i need to loop through everything and pull out each adress.
adresses = pd.json_normalize(df["beliggenhetsadresse.adresse"])
coordinates = getcoordinates(adresses, postalcode)

print(adresses)
