# Import libraries
import time
from datetime import datetime
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

#Makes loop infinite
while True:

    # Set the URL you want to webscrape from
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
    now = datetime.now()
    print("File read at:",now)
    
    #delays data capture by 1 hour
    time.sleep(3600)
    
