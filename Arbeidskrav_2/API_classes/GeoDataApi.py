from Arbeidskrav_2.API_classes.BaseApi import BaseApi
from Arbeidskrav_2.Models.GeoData import GeoData
class GeoDataApi(BaseApi):
    def __init__(self, url, params):
        super().__init__(url, params)

    def getresult(self) -> GeoData:
            data:list[GeoData] = self.getresults()
            if len(data) > 0:
                return data[0]
            raise FileNotFoundError("No GeoData found")

    def getresults(self) ->list[GeoData]:
        data:list[GeoData] = []
        parser = self.getrequest()
        return [GeoData(p) for p in parser]

        
