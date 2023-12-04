from api import API
from constants import Constants
import json
from datetime import date
import time
from selenium.webdriver.common.by import By
import random

ticketTimes = ['07:00', '07:15', '07:30', '07:45',
            '08:00', '08:15', '08:30', '08:45',
            '09:00', '09:15', '09:30', '09:40',
            '10:00', '10:15', '10:30', '10:45',
            '11:00', '11:15', '11:30', '11:55',
            '12:00', '12:15', '12:30', '12:45',
            "13:15", "13:30", "13:45", "13:50",
            "14:00", "14:15", "14:30", "14:45",
            "15:00", "15:15", "15:30", "15:45",
            "16:00", "16:15", "16:30", "16:45",
            "17:00", "17:15",'17:20', "17:30", 
            "17:45", "17:50","18:00", "18:15", 
            '18:20', "18:30", '18:35', "18:45",
            "19:00", "19:15", "19:30", "19:45",
            "20:00", "20:15", "20:30", "20:45",
            "21:00", "21:15", "21:30", "21:45",
            "22:00", "22:15", "22:30", "22:45",
            "23:00", "23:15", "23:30", "23:45"
            ]
ticketRows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']
ticketColumn = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']
averagePriceMap = {
    "AMC": "$16.50",
    "LOOK": "$16.00",
    "Harkins": "$16.50",
    "Majestic": "$16.00",
    "Cinemark": "$16.50",
    "FatCats": "$16.00",
    "Landmark": "$17.00",
    "Majestic": "$16.00",
    "Picture": "$16.50",
    "Regal": "$16.50",
    "RoadHouse": "$16.00",
    "The": "$17.00",
    "Touchstar": "$16.50",
    "America": "$18.00"
}

averageMatineePriceMap = {
    "AMC": "$12.50",
    "LOOK": "$12.00",
    "Harkins": "$12.50",
    "Majestic": "$12.00",
    "Cinemark": "$12.50",
    "FatCats": "$12.00",
    "Landmark": "$13.00",
    "Majestic": "$12.00",
    "Picture": "$12.50",
    "Regal": "$12.50",
    "RoadHouse": "$12.00",
    "The": "$13.00",
    "Touchstar": "$12.50",
    "America": "$14.00"
}


# Creates link used in create_tickets
def get_link(movie):

    # Pull the movie information
    name = movie['title'].replace(' ', '-')
    name = name.replace('(','')
    name = name.replace(')', '')
    id = movie['movieID']
    
    # https://www.fandango.com/killers-of-the-flower-moon-2023-232014/movie-overview?date=2023-10-21
    # https://www.fandango.com/killers-of-the-flower-moon-2023-0/movie-overview?date=2023-10-21
    driver = API.getDriver()
    link = (Constants.link + "/" + name + "-" + str(id) + "/movie-overview?date=" + str(date.today())).lower()
    return link

def weeklyTickets():
    #for each movie generate 15 showtimes per day, then create tickets according to that information
    #for each theater, choose 6 - 12 random movies
    
    with open('movie.json', 'r') as json_file:
        Movies = json.load(json_file)

    with open('theater.json', 'r') as json_file:
        Theaters = json.load(json_file)

    with open('ticket.json', 'r') as json_file:
        Tickets = json.load(json_file)

    for theater in Theaters:
        for i in range(1, 7):
            theDate = f"11/{i+18}"
            showtime =  random.choice(ticketTimes)
            for row in ticketRows:
                for column in ticketColumn:
                    if ticketTimes.index(showtime) < 44:
                        isMatinee = True
                    else: isMatinee = False

                    if isMatinee:
                        price = averageMatineePriceMap[theater['name'][:theater['name'].index(" ")]]
                    else:
                        price = averagePriceMap[theater['name'][:theater['name'].index(" ")]]
                    data = {
                        "movieID": random.choice(Movies)['movieID'],
                        "theaterID": theater['theaterId'],
                        "showtime": showtime,
                        "date": theDate,
                        "seat": row + column,
                        "isMatinee": isMatinee,
                        "price": price
                    }
                    Tickets.append(data)
    with open('ticket.json', 'w') as json_file:
        json.dump(Tickets, json_file, indent=1)
    pass

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
    theater_list = soup.find_all("div", _class="js-movie-showtime-theater movie-showtimes__theater fd-panel dark__section")
    
    # Iterate through each theater
    for theater in theater_list:
        theaterId = theater.find_all("a", class_="movie-showtimes__detail-name")
        print(theaterId)

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
# with open('movie.json', 'r') as json_file:
#     movie_data = json.load(json_file)
#     # Iterate through each movie in the json object
#     for movie in movie_data:
#         create_tickets(movie)

# json_file.close()

weeklyTickets()