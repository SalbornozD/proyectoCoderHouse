import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Configuración inicial
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def consultar_tutor_ia(pregunta: str, estilo: str) -> str:
    """
    Realiza la consulta a la API de OpenAI y devuelve la respuesta.
    """
    prompt = f"""
Actúa como un tutor educativo. Explica el siguiente tema según el estilo de aprendizaje "{estilo}".
Adapta la respuesta para que sea clara, didáctica y comprensible para un estudiante.

Tema: {pregunta}
    """

    try:
        respuesta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un tutor paciente y claro, que adapta sus explicaciones según el estilo de aprendizaje del estudiante."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return respuesta["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error al generar la respuesta: {e}"


# Streamlit UI
st.set_page_config(page_title="Tutor-IA", page_icon="📚")
st.title("📚 Tutor-IA: Tu tutor personalizado con IA")

st.markdown("""
Tutor-IA es una aplicación educativa que adapta sus explicaciones según tu forma de aprender.
Puedes contestar un cuestionario o elegir tu estilo manualmente.
""")

# Estilo de aprendizaje
st.subheader("🎛 Configura tu estilo de aprendizaje")
modo_auto = st.toggle("¿Quieres detectar tu estilo automáticamente con un cuestionario?")

if "estilo" not in st.session_state:
    st.session_state["estilo"] = "Textual"

if modo_auto:
    with st.form("formulario_estilo"):
        q1 = st.radio("¿Cómo prefieres aprender algo nuevo?", [
            "Viendo imágenes o diagramas",
            "Escuchando explicaciones",
            "Leyendo o escribiendo sobre el tema"
        ])

        q2 = st.radio("¿Qué te resulta más fácil recordar?", [
            "Mapas, gráficos o colores",
            "Lo que escuchas",
            "Lo que lees o escribes"
        ])

        q3 = st.radio("En una clase ideal, preferirías...", [
            "Ver presentaciones o dibujos",
            "Escuchar podcasts o charlas",
            "Leer textos o tomar apuntes"
        ])

        submit = st.form_submit_button("Detectar mi estilo")

        if submit:
            respuestas = [q1, q2, q3]

            visual = sum(any(p in r.lower() for p in ["ver", "imagen", "mapa", "presentación", "diagrama", "visual"]) for r in respuestas)
            auditivo = sum(any(p in r.lower() for p in ["escuchar", "explicación", "hablado", "podcast", "charla", "auditivo"]) for r in respuestas)
            textual = sum(any(p in r.lower() for p in ["leer", "escribir", "texto", "apunte", "lectura"]) for r in respuestas)

            if visual >= 2:
                estilo = "Visual"
            elif auditivo >= 2:
                estilo = "Auditivo"
            else:
                estilo = "Textual"

            st.session_state["estilo"] = estilo
            st.success(f"Estilo detectado: {estilo}")
else:
    estilo_manual = st.selectbox("Selecciona tu estilo de aprendizaje:", ["Visual", "Auditivo", "Textual"])
    st.session_state["estilo"] = estilo_manual
    st.info(f"Estilo actual: {estilo_manual}")

# Chatbot
st.subheader("💬 Haz tu consulta a Tutor-IA")
pregunta = st.text_input("Escribe tu duda o tema que quieras entender mejor:")

if st.button("Consultar"):
    if not pregunta.strip():
        st.warning("Por favor, escribe una pregunta.")
    else:
        estilo = st.session_state["estilo"]
        respuesta = consultar_tutor_ia(pregunta, estilo)

        st.markdown("🧠 Respuesta del Tutor-IA:")
        st.info(respuesta)

# Pie de página
st.markdown("---")
st.caption("Aplicación desarrollada por Sebastián Albornoz – Proyecto")
