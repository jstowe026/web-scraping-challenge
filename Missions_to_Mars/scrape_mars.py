
#import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser


# NASA Mars News Section
browser = init_browser()

# Visit NASA News site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

#Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = BeautifulSoup(html, 'html.parser')

slide_elem = news_soup.select_one('ul.item_list li.slide')

def mars_news_scrape():
    # Get the latest news title and paragraph text
    news_title = slide_elem.find('div', class_='content_title').text
    print(news_title)

    # Get the latest news paragraphs text
    news_paragraph = slide_elem.find('div', class_='article_teaser_body').text
    print(news_paragraph)

     # Store data in a dictionary
    nasa_news_data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph
    }

    # Return results
    return nasa_news_data

mars_news_scrape()


# JPL Mars Space Images - Featured Image Section
def mars_image_scrape():
    browser = init_browser()

    # # Visit NASA JPL Mars Space full size featured image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    html = browser.html
    image_soup = BeautifulSoup(html, 'html.parser')

    image_elem = image_soup.select_one('div', class_='carousel_items')

    #find the image url for the current Featured Mars Image and
    #assign the url string to a variable called featured_image_url
    featured_image_path = image_elem.find('a', class_='button fancybox')["data-fancybox-href"]
    featured_img_url = url + featured_image_path

    # Store data in a dictionary
    mars_image_data = {
        "featured_img_url": featured_img_url
    }

    return featured_img_url

mars_image_scrape()


# Mars Weather Section
def mars_weather_scrape():
    
    browser = init_browser()
    
    # Visit Mars Weather Twitter page
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    weather_soup = BeautifulSoup(html, "html.parser")

    tweet_elem = weather_soup.select_one('div', class_='css-1dbjc4n')
    tweet = tweet_elem.select_one('div', class_='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0')

    #scrape the latest Mars weather tweet from the page. Save the tweet
    #text for the weather report as a variable called mars_weather
    mars_weather = tweet.find('span', class_= 'css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0').get_text()

    # Store data in a dictionary
    mars_weather_data = {
        "mars_weather": mars_weather
    }

    return mars_weather

mars_weather_scrape()


# Mars Fact Section
def mars_facts_scrape():
    browser = init_browser()
    url = 'https://space-facts.com/mars/'

    tables = pd.read_html(url)

    #grab the first table
    df = tables[0]
    df.columns = ['Fact', 'Measurement']

    #set index to Fact Column
    df = df.iloc[1:]
    df.set_index('Fact', inplace=True)

    #convert to html
    html_table = df.to_html()
    html_table.replace('\n', '')
    df.to_html('facts_table.html')

    return mars_facts_scrape

mars_facts_scrape()


# Mars Hemispheres
def mars_hemisphere_scrape():
    browser = init_browser()

    # Visit NASA News site
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

     # Scrape page into Soup
    html = browser.html
    hem_soup = BeautifulSoup(html, "html.parser")

    # Retrieve the parent divs for all hemispheres
    items = hem_soup.select_one('div.full-content' 'div.item')

    # loop over results to get hemisphere data
    for item in items:

        hemisphere_data = []

        # scrape the article header
        hem_title = item.find('h3')

        relative_image_path = item.find('img')['href']
        hem_img = url + relative_image_path

        # Dictionary to be inserted into MongoDB
        hem_data = {
            'title': hem_title,
            'image_url': hem_img
        }

        hemisphere_data.append(hem_data)

    # Return results
    return hemisphere_data

mars_hemisphere_scrape()

#combine multiple dictionaries
def Merge(nasa_news_data, mars_image_data, mars_weather_data, hemisphere_data):
    mars_dict = {**nasa_news_data, **mars_image_data, **mars_weather_data, **hemisphere_data}
    return mars_dict

Merge()


