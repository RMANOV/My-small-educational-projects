

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
from scrapy_splash import SplashRequest

class MangoSpider(scrapy.Spider):
    name = 'mango'
    start_urls = [
        'https://shop.mango.com/bg-en/men/t-shirts-plain/100-linen-slim-fit-t-shirt_47095923.html?c=07',
        'https://shop.mango.com/gb/women/skirts-midi/midi-satin-skirt_17042020.html?c=99'
    ]
    
    custom_settings = {
        'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
        'HTTPCACHE_STORAGE': 'scrapy_splash.SplashAwareFSCacheStorage',
    }
    
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                self.parse,
                meta={
                    'splash': {'args': {'wait': 3}},
                    'user-agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
                }
            )

    def parse(self, response):
        try:
            # First attempt to get data from the HTML
            product = {
                'name': self.get_product_name(response),
                'price': self.get_product_price(response),
                'color': self.get_product_color(response),
                'sizes': self.get_product_sizes(response),
            }
            yield product
        except ValueError:
            # If the above fails, try to parse embedded JSON
            script = response.xpath('//script[contains(., "window.__PRELOADED_STATE__")]/text()').get()
            if script:
                try:
                    data = json.loads(re.search(r'window\.__PRELOADED_STATE__\s*=\s*({.*?});', script).group(1))
                    product = {
                        'name': data['product']['name'],
                        'price': data['product']['price']['amount'],
                        'color': data['product']['color']['name'],
                        'sizes': data['product']['sizes'],
                    }
                    yield product
                except (KeyError, ValueError) as e:
                    self.log(f"Failed to extract data from embedded JSON on {response.url}: {e}")
            else:
                self.log(f"Failed to extract any data from {response.url}")

    @staticmethod
    def get_product_name(response):
        name = response.css('h1.product-name::text').get()
        if name:
            return name.strip()
        else:
            raise ValueError("Missing name")

    @staticmethod
    def get_product_price(response):
        price_text = response.css('span.product-sale::text').get()
        discounted_price_text = response.css('span.product-discounted-price::text').get()
        price_to_use = discounted_price_text or price_text
        if price_to_use:
            match = re.search(r'\d+\.\d+', price_to_use)
            if match:
                return float(match.group())
        raise ValueError("Missing price")

    @staticmethod
    def get_product_color(response):
        colors = response.css('span.color-name::text').getall()
        if colors:
            return ", ".join(color.strip() for color in colors)
        else:
            raise ValueError("Missing color")

    @staticmethod
    def get_product_sizes(response):
        sizes = response.css('div.size-selector-container > div > ul > li > a::text').getall()
        if sizes:
            return list(filter(None, map(str.strip, sizes)))
        else:
            raise ValueError("Missing sizes")


# To run the spider, you would use the following command:
# scrapy crawl mango -o products.json -s FEED_FORMAT=jsonlines
