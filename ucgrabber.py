# Import libraries
import time
import logging
import smtplib
from datetime import datetime
import pandas as pd
import requests


url = 'https://www.uc.edu/publichealth/covid-19-dashboard.html'

while True:

    r = requests.get(url)
    df_list = pd.read_html(r.text) # this parses all the tables in webpages to a list
    df = df_list[0]
    df2 = df_list[1]
    data = df.values
    housingdata = df2.values

    students = data[0,1]
    employees = data[1,1]
    visitors = data[2,1]
    total_cases = data[3,1]
    housingcases = housingdata[0,1]
    offcampuscases = housingdata[1,1]

    file = open('ucdata.txt','w')
    #clears contents of the file
    file.truncate()
    #writes data to .txt file
    file.write(str(students)+'\n'+str(employees)+'\n'+str(visitors)+'\n'+str(total_cases)+'\n'+str(housingcases)+'\n'+str(offcampuscases)+'\n')
    #closes file
    file.close()

    #for debugging
    now = datetime.now()
    print('Data read at: ',now)

    #sleep for a day
    time.sleep(86400)






