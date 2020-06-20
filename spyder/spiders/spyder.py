import scrapy


# this is the spyder that will scrape the url(s) specified by the user and retrieve the data that they want
class Spyder(scrapy.Spider):

    name = "spyder"

    def __init__(self, *args, **kwargs):
        super(Spyder, self).__init__(*args, **kwargs)
        # set the url to be scraped
        self.start_urls = kwargs.get("urls")
        # set the target dict for this spyder
        self.target_dict = kwargs.get("target_dict")
        # set the file dict for this spider
        self.file_dict = kwargs.get("file_dict")

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        selector_keypairs = self.target_dict[response.url]

        # create dictionary that will be the item that is yielded
        # add the url of this target to the dictionary
        item = {"url": response.url}

        # for each selector key-pair, use the key (pair[0]) as the key in item and extract the data using
        # the css selector itself (pair[1])
        for pair in selector_keypairs:
            item[pair[0]] = response.css(pair[1] + "::text").extract()

        yield item