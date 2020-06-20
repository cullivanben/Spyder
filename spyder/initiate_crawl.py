from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spyder.spiders.spyder import Spyder


def initiate_crawl(url_list, target_dict, file_dict):
    """
    Creates a crawler process using the Spyder spider class and feeds it the data that was input by the user
    :param url_list: a list of the target urls in the order that the user added them
    :param target_dict: a dictionary of the target urls and their corresponding css selector key-pairs in 2D list format
    :param file_dict: the user's desired output file types
    :return: void
    """
    # create and start the crawler process
    process = CrawlerProcess(get_project_settings())
    process.crawl(Spyder, file_dict=file_dict, target_dict=target_dict, urls=url_list)
    process.start()
