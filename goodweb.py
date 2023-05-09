# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 15:04:36 2022

@author: Tshegofatso Mohlala
"""

from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from Proxy import get_tor_session, renew_connection
import csv
import numpy as np
import urllib3  # the lib that handles the url stuff

alexa = "https://web.archive.org/web/20220411190134/https://www.alexa.com/topsites"  #The url to alexa.com top sites
urls = [] #Contains the list of good websites from Alexa.com
base_url = "/web/20220411190134/https://www.alexa.com/siteinfo/"
alexa1 = "https://web.archive.org/web/20210411123318/https://www.alexa.com/topsites"

def get_urls(url, base_url):
    '''
        * Gets the url of the website we want to extract
        * Returns a tuple where the first element is a list of inline scripts and the 
          second element is a list of absolute paths of the external js files
    '''
    # initialize a session
    session = get_tor_session()
    renew_connection()
    # set the User-agent as a regular browser
    session.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    
    # get the HTML content
    html = session.get(url).content
    
    # parse HTML using beautiful soup
    html_format = bs(html, "html.parser")
    url_list = []
    links = html_format.findAll("a",href=True)
    for a in links:
        #if a['href'].startswith(base_url):
        url_list.append(a['href'])
            
    return url_list

web = get_urls(alexa1, base_url)
print(web, len(web))


