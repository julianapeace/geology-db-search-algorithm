#http://ecp.iedadata.org/rest_search_documentation/
import urllib.parse
import requests
import json
import csv
import os
from datetime import *

url = 'http://ecp.iedadata.org/restsearchservice?author=peter&searchtype=rowdata&outputtype=csv&outputitems=&showcolumnnames=yes'

params ={}

response = requests.get(url, params=params)

myquery = response.text
splitn = myquery.split('\n')
value_list = []
for i in splitn:
    x = i.split(',')
    value_list.append(x)
print(value_list)
# print(datetime.strftime(datetime.now(), '%Y%m%d%H%m'))
file_name = datetime.strftime(datetime.now(), '%Y%m%d%H%m%s') + '.csv'
file_path = os.path.join('static/exports/', file_name)

if not os.path.exists('static/exports/'):
            os.makedirs('static/exports/')
with open(file_path, 'w', newline='') as outfile:
    writer = csv.writer(outfile, delimiter = ',')
    for x in value_list:
        writer.writerow(x)
outfile.close()
# render the file_path link to template
