@echo off
=============================================================
REM TITLE
=============================================================
echo PROGRAM_NAME：%~n0%~x0


echo pause>nul

set SrcPath=%~dp0\Geography_TXT_DATA
set /p SrcPath=請拖曳或輸入來源TXT檔案資料夾入境
echo %SrcPath%

set DestPath=%~dp0\Geography_CSV_DATA
set /p DestPath=請托曳或輸入要移置CSV資料夾入境
echo %DestPath%

FOR %%I IN ( %SrcPath%\*.txt ) DO (
REM    ECHO %%I  路徑的完整名稱C:...\xxx.xxx
REM    ECHO %%~nI  檔案名稱不含附檔名
REM    ECHO %%~xI  只有副檔名
REM    ECHO %%~nxI 檔案名稱含附檔名

copy "%%I" "%DestPath%\%%~nI.csv"

)

pause

echo PROGRAM_NAME：%~n0%~x0  END