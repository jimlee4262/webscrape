#dependencies
from flask import Flask, url_for, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#create flask setup
app = Flask(__name__)

#establish mongoDB connection w/ pymongo
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

#render index.html template using data from Mongo
@app.route("/")
def index():
    #Find data with mongoDB
    mars = mongo.db.mars.find_one()
    

    print(mars)
    #return template & data
    return render_template("index.html", mars=mars)

#trigger scrape fxn
@app.route("/scrape")
def scraper():
    mars_information=scrape_mars.scrape()

    #update mongoDB update & upsert
    mongo.db.mars.update({}, mars_information, upsert=True)

    #redirect home
    return redirect("/")

if __name__ == "__main__":
    app.run(debug = True)
