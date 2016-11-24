import scrapy
from dockerhub.items import *
import json
from scrapy.http import Request
import time


class DockerhubSpider(scrapy.Spider):
    name = "dockerhub"
    allowed_domains = ["hub.docker.com"]
    base_url = "https://hub.docker.com/explore/?page="
    # base_query_url = "https://hub.docker.com/v2/search/repositories/?page=1&query=nginx&page_size=100"
    # https: // docker - index - static.s3.amazonaws.com / sitemap / sitemap.xml
    start_urls = []
    for i in range(1, 10):
        start_url = base_url + str(i)
        start_urls.append(start_url)

    def parse(self, response):
        items = []
        for sel in response.xpath('//ul/li'):
            item = OfficialImageItem()
            link = sel.xpath('a/@href').re("/_/.*")
            if link:
                # f.write("%s\n" % (link[0].split("/")[-2]))
                item['name'] = link[0].split("/")[-2]
                item['link'] = "https://hub.docker.com" + link[0]
                with open("/home/pyt/dockerhub/images", "a+") as f:
                    f.write("%s\n" % item['name'])
                # print item
                items.append(item)

        # return items


class SingleImageSpider(scrapy.Spider):
    name = "singleimage"
    allowed_domains = ["hub.docker.com"]
    # base_url = "https://hub.docker.com/explore/?page="
    base_query_url = "https://hub.docker.com/v2/search/repositories/?page=1&page_size=100&query="
    download_delay = 1
    start_urls = []
    for line in open("/home/pyt/dockerhub/images", "r"):
        start_url = base_query_url + line.strip("\n")
        start_urls.append(start_url)

    def parse(self, response):
        url = response.url
        # items = []
        json_str = response.body
        json_ob = json.loads(json_str)
        count = json_ob['count']
        print count
        results = json_ob['results']
        for result in results:
            # time.sleep(1)
            item = ClassifiedImageItem()
            item['star_count'] = result['star_count']
            item['pull_count'] = result['pull_count']
            item['short_description'] = result['short_description'].encode('utf-8')
            item['is_automated'] = result['is_automated']
            item['is_official'] = result['is_official']
            item['repo_name'] = result['repo_name'].encode('utf-8')
            if item['is_official']:
                item['link'] = "https://hub.docker.com/_/" + item['repo_name'].encode('utf-8')
            else:
                item['link'] = "https://hub.docker.com/r/" + item['repo_name'].encode('utf-8')
            item['category'] = url.split("query=")[1].split("&")[0].replace('%2', '/').encode('utf-8')
            yield item

        next_page_link = json_ob['next']
        # print next_page_link
        if next_page_link:
            yield Request(next_page_link, callback=self.parse)

    def parse_item(self, item):
        return item


