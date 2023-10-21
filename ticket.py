from api import API
from constants import Constants
import json
from datetime import date
import time
from selenium.webdriver.common.by import By

# Creates link used in create_tickets
def get_link(movie):
    with open('movie.json', 'r') as json_file:
        movies = json.load(json_file)

    # Pull the movie information
    name = movie['movieTitle'].replace(' ', '-')
    id = movie['movieID']
    
    # https://www.fandango.com/killers-of-the-flower-moon-2023-232014/movie-overview?date=2023-10-21
    driver = API.getDriver()
    link = (Constants.link + "/" + name + "-" + id + "/movie-overview?date=" + str(date.today())).lower()
    return link

# Creates json object with showtime of movie
def create_tickets(movie):
    # TODO: Add code that opens original webpage 
    driver = API.getDriver()
    driver.get(get_link(movie))

    # Expand listed theaters
    elem3 = driver.find_element(By.XPATH, "//*[@id='see-more-theaters-btn']")
    elem3.click()
    time.sleep(3)
    
    # Pulls ticket info
    soup = API.getPageSource(driver)
    
    # Create a list of theater names that are showing this movie
    theater_list = soup.find(class_="js-movie-showtimes-content movie-showtimes").find_all(class_="js-movie-showtime-theater movie-showtimes__theater fd-panel dark__section").find_all("a", class_="movie-showtimes__detail-link").text
    
    # Iterate through each theater
    for theater in theater_list:
        # Pull all the showtimes
        showtime_list = soup.find("ol", class_="showtimes-btn-list").find_all("li", class_="showtimes-btn-list__item").find("a").text
        for showtime in showtime_list:
            ticket = {
                "movieID":movie.id,
                "theaterID":theater,
                "showtime":showtime,
                "isPreimuim":""
            }
            # TODO: Add the ticket to the JSON file, make sure we dont add duplicates
            with open('ticket.json', 'w') as json_file:
                json.dump(ticket, json_file, indent=1)

# Load the json object 
with open('movie.json', 'r') as json_file:
    movie_data = json.load(json_file)
    # Iterate through each movie in the json object
    for movie in movie_data:
        create_tickets(movie)