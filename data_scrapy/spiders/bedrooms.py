import scrapy
import geopandas as gpd
from scrapy_splash import SplashRequest
import urllib

data = gpd.read_file("pike-addresses-county.geojson")
urls = []

for indexlabel, row in data.iterrows():
    address_number = row["number"]
    address_street = row["street"]
    address_zip = row["postcode"]
    address_county = "pike"
    address_state = "pennsylvania"

    if address_zip == "":
        full_address = (
            address_number
            + " "
            + address_street
            + " "
            + address_county
            + " "
            + address_state
        )
    else:
        full_address = (
            address_number
            + " "
            + address_street
            + " "
            + address_zip
            + " "
            + address_state
        )

    params = {"q": full_address}

    url = "https://www.google.com/search?"
    google_url = url + urllib.parse.urlencode(params)
    urls.append(google_url)


class BedroomsSpider(scrapy.Spider):
    name = "bedrooms"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"

    def start_requests(self):
        for url in urls:
            yield SplashRequest(url)

    def parse(self, response):
        gmap_address_tag1 = response.xpath('//div[@class="aiAXrc"]//text()').get()
        gmap_address_tag2 = response.xpath('//span[@class="fMYBhe"]//text()').get()
        gzillow_address_tag1 = response.xpath('//a[contains(@href,"zillow")]//text()')[
            0
        ].get()
        gzillow_address_body1 = response.xpath(
            '((//a[contains(@href,"zillow")]/parent::node())/parent::node())/following-sibling::node()'
        )[0].get()

        print("---------------------------------------")
        print("address_number:", address_number)
        print("address_street:", address_street)
        print("address_zip:", address_zip)
        print("gmap_address_tag1:", gmap_address_tag1)
        print("gmap_address_tag2:", gmap_address_tag2)
        print("zillow_address_tag1:", gzillow_address_tag1)
        print("gzillow_address_body1:", gzillow_address_body1)
        print("---------------------------------------")

        yield {
            "address_number": address_number,
            "address_street": address_street,
            "address_zip": address_zip,
            "gmap_address_tag1": gmap_address_tag1,
            "gmap_address_tag2": gmap_address_tag2,
            "zillow_address_tag1": gzillow_address_tag1,
            "zillow_address_body1": gzillow_address_body1,
        }
