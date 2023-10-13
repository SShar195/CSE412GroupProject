import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from datetime import date
import json

class API:
    @staticmethod
    def getTheaters():
        Theaters = []
        driver = webdriver.Chrome()
        driver.get("https://www.fandango.com/phoenix_az_movietimes?date=" + str(date.today()))
        time.sleep(2)
        pageSource = driver.page_source

        soup = BeautifulSoup(pageSource, "html.parser")
        ulTag = soup.find("div", class_="fd-showtimes js-theaterShowtimes-loading").find("ul")
        for i in ulTag:
            aTag = i.find("a")
            if aTag != -1:
                Theaters.append(aTag.text.strip())
        return Theaters
    
class Movie:
    def __init__(self, movieId, movieName):
        self.movieId = movieId
        self.movieName = movieName 

class Theater:
    def __init__(self, theaterId, name, address):
        self.theaterId = theaterId
        self.name = name
        self.address = address

    
class TheaterList:
    theaterNames = API.getTheaters()
    theaters = []

    for i in theaterNames:
        theaters.append(Theater(name=i))