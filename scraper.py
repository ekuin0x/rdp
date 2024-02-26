from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as bs
from unidecode import unidecode
from pyppeteer import launch
from time import sleep
import requests, lxml
import threading
import random
import string
import json
import re

ua = UserAgent()
with open("gb.json", "r") as f :
    cities = list(json.loads(f.read()))
def proxy() :
    with open("prx.txt", 'r') as f :
        data = f.readlines()
        p = random.choice(data)
        proxy = ""
    for c in p : 
        if c.isalpha() == True  : 
            break
        else : proxy += c
    return proxy[:-1]

def getLinks():
    PROXY = proxy()
    variation = ""
    for i in range(2) :
        variation += random.choice(string.ascii_letters).lower()
    headers = { 'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0'}
    city = random.choice(cities) 
    params = {
		"q" : f'"@gmail.com" {city} {variation} site:uk.linkedin.com/company',
		"lang" : "en"
	     }
   
    proxies = {'https' : "http://" + PROXY}
    try : 
        html = requests.get("https://www.google.com/search",headers=headers,proxies=proxies,params=params,timeout=5).text
        soup = bs(html, "lxml")
        li = soup.select('.yuRUbf a')

        for l in li : 
            if "google.com" not in l["href"] :
                links.append(l['href'])
    except : pass
 

def has_numbers(inputString):
    return bool(re.search(r'\d', inputString))
    
def main(link):
    headers = { 'User-agent': ua.random}
    s = requests.Session()
    res = s.get(link, headers=headers)
    print(res.status_code)
    html = res.text
    soup = bs(html, "lxml")
    try :
        name = soup.find("h1").text.strip()
        address = ""
        loc = soup.select("#address-0 p")
        for p in loc :
            address += p.text.strip()

        niche = soup.find("h2").text.strip()
        
        description =  soup.select("section[data-test-id='about-us']")[0].text
        emails = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', description)
        if len(address) > 16 and has_numbers(address) and "GB" in address: 
            if len(emails) > 0 :
                new_record = {
                    "name" : unidecode(name),
                    "niche" : unidecode(niche),
                    "address" : unidecode(address),
                    "email" : unidecode(emails[0]),
                    "source" : unidecode(link)
                }
                new_data.append(new_record)
            
    except : 
        
        pass
    
while True : 
    #INITIATING LINKS FILE
    with open("links.json", 'r') as f :
        scraped_links = json.loads(f.read())

    #INITIATING DATA FILE
    with open("data.json", "r") as f:
        data = json.loads(f.read())
        
    links = [] ; new_data = []
    # GETTING NEW LINKS
    for i in range(200) : 
        t = threading.Thread(target=getLinks)
        t.start()
    sleep(5)
    links = list(set(links))
    
    # SCRAPING NEW LINKS
    if len(links) > 0 :
        for link in links : 
            if link not in scraped_links :
                t = threading.Thread(target=main, args=(link,))
                t.start()
    sleep(5)
            
    #UPDATING DATA FILE
    for new_record in new_data :
        if new_record not in data :
            data.append(new_record)
        
    with open("data.json", "w") as f :
        json.dump(data, f)
            




    

