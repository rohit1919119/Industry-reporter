# Developed by @sanuja : https://github.com/sanuja-gayantha

import requests
from bs4 import BeautifulSoup as soup
import concurrent.futures
import json

from constants import Proxies_located_url, Ip_checking_url, Connections


class rotatingProxy():
    
    def __init__(self, proxies_located_url, ip_checking_url):

        self.proxies_located_url= proxies_located_url
        self.ip_checking_url= ip_checking_url
        self.proxies = []


    # Find proxies IP's from web & Scrape them
    def get_proxies_from_web(self):

        response = requests.get(self.proxies_located_url)
        bsObj = soup(response.content, features="lxml")

        for ip in bsObj.findAll('table')[0].findAll('tbody')[0].findAll('tr'):    
            # put table rows to a list
            cols = ip.findChildren(recursive = False)
            cols = [element.text.strip() for element in cols]
            
            # proxy address
            proxy = 'socks4://'+ ':'.join([cols[0],cols[1]])
            self.proxies.append(proxy)


    # Find working/valid IP's
    def extract_valid_proxy(self, proxy):
        try:
            response = requests.get(self.ip_checking_url, 
                                        proxies={"http": proxy, "https": proxy}, timeout=3)
            # print(response.json())

        except Exception as e:
            pass

        return proxy


    # Store them in .json file for futher use
    def generate_json(self, results):

        temp_results=[]
        for result in results:
            temp_results.append(result)

        with open('proxyList.json', 'w') as file:
            json.dump(temp_results, file)



ins = rotatingProxy(Proxies_located_url, Ip_checking_url)
ins.get_proxies_from_web()

with concurrent.futures.ThreadPoolExecutor(max_workers=Connections) as executor:
    results = executor.map(ins.extract_valid_proxy, ins.proxies)

ins.generate_json(results)