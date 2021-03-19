from bs4 import BeautifulSoup
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import json

# from sites import NASA_Mars_News_Site, JPL_Featured_Space_Image, Mars_Facts, USGS_Astrogeology_site

# Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


def scrape_Nasa_Mars_news(url):
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    gallery = soup.find(class_='grid_gallery')
    news_title = gallery.find(class_='content_title').text
    news_p = gallery.find(class_='article_teaser_body').text
    # browser.quit()
    return news_title, news_p


def scrape_JPL_Mars_Space_images(url):
    browser.visit(url)
    # Handle search
    browser.find_by_tag('input').first.fill('Featured Mars')
    # Handle Sortby
    browser.find_by_id('searchHelpers_sortBy').first.select('latestDate')
    # results = browser.find_by_id('SearchListingPageResults')
    # results.links.find_by_partial_href('images').click()
    # time.sleep(3)
    results = browser.find_by_css('.SearchResultCard').first
    results.click()
    browser.find_by_text('Download JPG ').click()
    featured_image_url = browser.url
    # browser.quit()
    return featured_image_url


def scrape_Mars_fact(url):
    mars_facts_dfs = pd.read_html(url) # pd.read_html return dfs: a list of dictionary
    a_json = mars_facts_dfs[0].to_json(orient="records")
    # browser.quit()

    return a_json


def scrape_Mars_hemispheres(url):
    browser.visit(url)
    items = browser.find_by_css('.item')
    mars_hemispheres = []
    link_qty = len(items)
    for i in range(link_qty):
        result = browser.find_by_css('.item')[i].find_by_tag('h3')
        a_dict = {}
        a_dict["title"] = result.text

        result.click()
        html = browser.find_by_css('.downloads').html
        soup = BeautifulSoup(html, 'html.parser')
        result = soup.find('a')
        a_dict["img_url"] = result['href']
        
        mars_hemispheres.append(a_dict)
    
        browser.back()
    # browser.quit()
    return mars_hemispheres


def quit_browser():
    browser.quit()

