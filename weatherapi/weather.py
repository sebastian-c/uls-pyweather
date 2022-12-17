# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 11:30:23 2022

@author: Sebastian
"""

from weatherapi.rest_adapter import RestAdapter
from typing import Dict
from pandas import DataFrame

class ApiAdapter:
    def __init__(self, 
                 hostname: str = "data.opendatasoft.com", 
                 base_dataset: str = "donnees-synop-essentielles-omm@public",
                 api_key: str = "", 
                 ver: str = "v2", 
                 ssl_verify: bool = True):
        self._rest_adapter = RestAdapter(hostname, api_key, ver, ssl_verify)
        self.base_dataset = base_dataset

    def getRecord(self, dataset_id: str, endpoint: str = "catalog/datasets/{dataset_id}/records/{record_id}"):
        formatted_endpoint = endpoint.format_map(locals())
        response = self._rest_adapter.get(formatted_endpoint)
        return(response)
    
    def getDatasetInfo(self, dataset_id = "", 
                       endpoint = "catalog/datasets/"):
        if dataset_id is None:
            dataset_id = self.base_dataset
        response = self._rest_adapter.get(endpoint & dataset_id)
        return(response)
    
    def getRecords(self, params:Dict = None, 
                   dataset_id = None, 
                   endpoint = "catalog/datasets/{dataset_id}/records"):
        if dataset_id is None:
            dataset_id = self.base_dataset
        formatted_endpoint = endpoint.format_map(locals())
        response = self._rest_adapter.get(endpoint = formatted_endpoint, q_params = params)
        response = parseRecord(response)
        return(response)
    
    def getFacets(self, params:Dict = None, 
                   dataset_id = None, 
                   endpoint = "catalog/datasets/{dataset_id}/facets"):
        if dataset_id is None:
            dataset_id = self.base_dataset
        formatted_endpoint = endpoint.format_map(locals())
        response = self._rest_adapter.get(endpoint = formatted_endpoint, q_params = params)
        response = parseFacet(response)
        return(response)

    def exportRecords(self, params:Dict = {"limit":100},
                      dataset_id = None,
                      endpoint = "catalog/datasets/{dataset_id}/exports/{format}"):
        format = "json"
        if dataset_id is None:
            dataset_id = self.base_dataset
        formatted_endpoint = endpoint.format_map(locals())
        response = self._rest_adapter.get(endpoint = formatted_endpoint, q_params = params)
        response = parseExport(response)
        return(response)
        
def parseExport(dict_records:Dict):
    
    records_base = []
    for record_dict in dict_records:
        records_base.append(record_dict)
    ret = DataFrame.from_dict(records_base)
    return(ret)



def parseRecord(dict_records:Dict):
    
    records_base = []
    for record_dict in dict_records["records"]:
        row = record_dict["record"]["fields"]
        records_base.append(row)
    ret = DataFrame.from_dict(records_base)
    return(ret)

def parseFacet(facet_records: Dict):
    # Used for pulling in data about a facet
    # Used for to prefill dropdown menus
    facets_base = []
    for facet_dict in facet_records["facets"]:
        # Ensure that there's a column identifying the variable name
        var_name = {"variable_name" : facet_dict["name"]}
        var_facets = []
        for facet_row in facet_dict["facets"]:
            var_facets.append(
                {**var_name, **facet_row})
            
        facets_base.extend(var_facets)
    ret = DataFrame.from_dict(facets_base)
    return(ret)