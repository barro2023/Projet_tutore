# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


import scrapy

class RealEstateItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
    type = scrapy.Field()
    price = scrapy.Field()
    location = scrapy.Field()
    


#class RealEstateScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #pass
