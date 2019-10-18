# import the dependencies

import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import time

# define scrape and chromedriver


def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)




def scrape():
    
    browser = init_browser()
    scraped_data = {}

    # visit site 1 grab headline and paragraph

    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    time.sleep(1)
    mars_web_html = browser.html
    mars_web_soup = BeautifulSoup(mars_web_html, 'html.parser')

    news_list = mars_web_soup.find('ul', class_ = 'item_list')
    headline_title = news_list.find('li', class_ = 'slide')
    mars_headline = headline_title.find('div', class_ = 'content_title').text
    mars_body = headline_title.find('div', class_ = 'article_teaser_body' ).text
    
    scraped_data['mars_headline'] = mars_headline
    scraped_data['mars_body'] = mars_body

    browser.quit()


    #visit site 2 retrieving the feature image

    browser = init_browser()

    feature_img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(feature_img_url)
    time.sleep(1)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(1)

    feature_img_html = browser.html
    feature_img_soup = BeautifulSoup(feature_img_html, 'html.parser')
    feature_img = feature_img_soup.find('img', class_ = 'fancybox-image')['src']
    feature_img_path = f'https://www.jpl.nasa.gov{feature_img}'

    scraped_data['feature_img_path'] = feature_img_path

    browser.quit()

    

#visit site 3 scraping the weather tweet
    browser = init_browser()


    mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_weather_url)
    time.sleep(1)
    mars_weather_html = browser.html
    mars_weather_soup = BeautifulSoup(mars_weather_html, 'html.parser')

    mars_weather_tweet = mars_weather_soup.find('ol', class_ ='stream-items')
    mars_weather = mars_weather_tweet.find('p', class_ = 'tweet-text').text

    scraped_data['mars_weather'] = mars_weather

    browser.quit()

#visit site 4 retrieving the mars fact table


    facts_url = 'https://space-facts.com/mars/'

    time.sleep(1)
    table = pd.read_html(facts_url)
    table[1]
    df_mars_facts = table[1]
    df_mars_facts.columns = ["description", "Values"]
    clean_table = df_mars_facts.set_index(["description"])
    mars_html_table = clean_table.to_html()
    mars_html_table = mars_html_table.replace("\n", "")

    scraped_data['mars_df'] = mars_html_table

#visit site 5 scraping images of mars

    browser = init_browser()

    mars_pics_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(mars_pics_url)
    hemisphere_list = []
    links = browser.find_by_css("a.product-item h3")

    for h in range(len(links)):
        hemisphere = {}
        browser.find_by_css("a.product-item h3")[h].click()
        element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"]=element["href"]
        hemisphere["title"]=browser.find_by_css("h2.title").text
        hemisphere_list.append(hemisphere)
        browser.back()

    scraped_data['hemisphere_list'] = hemisphere_list

    browser.quit()

    return scraped_data







