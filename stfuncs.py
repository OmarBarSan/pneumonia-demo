import streamlit as st
import requests
# from cv2 import imencode
import io
import base64
from PIL import Image
import numpy as np
from modelo.model import create_model, make_prediction

def presentacion(placeholder):
    #with placeholder.container():
    placeholder.header("Presentación", divider="green")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Definición", "Objetivos", "Metodologia", "Resultados", "Futuro"])

    with tab1:#Definicion
        st.subheader("Diagnosticos tardados")
        st.text(
"""En la actualidad el tiempo requerido por un especialista para realizar analisis
de una radiografía para identificar neumonia es de 20 minutos.""")
        st.text(
"""Aunque considerando la carga de trabajo y el hecho de que los pacientes
deberan agendar cita hasta tener un resultado,
este tiempo aumenta y en los casos donde el resultado es positivo,
este tiempo puede significar la posibilidad de salvar una vida.""")
        #st.text("este tiempo aumenta y en los casos donde el resultado es positivo,")
        #st.text("este tiempo puede significar la posibilidad de salvar una vida.")
        st.image("imagenes/person1_bacteria_1.jpeg", width=600)

        st.subheader("Complicación en pocos días")
        st.text(
"""El tiempo medio desde los primeros síntomas
hasta el inicio de la disnea es de 5-8 días.""")
        st.image("imagenes/evolucion.jpeg", width=600)

        st.subheader("La propuesta")
        st.text(
"""Generar un sistema de consulta rapida que advierta a los medicos
desde la toma de radiografía que no se limite a informar entre Normal y Neumonia.""")

    with tab2:#Objetivos
        st.subheader("Creación de API de consultas")
        st.text("Realizar clasificación de 3 categorias:")
        col1,col2,col3 =st.columns(3)
        with col1:
            st.text("* Normal")
            st.image("imagenes/normal.jpeg", width=200)
        with col2:
            st.text("* Bacteria")
            st.image("imagenes/bacteria.jpeg", width=200)
        with col3:
            st.text("* Virus")
            st.image("imagenes/virus.jpeg", width=200)

        st.subheader("Alcance actual")
        st.text("* Complicaciones con procesamiento")
        st.text("* Se entrena el modelo solo con 600 imagenes")
        st.text("* Precision del 76 %")

        st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

    with tab3:#Metodología
        st.subheader("Datos usados")
        st.text("* 600 imagenes")
        st.image("imagenes/distribucion_datos.png", width=500)

        st.subheader("Procesamiento de las imagenes")
        st.text("* Ajuste de dimensiones")
        st.text("* Ecualización del histograma")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Relleno de la imagen")
            st.image("imagenes/bacteria.png", width=350)
        with col2:
            st.subheader("Reescalado a 1024 x 1024 pixel")
            st.image("imagenes/reescalado.jpg", width=350)

        st.subheader("Ecualización de imagenes")
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Imagen original")
            st.image("imagenes/bacteria.png", width=400)

        with col2:
            st.subheader("Imagen ecualizada")
            st.image("imagenes/bacteria_eq.png", width=400)
        
        st.subheader("Red Neuronal Convolucional (CNN)")
        st.text("* 3 capas convolucionales")
        st.text("* 3 capas de reducción de dimensionalidad")
        st.text("* 1 capa de aplanado")
        st.text("* 1 capa densa")
        st.text("* 1 capa de salida de categorias")
    
    with tab4:#Resultados
        st.subheader("Precisión")
        st.text("* Precisión 76% en el conjunto de pruebas.")
        st.image("imagenes/graficas_de_entrenamiento.png", width=600)

        st.subheader("Matriz de confusión")
        st.image("imagenes/matriz_confusion.png", width=600)
    
    with tab5:#Proximas acciones
        st.subheader("Siguientes fases")
        st.text("* Pruebas de augmentación de datos en un entrenamiento.")
        st.text("* Reentrenar con los datos restantes por partes.")
        st.text("* Mejorar la API para introducir lotes de imagenes.")
        st.write("Gracias a todos por su atención :pray:")

def prediciones(placeholder):
    #with placeholder.container():
    #placeholder.empty()
    #time.sleep(0.5)
    placeholder.title("Predicciones")
    uploaded_file = st.file_uploader("Elige una imagen :floppy_disk:")
    if uploaded_file is not None:
        print(f"uploaded {type(uploaded_file)}")
        print(f"uploaded {uploaded_file.__dict__}")
        st.image(uploaded_file, caption=f'{uploaded_file.name}')
        #st.button("Realiza prediccion", on_click=predice, args=[uploaded_file,])
        if st.button("Realiza prediccion"):
            predice(uploaded_file)

def make_request(image):
    st.text("haciendo request")
    # Request parameters
    url = "http://0.0.0.0:8000/predict"
    headers = {'Content-Type': 'image/jpeg'}
    headers = {'Content-Type': 'application/octet-stream'}
    #payload = {'date': date, 'hour': hour, 'imperfection_type': imperfection_id, 'machine': self._machine_id}
    # Sending request
    #bytes_data = imencode('.jpeg', image)[1]
    #bytes_image = io.BytesIO(image)
    bytes_data = image.getvalue()
    print(f"bytes_data {type(image.getvalue())}")
    img_bytes = io.BytesIO(bytes_data)
    # file=image.name;type=image/jpeg'
    #files = [('images', (image.name, bytes_data, 'image/jpeg'))]
    ##response = requests.post(url=url, headers=headers, data=bytes_data)
    #files = {"file": image}
    files = {"file": (image.name, img_bytes, "multipart/form-data")}
    #response = requests.post(url, files=files)
    encoded_image = base64.b64encode(bytes_data).decode('utf-8') 

    # Enviar la imagen a la API
    headers = {'Content-Type': 'application/json'}
    data = {'image': encoded_image}
    response = requests.post(url, json=data, headers=headers)
    st.write(response)

path = "pesos/model.h5"
model = create_model(path)
def predice(image):
    image = Image.open(io.BytesIO(image.getvalue()))
    image = np.array(image)
    result = make_prediction(model, image)
    st.subheader(f"Resultado: {result}")
