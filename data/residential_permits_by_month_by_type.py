#!/usr/bin/env python
# coding=utf-8

import csv
import json
from operator import itemgetter
import requests

#load in the JSON file we created with download_building_permit_data.py
with open("residential_permits_2010-2015.json") as json_infile:
    bp_api_data = json.load(json_infile)   

json_infile.close()

#create an empty dictionary to hold our per-month counts
permits_by_month = {}

#go through the JSON data
#create a dictionary that contains all the month-year combos in the data
for x in bp_api_data:
    month_string = x['issue_date'][0:7]
    if month_string not in permits_by_month:
        permits_by_month[month_string] = {'multifamily':0, 'single_duplex':0}
    else:
        pass

#go through the JSON again, the time add in the multifamily and single/duplex counts 
#for each month in permits_by_month dictionary we created in the last step
for x in bp_api_data:                    
    month_string = x['issue_date'][0:7]
    if x['category'] == 'MULTIFAMILY':
        permits_by_month[month_string]['multifamily'] = permits_by_month[month_string]['multifamily'] + 1
    elif x['category'] == 'SINGLE FAMILY / DUPLEX':
        permits_by_month[month_string]['single_duplex'] = permits_by_month[month_string]['single_duplex'] + 1
    else:
        print("found an unrecognized building category:" + x['category'])

#transfer our data from a dictionary to a list of dictionaries, so we can sort it easier
monthly_counts_list = [[k,v] for k,v in permits_by_month.items()]

#sort that list chronologically by month
sorted_monthly_counts_list = sorted(monthly_counts_list, key=itemgetter(0))

#print out our monthly counts by permit type to the terminal window
for x in sorted_monthly_counts_list:
    print(x[0] + " " + str(x[1]['single_duplex']) + " " + str(x[1]['multifamily'])) 

#store our monthly counts by permit type in a CSV file
with open('residential_by_month_by_type_2010-2015.csv', 'w') as csv_outfile:
    writer = csv.writer(csv_outfile)
    writer.writerow(('month', 'single duplex permits issued', 'multifamily permits issued'))
    for x in sorted_monthly_counts_list: 
        writer.writerow((x[0],x[1]['single_duplex'],x[1]['multifamily']))

csv_outfile.close()


