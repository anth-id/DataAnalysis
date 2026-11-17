from Models.SolarData import SolarData
from API_classes.BaseApi import BaseApi

class SolarDataApi(BaseApi):
    def __init__(self, url, params):
        super().__init__(url,params)


    def getresults(self) -> list[SolarData]:
        data:list[SolarData] = []
        records = self.getrequest()
        for rec in records['days']:
            data.append(SolarData(rec))
        return data