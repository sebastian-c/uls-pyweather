# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 18:32:34 2022

@author: Sebastian
"""

from weatherapi.rest_adapter import RestAdapter
from weatherapi.weather import ApiAdapter

weather_api = RestAdapter("data.opendatasoft.com")

record_data = weather_api.get("catalog/datasets/donnees-synop-essentielles-omm@public/records", q_params = {"limit" : 10})

adapter = ApiAdapter()

x = adapter.getRecords()    
