# -*- coding: UTF-8 -*-

from functools import wraps
import chardet

class BaseObject(object):
    '''基类'''
    def __getattr__(self, name):
        ''' 属性不存在时，调用子类实现的getProperty()函数'''
        name = "get%s" % name.capitalize()#方法名
        print " BaseObject __getattr__ %s \r\n" % name
        print " hasattr:%s callable:%s " % (hasattr(self, name), callable(getattr(self, name)))
        if hasattr(self, name) and callable(getattr(self, name)):
            print "__getattr__ class: %s , class name:%s , property name: %s %s" % ( self.__class__, self.__class__.__name__, name, (getattr(self, name)).__name__ )
            getattr(self, name)()
        else:
            raise Exception('Method %s.%s does not exist!' % (self.__class__.name, name) )
        return self

    def dump_func_info(f):
        '''调试函数调用情况'''
        @wraps(f)
        def with_dump(*args, **kwargs):
            print f.__name__ + ' was called'
            return f(*args, **kwargs)
        return with_dump

    def encoding(self, _s):
        detDict = chardet.detect(bytes(_s))

        return detDict['encoding']
