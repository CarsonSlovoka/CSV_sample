@echo off
=============================================================
REM TITLE
=============================================================
echo PROGRAM_NAME�G%~n0%~x0


echo pause>nul

set SrcPath=%~dp0\Geography_TXT_DATA
set /p SrcPath=�Щ즲�ο�J�ӷ�TXT�ɮ׸�Ƨ��J��
echo %SrcPath%

set DestPath=%~dp0\Geography_CSV_DATA
set /p DestPath=�Ц����ο�J�n���mCSV��Ƨ��J��
echo %DestPath%

FOR %%I IN ( %SrcPath%\*.txt ) DO (
REM    ECHO %%I  ���|������W��C:...\xxx.xxx
REM    ECHO %%~nI  �ɮצW�٤��t���ɦW
REM    ECHO %%~xI  �u�����ɦW
REM    ECHO %%~nxI �ɮצW�٧t���ɦW

copy "%%I" "%DestPath%\%%~nI.csv"

)

pause

echo PROGRAM_NAME�G%~n0%~x0  END