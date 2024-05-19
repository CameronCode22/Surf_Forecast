import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import datetime, timedelta

def get_surf_forecast():
    # Path to the Chrome executable for the desired version
    chrome_path = r"C:\Users\jscam\OneDrive\Documents\Programming\Chrome_driver\chrome-win64\chrome-win64\chrome.exe"

    # Set up Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = chrome_path

    # Set up the Chrome WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Navigate to web page
        driver.get("https://www.surf-forecast.com/breaks/Newquay-Town-Beach/forecasts/latest/six_day")

        # Wait for the page to load
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'forecast-table__cell')))

        page_source = driver.page_source

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find specific elements and extract data
        wind_cells = soup.find_all('td', class_ ='forecast-table__cell forecast-table-wind__cell')
        wave_cells = soup.find_all('td', class_ = 'forecast-table__cell forecast-table-wave-height__cell')

        wind_speed_element = []
        wind_direction_element = []
        swell_height_element = []
        swell_direction_element = []

        for wind_cell in wind_cells:
            text_element_ws = wind_cell.find('text', class_ = 'wind-icon__val')
            text_element_wd = wind_cell.find('div', class_ = 'wind-icon__letters')

            if text_element_ws:
                wind_speed_element.append(text_element_ws.get_text())
            else:
                wind_speed_element.append(None)  # Ensure the lists have the same length

            if text_element_wd:
                wind_direction_element.append(text_element_wd.get_text())
            else:
                wind_direction_element.append(None)  # Ensure the lists have the same length

        for wave_cell in wave_cells:
            swell_height_icon = wave_cell.find('div', class_ = 'swell-icon')
            swell_direction = wave_cell.find('div', class_ = 'swell-icon__letters')

            if swell_height_icon and 'data-height' in swell_height_icon.attrs:
                swell_height = swell_height_icon['data-height']
                swell_height_element.append(float(swell_height))
            else:
                swell_height_element.append(None)  # Ensure the lists have the same length

            if swell_direction:
                swell_direction_element.append(swell_direction.text.strip())
            else:
                swell_direction_element.append(None)  # Ensure the lists have the same length

        # Generate date elements
        date = datetime.now()
        date_element = [date + timedelta(days=i//2) for i in range(len(wind_speed_element))]

        # Print lengths of all lists to ensure they match
        # print(f"Length of date_element: {len(date_element)}")
        # print(f"Length of wind_speed_element: {len(wind_speed_element)}")
        # print(f"Length of wind_direction_element: {len(wind_direction_element)}")
        # print(f"Length of swell_height_element: {len(swell_height_element)}")
        # print(f"Length of swell_direction_element: {len(swell_direction_element)}")

        # Adding information to df
        df = pd.DataFrame({
            'day': date_element,
            'wind speed (km/h)': wind_speed_element,
            'wind direction': wind_direction_element,
            'swell height': swell_height_element,
            'swell direction': swell_direction_element
        })

        pd.set_option('display.max_rows', None)  # Show all rows
        pd.set_option('display.max_columns', None)  # Show all columns
        print(df)

    finally:
        driver.quit()

if __name__ == "__main__":
    get_surf_forecast()