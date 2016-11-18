import scrapy

class DockerhubSpider(scrapy.Spider):
    name = "dockerhub"
    allowed_domains = ["dmoz.org"]
    base_url = "https://hub.docker.com/explore/?page="
    base_query_url = "https://hub.docker.com/v2/search/repositories/?page=1&query=nginx&page_size=100"
    start_urls = []
    for i in range(1,10):
        start_url = base_url + str(i)
        start_urls.append(start_url)

    def parse(self, response):
        filename = "images"
        with open(filename, 'a+') as f:
            for sel in response.xpath('//ul/li'):
                link = sel.xpath('a/@href').re("/_/.*")
                if link != []:
                    f.write("%s\n" % (link[0].split("/")[-2]))
                    print link[0]

