from typing import Any
import requests
import json
import pandas as pd


BASE_URL_BRREG_API = 'https://data.brreg.no/enhetsregisteret/api/underenheter'


def get_api(url, args:dict = {}) -> Any:
    response = requests.get(url, args, timeout=10)
    if response.status_code == 200:
        data:str = response.text
        print(data)
        return json.loads(data)
    else:
        raise SystemError (f"Failed to retrieve data. Status code {response.status_code}")

Columns = [
    "beligenhetsadresse.postnummer",
    "naeringskode"
]





data = get_api(BASE_URL_BRREG_API, {"beliggenhetsadresse.postnummer":"0253","naeringskode": "47"})
df = pd.json_normalize(data["_embedded"]["underenheter"])[["antallAnsatte", "navn", "beliggenhetsadresse.postnummer"]]   
print(df)