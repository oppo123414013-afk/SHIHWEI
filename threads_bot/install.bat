@echo off
echo 安裝 Python 套件中...
"C:\Users\User\.local\bin\python3.14.exe" -m pip install --break-system-packages -r requirements.txt
echo.
echo 安裝完成！
echo 接下來請把 .env.template 複製為 .env 並填入 API Keys
pause
