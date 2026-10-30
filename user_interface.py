# ============================================================
# Maestría de Ciencia de Datos
#
# Curso: Transformers
#
# Autores:
# - Samir Mateo Sierra Blanco
# - Maria Fernanda González Acevedo
# ============================================================

# Se importan las librerías necesarias
import gradio as gr

# Se importa la función de análisis desarrollada en sentiment_analyzer.py
from sentiment_analyzer import analyze_sentiment

# ------------------------------------------------------------
# Configuración visual
# ------------------------------------------------------------

# Colores asociados a cada sentimiento (tonos sobrios, aptos para presentación académica)
SENTIMENT_STYLES = {
    "Positivo": {"color": "#1B6B4A", "background": "#EAF4EF"},
    "Neutral":  {"color": "#4A5568", "background": "#EFF1F4"},
    "Negativo": {"color": "#9B2C2C", "background": "#FBECEC"},
}

# Tema base de Gradio: tonos azules y grises, tipografía Inter
THEME = gr.themes.Base(
    primary_hue="blue",
    neutral_hue="slate",
    font=[gr.themes.GoogleFont("Inter"), "system-ui", "sans-serif"],
)

# Estilos CSS adicionales para el encabezado y la tarjeta de resultado
CSS = """
.gradio-container { max-width: 1100px !important; margin: 0 auto !important; }

.app-header {
    background: #1F3A5F;
    padding: 28px 32px;
    border-radius: 8px;
    margin-bottom: 12px;
}
.app-header .eyebrow {
    color: #B8C7DB !important;
    font-size: 0.8rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin: 0 0 6px 0;
}
.app-header h1 {
    color: #FFFFFF !important;
    font-size: 1.7rem;
    font-weight: 600;
    margin: 0 0 8px 0;
}
.app-header .subtitle {
    color: #D5DEEA !important;
    font-size: 0.95rem;
    margin: 0;
}

.result-card {
    padding: 24px 28px;
    border-radius: 8px;
    border: 1px solid #D9DEE5;
    min-height: 260px;
}
.result-card .caption {
    color: #5B6572 !important;
    font-size: 0.78rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin: 0 0 4px 0;
}
.result-card .sentiment {
    font-size: 2rem;
    font-weight: 700;
    margin: 0 0 6px 0;
}
.result-card .stars {
    font-size: 1.4rem;
    letter-spacing: 3px;
    margin: 0 0 4px 0;
}
.result-card .meta {
    color: #4A5568 !important;
    font-size: 0.9rem;
    margin: 0 0 18px 0;
}
.bar-track {
    background: #D9DEE5;
    border-radius: 4px;
    height: 10px;
    overflow: hidden;
    margin-bottom: 6px;
}
.bar-fill { height: 100%; border-radius: 4px; }
.placeholder-text { color: #6B7280 !important; font-size: 0.95rem; }
"""

# ------------------------------------------------------------
# Contenido estático
# ------------------------------------------------------------

HEADER_HTML = """
<div class="app-header">
    <p class="eyebrow">Maestría en Ciencia de Datos &middot; Curso: Transformers</p>
    <h1>Análisis de Sentimiento en Textos en Español</h1>
    <p class="subtitle">
        Clasificación con un modelo BERT multilingüe preentrenado
        (nlptown/bert-base-multilingual-uncased-sentiment).
    </p>
</div>
"""

EMPTY_RESULT_HTML = """
<div class="result-card">
    <p class="caption">Resultado</p>
    <p class="placeholder-text">
        Ingrese un texto y presione "Analizar sentimiento" para ver la clasificación.
    </p>
</div>
"""

EXAMPLES = [
    ["El servicio fue excelente, la atención fue rápida y el personal muy amable."],
    ["Es un producto aceptable, cumple su función pero nada más."],
    ["Una experiencia terrible, el pedido llegó tarde y en mal estado."],
    ["La película tiene buenos momentos, aunque el final me decepcionó bastante."],
]

METHODOLOGY_NOTE = """
**Modelo.** `nlptown/bert-base-multilingual-uncased-sentiment`, un modelo BERT
multilingüe ajustado (*fine-tuned*) para predecir una calificación de 1 a 5 estrellas
a partir de reseñas de productos.

**Reglas de conversión a tres clases.** 1 y 2 estrellas se clasifican como *Negativo*,
3 estrellas como *Neutral* y 4 y 5 estrellas como *Positivo*.

**Limitaciones.** El modelo fue entrenado con reseñas de productos, por lo que su
desempeño puede disminuir en otros dominios (política, textos formales, ironía).
La clase *Neutral* es una aproximación: corresponde a la calificación intermedia de
una escala de estrellas, no a una categoría de neutralidad entrenada de forma explícita.
La confianza mostrada es la probabilidad de la clase predicha, no una medida de
exactitud garantizada.
"""

# ------------------------------------------------------------
# Lógica de la interfaz
# ------------------------------------------------------------

def build_result_html(result: dict) -> str:
    """Construye la tarjeta HTML a partir del diccionario devuelto por analyze_sentiment."""
    style = SENTIMENT_STYLES[result["sentiment"]]

    # La etiqueta del modelo tiene la forma "4 stars"; se extrae el número
    stars = int(result["label"].split()[0])
    star_text = "★" * stars + "☆" * (5 - stars)

    confidence = result["score"] * 100

    return f"""
    <div class="result-card" style="background: {style['background']};
                                    border-left: 6px solid {style['color']};">
        <p class="caption">Sentimiento predominante</p>
        <p class="sentiment" style="color: {style['color']};">{result['sentiment']}</p>
        <p class="stars" style="color: {style['color']};">{star_text}</p>
        <p class="meta">Clase del modelo: {result['label']}</p>
        <p class="caption">Confianza del modelo</p>
        <div class="bar-track">
            <div class="bar-fill" style="width: {confidence:.1f}%;
                                         background: {style['color']};"></div>
        </div>
        <p class="meta">{confidence:.1f} %</p>
    </div>
    """


def classify_text(text: str) -> str:
    """Recibe el texto de la caja, llama al analizador y devuelve HTML para mostrar."""
    # Se valida que el usuario haya escrito algo antes de llamar al modelo
    if not text or not text.strip():
        return EMPTY_RESULT_HTML

    # analyze_sentiment devuelve una lista; como se envía un solo texto, se toma el primer elemento
    result = analyze_sentiment(text)[0]
    return build_result_html(result)


def clear_all():
    """Restablece la caja de texto y el panel de resultado."""
    return "", EMPTY_RESULT_HTML


# Se construye la función que crea la interfaz de usuario
def create_interface() -> gr.Blocks:
    with gr.Blocks(title="Análisis de Sentimiento en Español") as demo:

        gr.HTML(HEADER_HTML)

        with gr.Row(equal_height=False):
            # Columna izquierda: entrada
            with gr.Column(scale=1):
                text_input = gr.Textbox(
                    label="Texto en español",
                    placeholder="Escriba o pegue aquí el texto que desea analizar...",
                    lines=8,
                    max_lines=14,
                )
                with gr.Row():
                    clear_button = gr.Button("Limpiar", variant="secondary")
                    submit_button = gr.Button("Analizar sentimiento", variant="primary")

            # Columna derecha: resultado
            with gr.Column(scale=1):
                result_output = gr.HTML(value=EMPTY_RESULT_HTML)

        gr.Examples(
            examples=EXAMPLES,
            inputs=text_input,
            label="Ejemplos de texto",
        )

        with gr.Accordion("Nota metodológica", open=False):
            gr.Markdown(METHODOLOGY_NOTE)

        # Conexión de eventos: qué función se ejecuta al interactuar con cada componente
        submit_button.click(fn=classify_text, inputs=text_input, outputs=result_output)
        clear_button.click(fn=clear_all, inputs=None, outputs=[text_input, result_output])

    return demo