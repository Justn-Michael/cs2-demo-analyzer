@echo off
cd /d "%~dp0"
set PGPASSWORD=7204
py -3.12 src\app.py
