# -*- coding: utf-8 -*-
from huaban2.items import Huaban2Item
import scrapy


class HuabanSpider(scrapy.Spider):
    name = 'meipic'
    allowed_domains = ['meisupic.com']
    baseURL = 'http://www.meisupic.com/topic.php'
    start_urls = [baseURL]

    def parse(self, response):
        node_list = response.xpath("//div[@class='body glide']/ul")
        if len(node_list) == 0:
            return
        for node in node_list:
            sub_node_list = node.xpath("./li/dl/a/@href").extract()
            if len(sub_node_list) == 0:
                return
            for url in sub_node_list:
                new_url = self.baseURL[:-9] + url
                yield scrapy.Request(new_url, callback=self.parse2)

    def parse2(self, response):
        node_list = response.xpath("//div[@id='searchCon2']/ul")
        if len(node_list) == 0:
            return
        item = Huaban2Item()
        item["image_url"] = node_list.xpath("./li/a/img/@data-original").extract()
        yield item


