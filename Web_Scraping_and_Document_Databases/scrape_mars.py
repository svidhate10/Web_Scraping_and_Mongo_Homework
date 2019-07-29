from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import time


# Define scrape function
def scrape():
    # Create a library that holds all the Mars' Data
    mars_library = {}
    # Use splinter to navigate the JPL's Featured Space Image and scrape the current Featured Mars Image url (https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars)
    # Execute Chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    # #### NASA Mars News
    # We will scrape the lastest News Title and Paragragh Text from NASA Mars News Site(https://mars.nasa.gov/news/).
    # URL of page to be scraped
    url_1 = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    #Visit the page using the browser
    browser.visit(url_1)
    # assign html content
    html = browser.html
    # Create a Beautiful Soup object
    soup = bs(html, "html.parser")
    # Extract the text from the class="content_title" and clean up the text use strip
    news_title = soup.find_all('div', class_='content_title')[0].find('a').text.strip()
    # Extract the paragraph from the class="rollover_description_inner" and clean up the text use strip
    news_p = soup.find_all('div', class_='rollover_description_inner')[0].text.strip()
    # put infos into Library
    mars_library['news_title'] = news_title
    mars_library['news_p'] = news_p


    # #### JPL Mars Space Images - Featured Image
    # URL of page to be scraped
    url_2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    #Visit the page using the browser
    browser.visit(url_2)
    # assign html content
    html = browser.html
    # Create a Beautiful Soup object
    soup = bs(html, "html.parser")
    #Scrape Path for the Feature Image. got the partial path of the url
    img = soup.find_all('a', class_='fancybox')[0].get('data-fancybox-href').strip()
    #combine the root url to get the full address
    img_url = "https://www.jpl.nasa.gov"+img
    # Put infos into Library
    mars_library['featured_image_url'] = img_url


    # #### Mars Weather
    # Use splinter to scrape the latest Mars weather tweet from the Mars Weather twitter account  (https://twitter.com/marswxreport?lang=en)
    # URL of page to be scraped
    tweet_url = 'https://twitter.com/marswxreport?lang=en'
    #Visit the page using the browser
    browser.visit(tweet_url)
    # assign html content
    html = browser.html
    # Create a Beautiful Soup object
    soup = bs(html, "html.parser")
    #scrap latest Mars weather tweet
    mars_weather = soup.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')[0].text
    # Put infos into Library
    mars_library['mars_weather'] = mars_weather


    # #### Mars Facts
    # Use Pandas to scrape the table from Mars Facts webpage and convert the data to a HTML table string
    # URL of page to be scraped
    facts_url = 'https://space-facts.com/mars/'
    # use Pandas to get the url table
    mars_info = pd.read_html(facts_url)
    # Convert list of table into pandas dataframe
    mars = (mars_info[0])
    mars.columns = ['Mars-Earth Comparison', 'Mars','Earth']

    # Use pandas to  generate HTML tables from DataFrames and save as html file
    mars_facts=mars.to_html(justify='left')
    # Put infos into Library
    mars_library['mars_facts'] = mars_facts


    # #### Mars Hemisperes
    # USGS Astrogeology site to obtain high resolution images for each of Mar's hemispheres
    # URL of page to be scraped
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    #Visit the page using the browser
    browser.visit(hemisphere_url)
    # assign html content
    html = browser.html
    # Create a Beautiful Soup object
    soup = bs(html,"html.parser")
    # assigned list to store:
    hemisphere_image_urls = []
    # create empty dict
    dict = {}
    # get all the title
    results = soup.find_all('h3')
    # Loop through each result
    for result in results:
        # Get text info from result
        itema = result.text
        time.sleep(1)    
        browser.click_link_by_partial_text(itema)
        time.sleep(1)
        # assign html content
        htmla = browser.html
        # Create a Beautiful Soup object
        soupa = bs(htmla,"html.parser")
        time.sleep(1)
        # Grab the image link
        linka = soupa.find_all('div', class_="downloads")[0].find_all('a')[0].get("href")
            # Pass title to Dict
        time.sleep(1)
        dict["title"]=itema
        # Pass url to Dict
        dict["img_url"]=linka
        # Append Dict to the list 
        hemisphere_image_urls.append(dict)
        # Clean Up Dict
        dict = {}
        browser.click_link_by_partial_text('Back')
        time.sleep(1)
    # Put infos into Library
    mars_library['hemisphere_image_urls']=hemisphere_image_urls
    
    # Return Library
    return mars_library