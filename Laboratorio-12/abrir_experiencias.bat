@echo off
REM Abre Windows Terminal con una pestana por experiencia:
REM   panel izquierdo = servidor (npm run dev, puerto 300N)   panel derecho = pruebas
REM Requisitos: MySQL local encendido (Exp. 3) y servicio Aiven encendido (Exp. 4 a 6)
set R=%~dp0
set T=powershell -NoExit -ExecutionPolicy Bypass -File "%R%_ejecucion\pestana.ps1"
set S=powershell -NoExit -Command "npm run dev"
wt -w new ^
 new-tab --title "Experiencia 1 (3001)" -d "%R%experiencia1\api_biblioteca" %S% ; split-pane -V -d "%R%experiencia1\api_biblioteca" %T% 1 ; ^
 new-tab --title "Experiencia 2 (3002)" -d "%R%experiencia2\api_biblioteca" %S% ; split-pane -V -d "%R%experiencia2\api_biblioteca" %T% 2 ; ^
 new-tab --title "Experiencia 3 (3003)" -d "%R%experiencia3\api_biblioteca" %S% ; split-pane -V -d "%R%experiencia3\api_biblioteca" %T% 3 ; ^
 new-tab --title "Experiencia 4 (3004)" -d "%R%experiencia4\api_biblioteca" %S% ; split-pane -V -d "%R%experiencia4\api_biblioteca" %T% 4 ; ^
 new-tab --title "Experiencia 5 (3005)" -d "%R%experiencia5\api_biblioteca" %S% ; split-pane -V -d "%R%experiencia5\api_biblioteca" %T% 5 ; ^
 new-tab --title "Experiencia 6 (3006)" -d "%R%experiencia6\api_biblioteca" %S% ; split-pane -V -d "%R%experiencia6\api_biblioteca" %T% 6 ; ^
 focus-tab -t 0
