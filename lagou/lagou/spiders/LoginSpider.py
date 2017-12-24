# -*- coding: utf-8 -*-

import scrapy
from BaseSpider import BaseSpider

class LoginSpider(BaseSpider):

	name = "Login"



	def start_requests(self):
		
		loginPage = 'https://passport.lagou.com/login/login.html'

		yield scrapy.Request(url=loginPage, callback=self.parse_page)

	def parse(self, response):

		response.xpath()

