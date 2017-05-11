#!/usr/bin/python
# -*- coding: UTF-8 -*-

import csv
class CGeographyHeightByFile(object):

    #__LoggerNameList = {'log_yield_test':[LOGGER_yield,  logging.DEBUG],

    def __init__(self , csvFile):             
        f = open( csvFile , 'r', encoding='big5')
        reader = csv.reader(f) #讀取csv中的各列資料(含表頭)
        headers = next(reader) #讀取當前位置的資料給headers，隨後把當前位置指向下一筆資料(表頭資料就消失了)
        #row_count = len(reader) = 2     
        listReader = list(reader)   
        self.__row_count = len(listReader)   

        self.__objRow = {}
        for i , d in enumerate(listReader):
            #self.__objRow[i] = [] #宣告陣列
            self.__objRow[i] = { "min":d[0] , "max":d[1] } #objRow[0][min] = min-height objRow[0][max] = max-height
 
        #for r in reader:
        #    objRow[i].append( [ r[0] , r[1] ] )  #objRow[0][0] = min-height objRow[0][1] = max-height
        #    #objRow[i].append( { "min":r[0] , "max":r[1] } )  #objRow[0][min] = min-height objRow[0][max] = max-height
        #    i += 1
        #    next(reader)
        
        #print(self.__objRow)
        #pass

        #column = {} #此物件用來表示各欄
        #for h in headers:
        #    column[h] = [] #產生陣列        
        #
        #for row in reader:
        #    for h,v in  zip( headers , row ) :     
        #        column[h].append(currentValue)   

        #objHeight={}
        #for h in objHeight:
        #    column[h] = [] #產生陣列
        #self.__ACCOUNT =acount
        #self.__PASSWORD = password

    def CountRow(self):
        return self.__row_count

    def getRow(self):
        return self.__objRow