import openai
import streamlit as st

# Configuración de la clave API de OpenAI
openai.api_key = st.secrets["openai_api_key"]  # Asegúrate de que "openai_api_key" esté configurado en Streamlit Cloud

def generate_game_idea(theme, player_count, complexity):
    try:
        # Usar la nueva API de ChatCompletion
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # O usa "gpt-4" si tienes acceso
            messages=[
                {"role": "system", "content": "Eres un experto en diseño de juegos de mesa."},
                {"role": "user", "content": f"Por favor, genera una idea para un juego de mesa con la temática '{theme}', para {player_count} jugadores y con un nivel de complejidad '{complexity}'."}
            ],
            max_tokens=300,
            temperature=0.7
        )
        # Extraer el texto generado
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error al generar la idea de juego: {str(e)}"

# Interfaz de Streamlit
def main():
    st.title("Generador de Juegos de Mesa Personalizados")

    st.markdown(
        """
        Bienvenido a la aplicación para generar ideas de juegos de mesa personalizados.
        """
    )

    st.subheader("Personaliza tu juego de mesa")
    theme = st.text_input("¿Qué temática quieres para tu juego de mesa? (Ejemplo: fantasía, ciencia ficción, historia)")
    player_count = st.number_input("¿Para cuántos jugadores será el juego?", min_value=1, step=1)
    complexity = st.selectbox(
        "¿Qué nivel de complejidad prefieres?",
        ["Baja (fácil y rápido)", "Media (equilibrado)", "Alta (estrategia profunda)"]
    )

    if st.button("Generar idea de juego"):
        if theme:
            idea = generate_game_idea(theme, player_count, complexity)
            st.markdown(f"**Idea de juego generada:** {idea}")
        else:
            st.error("Por favor, completa la temática para generar una idea.")

if __name__ == "__main__":
    main()
