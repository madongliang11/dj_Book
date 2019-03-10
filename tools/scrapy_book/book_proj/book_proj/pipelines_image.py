# -*- coding: utf-8 -*-  

import scrapy
#from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        # for image_url in item['image_url']:
        item_name = item.get_name()
        if item_name == 'BookProjItem2':
            image_url = item['a_img_url']
            yield scrapy.Request(url=image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item


