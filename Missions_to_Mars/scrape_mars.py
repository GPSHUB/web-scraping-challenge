from bs4 import BeautifulSoup 
from splinter import Browser
import pandas as pd 
import time

# Start browser
def scrape_all(): 
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False) 

    news_title, news_p =  mars_news_scrape(browser)
    data = { "news_title": news_title,
             "news_p" : news_p, 
             "featured_image_url": mars_image_scrape(browser),
            # "mars_facts": mars_facts_scrape(),
             "hemisphere": mars_hemispheres_scrape(browser)

    }

    return data

   # mars_dict = {}

# MARS NEWS
def mars_news_scrape(browser):
    #executable_path = {'executable_path': 'chromedriver'}
    #browser = Browser('chrome', **executable_path, headless=False) 

    # browser = init_browser()
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(10)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    try: 
        news_title = soup.find('div', class_='bottom_gradient').find('a').text
        news_p = soup.find('div', class_='rollover_description_inner').text
        #return news_title, news_p
       # mars_dict['news_title'] = news_title
       # mars_dict['news_p'] = news_p
       # return mars_dict
    except AttributeError:
        return None, None
    return news_title, news_p
    

# Mars image
def mars_image_scrape(browser):   


    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    url_soup = BeautifulSoup(html, 'html.parser')        
    current_featured_mars_image = browser.find_by_id('full_image')
    current_featured_mars_image.click()
    browser.is_element_present_by_text('more info')
    more_info_2 = browser.links.find_by_partial_text("more info")
    more_info_2.click()
    html = browser.html
    url_soup = BeautifulSoup(html, 'html.parser')
    try:
        img_url = url_soup.find('figure', class_="lede")
        image = img_url.find('a')["href"]
        
        # Concatenate URL
        img_url = f"https://www.jpl.nasa.gov{image}"
       # img_url
        # Update Dictionary
        #mars_dict['featured_image_url'] = img_url
    except:
        return None
    return img_url

# Mars Facts
def mars_facts_scrape():  
    try:
        space_facts_url = 'https://space-facts.com/mars/'
        tables = pd.read_html(space_facts_url)
        mars_df = tables[1]
        mars_df.set_index('Mars - Earth Comparison', inplace=True)
        del mars_df['Earth']
    except BaseException:
        return None
    #mars_dict['mars_facts'] = data
    return mars_df

# # MARS HEMISPHERES
def mars_hemispheres_scrape(browser):
    dict_test = {}
    hem_result = []

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    result = soup.find_all('div', class_ = "item")

    for item in result:        
        title = item.find("div", class_="description")
        title2 = title.find('a', class_ = "itemLink product-item").find('h3').get_text()

        url = item.find('a', class_ = "itemLink product-item")["href"]
        full_url = f"https://astrogeology.usgs.gov{url}"

        browser.visit(full_url)
        time.sleep(5)
        html = browser.html
        url_soup = BeautifulSoup(html, 'html.parser')
        full_img_url = url_soup.find("div", class_ = "downloads") 
        result = full_img_url.select_one('ul li a')['href']  
        dict_test["title"] = title2
        dict_test["full_url"] =  f"https://astrogeology.usgs.gov{result}"
        hem_result.append(dict_test)
        #hem_img_url = f"{title2} {result}"
        #mars_dict['hem_img_url'] = hem_img_url
        return hem_result
