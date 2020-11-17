from bs4 import BeautifulSoup
import requests
import csv
import os

MAX_PAGES = 100
url = "https://etherscan.io/txs?a=0x74381D4533cc43121abFef7566010dD9FB7c9F7a&p="
page = 1
full_url = url + str(page)

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
response = requests.get(full_url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

table = soup.find("table", {"class": "table table-hover"})

table_headers = table.findAll("th")
csv_headers = []
for header in table_headers:
    csv_headers.append(header)

processed_table = []
for page in range(1, MAX_PAGES + 1):

    full_url = url + str(page)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(full_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", {"class": "table table-hover"})

    table_body = table.find("tbody")
    table_rows = table_body.findAll('tr')

    for row in table_rows:
        processed_row = []
        table_columns = row.findAll('td')
        for column in table_columns:
            if not column.text == '':
                processed_row.append(column.text)
        processed_table.append(processed_row)

    if page % 20 == 0:
        processed = page/MAX_PAGES*100
        print("{}% of content processed".format(processed))

with open('output.csv', 'w', newline='\n') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerows(processed_table)

sizefile = os.stat('output.csv').st_size
print("File generated with  {0} rows and size {1} Bytes".format(len(processed_table), sizefile))


