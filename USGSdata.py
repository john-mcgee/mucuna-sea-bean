# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Script to retrieve data from USGS HTML report and export to CSV
#
# (c) 2019, John McGee Mr.McGee@outlook.com
# ---------------------------------------------------------------------------
from bs4 import BeautifulSoup
import requests
import csv

# Retrieve HTML
# url=""    # URL can be coded in here manually if needed
url = input("Enter URL: ")      
html = requests.get(url).text
soup = BeautifulSoup(html, 'lxml')
text = soup.text
text_list = text.split("\n")

# Separate out data in text table
data_list = []
for line in text_list:
    if "USGS" in line:
        line_data = line.split("\t")
        if len(line_data) >= 5:
            data_list.append(line_data)

# Identify headers           
site = data_list[0][1]
csv_headers = ["Agency","Site #","Datetime"]        
header_start = text_list.index("#            TS   parameter     statistic     Description")+1
header_end = text_list.index("#", header_start)
header_list = text_list[header_start:header_end]
for line in header_list:
    value = line.split()
    csv_headers.append("p{x}s{y}".format(x=value[2],y=value[3]))
    csv_headers.append("Qualification")

# Create CSV and write headers
site_csv = "{site}.csv".format(site=site)
csv_file = open(site_csv, "w", newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(csv_headers)

# Write data table to CSV
for data in data_list:
    csv_writer.writerow(data)

# Close CSV file and print completion message
csv_file.close    
print("Completed. Saved file as {csv}".format(csv=site_csv))