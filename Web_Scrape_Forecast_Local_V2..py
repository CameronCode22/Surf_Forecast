#Assumptions:
#Only going between 6am and 9am so for that day, I need to know in that range
#if there is a above 60% chance of precipitation, if outside weather is less than 7 degrees
#get wind gusts for speed, take again an average of the time range given
#and wind direction but give surf forecast higher priority in the concatination
#on this forecast there are only 7 days
#as both data sets are moving data, yOU can only run this teh day before the usrf session
#this is correct as surf forecast give syou today morning but it would have already gone

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import datetime


# Path to the Chrome executable for the desired version
chrome_path = r"C:\Users\jscam\OneDrive\Documents\Programming\Chrome_driver\chrome-win64\chrome-win64\chrome.exe"

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = chrome_path

# Set up the Chrome WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Navigate to web page
driver.get("https://www.metoffice.gov.uk/weather/forecast/gbuqgfn0u#?forecastChoice=weather")

#wait for the page to load
WebDriverWait(driver, 10)

page_source = driver.page_source

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')
# #Find specific elements and extract data
#Extracting date of extraction
date_cells = soup.find_all('li', class_ ='forecast-tab')
temporary_date_element = []

for date_cell in date_cells:
      temporary_date_element = date_cell.find('h3', class_ = 'tab-day')

#finding cells in forecast container

cells = soup.find_all('div', class_ = 'forecast-table-container')
time_element = []

#find time of day
for time_cell in cells:
      time_elements = time_cell.find_all('tr', class_ = 'step-time')

      for time_element_temp in time_elements:
            time_table = time_element_temp.find_all('th')

            for elem in time_table:
                  time_text = elem.get_text().strip()
                  if time_text !='Time':
                        time_element.append(time_text)


#find the percipitation
time__ = []
percip_element = []

for percip_cell in cells:
      percip_elements = percip_cell.find_all('tr', class_ = 'step-pop comb-forecast')
      

      for percip_element_temp in percip_elements:
            percentage_percip = percip_element_temp.find_all('td')

            for elem in percentage_percip:
                  percip_element.append(elem.get_text())
                  time__ = elem['data-test-label']

#find the temperature
temperature_element = []

for temp_cell in cells:
      temp_elements = temp_cell.find_all('tr', class_ = 'step-temp comb-forecast')

      for temp_elem in temp_elements:
            each_temp = temp_elem.find('div', {'data-value':True})
            if each_temp:
                  temperature = each_temp['data-value']
                  temperature_element.append(temperature)
            else:
                  print("Temperature element not found.")

#put the date into array

date = datetime.now()
day = date.strftime("%d")

date_element = []
prev_hour = None

for date_time in time_element:
      
      #extract hour part
    hour = int(date_time.split(":")[0])

      #check if prev_hour is not None and current hour is less than prev_hour
    if prev_hour is not None and hour < prev_hour:
        #increment the day
        day = str(int(day)+1)
    
    date_element.append(day)
    prev_hour = hour

# print(len(date_element))
# print("\n")
# print(date_element)
# print(len(temperature_element))

#adding information to df
df = pd.DataFrame({'date':date_element,
                  'time': time_element,
                  'percipitation': percip_element
                  })

pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.max_columns', None)  # Show all columns
print(df) 


driver.quit()
