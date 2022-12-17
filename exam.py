# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 14:35:29 2022

@author: Sebastian
"""

from weatherapi.helpers import Presenter, KelvinToCelsius
from weatherapi.weather import ApiAdapter
from datetime import date, datetime, timedelta
import requests
import json
import os
import pandas as pd
import matplotlib.pyplot as plt

p = Presenter()

p.pause(title="Today's date")
date_today = date.today()
print(date_today)

p.pause(title="Welcome message")

print(
    f"Welcome to this fine piece of technological gadgetry allowing you to see the weather. The date is {date_today}")

p.pause("Weather station input")

raw_station = input("Please enter a weather station:\n")
#adapter = ApiAdapter()

p.pause("Weather station uppercase")

weather_station = raw_station.capitalize()
print(weather_station)

p.pause("Date entry")

raw_date = input("Please enter a valid date (yyyy-mm-dd):\n")

p.pause("Date validation")

try:
    chosen_date = datetime.strptime(raw_date, "%Y-%m-%d")
except (TypeError, ValueError):
    chosen_date = date_today - timedelta(days=1)
    print("Chosen date is invalid, using yesterday's date instead")
    
#Yes I could use a parser to be more generous about formats, but why bother?

p.pause("OpenData API site")

url = "https://data.opendatasoft.com/api/records/1.0/search/?dataset=donnees-synop-essentielles-omm%40public&q=&lang=en&rows=10000&sort=date&facet=date&facet=nom&facet=temps_present&facet=libgeo&facet=nom_epci&facet=nom_dept&facet=nom_reg&refine.date=2022%2F11&refine.nom=ROUEN-BOOS"
print(url)
with open("api_url.py", "w") as f:
    f.write("#" + url)

p.pause("Download data as json")

raw_response = requests.get(url)
print(f"Status code: {raw_response.status_code}")

p.pause("Display json on screen")

raw_json = raw_response.json()
json_chr = json.dumps(raw_json, sort_keys=True, indent=2)
print(json_chr)

p.pause("Create data directory")

os.makedirs("data", exist_ok=True)
os.path.exists("data")

p.pause("Write json data")

with open("data/november_2022_Rouen_weather.json", "w") as f:
    f.write(json_chr)

p.pause("Read in json")


# I wrote an API adapter to specifically handle this so instead of breaking the
# encapsulation, I'm just going to read the data again
adapter = ApiAdapter()
november_results = adapter.exportRecords({"limit": "10000",
                                          "sort": "date",
                                          "facets": ["nom", "temps_present", "libgeo", "nomepci", "nom_reg"],
                                          "refine": ["date:2022/11", "nom:ROUEN-BOOS"]
                                          })

print(november_results.head(10))

p.pause("Display additional information")

november_results["date"] = pd.to_datetime(november_results["date"], infer_datetime_format=True)
#november_results.resample("D", on="date").summary()

#Convert kelvin to C
november_results["t_c"] = KelvinToCelsius(november_results["t"])

#Temperature in celsius by day
november_results[["date", "t_c"]].dropna().groupby(pd.Grouper(freq="D", key="date", axis = 0)).mean()

#Missing values for 26th and 27th in the source data
p.pause("Make graphs")

# Temperature
tmp = plt.figure()
tmp.set_figwidth(10*1.618)
tmp.set_figwidth(10)
plt.plot(november_results["date"], november_results["t_c"], "r-")
plt.xticks(rotation=45, ha='right')
plt.xlabel("date")
plt.ylabel("Temperature (°C)")
plt.suptitle("Average November 2022 Temperature in Rouen")
plt.text(pd.Timestamp("2022-11-26"),12, "This line artifact is\ndue to missing data\non 26-27 November")

#Rainfall
tmp = plt.figure()
tmp.set_figwidth(10*1.618)
tmp.set_figwidth(10)
rain_data = november_results[["date", "rr3"]].groupby(pd.Grouper(freq="D", key="date", axis = 0)).sum()
plt.bar(rain_data.index, rain_data["rr3"])
plt.xticks(rotation=45, ha='right')
plt.xlabel("date")
plt.ylabel("Rainfall (mm)")
plt.suptitle("Daily November 2022 Rainfall in Rouen")

p.pause("Write to csv")

november_results.to_csv("data/november_2022_Rouen_weather.csv")

#p.pause
