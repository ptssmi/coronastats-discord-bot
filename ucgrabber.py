# Import libraries
import time
import logging
import smtplib
from datetime import datetime
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup


ucdata = []

url = 'https://www.uc.edu/publichealth/covid-19-dashboard.html'

# Connect to the URL
uClient = uReq(url)
page_html = uClient.read()
uClient.close()

#set html parsing
page_soup = soup(page_html,'html.parser')

#grabs the data from the webpage
for row in page_soup.table.find_all('tr')[1:]:
    data = (str(row.td.text))
    ucdata.append(data)

file = open('ucdata.txt','w')
#clears contents of the file
file.truncate()
#writes data to .txt file
file.write(ucdata[0])
#closes file
file.close()

#for debugging
now = datetime.now()
print('Data read at: ',now)

#sleep for a day
time.sleep(86400)





