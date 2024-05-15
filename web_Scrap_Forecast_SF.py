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
driver.get("https://www.surf-forecast.com/breaks/Newquay-Town-Beach/forecasts/latest/six_day")

#wait for the page to load
WebDriverWait(driver, 10)

page_source = driver.page_source

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

#Find specific elements and extract data
wind_cells = soup.find_all('td', class_ ='forecast-table__cell forecast-table-wind__cell')

wind_speed_element = []
wind_direction_element = []

for wind_cell in wind_cells:

    text_element_ws = wind_cell.find('text', class_ = 'wind-icon__val')
    text_element_wd = wind_cell.find('div', class_ = 'wind-icon__letters')
    #print(text_element_wd)

    if text_element_ws:
        wind_speed_element.append(text_element_ws.get_text())
    else:
        print("Wind speed element not found.")

    if text_element_wd:
        wind_direction_element.append(text_element_wd.get_text())
    else:
        print("Wind direction is not available.")

#Recieving wave data

wave_cells = soup.find_all('td', class_ = 'forecast-table__cell forecast-table-wave-height__cell')
swell_height_element = []
swell_direction_element = []

for wave_cell in wave_cells:
    
    swell_height_icon = wave_cell.find('div', class_ = 'swell-icon')
    swell_direction = wave_cell.find('div', class_ = 'swell-icon__letters').text.strip()
    swell_height = swell_height_icon['data-height']

    if swell_height:
        swell_height_element.append(float(swell_height))
    else:
        print("Swell height not available.")
    if swell_direction:
        swell_direction_element.append(swell_direction)
    else:
        print("swell direction not available.")

#morning and evening for 11 days
#take todays date

date = datetime.now()
day = date.strftime("%d")

date_element = []
offset = 0
for n in range(12):
    for n in range(2):
        date_element.append(int(day) + offset)
    offset += 1

print(len(date_element))
print(len(wind_speed_element))
print(len(wind_direction_element))
print(len(swell_height_element))
print(len(swell_direction_element))


#adding information to df
df = pd.DataFrame({'day': date_element,
                  'wind speed (km/h)':wind_speed_element,
                  'wind direction':wind_direction_element,
                  'swell height': swell_height_element,
                  'swell direction':swell_direction_element
                  })

print(df)

driver.quit()
