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
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Se especifica el modelo a utilizar
MODEL_ID = "nlptown/bert-base-multilingual-uncased-sentiment"

# Se carga el tokenizador y el modelo
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_ID)

# Se pone el modelo en modo evaluación para desactivar el dropout y las capas que solo se usan durante el entrenamiento
model.eval()  

# Se define la función para analizar el sentimiento de los textos
def analyze_sentiment(texts: str | list[str]) -> list[dict[str, str | float]]:

    # Se verifica si el input es un string o una lista de strings, y se convierte a lista si es necesario
    if isinstance(texts, str):
        texts = [texts]

    # Se tokenizan los textos, se aplica padding y truncation, y se convierten a tensores de PyTorch
    inputs = tokenizer(texts, padding = True, truncation = True, return_tensors = "pt")

    # Se realiza la inferencia con el modelo sin calcular gradientes 
    with torch.no_grad():
        # Se obtienen las salidas del modelo
        outputs = model(**inputs)

    # Se calculan las probabilidades a partir de los logits utilizando softmax
    probabilities = torch.softmax(outputs.logits, dim = -1)

    # Se obtiene la clase con la mayor probabilidad para cada texto
    predictions = torch.argmax(probabilities, dim = -1)

    results = []

    # Se itera sobre las predicciones y se construye la lista de resultados
    for index, prediction in enumerate(predictions):
        # Se obtiene la etiqueta y probabilidad correspondiente a la predicción
        label = model.config.id2label[prediction.item()]
        score = probabilities[index,prediction].item()

        # Se determina el sentimiento basado en la etiqueta
        stars = int(label.split()[0])

        # Se asigna el sentimiento según el número de estrellas
        if stars <=2:
            sentiment = "Negativo"
        elif stars == 3:
            sentiment = "Neutral"
        else:
            sentiment = "Positivo"

        # Se agrega el resultado al diccionario de resultados
        results.append({
            "text": texts[index],
            "label": label,
            "sentiment": sentiment,
            "score": round(score, 4)
        })

    return results
