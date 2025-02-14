import openai
import streamlit as st

# Verificar y cargar la clave API de OpenAI
try:
    openai.api_key = st.secrets["openai_api_key"]
except KeyError:
    st.error("Error: No se encontró la clave API de OpenAI. Revisa los secretos en Streamlit Cloud.")
    st.stop()

# Función para generar ideas de juegos de mesa
def generate_game_idea(theme, player_count, complexity):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Eres un experto en creación de juegos de mesa. "
                        "Ayuda a los usuarios a generar ideas personalizadas de juegos de mesa."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Quiero un juego de mesa con la temática '{theme}', "
                        f"para {player_count} jugadores, con un nivel de complejidad '{complexity}'. "
                        "Por favor, describe la mecánica, el objetivo y una idea única para el juego."
                    ),
                },
            ],
            max_tokens=500,
            temperature=0.7,
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        st.error(f"Error al generar la idea de juego: {e}")
        return None

# Interfaz de usuario con Streamlit
def main():
    st.title("Generador de Juegos de Mesa Personalizados")
    st.markdown(
        """
        Bienvenido a la aplicación para generar ideas de juegos de mesa personalizados. 
        Introduce tus preferencias y deja que la inteligencia artificial cree un juego para ti.
        """
    )

    # Entradas del usuario
    theme = st.text_input("¿Qué temática quieres para tu juego de mesa? (Ejemplo: fantasía, ciencia ficción, historia)")
    player_count = st.number_input("¿Para cuántos jugadores será el juego?", min_value=1, step=1)
    complexity = st.selectbox(
        "¿Qué nivel de complejidad prefieres?",
        ["Baja (fácil y rápido)", "Media (equilibrado)", "Alta (estrategia profunda)"]
    )

    # Botón para generar la idea
    if st.button("Generar idea de juego"):
        if theme:
            idea = generate_game_idea(theme, player_count, complexity)
            if idea:
                st.success("¡Idea de juego generada con éxito!")
                st.markdown(idea)
        else:
            st.error("Por favor, introduce una temática para generar la idea.")

if __name__ == "__main__":
    main()
