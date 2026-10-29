@echo off
setlocal EnableExtensions
title E-ESTADO - CONFERENCIA DE BENS
mode con: cols=90 lines=36
cd /d "%~dp0"
for /F %%a in ('echo prompt $E^| cmd') do set "ESC=%%a"
cls
echo.
echo %ESC%[96m      EEEEE   EEEEE   SSSSS  TTTTT   AAA   DDDD    OOOOO
echo %ESC%[96m      EE      EE      SS       T    A   A  DD  DD  OO   OO
echo %ESC%[94m      EEEE    EEEE    SSSSS    T    AAAAA  DD  DD  OO   OO
echo %ESC%[94m      EE      EE         SS   T    A   A  DD  DD  OO   OO
echo %ESC%[96m      EEEEE   EEEEE   SSSSS    T    A   A  DDDD    OOOOO
echo.
echo %ESC%[97m                    AUTOMACAO DE CONFERENCIA DE BENS
echo %ESC%[95m                Feito com ^<3 por Izabel Galvao :3
echo %ESC%[95m                Atualizacoes no meu GITHUB: https://github.com/i3b3l
echo.
echo %ESC%[94m   ^>_ INICIAR_ROBO_E-ESTADO
echo.
echo %ESC%[96m   +---------------------------------------------------------------+
echo %ESC%[96m   ^| %ESC%[97mPREPARANDO A EXECUCAO%ESC%[96m                                      ^|
echo %ESC%[96m   +---------------------------------------------------------------+
echo %ESC%[97m   O robo reclassifica e confere os bens pendentes.
echo %ESC%[94m   [OK]%ESC%[97m Preenche os campos definidos e salva a reclassificacao.
echo %ESC%[94m   [OK]%ESC%[97m Clica em Conferir quando permitido; ignora bens bloqueados.
echo.
echo %ESC%[95m   CAMPOS: %ESC%[97mServivel ^| Localizado ^| Uso e usufruto do bem ^| Bom
echo.
echo %ESC%[93m   ! IMPORTANTE
echo %ESC%[97m   - O Chrome sera aberto no E-ESTADO.
echo %ESC%[97m   - Faca login e deixe a lista de bens aberta.
echo %ESC%[97m   - Pressione %ESC%[93mESC%ESC%[97m para solicitar a interrupcao do robo.
echo %ESC%[96m   +---------------------------------------------------------------+
echo.
echo %ESC%[92m   [TECLADO] Pressione qualquer tecla para continuar...
echo %ESC%[0m
pause >nul
echo.
echo %ESC%[96m   [ABRINDO] Chrome de depuracao do E-ESTADO...%ESC%[0m
call "%~dp0Abrir_Chrome_Depuracao.bat"
echo.
echo %ESC%[97m   Faca login e abra a lista de bens.
echo   Pressione qualquer tecla para iniciar o robo...%ESC%[0m
pause >nul
echo.
if not exist "%~dp0Robo-E-Estado-Conferir.exe" goto Falha
echo %ESC%[92m   [INICIANDO] Robo-E-Estado-Conferir.exe%ESC%[0m
echo.
"%~dp0Robo-E-Estado-Conferir.exe"
set "CODIGO_SAIDA=%ERRORLEVEL%"
echo.
if "%CODIGO_SAIDA%"=="0" (echo %ESC%[92m   [ENCERRADO] Robo finalizado.%ESC%[0m) else (echo %ESC%[93m   [ATENCAO] Codigo de saida: %CODIGO_SAIDA%%ESC%[0m)
echo.
echo   Pressione qualquer tecla para sair.
pause >nul
exit /b %CODIGO_SAIDA%
:Falha
echo %ESC%[91m   [ERRO] Robo-E-Estado-Conferir.exe nao encontrado.%ESC%[0m
echo   Pressione qualquer tecla para sair.
pause >nul
exit /b 1
