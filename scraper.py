from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from time import sleep
import requests, lxml
import threading
import random
import string
import json
import re

headers = {
    'User-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

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
    params = {"q" : f'"@gmail.com" "GB" {variation} site:uk.linkedin.com/company'}
   
    proxies = {'https' : "http://" + PROXY}
    try : 
        html = requests.get("https://www.google.com/search", headers=headers,proxies=proxies,params=params,timeout=5).text
        soup = bs(html, "lxml")
        li = soup.select('.yuRUbf a')

        for l in li : 
            links.append(l['href'])
    except : pass
 
    
def linkedin(link):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    
    chrome = webdriver.Chrome(options=options)
    chrome.get(link)
    sleep(3)

    chrome.find_element(By.CSS_SELECTOR, 
    "icon[class='contextual-sign-in-modal__modal-dismiss-icon lazy-loaded']").click()
    sleep(2)

    name = chrome.find_element(By.CSS_SELECTOR, "h1").text
    niche = chrome.find_element(By.CSS_SELECTOR, "h2").text
    address = chrome.find_element(By.CSS_SELECTOR, "#address-0").text

    about = chrome.find_elements(By.CSS_SELECTOR, ".core-section-container__content")[0]
    emails = re.search(r'[\w.+-]+@[\w-]+\.[\w-]+', about.text)

    if "GB" in address :
        if emails != None :
            record = {
                "name" : name,
                "niche" : niche,
                "address" : address,
                "email" : emails[0],
            }
            data.append(record)


while True : 
    links = [] 
    data = []
    for i in range(100) : 
        t = threading.Thread(target=getLinks)
        t.start()
    
    sleep(5)
    
    if(len(links) > 0):
        for i in range(1) : 
            link = random.choice(links)
            t = threading.Thread(target=linkedin,args=(link,))
            t.start()
        sleep(15)
        
    with open("data.json", 'r') as f :
        local = json.loads(f.read())
        for record in data : 
            if record not in local :
                local.append(record)
        with open("data.json", 'w') as w :
            json.dump(local, w)
        
        
    

