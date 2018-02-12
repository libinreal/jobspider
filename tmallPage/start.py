#!c:\python27\python.exe
# -*- coding: utf-8 -*-
import os
import sys
sys.path.append('..')
from utils.common.Common import get_lan_ip
#获取公网IP
def get_public_ip(self):
    try:
        myip = _visit("http://whois.pconline.com.cn")   #visit访问节点
    except:
        try:
            myip = _visit("http://www.net.cn/static/customercare/yourip.asp")
        except:
            try:
                myip = _visit("http://ip.chinaz.com/getip.aspx")
            except:
                myip = '0'
                
    return myip

  
def _visit(self,url):
    urler = urllib.parse.urlparse(url)
    if url == urler.geturl():
        opener = urllib.request.urlopen(url)     
        strg = opener.read()
        strg = strg.decode('gbk')
    ipaddr = re.search('\d+\.\d+\.\d+\.\d+',strg).group(0)
    location = re.search(r"(.*)市(.*)",strg).group(0)
    location = location.expandtabs(1)
    
    return ipaddr+location


from scrapy.utils.project import inside_project, get_project_settings

def execute():
	settings = get_project_settings()
	'''
	ENVVAR = 'SCRAPY_SETTINGS_MODULE'
	settings_module_path = os.environ.get(ENVVAR)
    if settings_module_path:
        settings.setmodule(settings_module_path, priority='project')
	'''
	print settings.get('BOT_NAME')

	paginationIp = settings.get('TEMP_PAGINATION_IP')

	print 'localhost ip config test : ', 1 and '192.168.2.193' in paginationIp

	for k, v in paginationIp.items():
		if v:
			for vv in v:
				print "  %s : %s" %(k, vv)

	print 'ip address: %s' % get_lan_ip()
	# print dir(settings)

	# for k,v in settings.iteritems():
	# 	print "%s %s" % (k , v)

	# print inproject
	# print os.environ
	# print settings.BOT_NAME


if __name__ == '__main__':
    execute()