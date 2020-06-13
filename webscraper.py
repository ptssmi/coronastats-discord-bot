# Import libraries
import time
import logging
import smtplib
from datetime import datetime
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup


data = [ {  'url' : 'https://pomber.github.io/covid19/timeseries.json', 
            'file_name' : 'datastorage.txt',
            'debug_action' : 'Country data',
            'email_action' : 'country'}, 

        {   'url' : 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv',
            'file_name' : 'countydata.txt', 
            'debug_action' : 'County data',
            'email_action' : 'county'}, 

        {   'url' : 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv', 
            'file_name' : 'statedata.txt',
            'debug_action' : 'State data',
            'email_action' : 'state'}]
            
            
def emailsender(datatype):
        fromaddr = 'from_email'
        toaddrs  = 'to_email'
        
        if datatype == 'country':
            msg = 'There is an issue with country data.'
        elif datatype == 'state':
            msg = 'There is an issue with state data.'
        elif datatype == 'county':
            msg = 'There is an issue with county data.'
            
        username = 'email'
        password = 'pwd'
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(username,password)
        server.sendmail(fromaddr, toaddrs, msg)
        server.quit()


#Makes loop infinite
while True:
    for entry in range(0, len(data)):
        try:
            # Connect to the URL
            uClient = uReq(data[entry]['url'])
            page_html = uClient.read()
            uClient.close()

            #set html parsing
            page_soup = soup(page_html,'html.parser')
        
            #opens .txt file for temp data storage
            file = open(data[entry]['file_name'],'w')
        
            #clears contents of file
            file.truncate()
        
            #writes data to .txt file
            file.write(str(page_soup))

            #closes file
            file.close()

            #for debugging
            print('{0} read success'.format(data[entry]['debug_action']))
        except:
            print('{0} read failure'.format(data[entry]['debug_action']))
            logging.exception('message')
            emailsender(data[entry]['email_action'])
            pass

    #for debugging
    now = datetime.now()
    print('Files read at: ',now)
        
    #delays data capture by 1 hour
    time.sleep(3600)

