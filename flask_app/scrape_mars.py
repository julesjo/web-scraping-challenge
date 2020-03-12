# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# Dependencies and Setup
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
from pprint import pprint


# %%
# Set Executable Path & Initialize Chrome Browser
executable_path = {'executable_path': 'C:/Users/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


def mars_news(browser):
    # Visit the NASA Mars News Site
    mars_url = "https://mars.nasa.gov/news/"
    browser.visit(mars_url)


    # Find Everything Inside:

    html = browser.html
    news_soup = BeautifulSoup(html, "html.parser")
    #print(news_soup.prettify())

    try:
        slide_element = news_soup.select_one("ul.item_list li.slide")
        slide_element.find("div", class_="content_title")

        # Scrape the Latest News Title
        latest_news_title = slide_element.find("div", class_="content_title").get_text()
        #print(latest_news_title)

        # Scrape the Latest Paragraph Text
        latest_news_paragraph = slide_element.find("div", class_="article_teaser_body").get_text()
        #print(latest_news_paragraph)
    except AttributeError:
        return None, None
        return latest_news_title, latest_news_paragraph



def featured_image(browser):
    # Visit the url for JPL Featured Space Image
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    img = soup.select_one("figure.lede a img")
    
    try:
        featured_img_url = img.get("src")
    except AttributeError:
        return None
    featured_image_url= f"https://www.jpl.nasa.gov{featured_image_url}"
    return featured_image_url

    # Use splinter to navigate the site and find the image url for the current Featured Mars Image
    #featured_img_base = "https://www.jpl.nasa.gov"
    #featured_img_url_raw = soup.find("div", class_="carousel_items").find("article")["style"]
    #featured_img_url = featured_img_url_raw.split("'")[1]
    #featured_img_url = featured_img_base + featured_img_url
    #featured_img_url

def twitter_weather(browser):
    # Visit the Mars Weather twitter account and scrape the latest Mars weather tweet from the page.
    mars_twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(mars_twitter_url)

    html = browser.html
    tweet_soup = BeautifulSoup(html, 'html.parser')
    #print(soup.prettify())
    
    # Find a Tweet with the data-name `Mars Weather`
    mars_weather_tweet = tweet_soup.find("div", 
                                       attrs={
                                           "class": "tweet", 
                                            "data-name": "Mars Weather"
                                        })
    
    first_tweet = mars_weather_tweet.find('p', class_='TweetTextSize')
    #print(first_tweet)
    return first_tweet

def mars_facts():
    # Visit the Mars Facts webpage and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    try:
        mars_facts_df = pd.read_html("https://space-facts.com/mars/")[0]
    except BaseException:
        return None
    #print(mars_facts_df)
    mars_facts_df.columns=["Description", "Value"]
    mars_facts_df.set_index("Description", inplace=True)
    return mars_facts_df.to_html(classes="table table-striped")
    #mars_facts_df


def hemisphere(browser):
    # Visit the USGS Astrogeology site to obtain high resolution images for each of Mar's hemispheres.
    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(usgs_url)

    hemisphere_image_urls = []

    # Get a List of All the Hemispheres
    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}
    
        # Find Element on Each Loop to Avoid a Stale Element Exception
        browser.find_by_css("a.product-item h3")[item].click()
    
        # Find Sample Image Anchor Tag & Extract <href>
        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]
    
        # Get Hemisphere Title
        hemisphere["title"] = browser.find_by_css("h2.title").text
    
        # Append Hemisphere Object to List
        hemisphere_image_urls.append(hemisphere)
    
        # Navigate Backwards
        browser.back()

    return hemisphere_image_urls

def scrape_all():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)
    latest_news_title, latest_news_paragraph = mars_news(browser)
    featured_img_url = featured_image(browser)
    mars_weather = twitter_weather(browser)
    facts = mars_facts()
    hemisphere_image_urls = hemisphere(browser)
    timestamp = dt.datetime.now()

    data = {
        "news_title": latest_news_title,
        "news_paragraph": latest_news_paragraph,
        "featured_image": featured_img_url,
        "weather": first_tweet,
        "facts": mars_facts_df,
        "hemispheres": hemisphere_image_urls,
        "last_modified": timestamp
    }
    browser.quit()
    return data 

if __name__ == "__main__":
    print(scrape_all())



