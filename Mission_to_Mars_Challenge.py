#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from bs4 import BeautifulSoup
import requests
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[ ]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[ ]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# In[ ]:


slide_elem.find('div', class_='content_title')


# In[ ]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[ ]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# In[ ]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[ ]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[ ]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[ ]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[ ]:


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[ ]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# In[ ]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[ ]:


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[42]:


def hemisphere_images(browser):    
    # 1. Use browser to visit URL
    base_url = 'https://marshemispheres.com/'
    browser.visit(base_url)
    hemisphere_image_urls = []
    html = browser.html
    html_soup = soup(html, 'html.parser')
    rows = html_soup.find_all('div', class_= 'item')
    #print(rows[0].find('a').get('href'))
    
    for hemi in rows:
        # creat dictionary
        hemi_info = {}
        #get img url
        partial_link = hemi.find('a').get('href')
        full_url = f'{base_url}{partial_link}'
        browser.visit(full_url)
        hemi_html = browser.html
        hemi_soup = soup(hemi_html, 'html.parser')
        hemi_box = hemi_soup.find('div', class_ = 'downloads')
        half_img_url = hemi_box.find('a', target = '_blank').get('href')
        full_img_url = f'{base_url}{half_img_url}'
        
        #get title
        hemi_title = hemi_soup.find('h2', class_ = 'title').get_text()
        
        # add to dictionary
        hemi_info['img_url']=full_img_url
        hemi_info['title']=hemi_title
        
        # add to list of dictionaries
        hemisphere_image_urls.append(hemi_info)
                
    return hemisphere_image_urls


# In[43]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls = hemisphere_images(browser)
print(hemisphere_image_urls)


# In[44]:


# 5. Quit the browser
browser.quit()


# In[ ]:




