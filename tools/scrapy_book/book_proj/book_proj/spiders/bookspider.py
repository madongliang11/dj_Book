# -*- coding: utf-8 -*-
import random
import re
from book_proj.items import BookProjItem1,BookProjItem2,BookProjItem3,BookProjItem4
import scrapy
import logging
from scrapy import Request
import datetime

def create_img_figer(input_str, type='sha1'):
    import hashlib
    hash_inst =  hashlib.sha1(input_str.encode("utf8")) \
                 if type == "sha1"   else hashlib.md5(input_str.encode("utf8"))
    return hash_inst.hexdigest()

class BookspiderSpider(scrapy.Spider):
    name = 'bookspider'
    allowed_domains = ['www.quanshuwang.com']
    start_urls = ['http://www.quanshuwang.com/']

    def parse(self, response):
        self.log(f"start to parse url:{response.url}", level=logging.WARNING)
        print(f"start url:{response.url}")
        tag_li_list = response.xpath('//ul[@class="channel-nav-list"]/li')
        for tag_li in tag_li_list:
            t_name = tag_li.xpath('./a/text()').extract_first()
            t_url = tag_li.xpath('./a/@href').extract_first()
            id = re.match('.*?(\d+)_.*', t_url).group(1)

            item = BookProjItem1(
                id = id,
                t_name = t_name,
                t_url = t_url,
                t_createtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                t_flag = 0,
            )
            #print(item)
            yield item

            r = Request(url=t_url, callback=self.parse_tag_art)
            yield r

    def parse_tag_art(self,response):
        art_li_list = response.xpath('//ul[@class="seeWell cf"]/li')
        for art_li in art_li_list:
            a_title = art_li.xpath('./span/a[1]/@title').extract_first()
            a_info = art_li.xpath('./span/em/text()').extract_first()
            a_img_url = art_li.xpath('./a/img/@src').extract_first()
            id = re.match('.*/(\d+)s.*',a_img_url).group(1)
            t_id = re.match('.*?(\d+)_.*',response.url).group(1)
            a_price = random.randint(10,50)
            a_author = art_li.xpath('./span/a[2]/text()').extract_first()
            a_img_url_figer = create_img_figer(a_img_url)

            item = BookProjItem2(
                id = id,
                a_info = a_info,
                a_title = a_title,
                a_img_url = a_img_url,
                t_id = t_id,
                a_price = a_price,
                a_author = a_author,
                a_img_url_figer = a_img_url_figer,
                a_createtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                a_flag = 0,
            )
            print(f"BookProjItem2: {item}")
            yield item

            a_detail_url = art_li.xpath('./span/a[1]/@href').extract_first()
            r = Request(url=a_detail_url, callback=self.parse_art_content)
            yield r


        p = re.compile('.*_(\d+)')
        now_url = response.url
        now_num = p.match(now_url).group(1)
        print(now_num)
        next_url = 'http://www.quanshuwang.com/list/1_' + p.sub(f'{int(now_num)+1}', now_url)
        print(next_url)
        r = Request(url=next_url, callback=self.parse_tag_art)
        yield r


    def parse_art_content(self,response):
        a_content_tmp = response.xpath('//div[@id="waa"]/text()').extract_first()
        a_content = "".join(a_content_tmp.split())
        tmp_url  = response.url
        num = re.match('.*?(\d+)',tmp_url).group(1)
        a_id = num
        item = BookProjItem3(
            id = a_id,
            a_id = a_id,
            a_content = a_content
        )
        #print(item)
        yield item

        art_chapter_url = f'http://www.quanshuwang.com/book/{num[:3]}/{num}'
        r = Request(url=art_chapter_url, callback=self.parse_art_chapter)
        yield r

    def parse_art_chapter(self,response):
        print(f"chapter url: {response.url}")
        a_chapter_list = response.xpath('//div[@class="clearfix dirconone"]/li')
        for a_capter in a_chapter_list:
            capter_each_url = a_capter.xpath('./a/@href').extract_first()
            capter_each_title = a_capter.xpath('./a/text()').extract_first()
            id = capter_each_url.split("/")[-1].split(".")[0]
            title = capter_each_title
            a_id = capter_each_url.split("/")[-2]
            item = BookProjItem4(
                id = id,
                a_id = a_id,
                title = title,
                content = capter_each_url,
                create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            )
            print(item)
            yield item






