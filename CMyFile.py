#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging , os , sys
import ctypes
import shutil

def fnClearFolder(folderPath): #清空該資料夾內的所有東西
    try:
        if  os.path.exists( folderPath ):
            shutil.rmtree(folderPath)
            logging.info(u"資料夾：" + folderPath + u"已被刪除")
    
        if  not os.path.exists( folderPath ):
            os.makedirs(folderPath)
            logging.info(u"資料夾：" + folderPath + u"已建立")
    except Exception as e:
        logging.error("檔案開啟中，無法執行程式，請關閉使用中的csv檔案")
        ctypes.windll.user32.MessageBoxW(0, "檔案開啟中，無法執行程式，請關閉使用中的csv檔案", "Title:Error", 0)        
        sys.exit()
        




