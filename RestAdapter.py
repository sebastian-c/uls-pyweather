# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
from typing import List, Dict

#response = r.get("https://data.opendatasoft.com/api/records/1.0/search/?dataset=donnees-synop-essentielles-omm%40public&q=&lang=en&sort=date&facet=date&facet=nom&facet=temps_present&facet=libgeo&facet=nom_epci&facet=nom_dept&facet=nom_reg")


class RestAdapter:
    def __init__(self, 
                 hostname: str, 
                 api_key: str = "", 
                 ver: str = "v2", 
                 ssl_verify: bool = True):
        self.url = f"https://{hostname}/records/{ver}/"
        self._api_key = api_key
        self._ssl_verify = ssl_verify
        if not ssl_verify:
            requests.packages.urllib3.disable_warnings()

    def get(self, endpoint: str, q_params: Dict = None) -> List[Dict]:
        full_url = self.url + endpoint
        # headers =
        response = requests.get(url=full_url, 
                                verify = self._ssl_verify, 
                                params = q_params)
        data_out = response.json()
        if response.status_code >= 200 and response.status_code <= 299:
            return data_out
        #raise Exception(data_out["message"])
# def getWeather(q,lang,rows=10,start,sort="date",facets=)
