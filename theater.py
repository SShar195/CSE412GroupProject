from api import API
from constants import Constants
import json
from datetime import date

class Theater:
    Theaters = []
    def getTheaters(Theaters ,tag):
        with open('theater.json', 'r') as json_file:
            Theaters = json.load(json_file)

        for i in tag:
            theaterId = i['data-theater-id']
            if theaterId not in Theaters:
                name = i.find("a").text.strip()
                span = i.find(class_="fd-theater__address-wrap dark__text--secondary").text
                streetAddress = ""
                for j in span.split("\n"):
                    if(j.strip()):
                        streetAddress += " " + j.strip()
                data = {
                    "theaterId" : theaterId,
                    "name" : name,
                    "streetAddress" : streetAddress 
                }
                Theaters.append(data)
                with open('theater.json', 'w') as json_file:
                    json.dump(Theaters, json_file, indent=1)
    
    for i in Constants.theaterLinkMap.values():
        soup = API.getPageSource(i + "?date=" + str(date.today()))
        ulTag = soup.find(class_="fd-showtimes js-theaterShowtimes-loading").find_all("li", class_="fd-theater")
        getTheaters(Theaters, ulTag)
            