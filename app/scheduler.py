from apscheduler.schedulers.background import BackgroundScheduler

def check_for_new_ads():
    from app.notification import send_notification
    from app.models import Listing, SearchPreferences
    preferences = SearchPreferences.query.all()
    for pref in preferences:
        ads = Listing.query.filter(
            Listing.type == pref.type,
            Listing.price <= pref.price,
            Listing.location.like(f"%{pref.location}%")
        ).all()

        if ads:
            for ad in ads:
            # Envoyer une notification à l'utilisateur
                send_notification(pref.user.email, ad)

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=check_for_new_ads, trigger="interval", hours=1)
    scheduler.start()



#Imports
import schedule
import time
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from real_estate_scraper.real_estate_scraper.spiders.jumia_house_spider import AfribabaSpider
from real_estate_scraper.real_estate_scraper.spiders.vivastreet_spider import VivastreetSpider


def scrape_jumia():
    # Configuration pour lancer le spider Jumia avec Scrapy
    configure_logging()
    runner = CrawlerRunner()

    # Démarre le spider en utilisant CrawlerRunner
    d = runner.crawl(AfribabaSpider)
    d.addBoth(lambda _: reactor.stop())

    reactor.run()  # Bloque ici jusqu'à ce que le scraping soit terminé

def scrape_vivastreet():
    # Configuration pour lancer le spider Jumia avec Scrapy
    configure_logging()
    runner = CrawlerRunner()

    # Démarre le spider en utilisant CrawlerRunner
    d = runner.crawl(VivastreetSpider)
    d.addBoth(lambda _: reactor.stop())

    reactor.run()  # Bloque ici jusqu'à ce que le scraping soit terminé

    
# Planifie les tâches
schedule.every().day.at("10:00").do(scrape_jumia)
schedule.every().day.at("12:00").do(scrape_vivastreet)

# Boucle pour garder le planificateur actif
while True:
    schedule.run_pending()
    time.sleep(1)



