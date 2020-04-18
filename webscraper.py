# Import libraries
import time
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

#Makes loop infinite
while True:

    # Set the URL you want to webscrape from
    url = 'https://en.wikipedia.org/wiki/Template:2019%E2%80%9320_coronavirus_pandemic_data'
    
    # Connect to the URL
    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()
    
    #set html parsing
    page_soup = soup(page_html,"html.parser")
    
    #grabs the html containers you want
    container1 = page_soup.findAll("span",{"class":"nowrap"})
    container2 = page_soup.findAll("div",{"id":"covid19-container"})
    
    #further sorts down to exact text you want
    WorldInfections = container1[2].findAll("b")
    WorldDeaths 	= container1[3].findAll("b")
    WorldRecovered  = container1[4].findAll("b")
    
    #parses table for USA data
    data2 = container2[0]
    virusdata = data2.findAll("table")
    USAdata = virusdata[0].findAll("td")
    
    #opens .txt file for temp data storage
    file = open("datastorage.txt","w")
    
    #clears contents of file
    file.truncate()
    
    #writes data to .txt file
    file.write("Worldwide Coronavirus Pandemic Data" + "\n")
    file.write("Infections: " + WorldInfections[0].text + "\n")
    file.write("Deaths:     " + WorldDeaths[0].text + "\n")
    file.write("Recovered:  " + WorldRecovered[0].text + "\n")

    file.write("USA Coronavirus Pandemic Data" + "\n")
    file.write("Infections: " + USAdata[0].text.strip() + "\n")
    file.write("Deaths:     " + USAdata[1].text.strip() + "\n")
    file.write("Recovered:  " + USAdata[2].text.strip() + "\n")
    
    #closes file
    file.close()
    
    #prints data to console for debugging
    print("Worldwide Coronavirus Pandemic Data" + "\n")
    print("Infections: " + WorldInfections[0].text)
    print("Deaths:     " + WorldDeaths[0].text)
    print("Infections: " + WorldRecovered[0].text + "\n")
    
    print("USA Coronavirus Pandemic Data" + "\n")
    print("Infections: " + USAdata[0].text.strip())
    print("Deaths:     " + USAdata[1].text.strip())
    print("Recovered:  " + USAdata[2].text.strip())
    
    #delays grabbing of data by an hour
    time.sleep(3600)
    
