@echo off
set PGPASSWORD=postgres45

"C:\programData\postgres\bin\dropdb.exe"  -h localhost -p 5432 -U postgres  -w bisystem 
