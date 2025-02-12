import streamlit as st
import openai
import pandas as pd

# Clave de API de OpenAI (reemplaza con tu clave)
openai.api_key = "TU_CLAVE_DE_API"

# Base de datos de juegos de mesa (ejemplo en CSV)
df_juegos = pd.read_csv("juegos_mesa.csv")

def obtener_sugerencia(prompt):
    respuesta = openai.Completion.create(
        engine="text-davinci-003",  # Puedes ajustar el modelo
        prompt=prompt,
        max_tokens=150,  # Ajusta la longitud de la respuesta
        n=1,
        stop=None,
        temperature=0.7,  # Ajusta la creatividad de la respuesta
    )
    return respuesta.choices[0].text.strip()

def buscar_juegos(criterios):
    # Aquí va la lógica para buscar juegos en df_juegos según los criterios
    # ... (implementa la búsqueda según tus necesidades)
    return juegos_encontrados

st.title("Sugerencias Lúdicas: Tu Bot Experto en Juegos de Mesa")

prompt = st.text_input("Ingresa tu prompt:")

if st.button("Obtener Sugerencia"):
    sugerencia = obtener_sugerencia(prompt)
    st.write(sugerencia)

    juegos_encontrados = buscar_juegos(prompt)
    if juegos_encontrados:
        st.write("Juegos Encontrados:")
        st.dataframe(juegos_encontrados)
