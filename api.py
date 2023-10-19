from selenium import webdriver
from bs4 import BeautifulSoup
import time

class API:
    @staticmethod
    def getPageSource(driver, link:str) -> BeautifulSoup:
        driver.get(link)
        time.sleep(1)
        pageSource = driver.page_source
        soup = BeautifulSoup(pageSource, "html.parser")
        return soup
    
    @staticmethod
    def getDriver():
        return webdriver.Chrome()
