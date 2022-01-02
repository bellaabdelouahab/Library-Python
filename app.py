from flask import Flask,render_template,redirect,url_for,request
from pymongo import MongoClient

app = Flask(__name__)
myclient = MongoClient('localhost', 27017) 
my_database = myclient["Book"]  
my_collection = my_database["Book"] 
BooksToReserve = my_database["ReservedBooks"]


@app.route("/")
def home_page():
    # number of documents in the collection
    mydoc = my_collection.find()
    x=0
    for i in mydoc:
        x+=1
    reserved = my_collection.find({"reserved" : 1})
    a=0
    for y in reserved:
        a+=1
    c=0
    books = BooksToReserve.find({})
    for y in books:
        c+=1
    return render_template("DashBoard.html" , total = x , reserved = a,ToReserve=c)

@app.route("/ToReserve",methods=["GET","POST"])
def Customers():
    if request.method == "POST":
        if request.form.get("Cancelation_i"):
            BooksToReserve.delete_one({"Full Name":request.form.get("Cancelation_i")})
        if request.form.get("Validation_i"):
            i=BooksToReserve.find({"Full Name":request.form.get("Validation_i")})
            Book={}
            for y in i:
                for key, value in y.items():
                    Book=value
            print(Book)
            my_collection.update_one({"title":Book},{"$set":{"reserved":2}})
            BooksToReserve.delete_one({"Full Name":request.form.get("Validation_i")})
    books = BooksToReserve.find({})
    y=0
    BooksRes=[]
    for i in books:
        y=[]
        for key, value in i.items():
            y.append(value)
        BooksRes.append(y)
    return render_template("Reserve.html",ToReserve=BooksRes)
    

@app.route("/Books")
def Books():
    books = my_collection.find({},{"title":1,"authors":1,"published_year":1,"_id":0})
    y=0
    Books=[]
    for i in books:
        y=[]
        for key, value in i.items():
            y.append(value)
        Books.append(y)
    return render_template("Books.html",Books=Books)

if __name__ == "__main__":
    app.run(debug = True)
      