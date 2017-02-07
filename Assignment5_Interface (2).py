#!/usr/bin/python2.7
#
# Assignment3 Interface
# Name: Praveen Chirutapudi
#

from pymongo import MongoClient
import os
import sys
import json
import re
import math
import re
EARTH_RADIUS = 3959

def FindBusinessBasedOnCity(cityToSearch, saveLocation1, collection):
    print "Searching for city :" + cityToSearch
    fo = open(saveLocation1, "w+")
    cityToSearch = cityToSearch.strip()
    if len(cityToSearch) == 0:
        print "Empty cityToSearch"
        return
    for row in collection.find({"city" : re.compile(cityToSearch, re.IGNORECASE)}):
        output = ""
        output =  output + row['name'] + "$" + re.sub(r"\n", " ", row['full_address']) + "$" + row['city'] + "$" + row['state'] + "\n"
        fo.write(output.upper().encode("utf-8"))

def FindBusinessBasedOnLocation(categoriesToSearch, myLocation, maxDistance, saveLocation2, collection):
    lat1 = math.radians(float(myLocation[0]))
    lon1 = math.radians(float(myLocation[1]))
    fo = open(saveLocation2, "w+")
    for row in collection.find({"categories": {'$in': categoriesToSearch}}):
        lon2 = math.radians(row['longitude'])
        lat2 = math.radians(row['latitude'])
        dist = Distance(lat2, lon2, lat1, lon1)
        if dist <= maxDistance:
            res = row['name'].upper().encode("utf-8")
            fo.write(res + "\n")

def Distance(lat2,lon2, lat1, lon1):
    global EARTH_RADIUS
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    dist = EARTH_RADIUS * c
    # print dist
    return dist