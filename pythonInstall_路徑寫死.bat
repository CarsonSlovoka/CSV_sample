@echo off
=============================================================
REM TITLE
=============================================================
echo PROGRAM_NAME�G%~n0%~x0




set FolderPath="C:\Users\Carson\myDoc\MY_PRACTICE\python\DemoFont\Demo\prjCSV"

cd %FolderPath%


rem pyinstaller.exe  --onefile --{windowed ; console} --icon=xxx.ico  xxxx.py          // -windowed �s�@�����{���C�]�{������ɤ��|����r�����X�{
pyinstaller.exe  --onefile --windowed --icon=myIcon.ico  prjCSV.py

FOR %%I IN ( dist\*.* ) DO (
REM    ECHO %%I  ���|������W��C:...\xxx.xxx
REM    ECHO %%~nI  �ɮצW�٤��t���ɦW
REM    ECHO %%~xI  �u�����ɦW
REM    ECHO %%~nxI �ɮצW�٧t���ɦW

copy "%%I" ".\%%~nxI"

)

echo PROGRAM_NAME�G%~n0%~x0  END
pause
