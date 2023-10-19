from api import API
from constants import Constants
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Theater:
    def getTheaters(tag):
        Theaters = []
        with open('theater.json', 'r') as json_file:
            Theaters = json.load(json_file)

        for i in tag:
            theaterId = i['data-theater-id']
            if not any(l['theaterId'] == theaterId for l in Theaters):
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
        elem2 = driver.find_element(By.CLASS_NAME, "nav-bar__go-btn")
        elem2.click()

        # cities page
        elem3 = driver.find_element(By.XPATH, "//*[@id='search-results-cities']/div/div/div/ul/li/a")
        elem3.click()

        # theater page
        soup = API.getPageSource(driver)
        ulTag = soup.find(class_="fd-showtimes js-theaterShowtimes-loading").find_all("li", class_="fd-theater")
        getTheaters(ulTag)
    
            