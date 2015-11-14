#!/usr/bin/env python
# coding=utf-8

import csv
import json
from operator import itemgetter

with open("multifamily_neighborhood_data.json") as json_infile:
    bp_neighborhood_data = json.load(json_infile)

json_infile.close()

permits_by_neighborhood = {}

for x in bp_neighborhood_data:
    if 'neighborhood' in x.keys():
        neighborhood = x['neighborhood']
        if neighborhood in permits_by_neighborhood:
            permits_by_neighborhood[neighborhood] = permits_by_neighborhood[neighborhood] + 1
        else:
            permits_by_neighborhood[neighborhood] = 1
    else:
        pass
        
print(sum(permits_by_neighborhood.values()))

neighborhood_counts_list = [[k,v] for k,v in permits_by_neighborhood.items()]
sorted_neighborhood_counts_list = sorted(neighborhood_counts_list, key=itemgetter(1), reverse=True)

for x in sorted_neighborhood_counts_list:
    print(x[0] + " " + str(x[1]))

with open('multifamily_by_neighborhood_2010-2015_no_api.csv', 'w') as csv_outfile:
    writer = csv.writer(csv_outfile)
    writer.writerow(('neighborhood', 'permits issued'))
    for x in sorted_neighborhood_counts_list:
        writer.writerow((x[0],x[1]))

csv_outfile.close()



