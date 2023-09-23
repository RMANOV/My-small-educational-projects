

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
import re  # Required for regex in get_product_price()


class MangoSpider(scrapy.Spider):

    name = 'mango'
    start_urls = [
        'https://shop.mango.com/bg-en/men/t-shirts-plain/100-linen-slim-fit-t-shirt_47095923.html?c=07',
        'https://shop.mango.com/gb/women/skirts-midi/midi-satin-skirt_17042020.html?c=99'
    ]

    def parse(self, response):
        product = {
            'name': self.get_product_name(response),
            'price': self.get_product_price(response),
            'colour': self.get_product_colour(response),
            'sizes': self.get_product_sizes(response),
        }

        for key, value in product.items():
            if value is None:
                raise ValueError(f"Missing {key}")

        yield product

    @staticmethod
    def get_product_name(response):
        name = response.css('h1.product-name::text').get()
        return name.strip() if name else None

    @staticmethod
    def get_product_price(response):
        price_text = response.css('span.product-sale::text').get()
        match = re.search(r'\d+\.\d+', price_text) if price_text else None
        return float(match.group()) if match else None

    @staticmethod
    def get_product_colour(response):
        colour = response.css('span.color-name::text').get()
        return colour.strip() if colour else None

    @staticmethod
    def get_product_sizes(response):
        sizes = response.css('div.size-selector-container > div > ul > li > a::text').getall()
        return list(filter(None, map(str.strip, sizes))) if sizes else None


class MangoFeedExport(scrapy.exporters.JsonItemExporter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file = None

    def open_spider(self, spider):
        self.file = open(self.filename, 'a', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()

    def export_item(self, item):
        if self.first_item:
            self.file.seek(0)
            self.file.truncate()

        self.file.write(json.dumps(item, indent=4) + '\n')


# To run the spider, you would use the following command:
# scrapy crawl mango -o products.json -s FEED_EXPORTERS={'products': 'MangoFeedExport'}
