# -*- coding: utf-8 -*-

import sys
import scrapy
import json

class JobSpider(scrapy.Spider):
    allowed_domains = ["lagou.com"]

    name = 'Job'

    '''paganation info'''
    pageCount = 0
    pageNo = 1

    #current request url 
    reqUrl = ''

    #current kd
    kd = ''

    header = {
        'Accept':'Accept:application/json, text/javascript, */*; q=0.01',
        'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding':'gzip, deflate, br',
        'Host':'www.lagou.com',
        'User-Agent':[
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'
        ],
        'Referer':'https://www.lagou.com/jobs/list_PHP',
        'X-Requested-With':'XMLHttpRequest',
        'X-Anit-Forge-Token':'None',
        'X-Anit-Forge-Code':'0'
    }

    def start_requests(self):
        '''
        check job with multiple kd <key word> and multiple location
        '''

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
            # print fks,' fks '
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
                            queryString1 = queryString1 + '%s=%s&' % (f, v)

                            queryStringList.append( queryString + queryString1[0:-1] )
                            print queryStringList, ' queryStringList '

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

        # print queryStr[0:-1],' queryStr start_requests '
        #constant request url

        for q in queryStringList:

            self.reqUrl = 'https://www.lagou.com/jobs/positionAjax.json?%s' % q

            #dynamic form data
            for kd in kdList:
                self.kd = kd
                '''
                dc = {'url':self.reqUrl, 'formdata':{'pn':self.pageNo,'kd':self.kd,'first':False}, 'method':'POST', 'headers':self.header, 'callback':self.parse}
                print dc
                sys.exit()
                '''
                yield scrapy.http.FormRequest(url=self.reqUrl, formdata={'pn':str(self.pageNo),'kd':self.kd,'first':'false'}, method='POST', headers=self.header, callback=self.parse)

    def parse(self, response):
        fp = open('1.html','a+')
        fp.write(response.body)
        fp.close()
        '''
        override处理下载的response的默认方法

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
        


        jsonData = json.loads(response.body)
        jsonContent = jsonData['content']
        jsonResult = jsonContent['positionResult']
        jsonItems = jsonResult['result']
        # print jsonData, 'jsonData'
        self.pageCount = jsonResult['totalCount'] / jsonContent['pageSize'] + 1

        for e in jsonItems:
            '''
            print e['companyId'] #公司id
            print e['positionId'] #职位id
            print e['subwayline'] #地铁线
            print e['createTime']
            print e['district']
            print e['education']
            print e['industryField']
            '''
            pass
            
        if self.pageNo <= self.pageCount:
            self.pageNo += 1
            yield scrapy.http.FormRequest(url=self.reqUrl, formdata={'pn':str(self.pageNo),'kd':self.kd,'first':'false'}, method='POST', headers=self.header, callback=self.parse)