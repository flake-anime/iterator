import requests

http_proxy  = "http://197.149.247.82:8080"

proxies = { 
              "http"  : http_proxy, 
            }

url = "http://httpbin.org/ip"
r = requests.get(url, proxies=proxies)
print(r.json()["origin"])