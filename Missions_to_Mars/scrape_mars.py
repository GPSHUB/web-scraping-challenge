from bs4 import BeautifulSoup 
from splinter import Browser
import pandas as pd 
import time

# Start browser
def scrape_all(): 
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False) 

# Dictionary
    news_title, news_p =  mars_news_scrape(browser)
    data = { "news_title": news_title,
             "news_p" : news_p, 
             "featured_image_url": mars_image_scrape(browser),
             "mars_facts": mars_facts_scrape(),
             "hemisphere": mars_hemispheres_scrape(browser)    

    }
    return data   

# MARS NEWS
def mars_news_scrape(browser):

    # Initiate browser, URL, Parse    
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    time.sleep(10)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # scrape
    try: 
        result = soup.select_one('ul.item_list li.slide')        
        news_title = result.find('div', class_='bottom_gradient').text
        news_p = soup.find('div', class_='rollover_description_inner').text        
    except AttributeError:
        return None, None
    return news_title, news_p    

# MARS IMAGE
def mars_image_scrape(browser):   

    # Initiate browser, URL, Parse   
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    url_soup = BeautifulSoup(html, 'html.parser')      

    # scrape  
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
       
    except:
        return None
    return img_url

# MARS FACTS
def mars_facts_scrape():  
    try:
        space_facts_url = 'https://space-facts.com/mars/'
        tables = pd.read_html(space_facts_url)
        mars_df = tables[1]        
        mars_df.set_index('Mars - Earth Comparison', inplace=True)
        del mars_df['Earth']
        mars_df = pd.DataFrame(mars_df)
    except BaseException:
        return None            
    return mars_df.to_html(classes="table")    

# # MARS HEMISPHERES
def mars_hemispheres_scrape(browser):
    dict_test = {}
    hem_result = []

    # Initiate browser, URL, Parse   
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    result = soup.find_all('div', class_ = "item")
    print(len(result))

    for item in result:        
        print(item)
        # title loop
        title = item.find("div", class_="description")
        title2 = title.find('a', class_ = "itemLink product-item").find('h3').get_text()
        
        # Thumbnail URL loop
        url = item.find('a', class_ = "itemLink product-item")["href"]
        
        # define "full page" URL by concatenating base url from thumbnail url - call it "full_url"
        full_url = f"https://astrogeology.usgs.gov{url}"
        
        # Initiate browser, URL, Parse 
        browser.visit(full_url)
        time.sleep(10)
        html = browser.html
        url_soup = BeautifulSoup(html, 'html.parser')
        
        #scrape full image URL
        full_img_url = url_soup.find("div", class_ = "downloads") 
        full_img_url_final = full_img_url.select_one('ul li a')['href']  
        dict_test["title"] = title2
        dict_test["full_url"] =  f"https://astrogeology.usgs.gov/{full_img_url_final}"
        hem_result.append(dict_test)

        return hem_result
        
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path, headless=False) 
mars_hemispheres_scrape(browser)