from api import API
from constants import Constants
import json
from datetime import date
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

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
            time.sleep(3)
            
            # find movies in each theater
            movie_tags = soup.find(class_="fd-showtimes js-theaterShowtimes-loading").find_all("li", class_="fd-movie")
            # movie_link = soup.find(class_="fd-showtimes js-theaterShowtimes-loading").find(By.TAG_NAME, "a")
            
            for j in movie_tags:
                movie_title = j.find("h3").text
                if not any(l['title'] == movie_title for l in Movies):
                    data = {
                        "title": movie_title,
                        "movieID": 000000
                    }

                    Movies.append(data)
                    with open('movie.json', 'w') as json_file:
                        json.dump(Movies, json_file, indent=1)
            # for j in movie_tags:
            #     movie_title = j.find("a", class_="fd-movie__title font-sans-serif font-lg font-300 uppercase dark dark__text")
            #     movie_link_element = j.find("a", class_="fd-movie__link")
            #     movie_URL = j.find("a", _class="fd-movie__link").get('href')
            #     movie_ID = extract_movie_id(movie_URL)
                
            #     movie_info = {
            #         "title": movie_title,
            #         "movieID": movie_ID
            #     }
                
            #     Movies.append(movie_info)
                
        driver.quit()

def extract_movie_id(movie_url):
    if movie_url:
        return movie_url.split('-')[-1]
    else:
        return None

if __name__ == "__main__":
    Movie.getMovies()
