# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    image_dict = hemisphere_images(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "image_dict": image_dict
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

def hemisphere_images(browser):    
    # 1. Use browser to visit URL
    base_url = 'https://marshemispheres.com/'
    browser.visit(base_url)
    hemisphere_image_urls = []
    html = browser.html
    html_soup = soup(html, 'html.parser')
    rows = html_soup.find_all('div', class_= 'item')
    
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

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())
