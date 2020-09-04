# Import libraries
import time
from datetime import datetime
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup


while True:

    url = 'https://www.uc.edu/publichealth/covid-19-dashboard.html'

    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()

    #finds all p html elements
    page_soup = soup(page_html,'lxml')
    tags = page_soup.find_all('p')
    type(tags)

    #Seperates numbers from text
    housingdata = tags[6].text
    splithousingdata = housingdata.split()

    #sorts p html elements
    students = tags[5].text
    employees = tags[7].text
    visitors = tags[8].text
    total_cases = tags[4].text
    housingcases = splithousingdata[0]
    offcampuscases = splithousingdata[5]

    file = open('ucdata.txt','w')
    #clears contents of the file
    file.truncate()
    #writes data to .txt file
    file.write(str(students)+str(employees)+'\n'+str(visitors)+'\n'+str(total_cases)+'\n'+str(housingcases)+'\n'+str(offcampuscases)+'\n')
    #closes file
    file.close()

    #for debugging
    now = datetime.now()
    print('Data read at: ',now)

    #sleep for 2 hours
    time.sleep(7200)






