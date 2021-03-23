from flask import Flask, render_template, redirect
import pymongo
import pandas as pd
import scrape_mars
from sites import NASA_Mars_News_Site, JPL_Featured_Space_Image, Mars_Facts, USGS_Astrogeology_site
from scrape import scrape_Nasa_Mars_news, scrape_JPL_Mars_Space_images, scrape_Mars_fact, scrape_Mars_hemispheres, quit_browser
from config import ATLAS_PASSWORD

# Localhost mongodb
# local_connection = 'mongodb://localhost:27017'
# client = pymongo.MongoClient(local_connection)

# Online atlas host mongodb
atlas_connection = f"mongodb+srv://simon:{ATLAS_PASSWORD}@cluster0.23jm7.mongodb.net/retryWrites=true&w=majority"
client = pymongo.MongoClient(atlas_connection)


app = Flask(__name__)

# Create a root route `/` that will query your Mongo database and pass the mars data into an HTML template to display the data.
@app.route("/")
def landing_page():
    mars_data = client.Mars_db.mars.find_one()
    table_string = pd.read_json(mars_data["mars_facts_df"]).to_html().replace("dataframe", "table table-striped")
    print(table_string)
    return render_template("index.html", data=mars_data, table_string=table_string)


# create a route called `/scrape` that will import your `scrape_mars.py` script and call your `scrape` function.
@app.route("/scrape")
def scraping():
    data = client.Mars_db.mars.find_one()
    id = data["_id"]
    news_title, news_p = scrape_Nasa_Mars_news(NASA_Mars_News_Site)
    featured_image_url = scrape_JPL_Mars_Space_images(JPL_Featured_Space_Image)
    mars_facts_df = scrape_Mars_fact(Mars_Facts)
    mars_hemispheres = scrape_Mars_hemispheres(USGS_Astrogeology_site)
    client.Mars_db.mars.update({"_id": id}, {"$set": {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_facts_df": mars_facts_df,
        "mars_hemispheres": mars_hemispheres
    }})


    # client.Mars_db.mars.update_one({}, data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)