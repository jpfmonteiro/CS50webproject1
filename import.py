import csv, psycopg2

conn = psycopg2.connect(database="dccjl8dpu5qv1", user ="ybxklrivkotsnd", password="93c6553e0a2ab0e5c9eccd7ed20c88671791032de441bf55a235d7126393f8d8", host="ec2-54-246-85-151.eu-west-1.compute.amazonaws.com", port="5432")
db=conn.cursor()


with open("books.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        isbn = row["isbn"]
        title = row["title"]
        author = row["author"]
        year = row["year"]
        db.execute("""INSERT INTO BOOKS (ISBN,TITLE,AUTOR,YEAR) VALUES (%s, %s, %s, %s); """, (isbn, title, author, year))
        conn.commit()        

conn.close()

