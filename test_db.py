import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

username = "jpfmonteiro"
hash = 1980

# query database for username
rows = db.execute("SELECT * FROM users WHERE username = :username", {"username": username})

    # ensure username exists and password is correct
if len(rows.fetchall()) >= 1:
    print("username already exists")
#rows = db.execute("SELECT * FROM books WHERE year = :book", {"book": book})
#ID = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash) RETURNING id", {"username": username, "hash": hash})
#rows = db.execute("SELECT * FROM users")
#db.commit()
#print(ID.fetchone()[0])
#for row in ID.fetchall():
    #print(row[0])
print("sucess")