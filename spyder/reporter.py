# Developed by @sanuja : https://github.com/sanuja-gayantha

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import requests
from bs4 import BeautifulSoup

import time
import json
import os

from .constants import BASE_URL, IP_CHECKING_URL


class Reporter(webdriver.Chrome):

    def __init__(self, answer, headless=True):

        self.headless = headless
        options = webdriver.ChromeOptions()
        if self.headless:
            options.add_argument("--headless=new")
        super(Reporter, self).__init__(service=ChromeService(ChromeDriverManager().install()), options=options)

        self.answer = answer
        self.domains:list
        self.domains_path = os.path.join(os.getcwd(), 'Domains.json')
        self.implicitly_wait(15)
        
    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.quit()


    def read_json_file(self, path):
        with open(path) as json_file:
            domains = json.load(json_file)
            return domains


    def write_to_json_file(self, path, payload):
        with open(path, 'w') as file:
            json.dump(payload, file, indent=4)
        return
    

    def get_domains(self):
        # Call Api for to get domains <-- write Api !!

        # Then bsed on Question do following
            # 1. If yes delete Links.json & Pdfs.json & rewrite Domains.json <-- This will start the process from the beginning
            # 2. If not call the last domain, continue <-- If something went wrong, this willl help

        # domain_list will be replaced in future!!!
        domain_list =[{"name" : "https://www.bain.com/", "status" : True, },{"name" : "https://kalaari.com/", "rollno" : True, }]      
        
        # Read filtered domains
        self.domains = self.read_json_file(self.domains_path)
        return



    def scrape_website_urls(self):

        # Get valid domains from get_domains function
        self.get_domains()
        print(self.domains)

        # Navigate to home page (use proxy IP's)
        # Check if there is sitemap or not
            # 1. Navigate to sitemap & collect all href links
            # 2. Nf not pass & collect all href links
            # 3. Store then in a list
        # Navigate to each link 
            # 1. Find href links
            # 2. Add href links to the list(save links to .json file) if they does not exists already
                # If there is .pdf link, download it, upload to google drive <-- write Api !!
                    # <-- For now only do .pdf link filtering..
            # 3. Repeat navigation process until count of new links existance equal to zero

        self.get("https://www.nddb.coop/services/animalnutrition/cattlefeed/quality-mark")
        
        soup = BeautifulSoup(self.page_source, 'html.parser')
        for link in soup.find_all('a'):
            print(link.get('href'))

            


# Question : Is this a brand new scraping? 
def questions():
    print("Is this a brand new scraping?\n Type 'y' to yes... \n Type 'n'... to no \n Type 'exit' to quit..")
    while True:
        command = input("> ")
        if command == "exit":
            break
        if command == "y":
            return [True, "y"]
        if command == "n":
            return [True, "n"]
        try:
            print(eval(command))
        except Exception as e:
            # print(f"Exception: {str(e)}")
            print("[*] Input is not valid. Try again...")


def reporter_main():
    answer = questions()
    if answer[0]:
        with Reporter(answer=answer[1], headless=False) as manager:
            manager.scrape_website_urls()
            # print('Exiting...')







