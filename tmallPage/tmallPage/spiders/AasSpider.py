# -*- coding: utf-8 -*-
import scrapy
import urllib

class AasSpider(scrapy.Spider):
    name = 'Aas'
    allowed_domains = ['https://list.tmall.com/search_product.htm']

    def start_requests(self):
    	self.initHead = {
			"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
			"accept-encoding":"gzip, deflate, br",
			"accept-language":"zh-CN,zh;q=0.9",
			"cache-control":"max-age=0",
			"referer":"https://www.tmall.com/",
			"upgrade-insecure-requests":"1"
		}

    	self.url = self.allowed_domains[0] + "?q=%s&type=p&cat=all"
    	self.url = self.url % "OPPO手机拍照"
    	yield scrapy.http.FormRequest(url=self.url, method='GET', headers=self.initHead, callback=self.parsePage)

    def parsePage(self, response):
      print "  response url \n", response.url, "\n"
      proto, rest = urllib.splittype(response.url)
      res, rest = urllib.splithost(rest)
      if res == 'sec.taobao.com':
        print ' input verify code '

    def antiLogin(self, response):
        pass

    def antiVerify(self, response):
      verifyFormAction = 'https://sec.taobao.com/query.htm'
   		
      initVerifyFormData = {
      	'action': None,
      	'event_submit_do_query': None,
      	'smPolicy': None,
      	'smReturn': None,
      	'smApp': None,
      	'smCharset': None,
      	'smTag': None,
      	'smSign': None,
      	'identity': None,
      	'captcha': None,
      	'checkcode': None,
      	'ua': None
      }

      verifyFormHead = dict(self.initHead)

      verifyFormData = dict()

      for vfk, vfv in initVerifyFormData.items():
        verifyFormData[vfk] = response.xpath("//input[@name='%s']/@value" % vfk).extract()

      scrapy.http.FormRequest(url=verifyFormAction, method='POST', headers=verifyFormHead, callback=self.parsePage)
