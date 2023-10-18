from selenium import webdriver
from bs4 import BeautifulSoup
import time

class API:
    @staticmethod
    def getPageSource(link:str) -> BeautifulSoup:
        driver = webdriver.Chrome()
        driver.get(link)
        time.sleep(1)
        pageSource = driver.page_source
        soup = BeautifulSoup(pageSource, "html.parser")
        return soup