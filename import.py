"""
This file imports the 5000 books from the CSV in the table books.

For each book, it calls the API and stores the number of ratings it received on Goodreads, and the average rating.
"""

import os

from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import csv

import requests
import json

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

db.execute("CREATE TABLE books (isbn VARCHAR PRIMARY KEY, "
           "title VARCHAR NOT NULL, "
           "author VARCHAR NOT NULL, "
           "year INTEGER NOT NULL,"
           "nb_ratings INTEGER,"
           "avg_ratings REAL)")

f = open('books.csv')
reader = csv.reader(f)
first_row = next(reader)

for isbn, title, author, year in reader:

    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": 'f19o4gh6FnE7AptGTivqQ', "isbns": isbn})

    try:
        dic = res.json()
        nb_ratings = int(dic['books'][0]['work_ratings_count'])
        avg_ratings = float(dic['books'][0]['average_rating'])

        db.execute("INSERT INTO books (isbn, title, author, year, nb_ratings, avg_ratings)"
                   "VALUES (:isbn, :title, :author, :year, :nb_ratings, :avg_ratings)",
                   {"isbn": isbn, "title": title, "author": author, "year": int(year), "nb_ratings": nb_ratings, "avg_ratings": avg_ratings})

    except json.decoder.JSONDecodeError:
        db.execute("INSERT INTO books (isbn, title, author, year)"
                   "VALUES (:isbn, :title, :author, :year)",
                   {"isbn": isbn, "title": title, "author": author, "year": int(year)})

    db.commit()
