# -*- coding: utf-8 -*-  
__author__ = 'zhougy'
__date__ = '2018/10/23 上午10:56'

'''
scrapy 操作mysql数据库解决方案：
1. pymysql
2. 采用scrapy内置的twisted网络库自带的企业级的异步database api库 --- adbapi

'''

from twisted.enterprise import adbapi
from .settings import MYSQL_SETTINGS, SPIDER_DB_OP_DISPACH
import logging

class MySQLPipeLine(object):
	def __init__(self, dbpool):
		self.__dbpool = dbpool

	@classmethod
	def from_crawler(cls, *args, **kwargs):
		# 读取配置文件内容
		dbparms = dict(
			host=MYSQL_SETTINGS['HOST'],
			db=MYSQL_SETTINGS['DATABASE'],
			user=MYSQL_SETTINGS['USER'],
			passwd=MYSQL_SETTINGS['PASSWORD'],
			charset=MYSQL_SETTINGS['CHARSET'],
		)
		# 创建mysql数据库实例
		dbpool = adbapi.ConnectionPool("pymysql", **dbparms)
		return cls(dbpool)   # 等同于调用 MySQLPipeLine(dbpool)


	def process_item(self, item, spider):
		'''
		使用twisted提供的adbapi进行操作
		:param item:
		:param spider:
		:return:
		'''
		defferd = self.__dbpool.runInteraction(self.db_insert_handle, item, spider)
		defferd.addErrback(self.db_insert_error_handle, item, spider)

		#defferd = self.__dbpool.runInteraction(self.db_update_handle, item, spider)
		#defferd.addErrback(self.db_update_error_handle, item, spider)
		return item

	def db_insert_handle(self, cursor, item, spider):
		'''
		数据库插入操作
		:return:
		'''
		key = spider.name
		insert_sql = SPIDER_DB_OP_DISPACH[key].get(item.get_name())[0]
		item_fields = SPIDER_DB_OP_DISPACH[key].get(item.get_name())[1]
		field_count = len(item_fields)
		item_values = []
		for index in range(field_count):
			item_values.append(item[item_fields[index]])
		try:
			cursor.execute(insert_sql, item_values)
		except Exception as e:
			logging.error(f"{spider.name} db_insert_handle has error with {e}")
			return False
		return True

	def db_insert_error_handle(self, error, item, spider):
		logging.error(f"{spider.name} db_insert_error_handle has error with {error}")

		return False





