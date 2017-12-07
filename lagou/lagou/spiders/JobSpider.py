# -*- coding: utf-8 -*-

import sys
import scrapy
import json

from scrapy.exceptions import CloseSpider

class JobSpider(scrapy.Spider):
    allowed_domains = ["lagou.com"]

    name = 'Job'

    def start_requests(self):
        '''
        check job with multiple kd <key word> and multiple location
        '''

        self.header = {
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

        #list of multi query string spelled base on filterDict
        queryStringList = []

        #dict single node key-val for spell query string
        filterDictNode = {
            'jd':[],#融资阶段 可同时指定多个
            'px':'default',#排序方式 一次一个
            'needAddtionalResult':'false',
            'isSchoolJob':0
        }

        #dict tree nodes key-val for spell query string, if value is empty set None
        filterDictTree = {
            'city_上海':{'district_徐汇区':['bizArea_漕宝路', 'bizArea_上海南站', 'bizArea_植物园', 'bizArea_上海师大', 'bizArea_田林', 'bizArea_龙华']} # 方便遍历
        }

        #key word list for search form-data
        kdList = ['PHP', 'Python', 'Go']

        queryString = ''

        #filter of single dict node
        for fk in filterDictNode:
            
            #current spelled string for value of fk in filterDict
            fks = ''

            #list type
            if type(filterDictNode[fk]) == list:

                #在queryString中可以有多个值，用','分割
                #loop fki in filerDict[fk]:[fki … ]
                for fki in filterDictNode[fk]:
                    if type(fki) == str or type(fki) == unicode:
                        if fki.strip() == '':
                            continue
                        else:
                            fks = fks + '%s,' % fki
                if len(fks) > 0:
                    fks = fks[0:-1]

            #string type
            elif type(filterDictNode[fk]) == str or type(filterDictNode[fk]) == unicode:
                if filterDictNode[fk].strip() == '':
                    continue
                fks = filterDictNode[fk]

            #other types e.g. int,boolean,object…
            else:
                fks = filterDictNode[fk]

            if (type(fks) == str or type(fks) == unicode) and len(fks) == 0:
                continue
            
            #spell query string such as: city=上海&…
            # print ' spell queryString ', fk, fks
            queryString = queryString + '%s=%s&' % (fk, fks)

        if len(queryString) > 0:
            queryString = queryString[0:-1]
        
        #filter of tree dict nodes [at most 3 level]
        for (tk, tv) in filterDictTree.items():

            if len(queryString) > 0:
                queryString1 = '&'
            else:
                queryString1 = ''

            #loop level 1
            if type(tv) == dict:
                #tk
                f, v = tk.split('_')
                queryString1 = queryString1 + '%s=%s&' % (f, v)

                #loop level 2
                for (tk1, tv1) in tv.items():

                    #loop level 3
                    if type(tv1) == list:
                        #tk1
                        f, v = tk1.split('_')
                        queryString1 = queryString1 + '%s=%s&' % (f, v)

                        #loop list value tv1
                        for tv2 in tv1:
                            #tv2
                            f, v = tv2.split('_')
                            queryStringList.append( queryString + queryString1 + '%s=%s' % (f, v) )

                    elif type(tv1) == None:
                        #tk1
                        f, v = tk1.split('_')
                        queryString1 = queryString1 + '%s=%s&' % (f, v)

                        queryStringList.append( queryString + queryString1[0:-1] )

            elif type(tv) == list:
                #tk
                f, v = tk.split('_')
                queryString1 = queryString1 + '%s=%s&' % (f, v)

                #loop list value tv1
                for tv1 in tv:
                    f, v = tv1.split('_')
                    queryString1 = queryString1 + '%s=%s&' % (f, v)

                    queryStringList.append( queryString + queryString1[0:-1] )

            elif type(tv) == None:
                #tk
                f, v = tk.split('_')
                queryString1 = queryString1 + '%s=%s&' % (f, v)

                queryStringList.append( queryString + queryString1[0:-1] )

        #constant request url
        
        # print ','.join(queryStringList)

        for q in queryStringList:

            reqUrl = 'https://www.lagou.com/jobs/positionAjax.json?%s' % q

            #dynamic form data
            for kd in kdList:

                # print "1", "\t", reqUrl, "\t", kd

                yield scrapy.http.FormRequest(url=reqUrl, formdata={'pn':'1','kd':kd,'first':'false'}, method='POST', headers=self.header, callback=self.parse)

    def parse(self, response):
        '''
        override处理下载的positionAjax.json的response<TextResponse>的默认方法

        json body:
        {
            content:{
                        pageNo:1
                        pageSize:15
                        positionResult:{
                                            result:{
                                                        companyId:47993
                                                        positionId:3287191
                                                    }
                                            resultSize:15
                                            totalCount:19
                                        }
                    }

        }
        '''
        # print response.body

        jsonData = json.loads(response.body)

        if jsonData.has_key('content') == False:
            raise CloseSpider('Response has no content attribute')

        jsonContent = jsonData['content']
        jsonResult = jsonContent['positionResult']
        jsonItems = jsonResult['result']
   
        totalPageCount = jsonResult['totalCount'] / jsonContent['pageSize'] + 1

        # print jsonContent['pageNo'], "\t", jsonResult['resultSize'], "\t", jsonResult['totalCount']
        # print type(response), response.request.body, response.request.url

        
        '''        
            print jsonResult['resultSize'], "\t", jsonResult['totalCount'], "\t", totalPageCount
        '''

        #debug
        '''
        for (rk, rv) in jsonResult.items():
            if rk == 'totalCount':
                print '%s:%s' % (rk, rv)
            elif rk == 'pageSize':
                print '%s:%s' % (rk, rv)
            elif rk == 'result':
                print '%s:%s' % (rk, rv)
        '''
        print "\n\n",response.request.body
        for e in jsonItems:
            
            print e['companyId'] #公司id
            print e['positionId'] #职位id
            print e['subwayline'] #地铁线
            print e['createTime']
            print e['district']
            print e['education']
            print e['industryField']
            print e['positionName']

        print "\n\n"
        
        if jsonContent['pageNo'] < totalPageCount:
            
            #last request form data
            d = self.__getFormDataFromResponse(response)
            #next page
            d['pn'] = str( int(d['pn']) + 1 )

            # print self.pageNo, "\t", self.pageCount, "\t", self.reqUrl, "\t", self.kd
            yield scrapy.http.FormRequest(response.request.url, formdata=d, method='POST', headers=self.header, callback=self.parse)

    def __getFormDataFromResponse(self, response):
        '''
        返回响应对应的请求数据，dict类型
        '''

        d = {}

        a = response.request.body.split('&')

        for i in a:
            k, v = i.split('=')
            d[k] = v

        return d
        
    def parse_job(self, response):
        '''
        分析 https://www.lagou.com/jobs/3461000.html 的response,获取job detail
        '''
        response.body


