import csv
import json
from constants import Constants
import psycopg2
import os

# connect = psycopg2.connect(host='localhost', database='CSE412GroupProject', user='user', password='password')
# cursor = connect.cursor()
# sql = '''
# CREATE TABLE theater(theaterId char[] NOT NULL,\
# name char[],\
# streetAddress char[]);
# '''
# cursor.execute(sql)

# with open('theater.csv', 'r') as csv_file:
#     next(csv_file)
#     cursor.copy_from(csv_file, 'theater', sep='|')
# connect.commit()
# Automated Table Creation and Importing

class JsonToCSV:
    @staticmethod
    def csvify(filename):
        with open(f'{filename}.json', 'r') as json_file:
            List = json.load(json_file)

        file = open(f'{filename}.csv', 'w', newline = '')
        csvWriter = csv.writer(file, delimiter=";")

        count = 0
        for i in List:
            if count == 0:
                header = i.keys()
                csvWriter.writerow(header)
                count += 1
            csvWriter.writerow(i.values())
        file.close()