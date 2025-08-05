@echo off
cd /d "C:\Users\Administrator\Desktop\guanwang250612"
start /min python -m http.server 8000
timeout /t 2 >nul
start http://localhost:8000
exit
