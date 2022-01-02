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
    d=0
    booksToAdd = BooksToAdd_.find({})
    for y in booksToAdd:
        d+=1
    last_Add=reserved = my_collection.find().sort("_id",-1).limit(10)
    return render_template("DashBoard.html" , total = x ,BookToAdd=d, reserved = a,ToReserve=c,LastAdded=last_Add)

@app.route("/ToReserve",methods=["GET","POST"])
def Customers():
    if request.method == "POST":
        print(request.form.get("testing"))
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
    Books=[]
    for i in books:
        y=[]
        for key, value in i.items():
            y.append(value)
        Books.append(y)
    return render_template("Books.html",Books=Books)
@app.route("/BooksToAdd",methods=["GET","POST"])
def BooksToAdd():
    b = BooksToAdd_.find({"title":request.form.get("title")})
    c={}
    for i in b:
        for key,value in i.items():
            c[key]=value
    if(request.form.get("ADDBOOK")):
        
        
        try:
            my_collection.insert_one(c)
        except(Exception):
            print("")
        BooksToAdd_.delete_one(c)
    if(request.form.get("CANCELBOOK")):
        BooksToAdd_.delete_one(c)
    books = BooksToAdd_.find({"title":{"$exists":True},"authors":{"$exists":True},"categories":{"$exists":True},"published_year":{"$exists":True}},{"_id":1,"title":1,"authors":1,"categories":1,"published_year":1}).limit(50)
    BooksToAdd=[]
    for i in books:
        y=[]
        for key, value in i.items():
            y.append(value)
        BooksToAdd.append(y)
    return render_template("BooksToAdd.html",ToAdd=BooksToAdd)


if __name__ == "__main__":
    app.run(debug = True,port =5817)