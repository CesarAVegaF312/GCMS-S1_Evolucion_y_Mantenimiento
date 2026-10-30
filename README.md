# GCMS S1 — Evolución y Mantenimiento

Material de la **Sesión 1** del curso *Gestión de Configuración y Mantenimiento de Software* (GCMS),
Unidad 1: **Evolución del software y mantenimiento**. Maestría en Ingeniería de Software,
Universidad de La Sabana.

El curso se trabaja con **aprendizaje basado en proyectos**. En esta unidad cada grupo elige un sistema
de software (académico, laboral o simulado), lo caracteriza y lo diagnostica. Ese mismo sistema sigue
en las unidades siguientes:

- en la Unidad 2 se le diseña la gestión de configuración;
- en la Unidad 3 se le implementan el control de versiones y el pipeline de CI/CD;
- en la Unidad 4 se le proponen e implementan mejoras.

Los temas de la unidad son las **leyes de Lehman**, el **envejecimiento del software**, los **tipos de
mantenimiento** (correctivo, adaptativo, perfectivo y preventivo) y la **deuda técnica**.

Las actividades de la unidad:

- **Actividad 0. Presentación del reto y contexto del sistema** · grupal, de 2 a 3 · formativa · 6 horas.
  - **Entregable:** un documento de **2 a 3 páginas** o una presentación de **5 a 7 diapositivas** que incluya:
    - descripción del sistema;
    - caracterización (tipo, usuarios, componentes);
    - problema inicial;
    - reto formulado como pregunta;
    - alcance;
    - criterios de éxito preliminares.
  - Se retroalimenta con una lista de chequeo.
- **Actividad 1. Análisis de evolución, deuda técnica y mantenimiento** · grupal, de 2 a 3 · **15 %** · 12 horas.
  - **Entregable:** un documento técnico de **5 a 7 páginas**, en **norma APA 7**, que incluya:
    - descripción y contexto del sistema;
    - problemas asociados a su evolución;
    - deuda técnica;
    - clasificación de los tipos de mantenimiento;
    - análisis de riesgos (cambios no controlados y falta de estrategias de evolución).
  - Se califica con la rúbrica del aula.
  - **Los formatos F-01 a F-07 no se suben:** son el borrador de los entregables.

---

## Empiecen aquí

**Todo el material se abre desde aquí, sin descargar nada:**
<https://cesaravegaf312.github.io/GCMS-S1_Evolucion_y_Mantenimiento/>

1. **Lean el [enunciado](documentos/1_actividades/GCMS_S1_Enunciado_Actividades.pdf).** El encargo, los
   criterios para elegir el sistema, los entregables, los criterios de evaluación y el paso a paso.
2. **Lean el [recorrido resuelto con Flask](documentos/2_ejemplo/GCMS_S1_Recorrido_Flask.pdf).** Así
   se ven los formatos llenos con un sistema real. Todos los números se pueden repetir con la
   herramienta de este repositorio.
3. **Elijan su sistema** con los criterios del F-01 y preparen la Actividad 0.
4. **Llenen los [Instrumentos F-01 a F-07](documentos/3_como_se_hace/GCMS_S1_Instrumentos.pdf)** en
   orden. **Primero se reúne la evidencia y se clasifica, después se analizan deuda y riesgos.**

Para trabajar sin conexión, descarguen el repositorio (botón verde **`Code` → `Download ZIP`**),
descomprímanlo y hagan doble clic en `index.html`: la portada abre todo lo demás.

---

## La herramienta de métricas

Si el sistema del grupo tiene historia en Git, `herramientas/metricas_evolucion.py` saca de ella la
evidencia para los formatos F-02 y F-03. Si no la tiene, la evidencia sale de tickets, incidentes y
versiones desplegadas.

| Archivo | Qué contiene | Formato |
|---|---|---|
| `evolucion_por_version.csv` | Una fila por versión: archivos y líneas de código fuente, commits y autores desde la versión anterior, archivos modificados y nuevos, líneas agregadas y eliminadas | F-02 |
| `muestra_cambios.csv` | Una muestra aleatoria de commits, repetible con una semilla, con una sugerencia heurística de tipo de mantenimiento y columnas vacías para la clasificación manual | F-03 |

Requiere **Python 3.8 o posterior** y **git**. No usa bibliotecas externas.

```bash
# 1. Clonar el sistema con toda su historia (sin --depth)
git clone https://github.com/<organizacion>/<sistema>.git

# 2. Ver las etiquetas para decidir qué cuenta como versión
git -C <sistema> tag

# 3. Correr la herramienta, indicando las rutas del código fuente
python herramientas/metricas_evolucion.py <sistema> \
    --incluir "src/<paquete>/**/*.py" --solo-fuente --muestra 20 --semilla 7 --salida salida
```

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
├── presentacion.html   ← las 21 diapositivas de la sesión
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
| [`presentacion.html`](presentacion.html) | La sesión en el navegador: 21 diapositivas con índice (**I**), glosario de códigos (**G**), cronómetro del taller (**T**), notas del docente (**N**), modo presentador (**P**) y modo de lectura para el teléfono (**L**). |
| [`documentos/4_clase/GCMS_S1_Deck.pdf`](documentos/4_clase/GCMS_S1_Deck.pdf) | Las mismas diapositivas en PDF. |

La sesión va en tres bloques:

1. **Primero, qué significa:** envejecimiento, tipos de programa, leyes de Lehman, tipos de mantenimiento,
   deuda técnica, riesgos de no gestionar la evolución y la cadena que sostiene el documento.
2. **Después, seis ejemplos guiados** con Flask.
3. **Al final, el taller en salas:** cada grupo elige su sistema y sale con la Actividad 0 en borrador.

### Documentos — carpeta `documentos/`

| Archivo | Descripción |
|---|---|
| [`1_actividades/GCMS_S1_Enunciado_Actividades.pdf`](documentos/1_actividades/GCMS_S1_Enunciado_Actividades.pdf) | El encargo, los criterios del sistema, las actividades 0 y 1, las secciones del documento, los criterios de evaluación y los errores frecuentes. |
| [`2_ejemplo/GCMS_S1_Recorrido_Flask.pdf`](documentos/2_ejemplo/GCMS_S1_Recorrido_Flask.pdf) | Los formatos F-01 a F-06 llenos con la historia real de Flask, con gráficos, casos difíciles y riesgos. |
| [`3_como_se_hace/GCMS_S1_Instrumentos.pdf`](documentos/3_como_se_hace/GCMS_S1_Instrumentos.pdf) | Los siete formatos en blanco, con instrucciones de llenado. |
| [`4_clase/GCMS_S1_Deck.pdf`](documentos/4_clase/GCMS_S1_Deck.pdf) | Las diapositivas de la sesión. |

### Recursos interactivos — carpeta `interactivos/`

| Archivo | Descripción |
|---|---|
| [`leyes_lehman_interactivo.html`](interactivos/leyes_lehman_interactivo.html) | Las ocho leyes con el dato que las mostraría y cómo se vieron en Flask. Incluye un modelo didáctico de la ley II y el tamaño real de Flask por versión. |
| [`clasificador_mantenimiento_interactivo.html`](interactivos/clasificador_mantenimiento_interactivo.html) | Trece cambios reales de Flask con su diff para clasificar. Muestra el razonamiento y lo que habría dicho la heurística. No califica. |

---

## Material de la unidad

**Obligatorio**

- Lehman, M. M. (1996). Laws of software evolution revisited. En C. Montangero (Ed.), *Software Process Technology* (pp. 108–124). Springer. https://doi.org/10.1007/BFb0017737
- O'Reilly. (2019). *Technical debt: A master class* [Grabación de video]. O'Reilly Media. Disponible en la biblioteca.
- Fowler, M. *Technical debt*. https://martinfowler.com/bliki/TechnicalDebt.html
- Pressman, R. S. (2010). *Software engineering: A practitioner's approach* (7.ª ed.). McGraw-Hill. Capítulo de mantenimiento.

**Complementario**

- Google. (2022). *The site reliability workbook*. https://sre.google/workbook/

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

## Referencias de la sesión

- Fowler, M. (2009). *Technical debt quadrant*. https://martinfowler.com/bliki/TechnicalDebtQuadrant.html
- ISO/IEC/IEEE. (2022). *ISO/IEC/IEEE 14764:2022 Software engineering — Software life cycle processes — Maintenance*.
- Lehman, M. M. (1980). Programs, life cycles, and laws of software evolution. *Proceedings of the IEEE, 68*(9), 1060–1076.
- Lehman, M. M. (1996). Laws of software evolution revisited. En C. Montangero (Ed.), *Software Process Technology* (pp. 108–124). Springer.
- Lions, J. L. (1996). *Ariane 5 flight 501 failure: Report by the inquiry board*. European Space Agency.
- Parnas, D. L. (1994). Software aging. En *Proceedings of the 16th International Conference on Software Engineering* (pp. 279–287). IEEE.
- Pressman, R. S. (2010). *Software engineering: A practitioner's approach* (7.ª ed.). McGraw-Hill.
- Securities and Exchange Commission. (2013). *In the matter of Knight Capital Americas LLC* (Release No. 70694).

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
