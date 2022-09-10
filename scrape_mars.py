#imports
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime as dt

#scrape all functions
def scrape_all():

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #get the info from respective pages
    news_title, news_p = scrape_mars_news(browser)
    
    # build a dictionary using the information from the scrapes
    marsData = { 
        "newsTitle": news_title,
        "newsParagraph": news_p,
        "featuredImage": scrape_featured_image(browser),
        "facts": scrape_mars_facts(browser),
        "hemispheres": scrape_hemisphere(browser),
        "lastUpdated": dt.datetime.now()
    }

    browser.quit()
    return marsData

# scrape the mars news page
def scrape_mars_news(browser):
    #go to the news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    time.sleep(1)
    html1 = browser.html
    soup = bs(html1, "html.parser")
    news_title = soup.find('div', class_='content_title').get_text()
    news_p = soup.find('div', class_='article_teaser_body').get_text()

    # return the title and paragraph
    return news_title, news_p

# scrape through the featured image page

def scrape_featured_image(browser):
    url2 = 'https://spaceimages-mars.com'
    browser.visit(url2)

    html = browser.html
    soup = bs(html, 'html.parser')

    img_start = 'https://spaceimages-mars.com/'
    img_end = soup.find_all('a',class_='showimg fancybox-thumbs')[0]['href']
    featured_url = img_start+img_end

    return featured_url

# scrape through the facts page
def scrape_mars_facts(browser):
    url3 = 'https://galaxyfacts-mars.com'
    browser.visit(url3)
   
    html = browser.html
    soup = bs(html, 'html.parser')

    facts_location = soup.find('div', class_='diagram mt-4')
    facts_table = facts_location.find('table')
    facts = ""
    facts += str(facts_table)

    return facts

#scrape through the hemisphere pages
def scrape_hemisphere(browser):
    url4 = 'https://marshemispheres.com/'
    browser.visit(url4)

    hemi_images = []

    for x in range(4):
        hemiInfo ={}
    
        browser.find_by_css('a.product-item img')[x].click()
        links = browser.links.find_by_text('Sample').first
        hemiInfo["img_url"] = links['href']
        
        hemiInfo['title'] = browser.find_by_css('h2.title').text
    
        hemi_images.append(hemiInfo)
        
        browser.back()

        return hemi_images


# set up a flask app
if __name__ == "__main__":
    print(scrape_all())