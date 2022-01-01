from flask import Flask,render_template
from pymongo import MongoClient
import pymongo

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
    return render_template("index.html" , total = x , reserved = a)



@app.route("/reserve")
def reserve():
    return render_template("Reservable.html")

if __name__ == "__main__":
    app.run(debug = True)
      