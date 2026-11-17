from API_classes.BaseApi import BaseApi
from Models.GeoData import GeoData
class GeoDataApi(BaseApi):
    def __init__(self, url:str, params:dict):
        super().__init__(url, params)


    def getresults(self) ->list[GeoData]:
        
        data:list[GeoData] = []
        records = self.getrequest()
        for rec in records:
             data.append(GeoData(rec))
        return data

        
