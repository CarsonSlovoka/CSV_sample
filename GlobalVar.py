#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os,sys ,threading , logging , platform

class result_container:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs) # copy arguments to attributes

IS_PY2 =  sys.version[0] == '2'
IS_OSX_PLATFORM = platform.system() == 'Darwin'  # – 傳回 Windows、Linux、Darwin(OS X)、Java 等字串。
IS_WINDOWS_PLATFORM = platform.system() == 'Windows' 


PATH = result_container()
PATH.FORDER = result_container()
PATH.FILE = result_container()
PATH.PNG = result_container()
PATH.ICON = result_container()
PATH.JPEG = result_container()


PATH.FORDER.LOG = os.path.dirname(os.path.abspath('__file__'))+ "\\LOG\\"
#PATH.FORDER.CSV = os.path.dirname(os.path.abspath('__file__'))+ "\\Geography_CSV_DATA\\"
PATH.FORDER.CSV = './Geography_CSV_DATA'
PATH.FORDER.TXT = './Geography_TXT_DATA'
#PATH.FORDER.CSV.HEIGHT = './Geography_CSV_DATA'

PATH.FILE.RESULT_CSV = './Geography_CSV_DATA/'
