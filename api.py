from selenium import webdriver
from bs4 import BeautifulSoup
import time
from datetime import date
import json

class API:
    @staticmethod
    def getPageSource() -> BeautifulSoup:
        driver = webdriver.Chrome()
        driver.get("https://www.fandango.com/phoenix_az_movietimes?date=" + str(date.today()))
        time.sleep(2)
        pageSource = driver.page_source
        soup = BeautifulSoup(pageSource, "html.parser")
        return soup