from api import API
from constants import Constants
import json
from datetime import date
import os
from selenium import webdriver
from selenium.webdriver.common.by import By

class Movie:
    def getMovies():
        Movies = []
        driver = webdriver.Chrome()

        if os.path.exists('movie.json'):
            with open('movie.json', 'r') as json_file:
                Movies = json.load(json_file)

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
            
            # find movies in each theater
            movie_tags = soup.find_all("div", class_="fd-movie")

            
            for j in movie_tags:
                movie_title = j.find("a", class_="fd-movie__title font-sans-serif font-lg font-300 uppercase dark dark__text").text.strip()
                showtimes_tags = j.find_all("a", class_="btn showtime-btn showtime-btn--available showtime-btn--small")
                showtimes = [showtime.text.strip() for showtime in showtimes_tags]
                
                movie_info = {
                    "title": movie_title,
                    "showtimes": showtimes
                }
                
                Movies.append(movie_info)
                
        driver.quit()
        
        with open('movie.json', 'w') as json_file:
            json.dump(Movies, json_file, indent=1)

if __name__ == "__main__":
    Movie.getMovies()
