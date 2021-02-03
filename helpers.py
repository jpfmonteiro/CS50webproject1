            
def get_books(rows):
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
    return books 
