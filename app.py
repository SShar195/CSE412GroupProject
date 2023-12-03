from flask import Flask, render_template, request
import requests
import psycopg2
import requests
import os
import csv
from dotenv import load_dotenv
from tabulate import tabulate

load_dotenv()

app = Flask(__name__, template_folder="templates")

username_secret = os.getenv("DATABASE_USERNAME") # Make sure you have a .env file with all three of these in it
password_secret = os.getenv("DATABASE_PASSWORD")
database_secret = os.getenv("DATABASE_NAME")

connection = psycopg2.connect(host='localhost', database = database_secret, user = username_secret, password = password_secret)
cursor = connection.cursor()
connection = psycopg2.connect(host='localhost', database = database_secret, user = username_secret, password = password_secret)
cursor = connection.cursor()

ticket_table = '''
    CREATE TABLE IF NOT EXISTS ticket (
        movieID VARCHAR(6),
        theaterID VARCHAR(5),
        showtime VARCHAR(5),
        seat VARCHAR(3),
        isMatinee BOOLEAN,
        price VARCHAR(6)
    )'''
ticket_table = '''
    CREATE TABLE IF NOT EXISTS ticket (
        movieID VARCHAR(6),
        theaterID VARCHAR(5),
        showtime VARCHAR(5),
        seat VARCHAR(3),
        isMatinee BOOLEAN,
        price VARCHAR(6)
    )'''

movie_table = '''
    CREATE TABLE IF NOT EXISTS movie (
        title VARCHAR(124),
        movieID VARCHAR(6)
    )'''

theater_table = '''
    CREATE TABLE IF NOT EXISTS theater (
        theaterID VARCHAR(5),
        name VARCHAR(124),
        StreetAddress VARCHAR(248)
    )'''

cursor.execute(ticket_table)
cursor.execute(movie_table)
cursor.execute(theater_table)

with open('ticket.csv', 'r') as f:
    next(f) # Skip the header row.
    cursor.copy_from(f, 'ticket', sep=';')

with open('theater.csv', 'r') as f:
    next(f)
    cursor.copy_from(f, 'theater', sep=',')

with open('movie.csv', 'r') as f:
    next(f)
    cursor.copy_from(f, 'movie', sep=';')

connection.commit()
connection.close()
cursor.close()

@app.route('/')
def homepage():
    return render_template(r'homepage.html')

@app.route('/movie_info.html')
def movie_info():
    # Retrieve movieID from query parameters
    movie_id = request.args.get("movie_id")
    print(movie_id)

    # Fetch movie data based on the movie_id
    connection = psycopg2.connect(host='localhost', database=database_secret, user=username_secret, password=password_secret)
    cursor = connection.cursor()

    cursor.execute(f"SELECT * FROM movie WHERE movieID = '{movie_id}'")
    movie_data = cursor.fetchone()  # Assuming one row for a movie ID
    print(movie_data)

    cursor.close()

    # Fetch ticket data for the selected movieID
    cursor = connection.cursor()

    cursor.execute(f"SELECT theater.name, showtime, seat, ismatinee, price FROM ticket JOIN theater ON ticket.theaterid = theater.theaterid WHERE movieID = '{movie_id}' ORDER BY price ASC LIMIT 10;")
    ticket_data = cursor.fetchall()
    print('sucsess')

    cursor.close()
    connection.close()

    # ticket_table = tabulate(ticket_data, tablefmt='html')
    # print(ticket_table)

    # Pass both movie and ticket data to the template
    return render_template('movie_info.html', movie=movie_data, tickets=ticket_data)

if __name__ == '__main__':
    app.run(debug=True)
