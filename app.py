import time
import numpy as np
import streamlit as st

# Configuración de la página de Streamlit
st.set_page_config(
    page_title="Juego de la Vida - Conway", page_icon="🦠", layout="centered"
)


# Función que aplica las reglas del Juego de la Vida de Conway
def actualizar_grid(grid):
  # Contar vecinos usando sumas de desplazamientos (roll) en la matriz
  vecinos = (
      np.roll(grid, 1, axis=0)
      + np.roll(grid, -1, axis=0)
      + np.roll(grid, 1, axis=1)
      + np.roll(grid, -1, axis=1)
      + np.roll(np.roll(grid, 1, axis=0), 1, axis=1)
      + np.roll(np.roll(grid, 1, axis=0), -1, axis=1)
      + np.roll(np.roll(grid, -1, axis=0), 1, axis=1)
      + np.roll(np.roll(grid, -1, axis=0), -1, axis=1)
  )

  nuevo_grid = np.zeros_like(grid)
  # Reglas:
  # 1. Supervivencia: Célula viva con 2 o 3 vecinos vivos se queda viva.
  # 2. Nacimiento: Célula muerta con exactamente 3 vecinos vivos revive.
  nuevo_grid[(grid == 1) & ((vecinos == 2) | (vecinos == 3))] = 1
  nuevo_grid[(grid == 0) & (vecinos == 3)] = 1
  return nuevo_grid


# Título y descripción orientados a la presentación y storytelling
st.title("🦠 El Juego de la Vida de John Conway")
st.markdown("""
Simulación interactiva desarrollada como proyecto parcial de la materia optativa de Programación. 
Este autómata celular demuestra cómo patrones complejos pueden surgir a partir de reglas matemáticas simples.
""")

# Panel de control en la barra lateral
st.sidebar.header("⚙️ Controles de Simulación")
filas = st.sidebar.slider("Filas del tablero", 10, 50, 30)
columnas = st.sidebar.slider("Columnas del tablero", 10, 50, 30)
probabilidad = st.sidebar.slider(
    "Densidad inicial de vida", 0.1, 0.5, 0.20, 0.05
)
velocidad = st.sidebar.slider(
    "Velocidad de animación (segundos por generación)", 0.05, 1.0, 0.2, 0.05
)

# Inicializar el estado de la sesión en Streamlit para mantener la cuadrícula activa
if (
    "grid" not in st.session_state
    or st.session_state.grid.shape != (filas, columnas)
):
  st.session_state.grid = np.random.choice(
      [0, 1], size=(filas, columnas), p=[1 - probabilidad, probabilidad]
  )
  st.session_state.ejecutando = False


# Botones de control
col1, col2, col3 = st.sidebar.columns(3)
if col1.button("▶️ Iniciar"):
  st.session_state.ejecutando = True
if col2.button("⏸️ Pausar"):
  st.session_state.ejecutando = False
if col3.button("🔄 Reiniciar"):
  st.session_state.grid = np.random.choice(
      [0, 1], size=(filas, columnas), p=[1 - probabilidad, probabilidad]
  )
  st.session_state.ejecutando = False

# Contenedor para mostrar la cuadrícula de forma gráfica
espacio_visualizador = st.empty()

# Bucle de animación si está activo
placeholder_estado = st.sidebar.empty()

if st.session_state.ejecutando:
  placeholder_estado.warning("Simulación en ejecución...")
  while st.session_state.ejecutando:
    # Actualizar la matriz
    st.session_state.grid = actualizar_grid(st.session_state.grid)

    # Mostrar la matriz de forma visual (reemplazando ceros y unos con emojis o bloques)
    imagen_visual = np.where(st.session_state.grid == 1, "⬛", "⬜")
    espacio_visualizador.markdown(
        "\n".join(["".join(fila) for fila in imagen_visual])
    )

    time.sleep(velocidad)
    st.rerun()
else:
  placeholder_estado.info("Simulación pausada o detenida.")
  imagen_visual = np.where(st.session_state.grid == 1, "⬛", "⬜")
  espacio_visualizador.markdown(
      "\n".join(["".join(fila) for fila in imagen_visual])
  )