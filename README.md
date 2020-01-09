# Project 1 - Web Programming with Python and JavaScript - Book Review

## Brief Presentation

This project implements a book review website. 
It allows for logged in users to search for books by ISBN, title, or author.
Once a given book is selected, the user can consult informations about it and reviews left by others. 
User can also leave his own feedback.

## DataBases

To work, this web app requires 3 tables (as suggested :) ) :
- one managing the reviews
- one managing the users
- one managing the books.

## Getting started

To use this, you may want to follow the following steps :
0. To make sure you have all the required package, you may want to use "pip install requirements.txt".
1. run the 3 SQL requests that are into "table_initialization" : this will create the tables.
2. run import.py, that will import the books from the .csv into the books table. This will also call the goodreads API and log this useful info.
3. run the command flask run, when at the root.


