from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from helpers import get_books
import csv, os

# Set up database
db = create_engine(os.getenv("DATABASE_URL"))

meta = MetaData(db)

#books = Table(
 #   'books', meta,
  #  Column('id', Integer, primary_key = True),
   # Column('authors', String),
    #Column('isbn', String),
    #Column('title', String),
    #Column('pubdate', String),
    #Column('publisher', String),
    #Column('cover', String),
    #Column('rating', String),
    #Column('series', String),
    #Column('series_index', String),
    #Column('tags', String),
    #Column('booktype', String),
#)


books = get_books(db.execute("SELECT * FROM books").fetchall())
print(len(books))
print(books)
    #books.create()
    #with open("mybooks.csv", "r") as file:
        #reader = csv.DictReader(file)
        #for row in reader:
            #pubdate = row["pubdate"]     
            #insert_statement = books.insert().values(authors = row["authors"], isbn = row["isbn"], title = row["title"], pubdate = pubdate[:4], publisher = row["publisher"], cover = row["cover"], rating = row["rating"], series = row["series"], series_index = row["series_index"], tags = row["tags"], booktype = "ebook")
            #conn.execute(insert_statement)

