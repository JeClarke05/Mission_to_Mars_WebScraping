

from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': '/Users/jmleg/Anaconda3/envs/PythonData/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    #Mars News
    browser = init_browser()

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    html = browser.html
    soup = bs(html,"html.parser")

    mars_title = soup.find("div",class_="content_title").text
    mars_paragraph = soup.find("div", class_="article_teaser_body").text

    #Featured Image 
    featured_mars_url = ("https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars")

    browser.visit(featured_mars_url)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    browser.click_link_by_partial_text("more info")

    more_info = browser.html
    lg_img_Soup = bs(more_info,'html.parser')

    lg_img_src = lg_img_Soup.find('figure', class_='lede').find('img')['src']

    featured_image_url = 'https://www.jpl.nasa.gov' + lg_img_src

    #Mars Twitter
    mars_twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_twitter_url)
    mars_twitter_html = browser.html
    mars_twitter_soup = bs(mars_twitter_html, 'lxml').body

    mars_weather = mars_twitter_soup.find('p', class_="tweet-text").text.strip()

    #Mars Facts
    mars_facts_url = 'https://space-facts.com/mars/'

    tables = pd.read_html(mars_facts_url)

    df = tables[0]
    df.columns = ['', 'Values']
    df.set_index('', inplace=True)

    html_table = df.to_html(table_id=None, buf=None, bold_rows=True)

    #Mars Hemisphere
    hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hem_url)

    hemisphere_data = []

    for x in range (4):
        title = browser.find_by_tag('h3')
        title[x].click()
        
        html = browser.html
        soup = bs(html, 'html.parser')
        
        wide_image = soup.find("img", class_="wide-image")["src"]
        image_title = soup.find("h2",class_="title").text
        image_url = 'https://astrogeology.usgs.gov'+ wide_image
        
        dictionary = {"title":image_title,"img_url":image_url}
        hemisphere_data.append(dictionary)
        
        browser.back()
        time.sleep(5)
    
    #Save as Dictionary 
    mars_dict = {
        "News_Title" : mars_title,
        "News_Paragraph" : mars_paragraph,
        "Featured_Image" : featured_image_url,
        "Mars_Weather" :  mars_weather,
        "Mars_Facts" : html_table,
        "Mars_Hemispheres" : hemisphere_data
        }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_dict