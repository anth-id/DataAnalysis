from Models.SolarData import SolarData
from API_classes.BaseApi import BaseApi

class SolarDataApi(BaseApi):
    def __init__(self, url, params):
        super().__init__(url,params)

    def getresult(self) -> dict:
        data:dict = self.getrequest()
        if len(data) > 0:
            return data
        raise SystemExit("No solardata found")

    def getresults(self) -> list[SolarData]:
        data:list[SolarData] = []
        records = self.getrequest()
        for rec in records:
            data.append(SolarData(rec['days']))
        return data