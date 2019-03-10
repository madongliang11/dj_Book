# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class BookProjItem1(scrapy.Item):
    # 小说标签类
    id = scrapy.Field()
    t_name = scrapy.Field()
    t_createtime = scrapy.Field()
    t_url = scrapy.Field()
    t_flag = scrapy.Field()

    def get_name(self):
        return BookProjItem1.__name__

class BookProjItem2(scrapy.Item):
    # 小说内容
    id = scrapy.Field()
    a_title = scrapy.Field()
    a_img_url = scrapy.Field()
    t_id = scrapy.Field()   #  外键  关联文章标签
    a_price = scrapy.Field()
    a_author = scrapy.Field()
    a_info = scrapy.Field()
    a_img_url_figer = scrapy.Field()
    a_createtime = scrapy.Field()
    a_flag = scrapy.Field()

    def get_name(self):
        return BookProjItem2.__name__

class BookProjItem3(scrapy.Item):
    # 小说的章节信息
    id = scrapy.Field()
    a_id = scrapy.Field()   # 外键 关联art
    a_content = scrapy.Field()
    def get_name(self):
        return BookProjItem3.__name__

class BookProjItem4(scrapy.Item):
    # 小说的章节信息
    id = scrapy.Field()    #章节id
    a_id = scrapy.Field()   # 外键 关联art
    title = scrapy.Field()
    content = scrapy.Field()
    create_time = scrapy.Field()
    # content = scrapy.Field()

    def get_name(self):
        return BookProjItem4.__name__





