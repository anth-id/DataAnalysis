class GeoData:
    def __init__(self, rec:dict):
        self.city:str = rec['name']
        self.lat:float= rec['lat']
        self.lon:float = rec['lon']

    def __str__(self) -> str:
        return f"City: {self.city}\nLat: {self.lat}\nLon: {self.lon}"
