from flask import Flask,render_template,redirect,url_for
from pymongo import MongoClient

app = Flask(__name__)
myclient = MongoClient('localhost', 27017) 
my_database = myclient["Book"]  
my_collection = my_database["Book"] 


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
    return render_template("DashBoard.html" , total = x , reserved = a)

@app.route("/ToReserve")
def Customers():
    return render_template("Reserve.html")

@app.route("/Books")
def Books():
    return render_template("Books.html")

if __name__ == "__main__":
    app.run(debug = True)
      