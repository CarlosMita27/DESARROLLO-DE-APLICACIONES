# Panel de pruebas de la experiencia N: espera a que la API responda y ejecuta sus pruebas
param([int]$N)
$titulos = @{
  1 = 'Proyecto Node.js, Express y Nodemon'
  2 = 'Servicio RESTful CRUD con Express Router'
  3 = 'Persistencia con MySQL y procedimientos almacenados'
  4 = 'Base de datos MySQL en la nube (Aiven, TLS)'
  5 = 'Registro e inicio de sesion con JWT'
  6 = 'Proteccion de rutas con middleware JWT y roles'
}
$P = 3000 + $N
$pruebas = @{
  1 = @("curl.exe -s -w `" -> %{http_code}\n`" http://localhost:$P/api/libros/2", "curl.exe -s -w `" -> %{http_code}\n`" http://localhost:$P/api/libros/99")
  2 = @('node pruebas/verificar_exp2.js')
  3 = @('node pruebas/verificar_exp2.js')
  4 = @('node pruebas/probar_conexion.js', 'node pruebas/verificar_exp2.js')
  5 = @('node pruebas/verificar_exp5.js')
  6 = @('node pruebas/verificar_exp6.js')
}
$Host.UI.RawUI.WindowTitle = "Experiencia $N - pruebas"
[Console]::OutputEncoding = [Text.Encoding]::UTF8
Write-Host ""
Write-Host "  EXPERIENCIA $N : $($titulos[$N])" -ForegroundColor Green
Write-Host "  API en http://localhost:$P" -ForegroundColor DarkGray

# Espera a que el servidor (npm run dev) esté escuchando
Write-Host "  Esperando a que la API responda..." -ForegroundColor DarkGray
for ($i = 0; $i -lt 60; $i++) {
  try { Invoke-WebRequest "http://localhost:$P/" -UseBasicParsing -TimeoutSec 2 | Out-Null; break } catch { Start-Sleep 1 }
}
Write-Host ""
foreach ($cmd in $pruebas[$N]) {
  Write-Host "PS $(Get-Location)> " -NoNewline
  Write-Host $cmd -ForegroundColor Yellow
  Invoke-Expression $cmd
  Write-Host ""
}
