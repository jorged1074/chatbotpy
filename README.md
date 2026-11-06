# EstáticaBot · Asistente de estática y Python

Chatbot local construido con **Python + Streamlit** que responde preguntas de
**estática** (mecánica para ingeniería) y **programación básica en Python**.
No necesita internet, claves de API ni modelos externos: las respuestas salen
de una base de conocimiento incluida en el proyecto.

## Características

- 💬 Interfaz de chat con historial, sugerencias clicables y descarga de la conversación.
- 🧱 **16 temas de estática:** DCL, vectores, momentos, equilibrio, apoyos,
  centroides, fricción, armaduras, cortante/flector, cables, unidades, vigas…
- 🐍 **19 temas de Python:** variables, tipos, condicionales, bucles, funciones,
  listas, diccionarios, errores, recursividad, NumPy, Matplotlib, clases,
  archivos, validación y depuración.
- 🔗 **3 temas puente:** sistemas de equilibrio con NumPy, scripts de estática
  y manejo de unidades en código.
- 🔎 Búsqueda tolerante a tildes, mayúsculas, plurales y errores de tipeo.
- 🧮 Calculadora lateral de resultante de fuerzas y reacciones de viga.
- ✅ 22 tests automatizados (motor + calculadoras).

## Requisitos

- Python **3.10 o superior** (probado con Python 3.14).
- Windows, macOS o Linux. En Windows se incluyen scripts de arranque.

## Inicio rápido

### Windows (recomendado)

Haz doble clic en `run.bat` o ejecuta en PowerShell:

```powershell
.\run.ps1
```

El script crea `.venv`, instala las dependencias y abre la app en
<http://localhost:8501>.

> Si PowerShell bloquea el script, ejecuta una vez:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

### Manual (cualquier sistema)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

En macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Estructura del proyecto

```
chatbot/
├── app.py                  # Interfaz Streamlit
├── bot/
│   ├── __init__.py         # API pública del paquete
│   ├── engine.py           # Motor TF-IDF + intenciones + sugerencias
│   ├── knowledge_base.py   # 38 entradas de estática y Python
│   ├── text_utils.py       # Normalización, stemming y sinónimos
│   └── calculators.py      # Resultante y reacciones de viga
├── tests/
│   ├── test_engine.py
│   └── test_calculators.py
├── .streamlit/config.toml  # Tema y configuración de Streamlit
├── requirements.txt
├── run.ps1 / run.bat
└── README.md
```

## Cómo funciona

1. La pregunta se normaliza: minúsculas, sin tildes, sin signos.
2. Se eliminan palabras vacías y se aplica un *stemming* ligero de plurales.
3. Se expanden sinónimos (`torque → momento`, `truss → armadura`, `dcl → diagrama de cuerpo libre`).
4. Se corrigen tipeos leves comparando contra el vocabulario (`mometo → momento`).
5. Se calcula similitud de coseno entre la consulta y cada tema (TF-IDF).
6. Si la coincidencia es suficiente se responde; si es baja se ofrece la mejor
   aproximación con un aviso; si es muy baja se muestra ayuda con sugerencias.

Las intenciones conversacionales (saludo, ayuda, identidad, agradecimiento y
despedida) se detectan aparte para no interceptar preguntas técnicas.

## Añadir un tema nuevo

Edita `bot/knowledge_base.py` y agrega una entrada a `ENTRIES`:

```python
Entry(
    id="mi-tema",
    title="Mi tema nuevo",
    category="Programación",  # o "Estática" / "Estática ↔ Python"
    tags=("palabra clave", "otra palabra"),
    patterns=(
        "¿Cómo se hace mi tema?",
        "Pregunta de ejemplo",
    ),
    answer=r"""Aquí va la respuesta en **Markdown**.

$$F = m\,a$$

```python
print("ejemplo")
```
""",
    related=("variables", "funciones"),
),
```

No hace falta tocar el motor: el índice se construye automáticamente al iniciar.
Los `related` deben existir y las respuestas admiten LaTeX y bloques de código.

## Tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Los tests verifican integridad del catálogo, clasificación de preguntas
representativas, tolerancia a tipeos, intenciones, fallback y cálculos.

## Notas y limitaciones

- Es un chatbot **basado en reglas y recuperación**, no un modelo de lenguaje:
  responde bien sobre los temas incluidos y pide reformular fuera de ellos.
- Para ampliar la cobertura, agrega entradas a la base de conocimiento.
- Las respuestas son educativas; verifica siempre los cálculos de ingeniería.
- La calculadora de viga considera solo una carga puntual vertical.
