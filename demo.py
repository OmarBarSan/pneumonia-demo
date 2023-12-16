import streamlit as st
import time
from stfuncs import presentacion, prediciones
if __name__ == '__main__':
    placeholder = st.empty()
    placeholder.title("Demo Clasificación de Neumonia")
    placeholder2 = st.empty()
    sidebar = st.sidebar
    sidebar.header("Menú")
    #container = st.container(border=True)
    menu_options = ["Presentacion", "Predicciones"]
    selection = st.sidebar.radio("Selecciona una opción", menu_options)

    if selection == "Presentacion":#sidebar.button("Presentacion"):
        presentacion(placeholder2)
    if selection == "Predicciones":#sidebar.button("Predicciones"):
        prediciones(placeholder2)

    sidebar.info("Esta demo fue creada por Omar Said Bárcenas Sánchez contacto: omarsbarcenass@outlook.com")