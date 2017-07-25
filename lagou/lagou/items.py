# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobItem(scrapy.Item):
	title = scrapy.Field()#岗位名称
	month_salary = scrapy.Field()#月薪
	company = scrapy.Field()#公司名称
	industry = scrapy.Field()#所属行业
	scale = scrapy.Field()#公司规模
	phase = scrapy.Field()#融资阶段
	investors = scrapy.Field()#投资人
	city = scrapy.Field()#所在城市
	experience = scrapy.Field()#经验要求
	qualification = scrapy.Field()#学历要求
	full_or_parttime = scrapy.Field()#全职/兼职
	description = scrapy.Field()#职位描述、任职要求
    pass
