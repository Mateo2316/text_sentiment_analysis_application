---
title: Análisis de sentimiento
emoji: 💬
colorFrom: blue
colorTo: purple
sdk: gradio
app_file: app.py
---

# Análisis de sentimiento de textos

Aplicación para identificar el sentimiento expresado en un texto. La interfaz de usuario está prevista en [Gradio](https://www.gradio.app/) y el proyecto se prepara para su publicación como un [Hugging Face Space](https://huggingface.co/spaces).

## Modelo

El análisis utiliza [`nlptown/bert-base-multilingual-uncased-sentiment`](https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment), un modelo multilingüe de clasificación de sentimientos en cinco niveles de estrellas. La función `analyze_sentiment` devuelve el texto, la etiqueta de estrellas, una categoría general y la puntuación de la clase predicha:

| Estrellas | Categoría |
| --- | --- |
| 1–2 | Negativo |
| 3 | Neutral |
| 4–5 | Positivo |

El modelo y el tokenizador se descargan de Hugging Face la primera vez que se ejecuta el analizador. La puntuación es la probabilidad asignada por el modelo a su predicción; no representa una certeza objetiva.

## Requisitos

- Python 3.10 o posterior.
- `pip`.
- Conexión a Internet durante la primera ejecución para descargar el modelo.

Las dependencias están declaradas en [`requirements.txt`](./requirements.txt).

## Preparación local

Desde la raíz del proyecto, crea y activa un entorno virtual e instala las dependencias:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

En Windows, activa el entorno con:

```powershell
.venv\Scripts\Activate.ps1
```

### Estado de ejecución

La lógica de análisis está en `sentiment_analyzer.py`. La interfaz y el punto de entrada (`user_interface.py` y `app.py`), la aplicación se ejecuta con el comando `python app.py`.

## Estructura del proyecto

```text
.
├── app.py                 # Punto de entrada previsto para Gradio
├── user_interface.py      # Interfaz de usuario
├── sentiment_analyzer.py  # Carga del modelo y análisis de sentimiento
├── requirements.txt       # Dependencias de Python
└── README.md
```

## Limitaciones

El modelo predice una categoría de sentimiento a partir de patrones aprendidos; sus resultados pueden no reflejar el contexto, el sarcasmo o las particularidades de todos los idiomas y dominios. No debe interpretarse como una evaluación infalible del texto.