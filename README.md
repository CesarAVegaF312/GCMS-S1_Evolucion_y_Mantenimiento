# GCMS S1 — Evolución y Mantenimiento

Material de la **Sesión 1** del curso *Gestión de Configuración y Mantenimiento de Software* (GCMS),
Unidad 1: **Evolución del software y mantenimiento**. Maestría en Ingeniería de Software,
Universidad de La Sabana.

En esta unidad se pasa de la intuición sobre un sistema («está viejo», «está estable», «está lleno de
parches») a un **diagnóstico con evidencia**, sacada de la propia historia del sistema: el repositorio
Git, el registro de cambios y los issues. Los referentes son las **leyes de la evolución del software de
Lehman**, los **tipos de mantenimiento** de la norma ISO/IEC/IEEE 14764, el **modelo por etapas** de
Rajlich y Bennett y la **deuda técnica**.

Las actividades de la unidad:

- **Actividad 1.1. Presentación del reto** · individual · formativa · peso y horas: *por completar*.
  - **Entregable:** una reflexión de **1 a 2 páginas** en PDF y en norma APA 7. Debe responder qué
    tipo de mantenimiento consume más esfuerzo en un sistema que usted mantiene o conoce, y cómo lo
    demostraría. Cierra con la propuesta de un proyecto de código abierto y el **F-01** en borrador.
- **Actividad 1.2. Diagnóstico de evolución y mantenimiento** · grupal · peso y horas: *por completar*.
  - **Entregable:** un informe en PDF de **máximo 15 páginas**, en **norma APA 7**, sobre un proyecto de
    código abierto elegido por el grupo. Debe incluir:
    - métricas de evolución por versión;
    - la clasificación de una muestra de al menos 40 cambios;
    - el contraste con al menos cuatro leyes de Lehman;
    - la etapa del ciclo de vida;
    - cinco deudas técnicas localizadas;
    - una recomendación.
  - Como anexo van los dos CSV de la herramienta, con el comando exacto que los generó.
  - **Los formatos F-01 a F-07 no se suben:** son el borrador de las secciones del informe.

---

## Empiecen aquí

**Todo el material se abre desde aquí, sin descargar nada:**
<https://cesaravegaf312.github.io/GCMS-S1_Evolucion_y_Mantenimiento/>

1. **Lean el [enunciado](documentos/1_actividad_1_2/GCMS_S1_Enunciado_Actividad_1_2.pdf).** Tres
   páginas: el encargo, qué debe tener el informe, con qué criterios se evalúa y el paso a paso.
2. **Lean el [recorrido resuelto con Flask](documentos/2_ejemplo/GCMS_S1_Recorrido_Flask.pdf).** Así
   se ven los formatos llenos con un proyecto real. Todos los números se pueden repetir con la
   herramienta de este repositorio.
3. **Elijan el proyecto** con los criterios del F-01 y **corran la herramienta** sobre él (ver abajo).
4. **Llenen los [Instrumentos F-01 a F-07](documentos/3_como_se_hace/GCMS_S1_Instrumentos.pdf)** en
   orden. **Primero se mide y se clasifica, después se contrasta con las leyes.**

Para trabajar sin conexión, descarguen el repositorio (botón verde **`Code` → `Download ZIP`**),
descomprímanlo y hagan doble clic en `index.html`: la portada abre todo lo demás.

---

## La herramienta de métricas

`herramientas/metricas_evolucion.py` lee un repositorio Git clonado y escribe dos archivos CSV:

| Archivo | Qué contiene | Formato que alimenta |
|---|---|---|
| `evolucion_por_version.csv` | Una fila por versión con funcionalidad nueva: archivos y líneas de código fuente, commits y autores desde la versión anterior, archivos modificados y nuevos, líneas agregadas y eliminadas | F-02 |
| `muestra_cambios.csv` | Una muestra aleatoria de commits, repetible con una semilla, con una sugerencia heurística de tipo de mantenimiento y columnas vacías para la clasificación manual | F-03 |

Requiere **Python 3.8 o posterior** y **git**. No usa bibliotecas externas.

```bash
# 1. Clonar el proyecto con toda su historia (sin --depth)
git clone https://github.com/<organizacion>/<proyecto>.git

# 2. Ver las etiquetas para decidir qué cuenta como versión
git -C <proyecto> tag

# 3. Correr la herramienta, indicando las rutas del código fuente
python herramientas/metricas_evolucion.py <proyecto> \
    --incluir "src/<paquete>/**/*.py" --solo-fuente --muestra 40 --semilla 7 --salida salida
```

Opciones principales:

| Opción | Para qué sirve |
|---|---|
| `--incluir` | Rutas del código fuente en formato glob, separadas por coma. Si el código cambió de carpeta durante la historia, se ponen todas las rutas. |
| `--ext` y `--excluir` | Alternativa a `--incluir`: extensiones que cuentan y carpetas que no (por defecto `.py`; excluye pruebas, documentación, ejemplos y scripts). |
| `--versiones` | Expresión regular de las etiquetas que cuentan como versión. Por defecto `X.Y` o `X.Y.0`, con o sin `v`. |
| `--solo-fuente` | Toma la muestra solo entre los commits que tocan el código fuente medido. Recomendado: en Flask, el 60 % de una muestra sin esta opción no tocaba el producto. |
| `--muestra` y `--semilla` | Tamaño de la muestra y semilla, para que cualquiera pueda repetirla. |

La columna `sugerencia_heuristica` clasifica por palabras clave del mensaje del commit. **Es una
ayuda de lectura, no una clasificación:** en la muestra de Flask acierta en 15 de 40 casos. Cada
commit se clasifica leyendo su diff con `git show <commit>`.

---

## Estructura del repositorio

```text
GCMS-S1_Evolucion_y_Mantenimiento/
├── index.html          ← portada: abre desde aquí todo lo demás
├── presentacion.html   ← las 19 diapositivas de la sesión
├── README.md
├── LICENSE
├── documentos/         ← enunciado, recorrido resuelto, instrumentos y diapositivas (PDF)
├── interactivos/       ← leyes de Lehman y clasificador de mantenimiento en HTML
├── herramientas/       ← metricas_evolucion.py
├── ejemplo_flask/      ← los CSV del recorrido resuelto, con la clasificación manual
└── fuentes/            ← fuentes HTML de los PDF y scripts para regenerarlos
```

### La clase

| Archivo | Descripción |
|---|---|
| [`presentacion.html`](presentacion.html) | La sesión en el navegador: 19 diapositivas con índice (**I**), glosario de códigos (**G**), cronómetro del taller (**T**), notas del docente (**N**), modo presentador (**P**) y modo de lectura para el teléfono (**L**). |
| [`documentos/4_clase/GCMS_S1_Deck.pdf`](documentos/4_clase/GCMS_S1_Deck.pdf) | Las mismas diapositivas en PDF. |

La sesión va en tres bloques. **Primero, qué significa:** tipos de programa, leyes de Lehman, tipos de
mantenimiento, modelo por etapas, deuda técnica y la cadena que sostiene el informe. **Después, seis
ejemplos guiados**, uno por formato, recorridos con Flask. **Al final, el taller en salas**: cada grupo
sale con el proyecto elegido, el F-01 en borrador y los dos CSV generados.

### Documentos — carpeta `documentos/`

| Archivo | Descripción |
|---|---|
| [`1_actividad_1_2/GCMS_S1_Enunciado_Actividad_1_2.pdf`](documentos/1_actividad_1_2/GCMS_S1_Enunciado_Actividad_1_2.pdf) | El encargo, los entregables de las actividades 1.1 y 1.2, las secciones del informe, los criterios y los errores frecuentes. |
| [`2_ejemplo/GCMS_S1_Recorrido_Flask.pdf`](documentos/2_ejemplo/GCMS_S1_Recorrido_Flask.pdf) | Los formatos F-01 a F-06 llenos con la historia real de Flask, con gráficos, casos difíciles y recomendación. |
| [`3_como_se_hace/GCMS_S1_Instrumentos.pdf`](documentos/3_como_se_hace/GCMS_S1_Instrumentos.pdf) | Los siete formatos en blanco, con instrucciones de llenado. |
| [`4_clase/GCMS_S1_Deck.pdf`](documentos/4_clase/GCMS_S1_Deck.pdf) | Las diapositivas de la sesión. |

### Recursos interactivos — carpeta `interactivos/`

| Archivo | Descripción |
|---|---|
| [`leyes_lehman_interactivo.html`](interactivos/leyes_lehman_interactivo.html) | Las ocho leyes con el dato que las mostraría y cómo se vieron en Flask. Incluye un modelo didáctico de la ley II, para ver qué pasa con el crecimiento según el esfuerzo preventivo, y el tamaño real de Flask por versión. |
| [`clasificador_mantenimiento_interactivo.html`](interactivos/clasificador_mantenimiento_interactivo.html) | Trece cambios reales de Flask con su diff para clasificar. Muestra el razonamiento y lo que habría dicho la heurística. No califica: sirve para calibrar el criterio. |

---

## Cómo abrir los archivos

Los `.html` son **autocontenidos**: no requieren instalación, servidor ni conexión a internet.

- **En línea:** desde la [portada publicada](https://cesaravegaf312.github.io/GCMS-S1_Evolucion_y_Mantenimiento/).
- **En el computador:** descarguen el repositorio, descomprímanlo y hagan doble clic en `index.html`.
  Si se abre otro programa: clic derecho → **Abrir con** → Chrome, Edge o Firefox.

Al hacer clic sobre un `.html` **dentro de GitHub** se ve el código fuente, no la página. Hay que abrirlo
desde la portada publicada o descargarlo.

---

## Para el docente: regenerar los PDF

Los PDF se generan a partir de las fuentes HTML de `fuentes/`. Después de editar una fuente:

```bash
python fuentes/figuras.py      # gráficos del recorrido, desde ejemplo_flask/evolucion_por_version.csv
node fuentes/imprimir_pdf.js   # los cuatro PDF; requiere Playwright con Chromium
```

---

## Referencias

- Bourque, P., & Fairley, R. E. (Eds.). (2014). *Guide to the Software Engineering Body of Knowledge (SWEBOK v3.0)*. IEEE Computer Society.
- Cunningham, W. (1992). The WyCash portfolio management system. En *Addendum to the Proceedings of OOPSLA '92* (pp. 29–30). ACM.
- Fowler, M. (2009). *Technical debt quadrant*. https://martinfowler.com/bliki/TechnicalDebtQuadrant.html
- ISO/IEC/IEEE. (2022). *ISO/IEC/IEEE 14764:2022 Software engineering — Software life cycle processes — Maintenance*.
- Lehman, M. M. (1980). Programs, life cycles, and laws of software evolution. *Proceedings of the IEEE, 68*(9), 1060–1076.
- Lehman, M. M., Ramil, J. F., Wernick, P. D., Perry, D. E., & Turski, W. M. (1997). Metrics and laws of software evolution: The nineties view. En *Proceedings of the Fourth International Software Metrics Symposium* (pp. 20–32). IEEE.
- Parnas, D. L. (1994). Software aging. En *Proceedings of the 16th International Conference on Software Engineering* (pp. 279–287). IEEE.
- Rajlich, V. T., & Bennett, K. H. (2000). A staged model for the software life cycle. *Computer, 33*(7), 66–71.
- Swanson, E. B. (1976). The dimensions of maintenance. En *Proceedings of the 2nd International Conference on Software Engineering* (pp. 492–497). IEEE.

---

## Licencia

Este material se publica bajo la licencia
**[Creative Commons Atribución-NoComercial-CompartirIgual 4.0 Internacional (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.es)**.
Ver [`LICENSE`](LICENSE).

Pueden copiarlo y adaptarlo con fines no comerciales, siempre que den crédito al autor y compartan las
obras derivadas con la misma licencia.

*Los datos de los ejemplos provienen del repositorio público de [Flask](https://github.com/pallets/flask),
proyecto de Pallets con licencia BSD-3-Clause. Este repositorio analiza su historial; no redistribuye su
código.*
