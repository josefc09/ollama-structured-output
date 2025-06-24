Ejemplo práctico para generar resúmenes de texto en un formato JSON predefinido (title, summary, keywords) ejecutados modelos LLMs localmente con Ollama y utilizando Gramáticas GBNF en Python.

### Requisitos

Antes de ejecutar el proyecto, asegúrate de tener lo siguiente:
* Ollama instalado: Descarga e instala Ollama desde https://ollama.com/download.
* Modelo llama3.2:latest descargado.
* Python.

### Pasos:

```Bash
git clone <https://github.com/josefc09/machine-failure-predictor.git>
mkdir ollama_structured_output
cd ollama_structured_output
```

Entorno Virtual

```Bash
python -m venv .venv
source .venv/bin/activate
pip install ollama
```

Ejecutar script

```Bash
python generate_summary.py
```
