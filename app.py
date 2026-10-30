# ============================================================
# Maestría de Ciencia de Datos
#
# Curso: Transformers
#
# Autores:
# - Samir Mateo Sierra Blanco
# - Maria Fernanda González Acevedo
# ============================================================

# Se importan la función que construye la interfaz y su configuración visual
from user_interface import create_interface, THEME, CSS

# Se crea la aplicación
demo = create_interface()

# Se lanza la aplicación solo si este archivo se ejecuta directamente
if __name__ == "__main__":
    demo.launch(theme=THEME, css=CSS)