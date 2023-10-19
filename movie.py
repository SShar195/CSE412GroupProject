from api import API
from constants import Constants
import json
from datetime import date

class Movie:
    Movies = []
    def getMovies():
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
        
          # Save movie data as JSON
          with open('movie.json', 'w') as json_file:
              json.dump(Movies, json_file, indent=1)

if __name__ == "__main__":
    Movie.extract_movies()
