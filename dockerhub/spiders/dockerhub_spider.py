import scrapy
from dockerhub.items import *

class DockerhubSpider(scrapy.Spider):
    name = "dockerhub"
    allowed_domains = ["hub.docker.com"]
    base_url = "https://hub.docker.com/explore/?page="
    # base_query_url = "https://hub.docker.com/v2/search/repositories/?page=1&query=nginx&page_size=100"
    start_urls = []
    for i in range(1,10):
        start_url = base_url + str(i)
        start_urls.append(start_url)

    def parse(self, response):
        items = []
        for sel in response.xpath('//ul/li'):
            item = OfficialImageItem()
            link = sel.xpath('a/@href').re("/_/.*")
            if link != []:
                # f.write("%s\n" % (link[0].split("/")[-2]))
                item['name'] = link[0].split("/")[-2]
                item['link'] = "https://hub.docker.com" + link[0]
                print item
                items.append(item)

        return items

