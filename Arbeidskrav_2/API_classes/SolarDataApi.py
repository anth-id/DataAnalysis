from Arbeidskrav_2.Models.SolarData import SolarData
from Arbeidskrav_2.API_classes.BaseApi import BaseApi

class SolarDataApi(BaseApi):
    def __init__(self, url, params):
        super().__init__(url,params)

    def getresult(self) -> dict:
        data:dict = self.getrequest()
        if len(data) > 0:
            return data
        raise FileNotFoundError("No solardata found")

    def getresults(self) -> list[SolarData]:
        data:list[SolarData] = []
        parser = self.getrequest()
        return [SolarData(p) for p in parser['days']]