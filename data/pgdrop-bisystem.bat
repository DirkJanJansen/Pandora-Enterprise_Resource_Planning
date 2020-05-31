@echo off
set PGPASSWORD=postgres45
echo.
echo.
echo Pay Attention !!! The database bisystem is going to be removed.
echo.
echo.
echo Press any key to remove the database bisystem
echo.
echo.
echo Or press  Ctrl+C to cancel
pause > nul

"C:\programData\postgres\bin\dropdb.exe"  -h localhost -p 5432 -U postgres  -w bisystem 
echo.
echo The database bisystem is removed
echo Press any key to close
pause > nul
