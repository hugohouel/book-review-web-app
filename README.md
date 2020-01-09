# Book Review Wep Application

## Brief Presentation

This project implements a book review website. 
It allows for logged in users to search for books by ISBN, title, or author.
Once a given book is selected, the user can consult informations about it and reviews left by others, as well as leave his own feedback.

## DataBases

To work, this app requires 3 tables managing:
- reviews
- users
- books.

## Getting started

Follow the following steps :
* To make sure you have all the required package, run
```
pip install requirements.txt
```
* Assuming you have already setup a SQL database environement, set the DATABASE_URL environement variable. Then run the 3 SQL commands that are into "table_initialization" : this will create the tables.
* run 
```
python import.py
```
which will import the books from the .csv into the books table, call the goodreads API and log the data into the database.
* To launch the app : 
```
flask run
```

## Acknowledgement

This was my first Flask project. Any review on the code is more than welcomed.
