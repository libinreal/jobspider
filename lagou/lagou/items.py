# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst

class JobItem(scrapy.Item):
	company = scrapy.Field()#公司名称
	companyid = scrapy.Field()#公司名称
	department = scrapy.Field()#招聘部门
	industry = scrapy.Field()#所属领域/行业
	phase = scrapy.Field()#公司发展阶段
	scale = scrapy.Field()#公司规模
	homepage = scrapy.Field()#公司主页
	investors = scrapy.Field()#投资人
	job = scrapy.Field()#岗位名称
	jobid = scrapy.Field()#岗位名称
	salary = scrapy.Field()#月薪
	city = scrapy.Field()#所在城市
	experience = scrapy.Field()#经验要求
	education = scrapy.Field()#学历要求
	fulltime = scrapy.Field()#全职/兼职
	label = scrapy.Field()#关键词/标签
	createtime = scrapy.Field()#发布时间
	
	description = scrapy.Field()#职位描述、任职要求
	coordinate = scrapy.Field()#x,y坐标
	subwayline = scrapy.Field()#地铁沿线
	address = scrapy.Field()#详细工作地址
	platform = scrapy.Field()#平台


class JobItemLoader(scrapy.loader.ItemLoader):
	default_input_processor = MapCompose(unicode, unicode.strip)
	default_output_processor = TakeFirst()
