# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobItem(scrapy.Item):
	company = scrapy.Field()#公司名称
	companyid = scrapy.Field()#公司名称
	department = scrapy.Field()#招聘部门
	industry = scrapy.Field()#所属领域/行业
	phase = scrapy.Field()#公司发展阶段
	scale = scrapy.Field()#公司规模
	url = scrapy.Field()#公司主页
	investors = scrapy.Field()#投资人
	job = scrapy.Field()#岗位名称
	jobId = scrapy.Field()#岗位名称
	salary = scrapy.Field()#月薪
	city = scrapy.Field()#所在城市
	experience = scrapy.Field()#经验要求
	education = scrapy.Field()#学历要求
	fulltime = scrapy.Field()#全职/兼职
	kw = scrapy.Field()#关键词
	time = scrapy.Field()#发布时间
	
	description = scrapy.Field()#职位描述、任职要求
	addr = scrapy.Field()#工作地址 x,y
	subwayline = scrapy.Field()#地铁沿线
	pos = scrapy.Field()#工作地址

