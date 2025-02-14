import openai
import streamlit as st

# Verificar y cargar la clave API de OpenAI
try:
    openai.api_key = st.secrets["openai_api_key"]
except KeyError:
    st.error("Error: No se encontró la clave API de OpenAI. Revisa los secretos en Streamlit Cloud.")
    st.stop()

def main():
    # Título de la aplicación
    st.title("Generador de Juegos de Mesa Personalizados")

    # Descripción de la aplicación
    st.markdown(
        """
        Bienvenido a la aplicación para generar ideas de juegos de mesa personalizados. 
        Ya sea que necesites un juego para una actividad educativa, un evento temático o simplemente algo único para jugar con amigos, esta herramienta está diseñada para ayudarte a crear una experiencia inolvidable.
        """
    )

    # Sección de cómo funciona
    st.subheader("¿Cómo funciona?")
    st.markdown(
        """
        **Características clave de nuestra aplicación:**
        1. **Recopilación de preferencias:** Introduce tus intereses, temática deseada y nivel de complejidad.
        2. **Generación de ideas personalizadas:** Utilizando inteligencia artificial de OpenAI, creamos sugerencias de juegos únicos, incluyendo mecánicas, dinámicas y detalles temáticos.
        3. **Visualización:** Ofrecemos una descripción detallada de la experiencia del juego y generamos imágenes para ilustrar el concepto.
        4. **Resultados inmediatos:** Obtén ideas en cuestión de segundos para empezar a desarrollar tu juego.
        """
    )

    # Formulario para las preferencias del usuario
    st.subheader("Personaliza tu juego de mesa")
    theme = st.text_input("¿Qué temática quieres para tu juego de mesa? (Ejemplo: fantasía, ciencia ficción, historia)")
    player_count = st.number_input("¿Para cuántos jugadores será el juego?", min_value=1, step=1)
    complexity = st.selectbox(
        "¿Qué nivel de complejidad prefieres?", 
        ["Baja (fácil y rápido)", "Media (equilibrado)", "Alta (estrategia profunda)"]
    )

    # Botón para generar ideas
    if st.button("Generar idea de juego"):
        if theme:
            try:
                game_idea = generate_game_idea(theme, player_count, complexity)
                st.success("¡Aquí tienes una idea para tu juego de mesa!")
                st.markdown(f"**Nombre del juego:** {game_idea['name']}")
                st.markdown(f"**Descripción:** {game_idea['description']}")
                st.markdown(f"**Mecánica principal:** {game_idea['mechanic']}")
                st.markdown(f"**Número de jugadores:** {player_count}")
                st.markdown(f"**Nivel de complejidad:** {complexity}")
            except Exception as e:
                st.error(f"Error al generar la idea de juego: {e}")
        else:
            st.error("Por favor, completa la temática para generar una idea.")

# Función para generar ideas de juegos de mesa utilizando OpenAI
def generate_game_idea(theme, player_count, complexity):
    # Crear el prompt para OpenAI
    prompt = f"""
    Crea una idea de juego de mesa basado en los siguientes parámetros:
    - Temática: {theme}
    - Número de jugadores: {player_count}
    - Nivel de complejidad: {complexity}
    
    Incluye un nombre del juego, descripción, mecánicas principales y otras ideas importantes.
    """

    # Llamada a la API de OpenAI (actualización para la nueva versión)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Usa el modelo de chat más reciente de OpenAI
            messages=[
                {"role": "system", "content": "Eres un asistente útil para generar ideas de juegos de mesa."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=150,  # Limita la cantidad de tokens
            temperature=0.7,  # Controla la creatividad de la respuesta
        )
    except Exception as e:
        raise Exception(f"Error con la API de OpenAI: {e}")

    # Extraer el resultado
    game_idea = response['choices'][0]['message']['content'].strip().split("\n")
    
    if len(game_idea) < 3:
        raise ValueError("La respuesta de OpenAI no es válida. Asegúrate de que el prompt esté bien formado.")
    
    # Parsear la respuesta en un formato estructurado
    name = game_idea[0].replace("Nombre:", "").strip()
    description = game_idea[1].replace("Descripción:", "").strip()
    mechanic = game_idea[2].replace("Mecánica principal:", "").strip()
    
    return {
        "name": name,
        "description": description,
        "mechanic": mechanic
    }

if __name__ == "__main__":
    main()
