# =============================================================================
# ARCHIVO:      ejecutar_pruebas.py
# AUTOR:        Carlos Mita
# FECHA:        10/10/2026
# DESCRIPCIÓN:  Ejecuta el archivo pruebas.py de cada práctica y de cada
#               ejercicio en un proceso aparte y muestra un resumen final.
# =============================================================================
import os
import sys
import subprocess

RAIZ = os.path.dirname(os.path.abspath(__file__))
CARPETAS = sorted((c for c in os.listdir(RAIZ) if c.startswith(("practica_", "ejercicio_"))),
                  key=lambda carpeta: (carpeta.startswith("ejercicio_"), carpeta))
# Los procesos hijos escriben en UTF-8 para conservar las tildes en Windows
ENTORNO = {**os.environ, "PYTHONIOENCODING": "utf-8"}

total_casos, fallidas = 0, []
for carpeta in CARPETAS:
    # Cada script de pruebas se ejecuta dentro de su propia carpeta
    resultado = subprocess.run([sys.executable, "pruebas.py"], cwd=os.path.join(RAIZ, carpeta),
                               env=ENTORNO, capture_output=True, text=True,
                               encoding="utf-8", errors="replace")
    casos = sum(1 for linea in resultado.stdout.splitlines() if linea.startswith("OK"))
    total_casos += casos
    superada = resultado.returncode == 0
    if not superada:
        fallidas.append(carpeta)
    print(f"{carpeta:32s} {casos:3d} casos  ->  {'SUPERADAS' if superada else 'FALLIDAS'}")

print("-" * 64)
print(f"Total: {total_casos} casos verificados en {len(CARPETAS)} carpetas | "
      f"carpetas con fallos: {len(fallidas)}")
