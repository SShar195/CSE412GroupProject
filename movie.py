from api import API
from constants import Constants
import json
from datetime import date
import os
from selenium import webdriver

class Movie:
    def getMovies():
        Movies = []
        
        driver = webdriver.Chrome()
        
        if os.path.exists('movie.json'):
            with open('movie.json', 'r') as json_file:
                Movies = json.load(json_file)

        for theater_link in Constants.theaterLinkMap.values():
            soup = API.getPageSource(theater_link + "?date=" + str(date.today()))
            movie_tags = soup.find_all("div", class_="fd-movie")
            
            for movie_tag in movie_tags:
                movie_title = movie_tag.find("a", class_="fd-movie__title").text.strip()
                showtimes_tags = movie_tag.find_all("a", class_="fd-movie__showtime")
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
