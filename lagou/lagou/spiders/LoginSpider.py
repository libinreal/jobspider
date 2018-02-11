# -*- coding: utf-8 -*-

import scrapy
from BaseSpider import BaseSpider

class LoginSpider(BaseSpider):

	name = "Login"



	def start_requests(self):
		
		loginUrl = 'https://passport.lagou.com/login/login.html'

		loginHeader = {
			'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'Accept-Encoding':'gzip, deflate, br',
			'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
			'Cache-Control':'max-age=0',
			'Connection':'keep-alive',

            'Accept':'Accept:application/json, text/javascript, */*; q=0.01',
            'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding':'gzip, deflate, br',
            'Host':'www.lagou.com',
            'Origin':'https://www.lagou.com',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer':[
                'https://www.lagou.com/jobs/list_PHP',
                'https://www.lagou.com/jobs/list_PHP?px=default&jd=%E4%B8%8A%E5%B8%82%E5%85%AC%E5%8F%B8&city=%E4%B8%8A%E6%B5%B7&district=%E5%BE%90%E6%B1%87%E5%8C%BA&bizArea=%E6%BC%95%E5%AE%9D%E8%B7%AF',
                'https://www.lagou.com/jobs/list_PHP?px=default&city=%E4%B8%8A%E6%B5%B7&district=%E5%BE%90%E6%B1%87%E5%8C%BA&bizArea=%E6%BC%95%E5%AE%9D%E8%B7%AF',
                'https://www.lagou.com/jobs/list_Go?city=%E4%B8%8A%E6%B5%B7&district=%E5%BE%90%E6%B1%87%E5%8C%BA&bizArea=%E6%BC%95%E5%AE%9D%E8%B7%AF&cl=false&fromSearch=true&labelWords=&suginput=',
                'https://www.lagou.com/jobs/list_Python?city=%E4%B8%8A%E6%B5%B7&district=%E5%BE%90%E6%B1%87%E5%8C%BA&bizArea=%E6%BC%95%E5%AE%9D%E8%B7%AF&cl=false&fromSearch=true&labelWords=&suginput='
            ],
            'X-Requested-With':'XMLHttpRequest',
            'X-Anit-Forge-Token':'None',
            'X-Anit-Forge-Code':'0'
        }

		jsonUrl = ''

		jsonHeader = {

			'Accept':'Accept:application/json, text/javascript, */*; q=0.01',
            'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding':'gzip, deflate, br',
            'Host':'passport.lagou.com',
            'Origin':'https://passport.lagou.com',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
            'Referer':'https://passport.lagou.com/login/login.html',
            'X-Requested-With':'XMLHttpRequest',
            #'X-Anit-Forge-Token':'None',
            #'X-Anit-Forge-Code':'0'
		}

		yield scrapy.Request(url=loginPage, callback=self.parse_page)

	def parse(self, response):

		response.xpath()

