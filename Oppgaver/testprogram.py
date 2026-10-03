import requests
import pandas as pd

url = "https://data.brreg.no/enhetsregisteret/api/underenheter"

fields = requests.get(url, params={"size":20})
data = fields.json()


posts = data.get("_embedded", {}).get("underenheter", [])

for post in posts:
    name = post["navn"]
    orgnr = post["organisasjonsnummer"]
    kommun = post.get("beliggenhetsadresse", {}).get("kommunenummer")
    areacode = post.get("naeringskode1", {}).get("kode")
    print(name, areacode)

