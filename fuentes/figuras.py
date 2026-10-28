#!/usr/bin/env python3
"""Dibuja en SVG los gráficos del recorrido resuelto a partir de ejemplo_flask/evolucion_por_version.csv.

Uso, desde la raíz del repositorio:  python fuentes/figuras.py
Escribe fuentes/figuras/tamano.svg, crecimiento.svg y actividad.svg.
"""

import csv
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "fuentes" / "figuras"
OSC, GRIS, LINEA, CORAL, TEAL, CAFE = "#1C2B33", "#6B7A82", "#CFDAE0", "#C2622C", "#46707E", "#9E5C3B"
ANCHO, ALTO = 680, 260
IZQ, DER, ARR, ABA = 58, 16, 18, 42


def leer():
    with open(RAIZ / "ejemplo_flask" / "evolucion_por_version.csv", encoding="utf-8") as f:
        filas = list(csv.DictReader(f))
    for r in filas:
        r["dia"] = date.fromisoformat(r["fecha"])
    return filas


def svg(cuerpo, titulo):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ANCHO} {ALTO}" width="{ANCHO}" height="{ALTO}" '
            f'font-family="Segoe UI, Liberation Sans, Arial, sans-serif" role="img" aria-label="{titulo}">'
            f'<rect width="100%" height="100%" fill="#fff"/>{cuerpo}</svg>')


def eje_y(maximo, pasos, fmt=lambda v: f"{v:,.0f}".replace(",", "."), minimo=0):
    alto = ALTO - ARR - ABA
    partes = []
    for i in range(pasos + 1):
        v = minimo + (maximo - minimo) * i / pasos
        y = ARR + alto - (v - minimo) / (maximo - minimo) * alto
        partes.append(f'<line x1="{IZQ}" x2="{ANCHO - DER}" y1="{y:.1f}" y2="{y:.1f}" stroke="{LINEA}" stroke-width="1"/>'
                      f'<text x="{IZQ - 6}" y="{y + 4:.1f}" text-anchor="end" font-size="11" fill="{GRIS}">{fmt(v)}</text>')
    return "".join(partes)


def tamano(filas):
    d0, d1 = date(2010, 1, 1), date(2025, 1, 1)
    alto = ALTO - ARR - ABA
    x = lambda d: IZQ + (d - d0).days / (d1 - d0).days * (ANCHO - IZQ - DER)
    y = lambda v: ARR + alto - v / 10000 * alto
    partes = [eje_y(10000, 5)]
    for anio in range(2010, 2026, 2):
        xx = x(date(anio, 1, 1))
        partes.append(f'<text x="{xx:.1f}" y="{ALTO - ABA + 16}" text-anchor="middle" font-size="11" fill="{GRIS}">{anio}</text>')
    puntos = " ".join(f"{x(r['dia']):.1f},{y(int(r['lineas_fuente'])):.1f}" for r in filas)
    partes.append(f'<polyline points="{puntos}" fill="none" stroke="{CORAL}" stroke-width="2.2"/>')
    rotular = {"0.1", "0.5", "0.11", "1.0", "2.0.0", "2.2.0", "2.3.0", "3.1.0"}
    for r in filas:
        cx, cy = x(r["dia"]), y(int(r["lineas_fuente"]))
        partes.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="3.2" fill="{CORAL}"/>')
        if r["version"] in rotular:
            dx, dy, ancla = {"0.1": (7, 4, "start"), "0.5": (-7, -4, "end"), "2.3.0": (0, 15, "middle")}.get(
                r["version"], (0, -8, "middle"))
            partes.append(f'<text x="{cx + dx:.1f}" y="{cy + dy:.1f}" text-anchor="{ancla}" font-size="10.5" '
                          f'fill="{OSC}">{r["version"]}</text>')
    partes.append(f'<text x="14" y="{ARR + alto / 2}" transform="rotate(-90 14 {ARR + alto / 2})" text-anchor="middle" '
                  f'font-size="11" fill="{GRIS}">líneas de código fuente</text>')
    return svg("".join(partes), "Tamaño de Flask por versión")


def barras(filas, series, maximo, minimo, etiqueta_y, titulo, fmt=None):
    alto = ALTO - ARR - ABA
    n = len(filas)
    paso = (ANCHO - IZQ - DER) / n
    ancho_barra = paso * 0.78 / len(series)
    y = lambda v: ARR + alto - (v - minimo) / (maximo - minimo) * alto
    partes = [eje_y(maximo, 6, minimo=minimo, **({"fmt": fmt} if fmt else {}))]
    cero = y(0)
    partes.append(f'<line x1="{IZQ}" x2="{ANCHO - DER}" y1="{cero:.1f}" y2="{cero:.1f}" stroke="{GRIS}" stroke-width="1"/>')
    for i, r in enumerate(filas):
        x0 = IZQ + i * paso + paso * 0.11
        for k, (valor, color) in enumerate(series):
            v = valor(r)
            if v is None:
                continue
            arriba, abajo = (y(v), cero) if v >= 0 else (cero, y(v))
            partes.append(f'<rect x="{x0 + k * ancho_barra:.1f}" y="{arriba:.1f}" width="{ancho_barra - 1:.1f}" '
                          f'height="{max(abajo - arriba, 0.5):.1f}" fill="{color}"/>')
        partes.append(f'<text x="{IZQ + i * paso + paso / 2:.1f}" y="{ALTO - ABA + 14}" text-anchor="end" font-size="9.5" '
                      f'fill="{GRIS}" transform="rotate(-40 {IZQ + i * paso + paso / 2:.1f} {ALTO - ABA + 14})">{r["version"]}</text>')
    partes.append(f'<text x="14" y="{ARR + alto / 2}" transform="rotate(-90 14 {ARR + alto / 2})" text-anchor="middle" '
                  f'font-size="11" fill="{GRIS}">{etiqueta_y}</text>')
    return svg("".join(partes), titulo)


def numero(r, campo):
    return int(r[campo]) if r[campo] else None


def por_mes(filas):
    """Commits por mes en el intervalo que termina en cada versión: los intervalos tienen duraciones distintas."""
    out = []
    for i, r in enumerate(filas):
        if i == 0:
            out.append(None)
            continue
        meses = max((r["dia"] - filas[i - 1]["dia"]).days / 30.44, 0.5)
        out.append(int(r["commits_desde_anterior"]) / meses)
    return out


def main():
    SALIDA.mkdir(exist_ok=True)
    filas = leer()
    (SALIDA / "tamano.svg").write_text(tamano(filas), encoding="utf-8")
    crecimiento = barras(filas[1:], [(lambda r: numero(r, "lineas_agregadas"), TEAL),
                                     (lambda r: -numero(r, "lineas_eliminadas"), CAFE)],
                         3000, -3000, "líneas agregadas (+) y eliminadas (−)", "Crecimiento por versión",
                         fmt=lambda v: f"{v:+,.0f}".replace(",", ".") if v else "0")
    (SALIDA / "crecimiento.svg").write_text(crecimiento, encoding="utf-8")
    mensual = dict(zip((r["version"] for r in filas), por_mes(filas)))
    actividad = barras(filas[1:], [(lambda r: mensual[r["version"]], CORAL)], 150, 0,
                       "commits por mes entre versiones", "Actividad entre versiones")
    (SALIDA / "actividad.svg").write_text(actividad, encoding="utf-8")
    for r in filas[1:]:
        print(f'{r["version"]:<7} {mensual[r["version"]]:6.1f} commits/mes')


if __name__ == "__main__":
    main()
