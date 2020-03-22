@echo off
echo Restore database bisystem via bisystem.backup

set PGPASSWORD=postgres45
echo.
echo.
echo.
echo Verwijder eerst het bestaande bisystem met pgdrop-bisystem.bat
echo Ctrl+C om te annuleren!
echo.
echo.
echo U gaat nu de database bisystem.backup terugplaatsen
echo Druk een toets voor terugplaatsen database bisystem ........
pause > nul
echo.
echo.
echo Restore database bisystem via bisystem.backup
echo.
echo.
echo.

"C:\programdata\postgres\bin\createdb.exe"  -h localhost -p 5432 -U postgres -w bisystem

"C:\programdata\postgres\bin\pg_restore.exe" --dbname=bisystem  --verbose C:\programdata\postgres\backup\bisystem.backup
pause
