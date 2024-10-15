#Importation
import scrapy

class AfribabaSpider(scrapy.Spider):
    name = 'afribaba_ouaga'
    start_urls = ['https://bf.afribaba.com/ouagadougou/immobilier-location-vente/ventes-immobilieres/']

    def parse(self, reponse):
        #ads = reponse.css('div.card')
        next_page = None
        from real_estate_scraper.pipelines import get_db
        conn = get_db()  # Établir la connexion à la base de données
        cursor = conn.cursor()  # Créer un curseur

        for ad in reponse.css('div.card'):
            title = ad.css('a.stretched-link::text').get()
            description = ad.css('div.description::text').get(default = "Description not available.")
            type_ = ad.css('span.badge-pill.badge-soft-secondary::text').get()
            price = ad.css('span.badge-primary::text').get()
            location = ad.css('strong.font-size-11::text').get() 

            if title and description and type_ and price and location:

                location = location.strip(', ').capitalize()
        
                print(f"Type: {type_}, Price: {price}, Location: {location}, Title: {title}, Description:{description}")

                yield {
                        'type': type_,
                        'price': price,
                        'location': location,
                        'title':title,
                        'description':description
                    }
                

        next_page = reponse.css('li.page-item a.page-link pagelink::attr(href)').get()

        if next_page:
            self.log(f"Found next_page: {next_page}")
            yield reponse.follow(next_page, self.parse)
        else:
            self.log("No next page found.")


                


            # Insérer les données dans la base de données
            #try:
                #cursor.execute(
                    #"""
                    #INSERT INTO listing (type, price, location)
                    #VALUES (%s, %s, %s)
                    #ON CONFLICT (type, price, location) DO NOTHING 
                    #""",
                    #(item_type.strip(), price.strip(), location.strip())
                #)
            #except Exception as e:
               # print(f"Error inserting data: {e}")

        #conn.commit()  # Valider les changements
        #cursor.close()  # Fermer le curseur
        #conn.close()  # Fermer la connexion

        