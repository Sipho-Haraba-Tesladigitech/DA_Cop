# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 14:38:53 2022
Followed articles: 
https://www.thepythoncode.com/article/using-proxies-using-requests-in-python
https://www.torproject.org/download/  #Downloading Tor which enables the proxy
https://stackoverflow.com/questions/30286293/make-requests-using-python-over-tor#answer-33875657 #Configuring the browser and the proxy
@author: Tshegofatso Mohlala


Connects to the tor network using the tor browser as the proxy
"""

import requests
from stem.control import Controller
from stem import Signal

def get_tor_session():
    # initialize a requests Session
    session = requests.Session()
    # setting the proxy of both http & https to the localhost:9050 
    # this requires a running Tor service in your machine and listening on port 9050 (by default)
    session.proxies = {"http": "socks5://localhost:9150", "https": "socks5://localhost:9150"}
    return session

def renew_connection():
    with Controller.from_port(port=9151) as c:
        c.authenticate()
        # send NEWNYM signal to establish a new clean connection through the Tor network
        c.signal(Signal.NEWNYM)

if __name__ == "__main__":
    s = get_tor_session()
    ip = s.get("http://icanhazip.com").text
    print("IP:", ip)
    renew_connection()
    s = get_tor_session()
    ip = s.get("http://icanhazip.com").text
    print("IP:", ip)