from flask import Flask,render_template,redirect,url_for,request
from pymongo import MongoClient

app = Flask(__name__)
myclient = MongoClient('localhost', 27017) 
my_database = myclient["Book"]  
my_collection = my_database["Book"] 
BooksToReserve = my_database["ReservedBooks"]
BooksToAdd_=my_database["BookToAdd"]

@app.route("/")
def home_page():
    mydoc = my_collection.find()
    # Total Books
    x=0
    for i in mydoc:
        x+=1
    reserved = my_collection.find({"reserved" : 1})
    # reserved Books
    a=0
    for y in reserved:
        a+=1
    # Books to reserve
    c=0
    books = BooksToReserve.find({})
    for y in books:
        c+=1
    d=0
    # Books to add
    booksToAdd = BooksToAdd_.find({})
    for y in booksToAdd:
        d+=1
    # list of Recent added books
    last_Add_=reserved = my_collection.find({},{"title":1,"authors":1,"published_year":1,"_id":0}).sort("_id",-1)\
        .sort("published_year",-1).limit(3)
    last_Add=[]
    for i in last_Add_:
        y=[]
        for key, value in i.items():
            y.append(value)
        last_Add.append(y)
    return render_template("DashBoard.html" , total = x ,BookToAdd=d, reserved = a,ToReserve=c,LastAdded=last_Add)

@app.route("/ToReserve",methods=["GET","POST"])
def Customers():
    if request.method == "POST":
        print(request.form.get("testing"))
        
        if request.form.get("Cancelation_i"):
            # Cancel a reservation request
            BooksToReserve.delete_one({"Full Name":request.form.get("Cancelation_i")})
        if request.form.get("Validation_i"):
            # Confirm a reservation request
            i=BooksToReserve.find({"Full Name":request.form.get("Validation_i")})
            Book={}
            for y in i:
                for key, value in y.items():
                    Book=value
            # Update books list
            my_collection.update_one({"title":Book},{"$set":{"reserved":2}})
            # delete the reservation from collection
            BooksToReserve.delete_one({"Full Name":request.form.get("Validation_i")})
    # Find all reservation requests
    books = BooksToReserve.find({})
    y=0
    BooksRes=[]
    for i in books:
        y=[]
        for key, value in i.items():
            y.append(value)
        BooksRes.append(y)
    return render_template("Reserve.html",ToReserve=BooksRes,Data=BooksRes)
    

@app.route("/Books")
def Books():
    # Get information on all the books
    books = my_collection.find({},{"title":1,"authors":1,"published_year":1,"_id":0})
    Books=[]
    for i in books:
        y=[]
        for key, value in i.items():
            y.append(value)
        Books.append(y)
    return render_template("Books.html",Books=Books)
@app.route("/BooksToAdd",methods=["GET","POST"])
def BooksToAdd():
    # Get selected book in to add collection
    b = BooksToAdd_.find({"title":request.form.get("title")})
    c={}
    for i in b:
        for key,value in i.items():
            c[key]=value
    if(request.form.get("ADDBOOK")):
        # Confirm adding book
        try:
            my_collection.insert_one(c)
        except(Exception):
            print("")
        # delete book from Books to add collection
        BooksToAdd_.delete_one(c)
    if(request.form.get("CANCELBOOK")):
        # delete book from Books to add collection
        BooksToAdd_.delete_one(c)
    # Get all the books in to add collection
    books = BooksToAdd_.find({"title":{"$exists":True},"authors":{"$exists":True},\
            "categories":{"$exists":True},"published_year":{"$exists":True}},\
            {"_id":1,"title":1,"authors":1,"categories":1,"published_year":1}).limit(50)
    BooksToAdd=[]
    for i in books:
        y=[]
        for key, value in i.items():
            y.append(value)
        BooksToAdd.append(y)
    return render_template("BooksToAdd.html",ToAdd=BooksToAdd)


if __name__ == "__main__":
    app.run(debug = True,port =5818)