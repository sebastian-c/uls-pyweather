# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 11:30:23 2022

@author: Sebastian
"""

from weatherapi.rest_adapter import RestAdapter
from typing import Dict

class ApiAdapter:
    def __init__(self, 
                 hostname: str = "data.opendatasoft.com", 
                 api_key: str = "", 
                 ver: str = "v2", 
                 ssl_verify: bool = True):
        self._rest_adapter = RestAdapter(hostname, api_key, ver, ssl_verify)

    def getRecord(self, id: str, endpoint: str = ""):
        response = self._rest_adapter.get(endpoint & id)
        return(response)
    
    def getDatasetInfo(self, id: str = "donnees-synop-essentielles-omm@public", 
                       endpoint = "catalog/datasets/"):
        response = self._rest_adapter.get(endpoint & id)
        return(response)
    
    def getRecords(self, params:Dict = None, 
                   dataset_id = "donnees-synop-essentielles-omm@public", 
                   endpoint = "catalog/datasets/{dataset_id}/records"):
        formatted_endpoint = endpoint.format_map(locals())
        response = self._rest_adapter.get(endpoint = formatted_endpoint, q_params = params)
        return(response)


        
