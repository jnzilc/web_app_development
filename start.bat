@echo off
echo ==============================================
echo 🔮 正在為您啟動「線上算命系統」...
echo ==============================================

:: 檢查 python 指令是否存在
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ⚠️ 警告：系統找不到 python！嘗試尋找 py 指令...
    py --version >nul 2>&1
    IF %ERRORLEVEL% NEQ 0 (
        echo ❌ 錯誤：完全找不到 Python！
        echo 請問您安裝 Python 的時候有勾選「Add python.exe to PATH」嗎？
        echo 建議您重新安裝一次 Python，並務必打勾該選項，然後重新開機試試看！
        pause
        exit /b
    ) ELSE (
        set PYTHON_CMD=py
    )
) ELSE (
    set PYTHON_CMD=python
)

echo ✅ 成功找到 Python 指令！

if not exist ".venv" (
    echo 📦 正在建立獨立的 Python 虛擬環境...
    %PYTHON_CMD% -m venv .venv
)

echo ⚙️ 正在安裝套件...
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

echo 🗄️ 正在初始化資料庫籤詩與卡牌...
.\.venv\Scripts\python.exe seed_db.py

echo 🌐 網站伺服器啟動中！(請在瀏覽器打開 http://127.0.0.1:5000)
echo ==============================================
set FLASK_APP=app
set FLASK_ENV=development
.\.venv\Scripts\flask.exe run

pause
