# Import libraries
import time
import logging
from datetime import datetime
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

#Makes loop infinite
while True:

    try:

        # URL for country data
        url = 'https://pomber.github.io/covid19/timeseries.json'
        
        # Connect to the URL
        uClient = uReq(url)
        page_html = uClient.read()
        uClient.close()
        
        #set html parsing
        page_soup = soup(page_html,"html.parser")
        
        #opens .txt file for temp data storage
        file = open("datastorage.txt","w")
        
        #clears contents of file
        file.truncate()
        
        #writes data to .txt file
        file.write(str(page_soup))

        #closes file
        file.close()

        #for debugging
        print("Country data read success")
        
        # URL for US county data
        url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
        
        # Connect to the URL
        uClient = uReq(url)
        page_html = uClient.read()
        uClient.close()
        
        #set html parsing
        page_soup = soup(page_html,"html.parser")
        
        #opens .txt file for temp data storage
        file = open("countydata.txt","w")
        
        #clears contents of file
        file.truncate()
        
        #writes data to .txt file
        file.write(str(page_soup))

        #closes file
        file.close()

        #for debugging
        print("County data read success")

        #URL for state data
        url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"

        # Connect to the URL
        uClient = uReq(url)
        page_html = uClient.read()
        uClient.close()
        
        #set html parsing
        page_soup = soup(page_html,"html.parser")
        
        #opens .txt file for temp data storage
        file = open("statedata.txt","w")
        
        #clears contents of file
        file.truncate()
        
        #writes data to .txt file
        file.write(str(page_soup))

        #closes file
        file.close()

        #for debugging
        print("State data read success")

        #for debugging
        now = datetime.now()
        print("Files read at:",now)
        
        #delays data capture by 1 hour
        time.sleep(3600)

    except:
        #prints error message
        logging.exception("message")
        pass
    else:
        break
