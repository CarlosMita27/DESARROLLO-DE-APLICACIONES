@echo off
REM Abre una ventana de Windows Terminal que ejecuta las pruebas de las 6 experiencias
REM (las APIs ya deben estar corriendo en los puertos 3001 a 3006)
set R=%~dp0..\
set T=powershell -NoExit -ExecutionPolicy Bypass -File "%R%_ejecucion\pestana.ps1"
wt -w new ^
 new-tab --title "Pruebas Exp. 1" -d "%R%experiencia1\api_biblioteca" %T% 1 ; ^
 new-tab --title "Pruebas Exp. 2" -d "%R%experiencia2\api_biblioteca" %T% 2 ; ^
 new-tab --title "Pruebas Exp. 3" -d "%R%experiencia3\api_biblioteca" %T% 3 ; ^
 new-tab --title "Pruebas Exp. 4" -d "%R%experiencia4\api_biblioteca" %T% 4 ; ^
 new-tab --title "Pruebas Exp. 5" -d "%R%experiencia5\api_biblioteca" %T% 5 ; ^
 new-tab --title "Pruebas Exp. 6" -d "%R%experiencia6\api_biblioteca" %T% 6 ; ^
 focus-tab -t 0
