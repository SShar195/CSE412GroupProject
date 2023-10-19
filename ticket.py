from api import API
from constants import Constants
import json
from datetime import date
import time

# import api

with open('theater.json', 'r') as json_file:
    Theaters = json.load(json_file)

name = Theaters[0]['name'].replace(' ', '-')
id = Theaters[0]['theaterId']

driver = API.getDriver()
link = (Constants.link + "/" + name + "-" + id + "/theater-page?format=all").lower()
print(link)
driver.get(link)