#!/usr/bin/env python
# coding: utf-8

# # Finding the nearest train/tube station
# 
# The purpose of this project is to create module that takes a London postcode input e.g. N4 4AF and will output the nearest train station to it.

# In[1]:


# import pandas as pd
import requests
from geopy import distance
import re
import london_stations as ls

# In[2]:


# A csv file of london stations can be downloaded from this link
# https://www.doogal.co.uk/london_stations.php

# TODO join station data to tube line data using TFL api to get info
# Also replace hard coded file with retrieving lat/lon from TFL api
london_stations_df = ls.load_london_stations()


# In[3]:


LONDON_STATIONS = []
for x in london_stations_df[['Station', 'Latitude', 'Longitude']].values:
    LONDON_STATIONS.append((x[0],(x[1],x[2])))


# In[17]:


# TODO refactor - use less code
# TODO Add documentation
class NearestStation:
        
    def __init__(self, postcode, unit='m', stations=LONDON_STATIONS):
        self.postcode = postcode.lower()
        self.lat_lon = self.geo_dict['lat_lon']
        self._unit = unit
        self.stations = stations
     
    @staticmethod
    def extract_postcode(postcode):
        postcode = postcode
        regex_str = r'[A-Z]{1,2}[0-9R][0-9A-Z]? [0-9][A-Z]{2}'
        return re.findall(regex_str, postcode, flags=re.IGNORECASE)[0]
    
    @staticmethod
    def nearest_station(lat_lon, unit='m', n=1, stations=LONDON_STATIONS):
        if unit == 'm':
            distances = [(x[0], round(distance.distance(lat_lon, x[1]).miles,1)) for x in stations]
            distances.sort(key=lambda x:x[1])
            return distances[:n]
        elif unit == 'km':
            distances = [(x[0], round(distance.distance(lat_lon, x[1]).km,1)) for x in stations]
            distances.sort(key=lambda x:x[1])
            return distances[:n]
    
    @property
    def unit(self):
        return self._unit
    
    @unit.setter
    def unit(self, new_unit):
        if new_unit in ['m', 'km']:
            self._unit = new_unit
        else:
            raise ValueError('Enter "m" for miles or "km" for kilometers')
        
    @property
    def endpoint(self):
        pc = self.postcode.replace(' ','')
        return f'http://api.postcodes.io/postcodes/{pc}'
    
    @property
    def geo_dict(self):
        geocoded_dict = {}
        r = requests.get(self.endpoint)
        geocoded_dict['postcode'] = r.json()['result']['postcode']
        geocoded_dict['lat_lon'] = (r.json()['result']['latitude'], r.json()['result']['longitude'])
        return geocoded_dict
    
    @property
    def distances(self):
        if self._unit == 'm':
            distances = [(x[0], round(distance.distance(self.lat_lon, x[1]).miles,1)) for x in self.stations]
            distances.sort(key=lambda x:x[1])
            return distances
        elif self._unit == 'km':
            distances = [(x[0], round(distance.distance(self.lat_lon, x[1]).km,1)) for x in self.stations]
            distances.sort(key=lambda x:x[1])
            return distances
        
    def find_nearest_station(self): 
        return (self.distances[0])

    def find_nearest_n_stations(self,n):
        return (self.distances[:n])
    
    def find_stations_with_x_radius(self, n):
        return [x for x in self.distances if x[1] <= n]

