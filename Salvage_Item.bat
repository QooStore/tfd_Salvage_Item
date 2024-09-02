@echo off
:: 관리자 권한 체크
net session >nul 2>&1
if %errorLevel% == 0 (
    echo 관리자 권한으로 실행 중...
) else (
    echo 관리자 권한을 요청 중...
    powershell -Command "Start-Process '%0' -Verb RunAs"
    exit /b
)

:: 관리자 권한을 얻은 후 실행할 명령어
start pythonw.exe "%~dp0Salvage_Item.pyw"
exit