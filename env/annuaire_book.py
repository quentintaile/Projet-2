import re

import requests 

from bs4 import BeautifulSoup 


def get_all_pages() :
    urls = []
    page_number = 1

    for i in range (100): 
        i = f"https://books.toscrape.com/catalogue/page-{page_number}.html"
        page_number += 1
        urls.append(i)
        
        return urls 


def parse_attorney(): 
    r = requests.get("https://books.toscrape.com/catalogue/page-1.html")
    soup = BeautifulSoup(r.content, "html.parser")
  
    avocats = soup.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')
   

    for avocat in avocats : 
        nom = avocat.find('h3').text
        prix = avocat.find('p', class_='price_color').text
        stock = avocat.find('p', class_='instock availability').text
        stock_final = re.sub(r"\s+", " ", stock)
        
        chemin = r"C:\Users\Quentin\Desktop\Concepteur Python\Projet\Projet 2\annuaire_livre.csv"
        with open(chemin, "a") as f:
            f.write(f"{nom}\n")
            f.write(f"{prix}\n")
            f.write(f"{stock_final}\n\n")

parse_attorney()



get_all_pages()



