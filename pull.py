import requests
import time


sources = [
    "https://raw.githubusercontent.com/zloi-user/hideip.me/main/http.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt"
]

while True :
    try : 
        proxies = ""
        for source in sources :
            http = requests.get(source).text
            proxies += http

        with open('prx.txt','w',encoding='utf-8') as f:
            f.write(proxies)
        res = requests.get("https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies").text.splitlines()
        with open("prx.txt", 'a') as f :
            for line in res :
                f.write(line+"\n")

        print("PROXIES REFRESHED.....")
        time.sleep(60)
    except : pass
