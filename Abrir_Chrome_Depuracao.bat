@echo off
title E-ESTADO - Abrir Chrome para automacao
echo Abrindo Google Chrome com depuracao remota na porta 9222...
if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" (
  start "" "%ProgramFiles%\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="%USERPROFILE%\ChromeDebugProfile" "https://e-estado.ro.gov.br/"
  exit /b 0
)
if exist "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" (
  start "" "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="%USERPROFILE%\ChromeDebugProfile" "https://e-estado.ro.gov.br/"
  exit /b 0
)
echo ERRO: Google Chrome nao foi encontrado nos caminhos padrao.
pause
exit /b 1
