@echo off
setlocal
title E-ESTADO - GERAR EXECUTAVEL
cd /d "%~dp0"

echo ============================================================
echo  E-ESTADO - COMPILAR ROBO DE CONFERENCIA
echo ============================================================
echo Este processo recompila inventario.py para um executavel.
echo O arquivo final sera Robo-E-Estado-Conferir.exe.
echo.
python -m PyInstaller --noconfirm --clean --onefile --console --name Robo-E-Estado-Conferir --collect-all playwright --collect-all greenlet --collect-all pyautogui --collect-all keyboard inventario.py
if errorlevel 1 (
  echo.
  echo ERRO: nao foi possivel gerar o executavel.
  pause
  exit /b 1
)
copy /Y "dist\Robo-E-Estado-Conferir.exe" "Robo-E-Estado-Conferir.exe"
if errorlevel 1 (
  echo ERRO ao copiar o executavel para esta pasta.
  pause
  exit /b 1
)
echo.
echo Executavel gerado com sucesso.
echo Local: %~dp0Robo-E-Estado-Conferir.exe
pause
