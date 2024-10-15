#Importation
import scrapy
from real_estate_scraper.pipelines import get_db

def clean_price(price):
    # Supprimer le symbole de devise et les espaces insécables
    price = price.replace('€', '').replace('\u202f', '').replace(',', '').strip()
    try:
        return int(price)
    except ValueError:
        return None  # Retourne None si la conversion échoue

class VivastreetSpider(scrapy.Spider):
    name = 'vivastreet_immobilier'
    start_urls = ['https://www.vivastreet.com/immobilier-vente-maison/etranger-bf']

    def parse(self, response):

        # Établir la connexion à la base de données
        conn = get_db()  
        cursor = conn.cursor() 

        for ad in response.css('li.kiwii-clad-row'):
            # Extraire les informations
            title= ad.css('h2::text').get()
            price = ad.css('.clad__price::text').get() 
            description = ad.css('.clad__shortdesc::text').get()
            location = ad.css('.clad__first_geo::text').get()
            type = ad.css('.clad__spec').get(default = "Non spécifié.")

            # Valeur par défaut si aucun mot-clé ne correspond
            type_default = "Inconnu"
              
            if title:
                title_lower = title.lower()

                if 'appartement' in title_lower:
                    type_default = "Appartement"
                elif 'maison' in title_lower:
                    type_default = "Maison"
                elif 'terrain' in title_lower:
                    type_default = "Terrain"

            if description:
                description_lower = description.lower()
                if 'appartement' in description_lower:
                    type_default = "Appartement"
                elif 'maison' in description_lower:
                    type_default = "Maison"
                elif 'terrain' in description_lower:
                    type_default = "Terrain"

              
            if type and price and location :
                # Nettoyer le prix
                clean_price_value = clean_price(price)

                if clean_price_value is not None:
                    print(f"Type: {type_default}, Price: {clean_price_value}, Location: {location}, Title: {title}, Description: {description}")

                    yield {
                        'title': title,
                        'description': description,
                        'type': type_default,
                        'price': clean_price_value,
                        'location': location,
                    }        

        #next_page = response.css('a.next-page::attr(href)').get()
        #if next_page:
            #yield response.follow(next_page, self.parse)
            


                    