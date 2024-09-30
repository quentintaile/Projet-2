import re
import requests
from bs4 import BeautifulSoup
import pandas as pd  # Importation de pandas pour l'export CSV
import os

 
def get_all_pages():
    urls = []
    

    for page_number in range(1, 100):  # Boucle de 1 à 99 inclus
        url = f"https://books.toscrape.com/catalogue/page-{page_number}.html"
        urls.append(url)

    return urls  # Retourne toutes les URLs

def parse_books():
    books_data = []  # Liste pour stocker les informations sur les livres

    # Ici, on récupère toutes les pages pour scraper
    urls = get_all_pages()

    # Boucle sur toutes les URLs
    for url in urls:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")

        # Trouve tous les éléments contenant les informations sur les livres
        books = soup.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')

        for book in books:
            # Extraction du nom du livre
            nom = book.find('h3').text

            # Extraction du prix
            prix = book.find('p', class_='price_color').text

            # Extraction du stock et nettoyage des espaces
            stock = book.find('p', class_='instock availability').text
            stock_final = re.sub(r"\s+", " ", stock).strip()

            # Extraction de l'URL de l'image
            img_tag = book.find('img')
            img_url = img_tag['src'] if img_tag else 'Pas d\'image'
            img_url_full = f"https://books.toscrape.com/{img_url.replace('../', '')}"  # Correction du chemin relatif

            # Ajoute les informations dans la liste sous forme de dictionnaire
            books_data.append({
                "Nom": nom,            # Nom du livre
                "Prix": prix,          # Prix du livre
                "Stock": stock_final,  # Stock du livre
                "Image": img_url_full  # URL de l'image
            })

       

    # Utilisation de pandas pour créer un DataFrame et organiser les colonnes
    df = pd.DataFrame(books_data, columns=["Nom", "Prix", "Stock", "Image"])

    # Spécifie le chemin du fichier CSV
    chemin = r"C:\Users\Quentin\Desktop\Projet 2\annuaire_livre.csv"

    # Crée le dossier parent s'il n'existe pas déjà
    dossier_parent = os.path.dirname(chemin)
    if not os.path.exists(dossier_parent):
        os.makedirs(dossier_parent)

    # Sauvegarde des données dans un fichier CSV
    df.to_csv(chemin, index=False, sep=';')  # Utilisation de ";" comme séparateur pour une meilleure lisibilité

    print(f"Données exportées vers {chemin}")

# Appelle la fonction pour scraper les données et les exporter
parse_books()