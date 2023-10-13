from selenium import webdriver
from bs4 import BeautifulSoup
import time
from datetime import date
import json

class API:
    Theaters = []
    driver = webdriver.Chrome()
    driver.get("https://www.fandango.com/phoenix_az_movietimes?date=" + str(date.today()))
    time.sleep(2)
    pageSource = driver.page_source

    soup = BeautifulSoup(pageSource, "html.parser")
    ulTag = soup.find(class_="fd-showtimes js-theaterShowtimes-loading").find_all("li", class_="fd-theater")

    with open('theater.json', 'r') as json_file:
        loaded = json.load(json_file)
    loaded = []

    for i in ulTag:
        # print("-----------------------------------------")
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
        loaded.append(data)

    with open('theater.json', 'w') as json_file:
        json.dump(loaded, json_file, indent=1)
        