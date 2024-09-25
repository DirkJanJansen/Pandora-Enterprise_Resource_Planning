@echo off

set PGPASSWORD=postgres45

echo.
echo.
echo.
echo The present  empty backup is going to be overwritten
echo To preserve the present empty backup, save it in another folder or rename it!!
echo Press any key to backup empty database bisystem.
pause > nul
echo.

"C:\programdata\postgres\bin\pg_dump.exe" -U postgres -v --verbose -d  bisystem -Fc -f  "C:\ProgramData\Pandora\data\bisystem.empty.backup"
echo.
echo.
echo Backup of the empty database bisystem is saved.
echo.
echo Press any key to close.
pause > nul
#-Fp Plain
#-Fc Custom
#-Fd directory
#-Ft tar
