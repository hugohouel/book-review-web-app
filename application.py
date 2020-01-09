import os

from flask import Flask, session, render_template, request, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

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

@app.route("/", methods=['GET', 'POST'])
def index():
    # is_logged = session.get('user_logged')
    # username = request.form.get("username")
    # password = request.form.get("password ")
    # if db.execute('SELECT * FROM users WHERE username = :username AND password = :password',
    # {'username': username, 'password': password}).rowcount == 1:
    #     pass
    if 'username' not in session:
        login = 'NOT LOGGED IN'
    else:
        login = 'LOGGED IN as {}'.format(session['username'])
    return render_template('welcome.html', login=login)


@app.route('/create_account', methods=['POST'])
def create_account():
    username = request.form.get("sign_in_username")
    password = request.form.get("sign_in_password")
    if db.execute('SELECT * FROM users WHERE username = :username', {'username': username}).rowcount == 1:
        return render_template('error.html', message='Username already exists, choose another one.')
    db.execute('INSERT INTO users (username, password) VALUES (:username, :password)',
               {'username': username, 'password': password})
    db.commit()
    return render_template('welcome.html', message='Your account was created successfully. Please log in now.')


@app.route('/log_in', methods=['POST'])
def log_in():
    username = request.form.get("log_in_username")
    password = request.form.get("log_in_password")
    if db.execute('SELECT * FROM users WHERE username = :username AND password = :password',
                  {'username': username, 'password': password}).rowcount == 0:
        return render_template('error.html', message='Incorrect Credentials. Please try again')
    session['username'] = username
    return render_template('welcome.html', login='LOGGED_IN as {}'.format(username))


@app.route("/search_page", methods=['GET', 'POST'])
def search_page():

    if 'username' not in session:
        return render_template('error.html', message='You are not logged in. Please go back to home and log in.')

    return render_template('search_page.html', username=session.get('username') )


@app.route("/search", methods=['GET', 'POST'])
def search():
    query = request.form.get("input_query")
    propositions = db.execute("SELECT * FROM books WHERE author LIKE '%{}%' "
                              "OR title LIKE '%{}%'"
                              "OR isbn LIKE '%{}%'".format(query.capitalize(), query.capitalize(), query)).fetchall()
    if len(propositions) > 0:
        return render_template('search_page.html', message='We found the following books :', propositions=propositions)
    return render_template('search_page.html', message='We performed the request but could not find any matches.')


@app.route("/log_out")
def log_out():
    if 'username' in session:
        del session['username']
    return render_template('welcome.html', login='NOT LOGGED IN' )


@app.route("/book/<string:isbn>")
def book(isbn):
    info = db.execute("SELECT * FROM books WHERE isbn = :isbn", {'isbn': isbn}).fetchall()[0]
    reviews = db.execute("SELECT * FROM reviews WHERE isbn = :isbn", {'isbn': isbn}).fetchall()

    has_reviews = len(reviews) > 0
    has_goodreads_ratings = len(info) == 6

    if len(info) == 6:
        nb_ratings = info[4]
        avg_ratings = info[5]

    return render_template('book.html', info=info, reviews=reviews,
                           has_goodreads_ratings=has_goodreads_ratings, has_reviews=has_reviews)

@app.route("/book/add_review/<string:isbn>", methods=['GET', 'POST'])
def add_review(isbn):
    rating = request.form.get("rating")
    comment = request.form.get("comment")
    review_allowed = len(db.execute("SELECT * FROM reviews WHERE isbn = :isbn AND username = :username", {'isbn': isbn, 'username': session['username']}).fetchall()) == 0
    if review_allowed:
        db.execute("INSERT INTO reviews (rating, comment, username, isbn) VALUES (:rating, :comment, :username, :isbn)",
                   {'rating': rating, 'comment': comment, 'isbn': isbn, 'username': session['username']})
        db.commit()
        message = 'Your review for ISBN {} has been added.'.format(isbn)
    else:
        message = "You cannot submit more than one review for the same book"
    return render_template('after_comment.html', message=message)


@app.route("/api/<string:isbn>", methods=['GET'])
def book_api(isbn):
    req = db.execute("SELECT * FROM books WHERE isbn = :isbn", {'isbn': isbn}).fetchall()

    if len(req) > 0:
        info = req[0]
        res = {'title': info[1],
               'author': info[2],
                'year': info[3],
                'isbn': info[0],
                'review_count': info[4],
                'average_score': info[5]}
        return jsonify(res)
    else:
        return jsonify({'error': 'no book found with this ISBN'}), 404

