@echo off

set PGPASSWORD=postgres45

echo.
echo.
echo.
echo the present backup is going overwritten
echo To preserve the present backup, save it in another folder !!
echo Press any key to backup database bisystem.
pause > nul
echo.

"C:\programdata\postgres\bin\pg_dump.exe" -U postgres -v --verbose -d  bisystem -Fc -f  "C:\programdata\postgres\backup\bisystem.backup"
echo.
echo.
echo Backup of database bisystem is saved.
echo.
echo Press any key to close.
pause > nul
#-Fp Plain
#-Fc Custom
#-Fd directory
#-Ft tar
