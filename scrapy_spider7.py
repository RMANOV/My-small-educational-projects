

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
import re

class MangoSpider(scrapy.Spider):
    """This spider scrapes product information from Mango's online store."""
    
    name = 'mango'
    start_urls = [
        'https://shop.mango.com/bg-en/men/t-shirts-plain/100-linen-slim-fit-t-shirt_47095923.html?c=07',
        'https://shop.mango.com/gb/women/skirts-midi/midi-satin-skirt_17042020.html?c=99'
    ]

    def parse(self, response):
        """Parse the HTML to extract product details."""
        try:
            product = {
                'name': self.get_product_name(response),
                'price': self.get_product_price(response),
                'color': self.get_product_color(response),
                'sizes': self.get_product_sizes(response),
            }
            yield product
        except ValueError as e:
            self.log(f"Failed to extract data from {response.url}: {e}")

    @staticmethod
    def get_product_name(response):
        """Extract and return the product name, or raise ValueError."""
        name = response.css('h1.product-name::text').get()
        if name:
            return name.strip()
        else:
            raise ValueError("Missing name")

    @staticmethod
    def get_product_price(response):
        """Extract and return the product price, or raise ValueError."""
        price_text = response.css('span.product-sale::text').get()
        discounted_price_text = response.css('span.product-discounted-price::text').get()
        price_to_use = discounted_price_text or price_text  # Prioritize discounted price
        if price_to_use:
            match = re.search(r'\d+\.\d+', price_to_use)
            if match:
                return float(match.group())
        raise ValueError("Missing price")

    @staticmethod
    def get_product_color(response):
        """Extract and return the product color(s), or raise ValueError."""
        colors = response.css('span.color-name::text').getall()
        if colors:
            return ", ".join(color.strip() for color in colors)
        else:
            raise ValueError("Missing color")

    @staticmethod
    def get_product_sizes(response):
        """Extract and return the product sizes, or raise ValueError."""
        sizes = response.css('div.size-selector-container > div > ul > li > a::text').getall()
        if sizes:
            return list(filter(None, map(str.strip, sizes)))
        else:
            raise ValueError("Missing sizes")




# To run the spider, you would use the following command:
# scrapy crawl mango -o products.json -s FEED_FORMAT=jsonlines
