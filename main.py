#importing our used libraries
import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as np
import numpy as np
import requests

"""---------------------------------------------------------------"""
#intiating the driver "Beta version"


def getting_source(url):
    #initiating the Chrome driver
    options=Options()
    options.add_experimental_option("detach",True)
    driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
    driver.get(url)
    #clicking the video tap in the channel
    time.sleep(3)
    links=driver.find_elements("xpath","//a[@href]")
    for link in links:
        if "Videos" in link.get_attribute("innerHTML"):
            link.click()
            break
    time.sleep(1)
    #scrolling to get all videos
    SCROLL_PAUSE_TIME = 1
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    element=driver.find_element(By.TAG_NAME,'body')

    #scrolling to get all videos in the page
    while True:
        # Scroll down to bottom
        element.send_keys(Keys.END)

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    page_source=driver.page_source
    driver.quit()
    return page_source
def getting_url_titles(page_source):
    #getting the urls and titles from the page we got the source of in the first function
    soup=BeautifulSoup(page_source,"html.parser")
    titles=soup.findAll(id="video-title-link")
    urls=[]
    t=[]
    for i in titles:
        url=i.get('href')
        url='https://www.youtube.com'+str(url)
        title=i.get('title')
        urls.append(url)
        t.append(title)
    return urls,t

def getting_views_date(url):
    #that function will be used to get the date and views count of each video
    r = requests.get(url)
    page_source = r.content
    soup = BeautifulSoup(page_source, "html.parser")
    element = soup.find("meta", {"itemprop": "datePublished"})
    views_element = soup.find("meta", {"itemprop": "interactionCount"})
    date = element["content"]
    views = views_element["content"]
    return views,date


if __name__=='__main__':
    channel_url=input("please enter the channel url ")
    channel_name=channel_url[len('https://www.youtube.com/'):]
    df=pd.DataFrame(columns=['id','video_URL','video_title','video_Views','Video_date'])

    print("fetching the data please wait")
    print("opening the driver")
    urls,titles=getting_url_titles(page_source=getting_source(channel_url))
    print("all video urls of the channel collected ..... working on getting data")
    #looping throw the list  of urls that we extracted from the 1st function then returning a new raw in the dataframe
    for i in urls:
        print(str(i))
        v,d=getting_views_date(str(i))
        print(v,d)
        print('row number {} is done '.format(urls.index(i)))
        df.loc[len(df.index)] = [(urls.index(i))+1,i,titles[urls.index(i)],v,d]
    #saving the data to csv file with name of the channel name
    df.to_csv("{}.csv".format(channel_name),index=False)











