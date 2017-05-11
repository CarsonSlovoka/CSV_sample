#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging
import csv , sys , os
import subprocess #from subprocess import Popen
#from decimal import Decimal
import pathlib
from pathlib import Path

import GlobalVar
import CMyFile
from CGeographyHeightByFile import CGeographyHeightByFile

import ctypes #msgbox

class result_container:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs) # copy arguments to attributes


if 'Golbal':    
    if 'Logger Object Setting':
        if 'default root.logger Setting':
            logging.getLogger().setLevel(logging.DEBUG)
            #logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s -  -  %(threadName)s - %(processName)s -' )
            logging.basicConfig(level= logging.DEBUG , format = '%(message)s' )
        if 'My Logger Setting':
            LOGGER_yield    = logging.Logger('LOGGER_YIELD_TEST')  #全都可寫入    
            myLogger        = logging.Logger(' ')
            #LOGGER_DEBUG     = logging.Logger('LOGGER_DEBUG')
            #LOGGER_INFO      = logging.Logger('LOGGER_INFO')    #LOGGER_INFO.info流程執行結束
            #LOGGER_WARNING   = logging.Logger('LOGGER_WARNING') #檔案欠缺WARING.error
            #LOGGER_ERROR     = logging.Logger('LOGGER_ERROR')   #程式問題導致當機
            #LOGGER_CRITICAL  = logging.Logger('LOGGER_CRITICAL')

            __LoggerNameList = {'log_yield_test':[LOGGER_yield,  logging.DEBUG],
                                'myLogger':[myLogger,  logging.DEBUG] ,
                                #'DEBUG': [LOGGER_DEBUG,logging.DEBUG],
                                #'INFO': [LOGGER_INFO,  logging.INFO],                        
                                #'WARNING':[LOGGER_WARNING,logging.WARNING],
                                #'ERROR':[LOGGER_ERROR,logging.ERROR],
                                #'CRITICAL':[LOGGER_CRITICAL,logging.CRITICAL]
                                }        
            __logging_formatter = logging.Formatter('%(message)s')

            __log_console_handle = logging.StreamHandler()
            __log_console_handle.setLevel(logging.WARNING)
            __log_console_handle.setFormatter(__logging_formatter)
                       
            for Lname in __LoggerNameList:    
                logger = __LoggerNameList[Lname][0]
                loggerLevel = __LoggerNameList[Lname][1]
            
                loggerFile = Lname + '.log'       
                fh = logging.FileHandler(GlobalVar.PATH.FORDER.LOG + loggerFile , mode = 'w' )
                fh.setLevel(loggerLevel)    
                fh.setFormatter(__logging_formatter)

                logger.addHandler(fh)   #loggerName.removeHandler(fh)        
                if loggerLevel > logging.DEBUG : 
                    logger.addHandler(__log_console_handle) #ERRORJI以上的錯誤，除了寫入檔案，也會也到CONSOLE去！         


    IS_PY2 =  sys.version[0] == '2'
    if IS_PY2:
        input = raw_input
    else: #PYTHON 3
        input = input

    def Title(strTitleName):
        #logging.debug(strTitleName)
        LOGGER_yield.debug('\n' + strTitleName)
        return True

def main(STATISTICS_INTERVAL):
    #get hight data
    Gheightfile = CGeographyHeightByFile("HeightSetting.csv")
    HightData = Gheightfile.getRow()
    if not 'test':
        for i in range(  Gheightfile.CountRow() ):  #range(0,100,3) 0 3 6...
            print( HightData[i]['min'] )
            i += 1


    CMyFile.fnClearFolder(GlobalVar.PATH.FORDER.CSV)

    
    #STATISTICS_INTERVAL = 100

    if False:
        try:
            STATISTICS_INTERVAL = int(input("input STATISTICS_INTERVAL:") )
        except Exception as e:
            myLogger.error('請輸入整數')
            sys.exit()

    #del lst[:]
    #example:
    #
    #lst1 = [1, 2, 3]
    #lst2 = lst1
    #del lst1[:]
    #print(lst2)

    for dirs , subdir , files in os.walk( GlobalVar.PATH.FORDER.TXT ) :
        Groups={}
        TOTAL_DAY = 0
        TOTAL_GROUP = 0
        curFileName =''
        for file in files :
            curFileName = file
            f = open( dirs+'/'+file, 'r', encoding='big5')
            reader = csv.reader(f) #讀取csv中的各列資料(含表頭)
            headers = next(reader) #讀取當前位置的資料給headers，隨後把當前位置指向下一筆資料(表頭資料就消失了)
            #tmpheaders = headers #使用list後headers會跑掉
            #計算有幾天
            #countDay = list(reader)
            #TOTAL_DAY = len(countDay[0]) - 6 #6為不是天數的欄位            
            TOTAL_DAY = len(headers) - 6 #6為不是天數的欄位            
            TOTAL_GROUP = TOTAL_DAY / STATISTICS_INTERVAL + 1 if TOTAL_DAY % STATISTICS_INTERVAL  else TOTAL_DAY / STATISTICS_INTERVAL  #    a = 9 if False else 10 => a=10
            TOTAL_GROUP = int(TOTAL_GROUP)

            for i in range(TOTAL_GROUP):
                Groups[i] = [] #陣列宣告

            for row in reader: #單筆資料陣列 [ ... ]
                cur_DEM_value = 0
                curColumn = 0
                curIndex = 0
                curGroup = 0
                for h,v in  zip( headers , row ) :  # [ X1 , X2 ... Xn ]
                    curColumn+=1
                    if h == 'DEM':
                        cur_DEM_value = v
                        continue                      
                    if curColumn <= 4 : #前四個column忽略，不做處理
                        continue
                    if h in ('POINT_X' , 'POINT_Y'):
                        break                 
  
                    curIndex +=1
                    if curIndex > (STATISTICS_INTERVAL) :
                        curIndex = 1
                        curGroup +=1
                    #if (curColumn-4) % (STATISTICS_INTERVAL+1) == 0 :
                    #   curGroup += 1                    
                    Groups[curGroup].append( float(v) - float(cur_DEM_value) )
                    #Groups[int(curColumn/STATISTICS_INTERVAL)].append( float(v) - float(cur_DEM_value) )
                                
            RowData={}    
            for HeightIndex in range(Gheightfile.CountRow()) :
                RowData[HeightIndex] = {}
                for groupIndex in range(TOTAL_GROUP):
                    RowData[HeightIndex][groupIndex]= 0 #list() #[]
            #RowData={}    
            #for i in range(TOTAL_GROUP):
            #    RowData[i] = [] #陣列宣告

            curCount = 0
            for indexH in range(  Gheightfile.CountRow() ):        
                curMinHeight  = int(HightData[indexH]['min'])
                curMaxHeight = int(HightData[indexH]['max'])
                #for GroupIndex, g in enumerate(Groups):
                for GroupIndex  in Groups:
                    for currentValue in Groups[GroupIndex]:
                        if 'special Height case:' and curMaxHeight == 99999:
                            if 'case1:大於最大高度' and curMinHeight > 0 and currentValue > curMinHeight:                                
                                curCount+=1
                            if 'case2:負高度' and curMinHeight == -1 and currentValue < curMinHeight:                                
                                curCount+=1
                            if '負高度' and curMinHeight ==-9999 and currentValue == curMinHeight:
                                curCount+=1                            

                        elif currentValue > curMinHeight and currentValue < curMaxHeight :
                            curCount += 1
                    #RowData[GroupIndex].append(curCount)
                    #RowData[indexH][GroupIndex].append(curCount)
                    RowData[indexH][GroupIndex] = curCount
                    curCount = 0

            if '寫檔' : #再換下一筆高度之前先寫檔
                if pathlib.Path(GlobalVar.PATH.FILE.RESULT_CSV).is_file():
                    output = csv.writer(open(GlobalVar.PATH.FILE.RESULT_CSV + curFileName ,'a'), lineterminator='\n' )  #\r\n
                else:
                    output = csv.writer(open(GlobalVar.PATH.FILE.RESULT_CSV + curFileName ,'w'), lineterminator='\n' )  #\r\n
                    listTitle = list()               
                    listTitle.extend( ( 'min-Height' , 'max-Height'  ) )  #高度  #using "extend" to append multiple items in one line 
                    for i in range(TOTAL_GROUP):
                        if i == TOTAL_GROUP-1:
                            listTitle.append(TOTAL_DAY)
                        else: 
                            listTitle.append((i+1)*STATISTICS_INTERVAL)
                    output.writerow( listTitle )
                    #output.writerows( [ ['column1','column2' ....] ] )
                    """
                    writerows => [ [a1,a2, ... an] , [b1,b2...bn] , [x1,x2,...,xn] ]
                    a1 , a2 , ... an
                    b1 , b2 , ... bn
                    x1 , x2 , ... xn

                    writerow => [a1,a2,...an]
                    a1 , a2 , ... an
                    """            


                resultRow = list()
                for HeightIndex in range(Gheightfile.CountRow()) :
                    resultRow.extend( ( int(HightData[HeightIndex]['min']) , int(HightData[HeightIndex]['max'])  ) )  #高度            
                    for groupIndex in Groups:
                        resultRow.append(RowData[HeightIndex][groupIndex])
                    output.writerow( resultRow )
                    del resultRow[:] #清空

    ctypes.windll.user32.MessageBoxW(0, "程式執行結束", "Title:Info", 0)        
    sys.exit()
           
    



def test2():

    #get hight data
    Gheightfile = CGeographyHeightByFile("HeightSetting.csv")
    HightData = Gheightfile.getRow()
    if not 'test':
        for i in range(  Gheightfile.CountRow() ):  #range(0,100,3) 0 3 6...
            print( HightData[i]['min'] )
            i += 1


    CMyFile.fnClearFolder(GlobalVar.PATH.FORDER.CSV)

    #curMinHeight = 0
    #curMaxHeight = 500
    curCount = 0
    cur_Interval = 0
    cur_DEM_value = 0
    STATISTICS_INTERVAL = 100
    #statistics_interval = 100       
    listResultRowData = []
    for dirs , subdir , files in os.walk( GlobalVar.PATH.FORDER.TXT ) :
        for file in files :      
            f = open( dirs+'/'+file, 'r', encoding='big5')
            reader = csv.reader(f) #讀取csv中的各列資料(含表頭)
            headers = next(reader) #讀取當前位置的資料給headers，隨後把當前位置指向下一筆資料(表頭資料就消失了)
            #計算有幾天
            countDay = list(reader)
            TOTAL_DAY = len(countDay[0]) - 6 #6為不是天數的欄位

            TOTAL_GROUP = TOTAL_DAY / STATISTICS_INTERVAL

            

            column = {} #此物件用來表示各欄
            for h in headers:
                column[h] = [] #產生陣列
            #for i , row in enumerate(reader):
            for row in reader:
                curColumn = 0 
                for h,v in  zip( headers , row ) :
                    curColumn += 1
                    if h == 'DEM':
                        cur_DEM_value = v
                    if curColumn <= 4 : #前四個column忽略，不做處理
                        cur_Interval = 0
                        continue

                    if h in ('POINT_X' , 'POINT_Y'):
                        if '寫檔':
                            if pathlib.Path(PATH.FILE.RESULT_CSV).is_file():
                                output = csv.writer(open(PATH.FILE.RESULT_CSV,'a'), lineterminator='\n' )  #\r\n
                            else:
                                output = csv.writer(open(PATH.FILE.RESULT_CSV,'w'), lineterminator='\n' )  #\r\n
                                #output.writerows( [ ['column1','column2' ....] ] )
                            output.writerows( [ listResultRowData ]  )  #output.writerows( [ [ '20170410' , iSum] ]  )
                            output.close()
                        break

                    if cur_Interval > CONST_STATISTICS_INTERVAL :
                        listResultRowData.append(curCount) #把當前的計數紀錄下來
                        curCount = 0 #計數歸零
                        cur_Interval = 0                    
                        
                    currentValue = float(v) - float(cur_DEM_value)
                    for HeightFileIndex in range(  Gheightfile.CountRow() ):  #range(0,100,3) 0 3 6...
                        curMinHeight = HightData[HeightFileIndex]['min'] 
                        curMaxHeight = HightData[i]['max']                         
                        if currentValue > curMinHeight and currentValue < curMaxHeight :
                            #column[h].append(currentValue)
                            curCount += 1
                        HeightFileIndex += 1
                    cur_Interval +=1
            #print( column )            
            f.close()            
            print( curCount )
            #cur_Interval = 0
            #for c in column:    
            #    for r in column[c]:
            #        test = column[c][int(r)]                

            #if pathlib.Path(GlobalVar.PATH.FORDER.CSV + '//Result.csv').is_file():
            #    output = csv.writer(open('Result.csv','a'), lineterminator='\n' )  #\r\n
            #else:
            #    output = csv.writer(open('Result.csv','w'), lineterminator='\n' )  #\r\n
            #    for
            #    output.writerows( [ ['日期','成交金額'] ] )
            #
            #output.writerows( [ [ '20170410' , iSum] ]  ) # float object is not iterable:  http://stackoverflow.com/questions/8120019/typeerror-float-object-not-iterable
            #print (iSum)


            #proc_show_result = subprocess.Popen('notepad.exe testData.csv' )
            #proc_show_result.wait()
            break                            
        #sys.exit()                              

    
#http://stackoverflow.com/questions/5004687/python-csv-dictreader-with-utf-8-data
def UnicodeDictReader(utf8_data, **kwargs):
    csv_reader = csv.DictReader(utf8_data, **kwargs)
    for row in csv_reader:
        yield {unicode(key, 'utf-8'): unicode(value, 'utf-8') for key, value in row.iteritems()}        


def Test1():
    
    MyCase = int(input("input CASE:") )    
    f = open('testData.csv', 'r', encoding='big5')
    while True:
        if  MyCase == 1 and 'print all data':  
            for row in csv.reader(f):
                print(row)
        elif MyCase ==2 and 'print specific column':
            for row in csv.DictReader(f):
                print (row['date'])
        elif MyCase ==3 and 'select specific column and print specific column':
            #myDate = UnicodeDictReader(["日期", "成交股數", "成交金額", "成交筆數", "指數", "漲跌點數"] ) 
            #print( next(myDate ))
            for row in csv.DictReader(f, ['column_name1' , 'column_name2' , '成交金額' ,'column_nameN']  ) :  #這裡的欄位會自動與csv的欄位做對應。
                print ( row['成交金額'] )
        elif MyCase ==4 and 'caculate sum of 成交金額:':
            #bRowOfTitle = True
            iSum = 0            
            for row in csv.DictReader(f, ['column_name1' , 'column_name2' , '成交金額' ,'column_nameN']  ) :
                #if bRowOfTitle:
                #    bRowOfTitle = False
                #    continue                 
                
                #if type(aaa) == float or type(aaa) == int :
                #   iSum += aaa

                #if iSum == 0 :
                #    iSum = 1
                #    continue                
                try:
                    iSum += float(row['成交金額'])
                except ValueError:  # Exception as e: #它會掃到標頭，所以要把標頭過慮掉！  <--可以用next()慮掉標頭！
                    pass #print( e )

            #aaa = iSum/100000            
            #headers=['日期','成交金額']
            #my_dict = {"test": 1, "testing": 2}
            #output = csv.DictWriter(open('Result.csv','wb'), delimiter=',', lineterminator='\n', fieldnames=headers)  #\r\n
            #output = csv.DictWriter(open('Result.csv','w'), delimiter=',' , fieldnames=headers)  #\r\n
            if pathlib.Path('Result.csv').is_file():
                output = csv.writer(open('Result.csv','a'), lineterminator='\n' )  #\r\n
            else:
                output = csv.writer(open('Result.csv','w'), lineterminator='\n' )  #\r\n
                output.writerows( [ ['日期','成交金額'] ] )
            
            output.writerows( [ [ '20170410' , iSum] ]  ) # float object is not iterable:  http://stackoverflow.com/questions/8120019/typeerror-float-object-not-iterable
            print (iSum)

        elif MyCase ==5 and 'read csv title by program... ':
            #http://stackoverflow.com/questions/3428532/how-to-import-a-csv-file-using-python-with-headers-intact-where-first-column-is
            reader = csv.reader(f) #讀取csv中的各列資料(含表頭)
            headers = next(reader) #讀取當前位置的資料給headers，隨後把當前位置指向下一筆資料(表頭資料就消失了)
            column = {} #此物件用來表示各欄
            for h in headers:
                column[h] = [] #產生陣列
            for row in reader:
                for h,v in zip( headers , row ):
                    column[h].append(v)
    
            print(column)
                        
        else : #save data
            if not f.closed :
                f.close()
            #使用newline自動換到下一行去 http://stackoverflow.com/questions/3348460/csv-file-written-with-python-has-blank-lines-between-each-row
            #f = open('testData.csv', 'a' , newline='' ) #a = append ; w = write
            f = open('testData.csv', 'a' ) #a = append ; w = write
            listSaveData = [
      [' 101/01/31', '5,486,734,180', '162,361,181,834', '1,283,951', '7,517.08', '109.67'],
      [' 101/01/13', '3,497,838,901', '99,286,437,370', '819,762', '7,181.54', '-5.04'],
      [' 106/04/10', '3,497,838,901', '99,286,437,370', '819,762', '7,181.54', '-5.04']
    ]       
            
            w = csv.writer(f, lineterminator='\n') #如果lineterminator不特別寫，預設值為\r\n，這樣每次寫入都會多出空的一行出來。(用csv看)
            #w.writerows([]) #新增空的資料列 (新增空的一筆資料)
            w.writerows(listSaveData)                
            if not 'test':
                #解決會自動多出空行的問題： http://stackoverflow.com/questions/8746908/why-does-csv-file-contain-a-blank-line-in-between-each-data-line-when-outputting
                w = csv.DictWriter(open('file3.csv','w'), delimiter=',', lineterminator='\n', fieldnames=headers)
                headers=['日期','成交股數','成交金額','成交筆數','發行量加權股價指數','漲跌點數']
                output = csv.DictWriter(open('testData.csv','wb'), delimiter=',', lineterminator='\n', fieldnames=headers)  #\r\n
                #output.writerow(dict((fn,fn) for fn in headers))
                #output.writerows(rows)
                #output.writerows(listSaveData)
        break                          
    f.close()
    proc_show_result = subprocess.Popen('notepad.exe testData.csv' )
    proc_show_result.wait()
    sys.exit()


        
def yield_test():  #what is yield in python ?  http://blog.blackwhite.tw/2013/05/python-yield-generator.html
    a = 3
    b = 2
    yield a
    c = 4
    recive_parameter = yield b       
    ccc = 200
    yield recive_parameter


if __name__ == "__main__" :     

    if not Title("yield_test"):        
        if IS_PY2: #yield next in python 3 : http://stackoverflow.com/questions/12274606/theres-no-next-function-in-a-yield-generator-in-python-3
            generator = yield_test()      
            LOGGER_yield.debug(generator.next())
            LOGGER_yield.debug(generator.next())
        else: #PYTHON 3           
            generator = yield_test()      
            LOGGER_yield.debug (next(generator))  #執行a=3 ; b=2 ;  yield a
            LOGGER_yield.debug (next(generator))  #c=4 ; yield b ;
            LOGGER_yield.debug (generator.send(8))  # recive_parameter = 8 ; yield recive_parameter           
            #LOGGER_yield.debug (next(generator))  #error 已執行完，沒有next了，所以會錯
            LOGGER_yield.debug ('let generator renew') 
            generator = yield_test()      
            LOGGER_yield.debug (next(generator))  #c=4 ; yield b ;
        
        #↓ ref ↓ http://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do-in-python
        if Title('Iterables:')  :
            mylist = [1, 2, 3]
            for i in mylist:
                LOGGER_yield.debug(i)

            mylist = [x*x for x in range(3)]
            for i in mylist:
                LOGGER_yield.debug(i) #print( str(i) + '\n')
            LOGGER_yield.debug('\n') 
       

        if Title('generator'):
            mygenerator = (x*x for x in range(3))
            for i in mygenerator:
                LOGGER_yield.debug(i)
            for i in mygenerator:
                LOGGER_yield.debug(i)
        
        proc_show_yield_test_result = subprocess.Popen("notepad.exe " + PATH.FORDER.LOG + '\\log_yield_test.log' )
        proc_show_yield_test_result.wait()
    
    #Test1()
    #test2()

    from tkinter import *
    master = Tk()
    editBox = Entry(master)
    editBox.focus_set()
    editBox.pack() #對齊

    def callback():
        #print(e.get()) # This is the text you may want to use later
        main( int(editBox.get() ) )

    btnOK = Button(master, text = "OK", width = 10, command = callback)
    btnOK.pack()

    mainloop()    
    