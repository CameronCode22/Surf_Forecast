#Newquay is a west facing beach
#Westerly swells are the best, so anything including west is good, otherwise swell direction is not good
#If > 60% chnace of rain, then drive the car
#same for lower temperature

import time
import web_Scrape_Forecast_SF_V1
import Web_Scrape_Forecast_Local_V2

web_Scrape_Forecast_SF_V1.get_surf_forecast()
time.sleep(3)
print("New line")
Web_Scrape_Forecast_Local_V2.execute_script()

