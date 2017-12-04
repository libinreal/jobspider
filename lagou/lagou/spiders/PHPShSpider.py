# -*- coding: utf-8 -*-

import scrapy
from JobSpider import JobSpider

class PHPShSpider(JobSpider):
	'''继承JobSpider'''
	name = "PHPSh"
	start_urls = [
    	"https://www.lagou.com/jobs/positionAjax.json"
	]
