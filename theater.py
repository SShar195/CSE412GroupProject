from api import API
import json

class Theater:
    Theaters = []
    
    soup = API.getPageSource()
    ulTag = soup.find(class_="fd-showtimes js-theaterShowtimes-loading").find_all("li", class_="fd-theater")

    with open('theater.json', 'r') as json_file:
        Theaters = json.load(json_file)

    for i in ulTag:
        theaterId = i['data-theater-id']
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

        if data['theaterId'] not in Theaters:
            Theaters.append(data)

    with open('theater.json', 'w') as json_file:
        json.dump(Theaters, json_file, indent=1)
            