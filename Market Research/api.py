from typing import Any
from pandas import json_normalize
import requests
import json
import pandas as pd


BASE_URL_BRREG_API = 'https://data.brreg.no/enhetsregisteret/api/underenheter'


def get_api(url:str, args:dict = {} ) -> Any:
    response = requests.get(url, args, timeout=10)
    if response.status_code == 200:
        data:str = response.text
        print(data)
        return json.loads(data)
    else:
        raise SystemError (f"Failed to retrieve data. Status code {response.status_code}")

Columns = [
    "beliggenhetsadresse.postnummer",
    "naeringskode1.kode", 
    "antallAnsatte", 
    "navn"
]


#Secure that the postalcode is 4 digits. If not raises ValueError and returns wrong input as quote.
def search_units(postalcode:str, businesscode:str) -> dict:
    if not (postalcode.isdigit()) and len(postalcode) == 4:
        raise ValueError (f"Postal code needs to be 4 digits, you wrote {postalcode!r}")

    args:dict = {
        "beliggenhetsadresse.postnummer": postalcode,
        "naeringskode" : businesscode,
        "size":1000

    }
    data =  get_api(BASE_URL_BRREG_API, args)
    units = data.get("_embedded", {}).get("underenheter", [])
    total_units = data.get("page", {}).get("totalElements", len(units))

    if total_units > len(units):
        print(f"{total_units} were found but only {len(units)} were shown.")

    return units

postalcode = input("Postalcode: ")
businesscode = input("Businesscode: ")

results_units = search_units(postalcode, businesscode)

df = pd.json_normalize(results_units)[Columns]
print(df)


