

# As part of the EDITED team, you'll be responsible for keeping millions of products up-to-date.

# Using python scrapy framework, you have to retrieve the information about the name, selected colour, price and size of a single product located at: https://shop.mango.com/gb/women/skirts-midi/midi-satin-skirt_17042020.html?c=99.

# The solution needs to include the navigation to the product page and extracting the data.
# Output of the parsed data needs to be in a json file.

# Provide the solution as a link to github/gitlab repository. Mail containing link should be send to * 

# Following steps needs to be implemented:
#   - request to load the page located at https://shop.mango.com/bg-en/men/t-shirts-plain/100-linen-slim-fit-t-shirt_47095923.html?c=07
#   - parse of the html
#   - collect the data (name, price, selected default colour and size)
#   - output the data as json file, for example:
# 	{
#   	    "name": String
#   	    "price": Double,
#    	    "colour": String,
#   	    "size": Array
#  }


import scrapy
import json
import re


class MangoSpider(scrapy.Spider):

    filename = 'mango.json'
    name = 'mango'

    def start_requests(self):

        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        # get product name
        name = response.css('h1.product-name::text').get()

        # get product price
        price = response.css('span.product-sale::text').get()

        # get product colour
        colour = response.css('span.color-name::text').get()

        # get product sizes
        sizes = response.css('div.size-selector-container > div > ul > li > a::text').getall()

        # remove whitespaces from sizes
        sizes = [size.strip() for size in sizes]

        # remove empty sizes
        sizes = list(filter(None, sizes))

        # create dictionary
        product = {
            'name': name,
            'price': price,
            'colour': colour,
            'sizes': sizes
        }

        # write dictionary to json file
        with open(self.filename, 'w') as f:
            json.dump(product, f)

        # print dictionary
        print(product)

        # yield dictionary
        yield product


# run spider
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
