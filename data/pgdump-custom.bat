@echo off

set PGPASSWORD=postgres45

echo.
echo.
echo.
echo The present backup is going to be overwritten
echo To preserve the present backup, save it in another folder or rename it!!
echo Press any key to backup database bisystem.
pause > nul
echo.

"C:\programdata\postgres\bin\pg_dump.exe" -U postgres -v --verbose -d  bisystem -Fc -f  "D:\Programming\Pandora\data\bisystem.backup"
echo.
echo.
echo Backup of the database bisystem is saved.
echo.
echo Press any key to close.
pause > nul
#-Fp Plain
#-Fc Custom
#-Fd directory
#-Ft tar
