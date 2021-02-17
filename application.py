import os, psycopg2, isbnlib, json
from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flaskhelpers import *
from helpers import *
from passlib.apps import custom_app_context as pwd_context

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")
if not os.getenv("API_KEY"):
    raise RuntimeError("API_KEY is not set")

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
            books = get_books(db.execute("SELECT * FROM books WHERE title = :title", {"title": request.form.get("search_term")}).fetchall())
            return render_template("listed_books.html", books=books)
        #query database for author
        elif request.form.get("search_value") == "author":
            books = get_books(db.execute("SELECT * FROM books WHERE authors = :author", {"author": request.form.get("search_term")}).fetchall())
            return render_template("listed_books.html", books=books)
        #query database for ISBN
        elif request.form.get("search_value") == "ISBN":
            books = get_books(db.execute("SELECT * FROM books WHERE isbn = :ISBN", {"ISBN": request.form.get("search_term")}).fetchall())
            return render_template("listed_books.html", books=books)
        #query database for year
        elif request.form.get("search_value") == "year":
            books = get_books(db.execute("SELECT * FROM books WHERE pubdate = :year", {"year": request.form.get("search_term")}).fetchall())
            return render_template("listed_books.html", books=books)
        #list books by tag
        elif request.form.get("search_value") == "tag":
            search_value = request.form.get("search_term")
            search_term = "%" + search_value + "%"
            books = get_books(db.execute("SELECT * FROM books WHERE tags ILIKE :tag", {"tag": search_term}).fetchall())
            return render_template("listed_books.html", books=books)
        #list books by type
        else:
            books = get_books(db.execute("SELECT * FROM books").fetchall())
            return render_template("listed_books.html", books=books)  

    return render_template("index.html")

@app.route("/listed_books/<books>")
@login_required
def listed_books(books):
    return render_template("listed_books.html", books=books)

@app.route("/Book/<id>", methods=["GET", "POST"])
@login_required
def Book(id):
    book = get_books(db.execute("SELECT * FROM books WHERE id = :id", {"id": id}).fetchall())
    try:
        image = isbnlib.cover(book["isbn"][0])
        description = isbnlib.desc(book["isbn"][0])
        cover = image['thumbnail']
    except:
        #print("ISBN", book.isbn[0])
        cover = book["cover"][0]
        print(cover)
        description = "No description available"
    return render_template("Book.html", cover=cover, description=description, id=id)

@app.route("/view_reviews/<string:isbn>", methods=["GET", "POST"])
@login_required
def view_reviews(isbn):
    book = api_request(isbn)
    if len(book.keys()) < 1:
        return apology("UPS... SOMETHING WENT WRONG")
    volume = book["categories"]
    #volume = volumes[0]
    #print(volume["volumeInfo"])
    #print("new", volume["authors"])
    #print("book:", book)
        #if request.method == 'POST':
        # do stuff when the form is submitted
        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        #return redirect(url_for('author.html'))

    return render_template("view_reviews.html", book=volume)

@app.route("/make_reviews.html/", methods=["GET", "POST"])
@login_required
def make_reviews():
        #if request.method == 'POST':
        # do stuff when the form is submitted
    print("isbn")
        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        #return redirect(url_for('author.html'))

    return render_template("make_reviews.html")

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