import json
import lxml
import requests
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent

ua = UserAgent()
headers = { 'User-agent': ua.random}
s = requests.Session()
html = s.get("https://www.linkedin.com/company/angelbizlink", headers=headers).text

with open("test.html", "w", encoding="utf-8") as f :
    f.write(html)
    
  
    soup = bs(html, "lxml")
    
    about = soup.select("section[data-test-id='about-us']")[0]
    print(about.text)
    
    
    