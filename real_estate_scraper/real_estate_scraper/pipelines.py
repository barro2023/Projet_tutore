#Importation du module psycopg2
import psycopg2
from psycopg2 import pool

#Utilisation de la connexion separée
def get_db():
    conn = psycopg2.connect(
        dbname='dbproject', user='barro', password='BARROBA', host='localhost'
    )
    return conn



class RealEstatePipeline:
    def open_spider(self, spider):
        try:
            self.pool = psycopg2.pool.SimpleConnectionPool(1, 10,
                dbname='dbproject', user='barro', password='BARROBA', host='localhost'
            )
            self.conn = self.pool.getconn()
            self.cursor = self.conn.cursor()
        except psycopg2.Error as e:
            spider.logger.error(f"Erreur lors de la connexion à la base de données : {e}")
            raise

    def close_spider(self, spider):
        
            if self.pool:
                self.pool.closeall()
                spider.logger.info("Connection pool closed.")
        
    def process_item(self, item, spider):
       
        # Gestion du prix
        if item['price']:
            if isinstance(item['price'], str):
                try:
                    item['price'] = int(item['price'].replace(' Fcfa', '').replace(' ', ''))
                except ValueError:
                    spider.logger.error(f"Failed to convert price: {item['price']}")
                    item['price'] = None

        conn = self.pool.getconn()
        try:
            cursor = conn.cursor()

            # Vérification de doublon
            cursor.execute(
                """
                SELECT * FROM listing WHERE type = %s AND price = %s AND location = %s AND title = %s AND description = %s
                """,
                (item['type'], item['price'], item['location'], item['title'], item['description'])
            )
            exists = cursor.fetchone()

            if not exists:
                # Insérer une nouvelle annonce
                cursor.execute(
                    """
                    INSERT INTO listing (type, price, location, title, description)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (item['type'], item['price'], item['location'], item['title'], item['description'])
                )
                spider.logger.info(f"Inserted new listing: {item['title']} at price {item['price']}.")
            else:
                spider.logger.info(f"Duplicate listing found: {item['title']} at price {item['price']}. Skipping.")

            conn.commit()

        except Exception as e:
            spider.logger.error(f"Database operation failed: {e}")
        finally:
            cursor.close()
            self.pool.putconn(conn)

        return item

#Réutilisation de la connexion avec get_db()
"""
import psycopg2

def get_db():
    conn = psycopg2.connect(
        dbname='dbproject', user='barro', password='BARROBA', host='localhost'
    )
    return conn

class RealEstatePipeline:
    def open_spider(self, spider):
        # Ouverture de la connexion à la base de données
        self.conn = get_db()  # Utilise la fonction get_db
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        # Fermeture de la connexion à la base de données
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        try:
            # Insertion dans la base de données
            self.cursor.execute(
                """
                #INSERT INTO listing (type, price, location)
                #VALUES (%s, %s, %s)
               # ON CONFLICT (location) DO NOTHING
                #""",
                #(item['type'], item['price'], item['location'])
            #)

            # Valider la transaction
            #self.conn.commit()

        #except psycopg2.Error as e:
            # En cas d'erreur, loguer l'erreur avec le spider
            #spider.logger.error(f"Erreur lors de l'insertion dans la base de données : {e}")

        #return item

#"""
