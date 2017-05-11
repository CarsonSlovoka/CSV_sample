@echo off
=============================================================
REM TITLE
=============================================================
echo PROGRAM_NAME：%~n0%~x0




set FolderPath="C:\Users\Carson\myDoc\MY_PRACTICE\python\DemoFont\Demo\prjCSV"

cd %FolderPath%


rem pyinstaller.exe  --onefile --{windowed ; console} --icon=xxx.ico  xxxx.py          // -windowed 製作視窗程式。（程式執行時不會有文字視窗出現
pyinstaller.exe  --onefile --windowed --icon=myIcon.ico  prjCSV.py

FOR %%I IN ( dist\*.* ) DO (
REM    ECHO %%I  路徑的完整名稱C:...\xxx.xxx
REM    ECHO %%~nI  檔案名稱不含附檔名
REM    ECHO %%~xI  只有副檔名
REM    ECHO %%~nxI 檔案名稱含附檔名

copy "%%I" ".\%%~nxI"

)

echo PROGRAM_NAME：%~n0%~x0  END
pause
