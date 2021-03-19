import pymongo
from sites import NASA_Mars_News_Site, JPL_Featured_Space_Image, Mars_Facts, USGS_Astrogeology_site
from scape import scrape_Nasa_Mars_news, scrape_JPL_Mars_Space_images, scrape_Mars_fact, scrape_Mars_hemispheres, quit_browser

# Initialize Pymongo to work with MongoDB
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

a_dict = {}
a_dict["news_title"], a_dict["news_p"] = scrape_Nasa_Mars_news(NASA_Mars_News_Site)
a_dict["featured_image_url"] = scrape_JPL_Mars_Space_images(JPL_Featured_Space_Image)
a_dict["mars_facts_df"] = scrape_Mars_fact(Mars_Facts)
a_dict["mars_hemispheres"] = scrape_Mars_hemispheres(USGS_Astrogeology_site)
quit_browser()
print(a_dict)

# Define Database and Collection
db = client.Mars_db
collection = db.mars
collection.insert_one(a_dict)

