import os, requests, json, urllib3
#from urllib.request import urlopen

def get_books(rows):
    books = {}
    books.clear()
    for row in rows:
        if "id" not in books:
            books["id"] = list()
        books["id"].append(row["id"])
        if "authors" not in books:
            books["authors"] = list()
        books["authors"].append(row["authors"])
        if "isbn" not in books:
            books["isbn"] = list()
        books["isbn"].append(row["isbn"])
        if "title" not in books:
                books["title"] = list()
        books["title"].append(row["title"])
        if "year" not in books:
                books["year"] = list()
        books["year"].append(row["pubdate"])
        if "publisher" not in books:
            books["publisher"] = list()
        books["publisher"].append(row["publisher"])
        if "cover" not in books:
            books["cover"] = list()
        books["cover"].append(row["cover"])
        if "rating" not in books:
            books["rating"] = list()
        books["rating"].append(row["rating"])
        if "series" not in books:
            books["series"] = list()
        books["series"].append(row["series"])
        if "series_index" not in books:
            books["series_index"] = list()
        books["series_index"].append(row["series_index"])
        if "tags" not in books:
            books["tags"] = list()
        books["tags"].append(row["tags"])
        if "booktype" not in books:
            books["booktype"] = list()
        books["booktype"].append(row["booktype"])                       
    return books 

def api_request(isbn):
    key = os.getenv("API_KEY")
    query = "isbn:"+isbn
    params = {"q": query, "key": key}
    url = r"https://www.googleapis.com/books/v1/volumes"
    results = requests.get(url, params=params).json()
    book = {}
    if results:
        if len(results.keys()) >= 3:
                result = results["items"][0]
                book = result["volumeInfo"]
        else:
            print("BOOK NOT FOUND TRY DIFFERENT SEARCH PARAMETERS")
    else:
        print("ERROR")
    return book