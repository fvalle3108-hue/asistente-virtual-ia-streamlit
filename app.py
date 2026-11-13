"""
Asistente Virtual de la Clase
-----------------------------
Aplicación web hecha con Streamlit que se conecta al modelo
openai/gpt-oss-20b a través de la API de Groq.

Ejecución local:  streamlit run app.py
"""

import streamlit as st
from groq import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    Groq,
    RateLimitError,
)

# ---------------------------------------------------------------------------
# Configuración general
# ---------------------------------------------------------------------------
MODELO = "openai/gpt-oss-20b"
NOMBRE_SECRETO = "LLAVE_PROFESOR"
MENSAJE_SISTEMA = (
    "Eres el 'Asistente Virtual de la Clase', un asistente académico amable, "
    "claro y preciso. Responde siempre en español, explica los conceptos paso "
    "a paso cuando sea útil y usa ejemplos sencillos. Si no sabes algo, "
    "reconócelo con honestidad en lugar de inventar información."
)
MENSAJE_BIENVENIDA = (
    "¡Hola! Soy el Asistente Virtual de la Clase. "
    "Escribe tu pregunta y con gusto te ayudaré."
)

st.set_page_config(
    page_title="Asistente Virtual de la Clase",
    page_icon="🎓",
    layout="centered",
)


# ---------------------------------------------------------------------------
# Funciones auxiliares
# ---------------------------------------------------------------------------
def obtener_cliente() -> Groq | None:
    """Crea el cliente de Groq leyendo la clave desde st.secrets.

    Devuelve None y muestra un mensaje de error si la configuración es
    incorrecta.
    """
    try:
        clave = st.secrets[NOMBRE_SECRETO]
    except Exception:
        st.error(
            f"⚠️ No se encontró la clave de API `{NOMBRE_SECRETO}`. "
            "Crea el archivo `.streamlit/secrets.toml` (en local) o configura "
            "los *Secrets* en Streamlit Community Cloud. "
            "Consulta el archivo README.md para ver los pasos."
        )
        return None

    clave = str(clave).strip()
    if not clave or clave.startswith("PEGA_AQUI"):
        st.error(
            f"⚠️ La clave `{NOMBRE_SECRETO}` está vacía o aún contiene el "
            "valor de ejemplo. Reemplázala por una clave de API válida de Groq."
        )
        return None

    return Groq(api_key=clave)


def generar_respuesta(cliente: Groq, historial: list[dict]) -> str:
    """Envía el historial completo al modelo y devuelve el texto generado."""
    mensajes = [{"role": "system", "content": MENSAJE_SISTEMA}] + historial
    respuesta = cliente.chat.completions.create(
        model=MODELO,
        messages=mensajes,
        temperature=st.session_state.temperatura,
        max_tokens=2048,
    )
    return (respuesta.choices[0].message.content or "").strip()


def reiniciar_conversacion() -> None:
    """Borra el historial de la conversación actual."""
    st.session_state.mensajes = []


# ---------------------------------------------------------------------------
# Estado de la sesión
# ---------------------------------------------------------------------------
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []
if "temperatura" not in st.session_state:
    st.session_state.temperatura = 0.7

# ---------------------------------------------------------------------------
# Barra lateral
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Opciones")
    st.session_state.temperatura = st.slider(
        "Creatividad de las respuestas",
        min_value=0.0,
        max_value=1.5,
        value=st.session_state.temperatura,
        step=0.1,
        help="Valores bajos dan respuestas más precisas; valores altos, "
        "más creativas.",
    )
    st.button(
        "🗑️ Nueva conversación",
        on_click=reiniciar_conversacion,
        use_container_width=True,
    )
    st.caption(f"Modelo: `{MODELO}` (API de Groq)")

# ---------------------------------------------------------------------------
# Interfaz principal
# ---------------------------------------------------------------------------
st.title("🎓 Asistente Virtual de la Clase")
st.caption("Pregunta lo que quieras sobre los temas de la clase.")

cliente = obtener_cliente()

# Mostrar el historial
if not st.session_state.mensajes:
    with st.chat_message("assistant"):
        st.markdown(MENSAJE_BIENVENIDA)

for mensaje in st.session_state.mensajes:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

# Entrada del usuario
pregunta = st.chat_input(
    "Escribe tu pregunta aquí...", disabled=cliente is None
)

if pregunta and cliente is not None:
    st.session_state.mensajes.append({"role": "user", "content": pregunta})
    with st.chat_message("user"):
        st.markdown(pregunta)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Pensando..."):
                texto = generar_respuesta(cliente, st.session_state.mensajes)
            if not texto:
                texto = "No pude generar una respuesta. Intenta reformular tu pregunta."
            st.markdown(texto)
            st.session_state.mensajes.append(
                {"role": "assistant", "content": texto}
            )
        except AuthenticationError:
            st.session_state.mensajes.pop()
            st.error(
                "🔑 La clave de API no es válida o fue revocada. "
                "Verifica el valor de `LLAVE_PROFESOR`."
            )
        except RateLimitError:
            st.session_state.mensajes.pop()
            st.error(
                "⏳ Se alcanzó el límite de solicitudes. "
                "Espera unos segundos e inténtalo de nuevo."
            )
        except (APIConnectionError, APITimeoutError):
            st.session_state.mensajes.pop()
            st.error(
                "🌐 No se pudo conectar con la API de Groq. "
                "Revisa tu conexión a internet e inténtalo otra vez."
            )
        except APIStatusError as error:
            st.session_state.mensajes.pop()
            st.error(
                f"❌ La API devolvió un error (código {error.status_code}). "
                "Inténtalo nuevamente más tarde."
            )
        except Exception as error:  # noqa: BLE001
            st.session_state.mensajes.pop()
            st.error(f"❌ Ocurrió un error inesperado: {error}")
