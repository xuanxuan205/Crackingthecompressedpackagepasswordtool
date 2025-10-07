@echo off
chcp 65001 >nul
echo ========================================
echo 密码破解工具 v1.0.4
echo ========================================
echo.

REM 检查Python环境
echo [环境检测] 正在检测Python环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到Python环境，请先安装Python 3.7+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 检查主程序文件
if not exist "main.py" (
    echo [错误] 未找到主程序文件 main.py
    echo 请确保在正确的目录下运行此脚本
    pause
    exit /b 1
)

REM 检查依赖目录
if not exist "cracker" (
    echo [错误] 未找到cracker模块目录
    pause
    exit /b 1
)

if not exist "utils" (
    echo [错误] 未找到utils模块目录
    pause
    exit /b 1
)

echo [环境检测] Python环境正常
echo [环境检测] 主程序文件存在
echo.

REM 创建必要的目录
if not exist "logs" mkdir logs
if not exist "crack_results" mkdir crack_results
if not exist "dictionaries" mkdir dictionaries

echo [启动] 正在启动密码破解工具...
echo.

REM 启动主程序
python main.py

echo.
echo [退出] 程序已退出
pause 