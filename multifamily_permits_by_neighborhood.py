#!/usr/bin/env python
# coding=utf-8

import csv
import json
from operator import itemgetter
import requests
import time

#load in the JSON file we created with download_building_permit_data.py
with open("residential_permits_2010-2015.json") as json_infile:
    bp_api_data = json.load(json_infile)

json_infile.close()

#create an empty dictionary that will hold our per-neighborhood counts
permits_by_neighborhood = {}

#go through each permit record and get the neighborhood for each address.
for x in bp_api_data:

    #we're only interested in MULTIFAMILY construction right now, not SINGLE FAMILY / DUPLEX
    if x['category'] == "MULTIFAMILY":

        #add the city and state to the end of each address before querying the Google Maps API
        gmaps_api_params = {'address' : x['address'] + " Seattle WA"}
        gmaps_api_req = requests.get("http://maps.googleapis.com/maps/api/geocode/json", params=gmaps_api_params)
        gmaps_api_data = gmaps_api_req.json()

        #if the Google Maps API can't find a neighborhood for an address, we're going to skip it
        try:
            neighborhood = gmaps_api_data['results'][0]['address_components'][2]['long_name']
            if neighborhood in permits_by_neighborhood:
                permits_by_neighborhood[neighborhood] = permits_by_neighborhood[neighborhood] + 1
            else:
                permits_by_neighborhood[neighborhood] = 1
        except:
            pass
            
        #slow down our API requests, to avoid getting blocked by Google    
        time.sleep(0.2)
    else:
        pass

#print the total number of permits issued for all neighborhoods
print(sum(permits_by_neighborhood.values()))

#transfer our data from a dictionary to a list, so we can sort it easier
neighborhood_counts_list = [[k,v] for k,v in permits_by_neighborhood.items()]

#sort that list by number of permits issued
sorted_neighborhood_counts_list = sorted(neighborhood_counts_list, key=itemgetter(1), reverse=True)

#print out our list to the terminal window
for x in sorted_neighborhood_counts_list:
    print(x[0] + " " + str(x[1]))

#store our per-neighborhood counts in a CSV file
with open('multifamily_by_neighborhood_2010-2015.csv', 'w') as csv_outfile:
    writer = csv.writer(csv_outfile)
    writer.writerow(('neighborhood', 'permits issued'))
    for x in sorted_neighborhood_counts_list:
        writer.writerow((x[0],x[1]))

csv_outfile.close()



