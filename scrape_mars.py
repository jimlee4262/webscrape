from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests


#initizalize splinter function
def initiate_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = initiate_browser()

    #NASA
    nasaurl = 'https://mars.nasa.gov/news/'
    browser.visit(nasaurl)

    #beautiful soup
    nasahtml = browser.html
    nasasoup = BeautifulSoup(nasahtml, 'html.parser')

    #scrape the top headline and description
    article = nasasoup.find('div', class_='list_text')
    header = article.find('div', class_='content_title').text
    paragraph = article.find('div', class_='article_teaser_body').text

    #JPL Image
    jplurl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jplurl)

    #Beautiful Soup
    jplhtml = browser.html
    jplsoup = BeautifulSoup(jplhtml, 'html.parser')

    #JPL Image
    featured_image_url = "jpl.nasa.gov" + jplsoup.find('img', class_='thumb')['src']

    #Twitter
    twitterurl = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitterurl)

    #Beautiful Soup
    twitterhtml = browser.html
    twittersoup = BeautifulSoup(twitterhtml, 'html.parser')

    #Get recent tweet
    mars_weather = twittersoup.find('div', class_='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0').\
                    find('span', class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0").\
                    text
    
    #Mars Facts
    marsfacturl = 'https://space-facts.com/mars/'

    #Gettting the Mars Table via Pandas 
    tables = pd.read_html(marsfacturl)
    df = tables[0]

    #setting up the columns
    df.columns=['Mars Planet Profile', 'Numbers']
    
    #use the Mars Planet profile column as the index
    df = df.set_index(['Mars Planet Profile'])
    
    #converting html table string w/ pandas
    df_html = df.to_html()

    #Mars Hemispheres
    marshem = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(marshem)

    marshtml = browser.html
    marssoup = BeautifulSoup(marshtml, 'html.parser')
    #Get the link for each Hemisphere
    hemisphere_link=[]

    #Run a loop to get the list of links
    hemisphere_information = marssoup.find_all('div', class_='description')
    for links in hemisphere_information:
        info = links.find('a', class_='itemLink product-item')
        link = info['href']
        complete_link = (f'https://astrogeology.usgs.gov{link}')
        hemisphere_link.append(complete_link)

    #loop through the links to get the title and image
    hemisphere_dictionary = []
    for i in range(len(hemisphere_link)):
        browser.visit(hemisphere_link[i])
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        image_link = soup.find('img',class_= 'wide-image')['src']
        complete_image_link = (f'https://astrogeology.usgs.gov{image_link}')
        image_name = soup.find('h2',class_='title').text
        image_dictionary = {'title':image_name, 'link':complete_image_link}
        hemisphere_dictionary.append(image_dictionary)

    #Close the browser
    browser.quit()

    mars_information = {"Mars_Headline": header,
                        "Mars_Description": paragraph,
                        "jpl_link": featured_image_url,
                        "table_html": df_html,
                        "twitter": mars_weather,
                        "hemispheres": hemisphere_dictionary}
    
    return mars_information


    