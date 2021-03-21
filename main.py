from flask import Flask, render_template, redirect
import pymongo
import pandas as pd
import scrape_mars

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

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
    data = scrape_mars.scrape_mars()
    client.Mars_db.mars.update({}, data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)