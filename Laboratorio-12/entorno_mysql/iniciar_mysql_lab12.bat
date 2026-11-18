@echo off
REM Inicia las dos instancias MySQL usadas en el laboratorio (datos en D:\NUEVACARPTEAPS\_mysql_lab12_v2)
REM  - local : 127.0.0.1:3307  (Experiencia 3)       root / RootLocal#2026
REM  - nube  : localhost:3308  (Experiencias 4 a 6)  avnadmin / AdminNube#2026 (solo TLS)
set MYSQLD="C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqld.exe"
start "MySQL local 3307" /min %MYSQLD% --defaults-file="D:\NUEVACARPTEAPS\_mysql_lab12_v2\local.ini"
start "MySQL nube 3308"  /min %MYSQLD% --defaults-file="D:\NUEVACARPTEAPS\_mysql_lab12_v2\nube.ini"
echo Servidores iniciados: local 3307 y nube 3308 (TLS obligatorio)
