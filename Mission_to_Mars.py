#!/usr/bin/env python
# coding: utf-8

# In[1]:


from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time


# In[2]:


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


url = 'https://mars.nasa.gov/news/'
browser.visit(url)


# In[4]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')

article = soup.find('div', class_='list_text')
header = article.find('div', class_='content_title').text
paragraph = article.find('div', class_='article_teaser_body').text


# In[5]:


#JPL Image
jplurl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(jplurl)

html = browser.html
soup = BeautifulSoup(html, 'html.parser')
featured_image_url = soup.find('img', class_='thumb')['src']
featured_image_url


# In[6]:


#Twitter
twitterurl = 'https://twitter.com/marswxreport?lang=en'
browser.visit(twitterurl)

html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[7]:


mars_weather = soup.find('div', class_='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0').                    find('span', class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0").                    text
mars_weather


# In[8]:


#Mars Fact
marsfacturl = 'https://space-facts.com/mars/'
tables = pd.read_html(marsfacturl)
df = tables[0]
#setting up the columns
df.columns=['Mars Planet Profile', 'Numbers']
#use the Mars Planet profile column as the index
df = df.set_index(['Mars Planet Profile'])
df


# In[9]:


#convert pandas into string
df_html = df.to_html()
df_html


# In[20]:


#Mars Hemispheres
marshem = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(marshem)

html = browser.html
soup = BeautifulSoup(html, 'html.parser')

hemisphere_link=[]

hemisphere_information = soup.find_all('div', class_='description')
for links in hemisphere_information:
    info = links.find('a', class_='itemLink product-item')
    link = info['href']
    complete_link = (f'https://astrogeology.usgs.gov{link}')
    hemisphere_link.append(complete_link)
hemisphere_link
    


# In[19]:


hemisphere_dictionary = []
for i in range(len(hemisphere_link)):
    browser.visit(hemisphere_link[i])
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image_link = soup.find('img',class_= 'wide-image')['src']
    complete_image_link = (f'https://astrogeology.usgs.gov{image_link}')
    image_name = soup.find('h2',class_='title').text
    image_dictionary = {'Title':image_name, 'Link':complete_image_link}
    hemisphere_dictionary.append(image_dictionary)

hemisphere_dictionary


# In[ ]:




