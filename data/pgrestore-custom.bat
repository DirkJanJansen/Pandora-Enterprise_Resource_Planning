@echo off
echo Restore database bisystem by bisystem.backup

set PGPASSWORD=postgres45
echo.
echo.
echo.
echo First remove database bisystem with pgdrop-bisystem.bat
echo Ctrl+C to cancel
echo.
echo.
echo You are going to restore the database bisystem now!
echo Press any key to restore database bisystem ........
pause > nul
echo.
echo.
echo Restore database bisystem by bisystem.backup
echo.
echo.
echo.

"C:\programdata\postgres\bin\createdb.exe"  -h localhost -p 5432 -U postgres -w bisystem

"C:\programdata\postgres\bin\pg_restore.exe" --dbname=bisystem  --verbose C:\programdata\postgres\backup\bisystem.backup

echo.
echo Database bisystem is restored
echo press any key to end program
pause > nul
