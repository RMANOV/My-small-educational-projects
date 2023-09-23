

# As part of the EDITED team, you'll be responsible for keeping millions of products up-to-date.

# Using python scrapy framework, you have to retrieve the information about the name, selected color, price and size of a single product located at: https://shop.mango.com/gb/women/skirts-midi/midi-satin-skirt_17042020.html?c=99.

# The solution needs to include the navigation to the product page and extracting the data.
# Output of the parsed data needs to be in a json file.

# Provide the solution as a link to github/gitlab repository. Mail containing link should be send to * 

# Following steps needs to be implemented:
#   - request to load the page located at https://shop.mango.com/bg-en/men/t-shirts-plain/100-linen-slim-fit-t-shirt_47095923.html?c=07
#   - parse of the html
#   - collect the data (name, price, selected default color and size)
#   - output the data as json file, for example:
# 	{
#   	    "name": String
#   	    "price": Double,
#    	    "color": String,
#   	    "size": Array
#  }


import scrapy
import json
import re
import os


class MangoSpider(scrapy.Spider):

    filename = 'mango.json'
    name = 'mango'
    start_urls = [
        'https://shop.mango.com/bg-en/men/t-shirts-plain/100-linen-slim-fit-t-shirt_47095923.html?c=07',
        'https://shop.mango.com/gb/women/skirts-midi/midi-satin-skirt_17042020.html?c=99'
    ]

    def parse(self, response):
        product = {
            'name': self.get_product_name(response),
            'price': self.get_product_price(response),
            'color': self.get_product_color(response),
            'sizes': self.get_product_sizes(response),
        }

        self.write_to_json(product)
        yield product

    @staticmethod
    def get_product_name(response):
        return response.css('h1.product-name::text').get().strip()

    @staticmethod
    def get_product_price(response):
        price_text = response.css('span.product-sale::text').get()
        return float(re.search(r'\d+\.\d+', price_text).group()) if price_text else None

    @staticmethod
    def get_product_color(response):
        return response.css('span.color-name::text').get().strip()

    @staticmethod
    def get_product_sizes(response):
        sizes = response.css('div.size-selector-container > div > ul > li > a::text').getall()
        return list(filter(None, map(str.strip, sizes)))

    def write_to_json(self, data):
        existing_data = []

        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                existing_data = json.load(f)
        
        existing_data.append(data)

        with open(self.filename, 'w') as f:
            json.dump(existing_data, f, indent=4)


# To run the spider, the command remains the same:
# scrapy runspider mango.python


# run spider and save output to json file
# scrapy runspider mango.python -o mango.json

# run spider and save output to json file and log to log file
# scrapy runspider mango.python -o mango.json -s LOG_FILE=mango.log

# run spider and save output to json file and log to log file and disable log to stdout
# scrapy runspider mango.python -o mango.json -s LOG_FILE=mango.log -s LOG_STDOUT=False

# run spider and save output to json file and log to log file and disable log to stdout and disable log to stderr
# scrapy runspider mango.python -o mango.json -s LOG_FILE=mango.log -s LOG_STDOUT=False -s LOG_STDERR=False

# run spider and save output to json file and log to log file and disable log to stdout and disable log to stderr and disable log to file
# scrapy runspider mango.python -o mango.json -s LOG_FILE=mango.log -s LOG_STDOUT=False -s LOG_STDERR=False -s LOG_ENABLED=False
