from api import API
from constants import Constants
import json
from datetime import date
import time
from selenium.webdriver.common.by import By

class Theater:
    def getTheaters(tag):
        Theaters = set([])
        with open('theater.json', 'r') as json_file:
            Theaters = json.load(json_file)

        for i in tag:
            theaterId = i['data-theater-id']
            name = i.find("a").text.strip()
            span = i.find(class_="fd-theater__address-wrap dark__text--secondary").text
            streetAddress = ""
            for j in span.split("\n"):
                if(j.strip()):
                    streetAddress += " " + j.strip()
            data = {
                "theaterId" : theaterId,
                "name" : name,
                "streetAddress" : streetAddress 
            }
            Theaters.append(data)
            with open('theater.json', 'w') as json_file:
                json.dump(Theaters, json_file, indent=1)

    driver = API.getDriver()
    driver.get(Constants.link)
    for i in Constants.theaterLinkMap.values():
        elem = driver.find_element(By.ID, "global-header-search-input")
        elem.click()
        elem.send_keys(i)

        time.sleep(4)

        soup = API.getPageSource(driver, driver.current_url)
        print(soup)
        # ulTag = soup.find(class_="fd-showtimes js-theaterShowtimes-loading").find_all("li", class_="fd-theater")
        # getTheaters(ulTag)
    
            