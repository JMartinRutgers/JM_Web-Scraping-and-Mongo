#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies
import os
from splinter import Browser 
from bs4 import BeautifulSoup as bs
import os
import pandas as pd
import time


# In[2]:


# https://splinter.readthedocs.io/en/latest/drivers/chrome.html
get_ipython().system('which chromedriver')


# In[3]:


#pointing to the directory where chromedriver exists
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# In[10]:


#visiting the page
url = 'https://mars.nasa.gov/news/'
browser.visit(url)


# In[11]:


#using bs to write it into html
html = browser.html
soup = BeautifulSoup(html, 'html.parser')

#soup = bs(html,"html.parser")


# # Nasa Mars News 

# In[12]:


news_title = soup.find("div",class_="content_title").text
news_paragraph = soup.find("div", class_="article_teaser_body").text
print(f"Title: {news_title}")
print(f"Para: {news_paragraph}")


# # Space Images  

# In[56]:


url_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(url_image)


# In[57]:


#Getting the base url
from urllib.parse import urlsplit
base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url_image))
print(base_url)


# In[58]:


# Scrape the browser into soup and use soup to find the image of mars
# Save the image url to a variable called `img_url`
html = browser.html
soup = BeautifulSoup(html, 'html.parser')
image = soup.find("img", class_="thumb")["src"]
img_url = "https://jpl.nasa.gov"+image
featured_image_url = img_url


# In[59]:


# Use the requests library to download and save the image from the `img_url` above
import requests
import shutil
response = requests.get(img_url, stream=True)
with open('img.jpg', 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)


# In[60]:


# Display the image with IPython.display
from IPython.display import Image
Image(url='img.jpg')


# In[97]:


#Design an xpath selector to grab the image
xpath = "//*[@id=\"page\"]/section[3]/div/ul/li[1]/a//div[2]/img"


# In[99]:


#Use splinter to click on the mars featured image
#to bring the full resolution image
results = browser.find_by_xpath(xpath)
img = results[0]
img


# In[103]:


#get image url using BeautifulSoup
html_image = browser.html
soup = bs(html_image, "html.parser")
img_url = soup.find("img", class_="thumb")["src"]
full_img_url = base_url + img_url
print(full_img_url)


# # Mars Weather 

# In[24]:


#get mars weather's latest tweet from the website
url_weather = "https://twitter.com/marswxreport?lang=en"
browser.visit(url_weather)


# In[23]:


html_weather = browser.html
soup = bs(html_weather, "html.parser")
#temp = soup.find('div', attrs={"class": "tweet", "data-name": "Mars Weather"})
mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
print(mars_weather)
#temp


# # Mars Facts 
# 

# In[25]:


url_facts = "https://space-facts.com/mars/"


# In[81]:


table = pd.read_html(url_facts)
table[0]


# In[82]:


table[1]


# In[92]:


df_mars_facts = table[1]
df_mars_facts.columns = ["Diameter", "Mars"]
df_mars_facts.set_index(["Diameter"])


# In[96]:


df_mars_facts = table[1]
df_mars_facts.columns = ["Mass", "Mars"]
df_mars_facts.set_index(["Mass"])


# In[28]:


mars_html_table = df_mars_facts.to_html()
mars_html_table = mars_html_table.replace("\n", "")
mars_html_table


# # Mars Hemispere

# In[29]:


url_hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(url_hemisphere)


# In[30]:


#Getting the base url
hemisphere_base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url_hemisphere))
print(hemisphere_base_url)


# # Cerberus-Himisphere-image
# 

# In[40]:


hemisphere_img_urls = []
count = 1
for x in range(1,4):
    results = browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[x]/a/img")
    time.sleep(2)
    cerberus_open_click = browser.find_by_xpath( "//*[@id='wide-image-toggle']")
    time.sleep(1)
    cerberus_image = browser.html
    soup = bs(cerberus_image, "html.parser")
    cerberus_url = soup.find("img", class_="wide-image")["src"]
    cerberus_img_url = hemisphere_base_url + cerberus_url
    print(cerberus_img_url)
    cerberus_title = soup.find("h2",class_="title").text
    print(cerberus_title)
    back_button = browser.find_by_xpath("//*[@id='splashy']/div[1]/div[1]/div[3]/section/a")
    cerberus = {"image title":cerberus_title, "image url": cerberus_img_url}
    hemisphere_img_urls.append(cerberus)
    count = count+1


# In[43]:


hemisphere_img_urls = []
results = browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[1]/a/img")
cerberus_open_click = browser.find_by_xpath( "//*[@id='wide-image-toggle']")
time.sleep(1)
cerberus_image = browser.html
soup = bs(cerberus_image, "html.parser")
cerberus_url = soup.find("img", class_="wide-image")["src"]
cerberus_img_url = hemisphere_base_url + cerberus_url
print(cerberus_img_url)
cerberus_title = soup.find("h2",class_="title").text
print(cerberus_title)
back_button = browser.find_by_xpath("//*[@id='splashy']/div[1]/div[1]/div[3]/section/a")
cerberus = {"image title":cerberus_title, "image url": cerberus_img_url}
hemisphere_img_urls.append(cerberus)


# # Schiaparelli-Hemisphere-imag

# In[ ]:


results1 = browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[2]/a/img").click()
time.sleep(2)
schiaparelli_open_click = browser.find_by_xpath( "//*[@id='wide-image-toggle']").click()
time.sleep(1)
schiaparelli_image = browser.html
soup = bs(schiaparelli_image, "html.parser")
schiaparelli_url = soup.find("img", class_="wide-image")["src"]
schiaparelli_img_url = hemisphere_base_url + schiaparelli_url
print(schiaparelli_img_url)
schiaparelli_title = soup.find("h2",class_="title").text
print(schiaparelli_title)
back_button = browser.find_by_xpath("//*[@id='splashy']/div[1]/div[1]/div[3]/section/a").click()
schiaparelli = {"image title":schiaparelli_title, "image url": schiaparelli_img_url}
hemisphere_img_urls.append(schiaparelli)


# # Syrtis Major Hemisphere

# In[44]:


results1 = browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[3]/a/img")
time.sleep(2)
syrtis_major_open_click = browser.find_by_xpath( "//*[@id='wide-image-toggle']")
time.sleep(1)
syrtis_major_image = browser.html
soup = bs(syrtis_major_image, "html.parser")
syrtis_major_url = soup.find("img", class_="wide-image")["src"]
syrtis_major_img_url = hemisphere_base_url + syrtis_major_url
print(syrtis_major_img_url)
syrtis_major_title = soup.find("h2",class_="title").text
print(syrtis_major_title)
back_button = browser.find_by_xpath("//*[@id='splashy']/div[1]/div[1]/div[3]/section/a")
syrtis_major = {"image title":syrtis_major_title, "image url": syrtis_major_img_url}
hemisphere_img_urls.append(syrtis_major)


# # Valles Marineris Hemisphere

# In[45]:


results1 = browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[4]/a/img")
time.sleep(2)
valles_marineris_open_click = browser.find_by_xpath( "//*[@id='wide-image-toggle']")
time.sleep(1)
valles_marineris_image = browser.html
soup = bs(valles_marineris_image, "html.parser")
valles_marineris_url = soup.find("img", class_="wide-image")["src"]
valles_marineris_img_url = hemisphere_base_url + syrtis_major_url
print(valles_marineris_img_url)
valles_marineris_title = soup.find("h2",class_="title").text
print(valles_marineris_title)
back_button = browser.find_by_xpath("//*[@id='splashy']/div[1]/div[1]/div[3]/section/a")
valles_marineris = {"image title":valles_marineris_title, "image url": valles_marineris_img_url}
hemisphere_img_urls.append(valles_marineris)


# In[46]:


hemisphere_img_urls


# In[ ]:




