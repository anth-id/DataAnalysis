from abc import ABC, abstractmethod
import json
import requests
import keyring
from typing import Any


class BaseApi(ABC):
    def __init__(self, url:str, params:dict):
        self.url = url
        self.params = params

    @abstractmethod
    def getresult(self) -> Any:
        pass

    @abstractmethod
    def getresults(self) -> list[Any]:
        pass
        
#Creating a function to call api and save to a python readable JSON file. Since this is a general function to call the API. We set the return type annotation to Any.
    def getrequest(self) -> Any:
        response = requests.get(self.url, self.params,timeout=10)
        if response.status_code == 200:
            data:str = response.text
            return json.loads(data)
        else:
            raise SystemError (f"Failed to retrieve data. Status code {response.status_code}")

