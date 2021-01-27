import os
import psycopg2
import isbnlib
from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flaskhelpers import *

#from helpers import *
from passlib.apps import custom_app_context as pwd_context

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

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    #if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        #ensure username was submitted
        if not request.form.get("search_term"):
            return apology("Must submit a query")
        
        #query database for title
        if request.form.get("search_value") == "title":
            rows = db.execute("SELECT * FROM books WHERE title = :title", {"title": request.form.get("search_term")}).fetchall()
            books = {}
            for row in rows:
                if "isbn" not in books:
                    books["isbn"] = list()
                books["isbn"].append(row["isbn"])
                if "title" not in books:
                    books["title"] = list()
                books["title"].append(row["title"])
                if "author" not in books:
                    books["author"] = list()
                books["author"].append(row["autor"])
                if "year" not in books:
                    books["year"] = list()
                books["year"].append(row["year"]) 
            return render_template("listed_books.html", books=books)
        
        elif request.form.get("search_value") == "author":
            rows = db.execute("SELECT * FROM books WHERE autor = :author", {"author": request.form.get("search_term")}).fetchall()
            books = {}
            for row in rows:
                if "isbn" not in books:
                    books["isbn"] = list()
                books["isbn"].append(row["isbn"])
                if "title" not in books:
                    books["title"] = list()
                books["title"].append(row["title"])
                if "author" not in books:
                    books["author"] = list()
                books["author"].append(row["autor"])
                if "year" not in books:
                    books["year"] = list()
                books["year"].append(row["year"]) 
            
            return render_template("listed_books.html", books=books)

        elif request.form.get("search_value") == "ISBN":
            rows = db.execute("SELECT * FROM books WHERE isbn = :ISBN", {"ISBN": request.form.get("search_term")}).fetchall()
            books = {}
            for row in rows:
                if "isbn" not in books:
                    books["isbn"] = list()
                books["isbn"].append(row["isbn"])
                if "title" not in books:
                    books["title"] = list()
                books["title"].append(row["title"])
                if "author" not in books:
                    books["author"] = list()
                books["author"].append(row["autor"])
                if "year" not in books:
                    books["year"] = list()
                books["year"].append(row["year"]) 
            return render_template("listed_books.html", books=books)
        else:
            rows = db.execute("SELECT * FROM books WHERE year = :year", {"year": request.form.get("search_term")}).fetchall()
            books = {}
            for row in rows:
                if "isbn" not in books:
                    books["isbn"] = list()
                books["isbn"].append(row["isbn"])
                if "title" not in books:
                    books["title"] = list()
                books["title"].append(row["title"])
                if "author" not in books:
                    books["author"] = list()
                books["author"].append(row["autor"])
                if "year" not in books:
                    books["year"] = list()
                books["year"].append(row["year"]) 
            return render_template("listed_books.html", books=books)
        #query database for author
        #elif not request.form.get("author")and not request.form.get("ISBN"):

        #query database for ISBN
        #elif not request.form.get("title")and not request.form.get("author"):
    return render_template("index.html")

@app.route("/listed_books/<books>")
@login_required
def listed_books(books):
    return render_template("listed_books.html", books=books)

@app.route("/Book/<string:isbn>", methods=["GET", "POST"])
@login_required
def Book(isbn):
    try:
        image = isbnlib.cover(isbn)
        description = isbnlib.desc(isbn)
        cover = image['thumbnail']
    except:
        print("Error with isbnlib")
        cover = "error"
        description = "error"
    return render_template("Book.html", cover=cover, description=description)

@app.route("/author", methods=["GET", "POST"])
@login_required
def author():
        #if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        #return redirect(url_for('author.html'))

    return render_template("author.html")

@app.route("/ISBN", methods=["GET", "POST"])
@login_required
def ISBN():
    return render_template("ISBN.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    #forget any user_id
    session.clear()

    #if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        #ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        #ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        #query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", {"username": request.form.get("username")}).fetchone()
        print(rows)
        #ensure username exists and password is correct
        if rows is None or not pwd_context.verify(request.form.get("password"), rows[2]):
            return apology("invalid username and/or password")

        #remember which user has logged in
        session["user_id"] = rows[0]

        #redirect user to home page
        return redirect(url_for("index"))

    #else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    #forget any user_id
    session.clear()

    #redirect user to login form
    return redirect(url_for("login"))
    
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    #forget any user_id
    session.clear()

    #if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        #ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        #ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")
        elif len(request.form.get("password")) < 8 or len(request.form.get("password")) > 16:
            return apology("Password must have between 8 and 16 characters")
        elif not request.form.get("password-confirmation"):
            return apology("must confirm password")
        elif request.form.get("password") != request.form.get("password-confirmation"):
            return apology("passwords do not match")

        username = request.form.get("username")
        
        #query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", {"username": username})

        #ensure username exists and password is correct
        if len(rows.fetchall()) >= 1:
            return apology("username already exists")

        #Builds password hash
        hashedpwd = pwd_context.hash(request.form.get("password"))

        #Inserts username and hashed password in db
        ID = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash) RETURNING id", {"username": username, "hash": hashedpwd})
        db.commit()
        session["user_id"] = ID.fetchone()[0]
        #print(session["user_id"])
        return redirect(url_for("index"))
         
        # remember which user has logged in
        session["user_id"] = ID

        # redirect user to home page
        return redirect(url_for("index"))


    return render_template("register.html")