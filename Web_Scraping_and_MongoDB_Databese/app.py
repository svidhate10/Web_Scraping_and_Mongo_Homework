from flask import Flask, render_template, jsonify, redirect

import scrape_mars
import pymongo

app = Flask(__name__)
#conn = 'mongodb://localhost:27017'
#client = pymongo.MongoClient(conn)

mongo = pymongo(app, uri="mongodb://localhost:27017")
mongo = pymongo(app)


@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

# Scrape Data and pull into Mongo DB
@app.route('/scrape')
def get():
    mars = mongo.db.mars
    marsdata = scrape_mars.scrape()
    mars.update({}, marsdata, upsert=True)
    return redirect("/", code=302)



if __name__ == "__main__":
    app.run()