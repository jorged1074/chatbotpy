"""Interfaz Streamlit de EstáticaBot.

Ejecutar con:
    streamlit run app.py
"""

from __future__ import annotations

import streamlit as st

from bot import ChatBot
from bot.calculators import beam_reactions_point_load, resultant_two_forces

st.set_page_config(
    page_title="EstáticaBot · Estática y Python",
    page_icon="🧮",
    layout="centered",
)

# ---------------------------------------------------------------------------
# Estilos propios (solo detalles visuales; la app funciona sin ellos)
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
        .block-container { padding-top: 1.6rem; padding-bottom: 3rem; max-width: 880px; }
        [data-testid="stChatMessage"] { border-radius: 14px; }
        [data-testid="stSidebar"] .stButton button { text-align: left; }
        .stChatInput { padding-bottom: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

WELCOME = """### 👋 ¡Hola! Soy **EstáticaBot**

Tu asistente de **estática** (mecánica para ingeniería) y **programación básica en Python**.

Puedo explicarte teoría paso a paso, mostrarte fórmulas y darte ejemplos de código. Por ejemplo:

- *¿Cómo hago un diagrama de cuerpo libre?*
- *¿Cómo calculo el momento de una fuerza?*
- *¿Cómo funciona un bucle `for`?*
- *¿Cómo resuelvo un sistema de equilibrio con NumPy?*

Escribe tu pregunta abajo o pulsa una de las sugerencias. 💬
"""

WELCOME_SUGGESTIONS = (
    {"label": "Diagrama de cuerpo libre", "question": "¿Cómo hago un diagrama de cuerpo libre?"},
    {"label": "Momento de una fuerza", "question": "¿Cómo calculo el momento de una fuerza?"},
    {"label": "Bucle for", "question": "¿Cómo funciona el bucle for en Python?"},
    {"label": "NumPy y equilibrio", "question": "¿Cómo resuelvo un sistema de equilibrio con NumPy?"},
)


@st.cache_resource(show_spinner=False)
def get_bot() -> ChatBot:
    """Carga la base de conocimiento una sola vez por proceso."""
    return ChatBot()


BOT = get_bot()


def welcome_message() -> dict:
    return {
        "role": "assistant",
        "content": WELCOME,
        "suggestions": [dict(item) for item in WELCOME_SUGGESTIONS],
    }


if "messages" not in st.session_state:
    st.session_state.messages = [welcome_message()]


# ---------------------------------------------------------------------------
# Acciones
# ---------------------------------------------------------------------------
def queue(question: str) -> None:
    """Guarda una pregunta de un botón para procesarla en el siguiente rerun."""
    st.session_state.pending = question


def respond(question: str) -> None:
    question = " ".join(str(question).split())
    if not question:
        return

    reply = BOT.answer(question)
    st.session_state.messages.append({"role": "user", "content": question})
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": reply.text,
            "topic": reply.topic_title,
            "suggestions": [
                {"label": suggestion.label, "question": suggestion.question}
                for suggestion in reply.suggestions
            ],
        }
    )


def reset_chat() -> None:
    st.session_state.messages = [welcome_message()]
    st.session_state.pop("pending", None)


def transcript() -> str:
    lines: list[str] = ["# Conversación con EstáticaBot", ""]
    for message in st.session_state.messages:
        author = "Tú" if message["role"] == "user" else "EstáticaBot"
        lines.append(f"**{author}:**")
        lines.append("")
        lines.append(message["content"])
        lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Barra lateral
# ---------------------------------------------------------------------------
with st.sidebar:
    st.title("🧮 EstáticaBot")
    st.caption("Estática + Python · 100 % local")

    with st.expander("📚 Explorar temas", expanded=False):
        category = st.selectbox(
            "Categoría",
            ["Todas", *BOT.categories],
            key="topic-category",
        )
        for entry in BOT.entries_by_category(category):
            st.button(
                entry.title,
                key=f"topic-{entry.id}",
                on_click=queue,
                args=(entry.title,),
                use_container_width=True,
            )

    with st.expander("🧮 Calculadora rápida", expanded=False):
        tab_resultant, tab_beam = st.tabs(["Resultante", "Viga"])

        with tab_resultant:
            st.caption("Dos fuerzas concurrentes. Ángulos en grados desde el eje x.")
            f1 = st.number_input("F₁ (N)", min_value=0.0, value=100.0, step=10.0, key="calc-f1")
            a1 = st.number_input("θ₁ (°)", value=0.0, step=15.0, key="calc-a1")
            f2 = st.number_input("F₂ (N)", min_value=0.0, value=100.0, step=10.0, key="calc-f2")
            a2 = st.number_input("θ₂ (°)", value=90.0, step=15.0, key="calc-a2")
            result = resultant_two_forces(f1, a1, f2, a2)
            st.metric("Resultante R", f"{result.r:.2f} N")
            st.caption(
                f"θ = {result.angle:.1f}° · "
                f"Rx = {result.fx:.2f} N · Ry = {result.fy:.2f} N"
            )

        with tab_beam:
            st.caption("Viga simplemente apoyada con carga puntual.")
            span = st.number_input(
                "Luz L (m)", min_value=0.1, value=4.0, step=0.5, key="calc-span"
            )
            distance = st.number_input(
                "Posición de la carga a (m)",
                min_value=0.0,
                value=1.0,
                step=0.5,
                key="calc-distance",
            )
            load = st.number_input(
                "Carga F (N)", min_value=0.0, value=1000.0, step=100.0, key="calc-load"
            )
            try:
                reactions = beam_reactions_point_load(span, distance, load)
            except ValueError as error:
                st.error(str(error))
            else:
                st.metric("R_A", f"{reactions.ra:.2f} N")
                st.metric("R_B", f"{reactions.rb:.2f} N")
                st.caption(f"R_A + R_B = {reactions.ra + reactions.rb:.2f} N")

    st.divider()
    st.download_button(
        "⬇️ Descargar conversación",
        data=transcript(),
        file_name="conversacion_estaticabot.md",
        mime="text/markdown",
        use_container_width=True,
    )
    st.button(
        "🗑️ Limpiar conversación",
        on_click=reset_chat,
        use_container_width=True,
    )
    st.caption(
        "Las respuestas se generan con una base de conocimiento local. "
        "Verifica siempre tus cálculos."
    )


# ---------------------------------------------------------------------------
# Conversación
# ---------------------------------------------------------------------------
if "pending" in st.session_state:
    pending_question = st.session_state.pop("pending")
    respond(pending_question)

st.title("🧮 EstáticaBot")
st.caption(
    "Pregunta sobre **estática** y **programación básica en Python**. "
    "Funciona sin internet y sin claves de API."
)

for index, message in enumerate(st.session_state.messages):
    avatar = "🧮" if message["role"] == "assistant" else None
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

        if message.get("topic"):
            st.caption(f"📚 Tema: {message['topic']}")

        suggestions = message.get("suggestions") or []
        if suggestions:
            st.caption("Sigue explorando:")
            columns = st.columns(min(len(suggestions), 3))
            for position, (column, suggestion) in enumerate(
                zip(columns, suggestions[:3])
            ):
                with column:
                    st.button(
                        suggestion["label"],
                        key=f"suggestion-{index}-{position}",
                        on_click=queue,
                        args=(suggestion["question"],),
                        use_container_width=True,
                        help=suggestion["question"],
                    )

if prompt := st.chat_input("Escribe tu pregunta de estática o Python…"):
    respond(prompt)
    st.rerun()
