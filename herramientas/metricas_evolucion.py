#!/usr/bin/env python3
"""Métricas de evolución de un repositorio Git, versión por versión.

Material de la Unidad 1 de GCMS (Gestión de Configuración y Mantenimiento de Software).
Produce dos archivos CSV que sirven de evidencia para los formatos F-02 y F-03:

  evolucion_por_version.csv  una fila por versión: tamaño, crecimiento y actividad entre versiones
  muestra_cambios.csv        una muestra aleatoria de commits para clasificar a mano por tipo de
                             mantenimiento, con una sugerencia heurística que hay que verificar

Solo usa la biblioteca estándar de Python 3.8 o posterior y el comando git.

Uso:
  python metricas_evolucion.py RUTA_DEL_REPOSITORIO
  python metricas_evolucion.py RUTA --ext .py --excluir tests,docs,examples --muestra 40 --semilla 7
  python metricas_evolucion.py RUTA --incluir "flask.py,flask/**/*.py,src/flask/**/*.py" --solo-fuente

El repositorio debe estar clonado con su historia completa (sin --depth).
"""

import argparse
import csv
import random
import re
import subprocess
import sys
from pathlib import Path

# Etiquetas que cuentan como versión con funcionalidad nueva: 1.2, v1.2, 1.2.0, v1.2.0.
# Las de corrección (1.2.3) y las preliminares (rc, beta) quedan fuera por defecto.
PATRON_VERSIONES = r"^v?\d+\.\d+(\.0)?$"

# Heurística por palabras clave del asunto del commit. El orden importa: gana la primera que coincide.
# Es una sugerencia para acelerar la lectura de la muestra, no una clasificación: el F-03 se llena a mano.
REGLAS = [
    ("documentación o publicación", r"\b(docs?|documentation|readme|changelog|changes|typos?|release|"
                                    r"bump version|version number|documenta\w*|publica)\b"),
    ("correctivo", r"\b(fix(es|ed|ing)?|bug|error|crash|regression|broken|wrong|incorrect|handle|"
                   r"corrige|arregla|falla)\b"),
    ("adaptativo", r"\b(python ?\d|drop(ped)? support|deprecat\w*|compat\w*|upgrade|bump|dependenc\w*|"
                   r"migrat\w*|ci|pre-commit|github actions|workflow|actualiza|compatib\w*)\b"),
    ("preventivo", r"\b(refactor\w*|clean(up|s|ed)?|simplif\w*|renam\w*|remov\w* (unused|unnecessary|old)|"
                   r"tests?|typ(e|ing)|annotat\w*|lint\w*|format\w*|reorgani[sz]\w*|standardi[sz]\w*|"
                   r"refactoriza|limpia|pruebas?)\b"),
    ("perfectivo", r"\b(add(s|ed)?|feature|implement\w*|new|allow\w*|improv\w*|performance|optimi[sz]\w*|"
                   r"support for|agrega|nuev[oa]|mejora|permite)\b"),
]


def git(repo, *args):
    resultado = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True,
                               encoding="utf-8", errors="replace")
    if resultado.returncode != 0:
        sys.exit(f"Falló: git {' '.join(args)}\n{resultado.stderr.strip()}")
    return resultado.stdout


def rutas(extensiones, excluir, incluir):
    if incluir:
        incluidas = [f":(glob){r.strip()}" for r in incluir if r.strip()]
    else:
        incluidas = [f":(glob)**/*{e if e.startswith('.') else '.' + e}" for e in extensiones]
    excluidas = [f":(exclude,glob)**/{d.strip('/')}/**" for d in excluir if d.strip()]
    return incluidas + excluidas


def versiones(repo, patron):
    etiquetas = [t for t in git(repo, "tag").split() if re.match(patron, t)]
    con_fecha = []
    for t in etiquetas:
        fecha = git(repo, "log", "-1", "--format=%cs", t).strip()
        con_fecha.append((fecha, t))
    return sorted(con_fecha)


def tamano(repo, ref, spec):
    """Archivos y líneas de código fuente en una versión, sin hacer checkout."""
    salida = git(repo, "grep", "-c", "", ref, "--", *spec)
    archivos, lineas = 0, 0
    for fila in salida.splitlines():
        try:
            lineas += int(fila.rsplit(":", 1)[1])
            archivos += 1
        except (IndexError, ValueError):
            pass
    return archivos, lineas


def entre(repo, anterior, actual, spec):
    """Actividad entre dos versiones: commits, autores distintos y cambios sobre el código fuente."""
    rango = f"{anterior}..{actual}" if anterior else actual
    commits = int(git(repo, "rev-list", "--count", "--no-merges", rango).strip() or 0)
    autores = len(set(git(repo, "log", "--no-merges", "--format=%aE", rango).split()))
    if not anterior:
        return commits, autores, "", "", "", ""
    modificados = len(git(repo, "diff", "--name-only", anterior, actual, "--", *spec).split())
    nuevos = len(git(repo, "diff", "--name-only", "--diff-filter=A", anterior, actual, "--", *spec).split())
    stat = git(repo, "diff", "--shortstat", anterior, actual, "--", *spec)
    agregadas = re.search(r"(\d+) insertion", stat)
    eliminadas = re.search(r"(\d+) deletion", stat)
    return (commits, autores, modificados, nuevos,
            int(agregadas.group(1)) if agregadas else 0, int(eliminadas.group(1)) if eliminadas else 0)


def sugerir(asunto):
    texto = asunto.lower()
    for tipo, patron in REGLAS:
        if re.search(patron, texto):
            return tipo
    return "sin sugerencia"


def muestra(repo, n, semilla, desde, spec):
    rango = [f"{desde}..HEAD"] if desde else []
    rutas_fuente = ["--", *spec] if spec else []
    filas = git(repo, "log", "--no-merges", "--format=%H\x1f%cs\x1f%s", *rango, *rutas_fuente).splitlines()
    commits = [f.split("\x1f") for f in filas if f.count("\x1f") == 2]
    elegidos = random.Random(semilla).sample(commits, min(n, len(commits)))
    elegidos.sort(key=lambda c: c[1])
    return [{"commit": h[:10], "fecha": f, "asunto": s, "sugerencia_heuristica": sugerir(s),
             "clasificacion_manual": "", "evidencia": ""} for h, f, s in elegidos], len(commits)


def main():
    p = argparse.ArgumentParser(description="Métricas de evolución de un repositorio Git, versión por versión.")
    p.add_argument("repo", help="ruta del repositorio clonado con historia completa")
    p.add_argument("--ext", default=".py", help="extensiones del código fuente, separadas por coma (por defecto .py)")
    p.add_argument("--excluir", default="tests,test,testsuite,docs,examples,scripts",
                   help="carpetas que no cuentan como código fuente, separadas por coma")
    p.add_argument("--incluir", default="",
                   help="rutas del código fuente en formato glob, separadas por coma; reemplaza a --ext. "
                        "Ejemplo: 'flask.py,flask/**/*.py,src/flask/**/*.py'")
    p.add_argument("--versiones", default=PATRON_VERSIONES, help="expresión regular de las etiquetas que cuentan")
    p.add_argument("--muestra", type=int, default=40, help="tamaño de la muestra de commits (por defecto 40)")
    p.add_argument("--semilla", type=int, default=1, help="semilla de la muestra, para poder repetirla")
    p.add_argument("--desde", default="", help="tomar la muestra solo desde esta etiqueta (opcional)")
    p.add_argument("--solo-fuente", action="store_true",
                   help="tomar la muestra solo entre los commits que tocan el código fuente medido")
    p.add_argument("--salida", default=".", help="carpeta donde se escriben los CSV")
    a = p.parse_args()

    repo = Path(a.repo).resolve()
    if git(repo, "rev-parse", "--is-shallow-repository").strip() == "true":
        sys.exit("El repositorio es superficial (clonado con --depth). Clónelo completo o use: git fetch --unshallow")
    spec = rutas(a.ext.split(","), a.excluir.split(","), a.incluir.split(",") if a.incluir else [])
    lista = versiones(repo, a.versiones)
    if not lista:
        sys.exit("Ninguna etiqueta coincide con el patrón de versiones. Revise git tag y ajuste --versiones.")

    salida = Path(a.salida)
    salida.mkdir(parents=True, exist_ok=True)
    campos = ["version", "fecha", "archivos_fuente", "lineas_fuente", "commits_desde_anterior",
              "autores_desde_anterior", "archivos_modificados", "archivos_nuevos", "lineas_agregadas",
              "lineas_eliminadas"]
    filas, anterior = [], None
    for fecha, etiqueta in lista:
        archivos, lineas = tamano(repo, etiqueta, spec)
        filas.append(dict(zip(campos, (etiqueta, fecha, archivos, lineas, *entre(repo, anterior, etiqueta, spec)))))
        anterior = etiqueta
        print(f"  {etiqueta:<10} {fecha}  {archivos:>4} archivos  {lineas:>7} líneas")

    with open(salida / "evolucion_por_version.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        w.writerows(filas)

    cambios, total = muestra(repo, a.muestra, a.semilla, a.desde, spec if a.solo_fuente else [])
    with open(salida / "muestra_cambios.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(cambios[0].keys()) if cambios else ["commit"])
        w.writeheader()
        w.writerows(cambios)

    print(f"\n{len(filas)} versiones en evolucion_por_version.csv")
    print(f"{len(cambios)} de {total} commits en muestra_cambios.csv (semilla {a.semilla})")
    print("La columna sugerencia_heuristica es una ayuda de lectura: la clasificación del F-03 se hace a mano.")


if __name__ == "__main__":
    main()
