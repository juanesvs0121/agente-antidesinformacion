import re

import streamlit as st

from src.agente import verificar


# ==========================================================
# CONFIGURACIÓN
# ==========================================================

NOMBRE_APP = "Dizque"
MAX_MB = 10
TIPOS_IMAGEN = ["png", "jpg", "jpeg", "webp"]
MAX_CARACTERES = 3000

st.set_page_config(
    page_title=f"{NOMBRE_APP} — Verificación",
    page_icon="◈",
    layout="centered",
    initial_sidebar_state="expanded"
)


# ==========================================================
# ESTADO DE LA CONVERSACIÓN
# ==========================================================

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []


# ==========================================================
# ESTILOS
# ==========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600;700&family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600;6..72,700&display=swap');

:root {
    --paper: #EDF1F7;
    --paper-light: #FBFCFE;
    --ink: #0F1B33;
    --body: #2A3650;
    --muted: #5B6679;
    --line: #D3DAE6;
    --accent: #2B4FD8;
    --accent-dark: #1E3799;
    --accent-soft: #E4EAFB;
    --shadow: 0 2px 10px rgba(15, 27, 51, 0.07);
}

.stApp,
[data-testid="stAppViewContainer"] {
    background-color: var(--paper);
    color: var(--ink);
}

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stToolbar"] {
    display: none;
}

#MainMenu,
footer {
    visibility: hidden;
}

.block-container {
    max-width: 900px;
    padding-top: 2rem;
    padding-bottom: 7rem;
}


/* ---------------- SIDEBAR ---------------- */

[data-testid="stSidebar"] {
    background-color: #E2E8F2;
    border-right: 1px solid var(--line);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 2rem;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] li {
    color: var(--body);
    font-size: 0.91rem;
    line-height: 1.65;
}

[data-testid="stSidebar"] strong {
    color: var(--ink);
}

.side-wordmark {
    font-family: 'Newsreader', serif;
    font-size: 2rem;
    font-weight: 700;
    letter-spacing: -1.5px;
    color: var(--ink);
}

.side-wordmark span {
    color: var(--accent);
}

.side-eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 1px;
    color: var(--muted);
    margin-bottom: 1.1rem;
}

.side-section {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.66rem;
    letter-spacing: 1px;
    color: var(--accent-dark);
    margin-top: 1.5rem;
    margin-bottom: 0.6rem;
    border-bottom: 1px solid #C3CCDD;
    padding-bottom: 0.5rem;
}

.side-note {
    font-size: 0.8rem;
    line-height: 1.6;
    color: var(--body);
    background: var(--accent-soft);
    border-left: 3px solid var(--accent);
    border-radius: 0 8px 8px 0;
    padding: 0.8rem 0.9rem;
    margin-top: 1rem;
}


/* ---------------- BOTONES ---------------- */

.stButton > button {
    border-radius: 10px;
    border: 1px solid var(--accent);
    background: var(--accent);
    color: #FFFFFF;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.76rem;
    letter-spacing: 0.3px;
    padding: 0.65rem 1rem;
    box-shadow: var(--shadow);
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: var(--accent-dark);
    border-color: var(--accent-dark);
    color: #FFFFFF;
    transform: translateY(-1px);
}

.stButton > button:active {
    transform: translateY(0);
}


/* ---------------- CABECERA ---------------- */

.topline {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    flex-wrap: wrap;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 1px;
    color: var(--muted);
    padding-bottom: 0.85rem;
    border-bottom: 1px solid var(--line);
}

.masthead {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 0 0.9rem;
    border-bottom: 3px double #A9B4C8;
}

.wordmark {
    font-family: 'Newsreader', serif;
    font-size: 2.55rem;
    line-height: 1;
    letter-spacing: -2px;
    font-weight: 700;
    color: var(--ink);
}

.wordmark-dot {
    color: var(--accent);
}

.masthead-note {
    font-family: 'IBM Plex Mono', monospace;
    color: var(--muted);
    font-size: 0.62rem;
    letter-spacing: 1px;
    text-align: right;
}


/* ---------------- HERO ---------------- */

.hero {
    padding: 2.6rem 0 2rem;
}

.hero-kicker {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 1px;
    color: var(--accent);
    margin-bottom: 1rem;
}

.hero h1 {
    color: var(--ink);
    font-family: 'Newsreader', serif;
    font-size: clamp(2.8rem, 7vw, 4.8rem);
    font-weight: 500;
    letter-spacing: -2.8px;
    line-height: 0.99;
    margin: 0;
    padding: 0;
}

.hero h1 em {
    font-weight: 400;
    color: var(--accent);
}

.hero-description {
    color: var(--muted);
    font-size: 1rem;
    line-height: 1.7;
    max-width: 550px;
    margin-top: 1.3rem;
}


/* ---------------- GUÍA INICIAL ---------------- */

.welcome-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 1px;
    color: var(--muted);
    border-bottom: 1px solid var(--line);
    padding-bottom: 0.7rem;
    margin-bottom: 0.9rem;
}

.welcome-item {
    background: var(--paper-light);
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 1.1rem 1.1rem 1.2rem;
    height: 100%;
    box-shadow: var(--shadow);
}

.welcome-number {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: var(--accent);
    margin-bottom: 0.6rem;
}

.welcome-title {
    font-family: 'Newsreader', serif;
    font-size: 1.25rem;
    color: var(--ink);
    margin-bottom: 0.3rem;
}

.welcome-description {
    font-size: 0.82rem;
    color: var(--muted);
    line-height: 1.55;
}


/* ---------------- CONVERSACIÓN ---------------- */

[data-testid="stChatMessage"] {
    background: var(--paper-light);
    border: 1px solid var(--line);
    border-left: 4px solid var(--accent);
    border-radius: 14px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 1rem;
    box-shadow: var(--shadow);
}

/* Mensaje del usuario: tono distinto para diferenciarlo */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    background: var(--accent-soft);
    border-left-color: var(--accent-dark);
}

/* Color explícito del texto: evita el gris claro heredado del tema oscuro */
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] span,
[data-testid="stChatMessage"] strong,
[data-testid="stChatMessage"] em,
[data-testid="stChatMessage"] h1,
[data-testid="stChatMessage"] h2,
[data-testid="stChatMessage"] h3,
[data-testid="stChatMessage"] td,
[data-testid="stChatMessage"] th {
    color: var(--ink);
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li {
    font-size: 0.97rem;
    line-height: 1.7;
}

[data-testid="stChatMessage"] a {
    color: var(--accent-dark);
    text-decoration: underline;
    text-underline-offset: 2px;
    word-break: break-word;
}

[data-testid="stChatMessage"] code {
    color: var(--accent-dark);
    background: var(--accent-soft);
    border-radius: 4px;
    padding: 0.1rem 0.35rem;
}

[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p {
    color: var(--muted);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
}

[data-testid="stChatMessage"] img {
    border: 1px solid var(--line);
    border-radius: 10px;
}

.message-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.63rem;
    letter-spacing: 1px;
    color: var(--accent-dark);
    font-weight: 500;
    margin-bottom: 0.6rem;
}

.badge {
    display: inline-block;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    padding: 0.4rem 0.8rem;
    border-radius: 999px;
    margin-bottom: 0.8rem;
}


/* ---------------- ÁREA DE TEXTO ---------------- */

[data-testid="stChatInput"],
[data-testid="stChatInput"] > div {
    background: var(--paper-light);
    border-radius: 14px;
}

[data-testid="stChatInput"] {
    border: 1px solid #B8C3D6;
    box-shadow: 0 4px 16px rgba(15, 27, 51, 0.10);
}

[data-testid="stChatInput"]:focus-within {
    border-color: var(--accent);
    box-shadow: 0 0 0 3px rgba(43, 79, 216, 0.18);
}

[data-testid="stChatInput"] textarea {
    background: transparent;
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 0.95rem;
    color: var(--ink);
    caret-color: var(--accent);
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #6B7588;
    opacity: 1;
}

[data-testid="stChatInput"] button {
    color: var(--accent);
}


/* ---------------- IMÁGENES Y ELEMENTOS ---------------- */

[data-testid="stImage"] {
    margin-top: 0.4rem;
    margin-bottom: 0.5rem;
}

hr {
    border-color: var(--line);
}

[data-testid="stSpinner"] p {
    color: var(--body);
}

div[data-testid="stSpinner"] > div {
    border-top-color: var(--accent) !important;
}

[data-testid="stAlert"] p {
    color: var(--ink);
}


/* ---------------- RESPONSIVE ---------------- */

@media (max-width: 600px) {

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
        padding-top: 1rem;
    }

    .wordmark {
        font-size: 2.1rem;
    }

    .masthead-note {
        max-width: 120px;
        font-size: 0.55rem;
    }

    .hero {
        padding-top: 2rem;
    }

    .hero h1 {
        letter-spacing: -1.5px;
    }

}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# BARRA LATERAL
# ==========================================================

with st.sidebar:

    st.markdown(
        '<div class="side-wordmark">dizque<span>.</span></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="side-eyebrow">OBSERVATORIO DIGITAL / COLOMBIA</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        Una herramienta para cuestionar lo que circula,
        contrastar afirmaciones y examinar contenido visual.
        """
    )

    st.markdown('<div class="side-section">CÓMO FUNCIONA</div>',
                unsafe_allow_html=True)

    st.markdown(
        """
        **01 / Consulta**

        Escribe una afirmación, pega una noticia o adjunta una captura.

        **02 / Análisis**

        El sistema examina el contenido visual y busca verificaciones
        y fuentes disponibles.

        **03 / Contraste**

        Recibirás un análisis con los elementos encontrados y sus
        respectivas limitaciones.
        """
    )

    st.markdown('<div class="side-section">ANTES DE EMPEZAR</div>',
                unsafe_allow_html=True)

    st.markdown(
        """
        - Puedes enviar texto e imágenes al mismo tiempo.
        - Formatos admitidos: PNG, JPG y WEBP.
        - Tamaño máximo: 10 MB.
        """
    )

    st.markdown(
        """
        <div class="side-note">
        El análisis de una imagen no demuestra por sí solo
        su autenticidad. Una captura puede contener información
        manipulada o sacada de contexto.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    if st.button("＋ Nueva conversación", use_container_width=True):
        st.session_state.mensajes = []
        st.rerun()

    st.markdown(
        """
        <div class="side-eyebrow" style="margin-top: 1.5rem;">
        UNA HERRAMIENTA PARA PENSAR ANTES DE COMPARTIR.
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# CABECERA PRINCIPAL
# ==========================================================

st.markdown(
    """
    <div class="topline">
        <span>OBSERVATORIO DIGITAL / COLOMBIA</span>
        <span>VERIFICACIÓN DE INFORMACIÓN · BETA</span>
    </div>

    <div class="masthead">
        <div class="wordmark">
            dizque<span class="wordmark-dot">.</span>
        </div>
        <div class="masthead-note">
            INFORMACIÓN<br>BAJO LA LUPA
        </div>
    </div>

    <div class="hero">
        <div class="hero-kicker">
            01 / VERIFICACIÓN DE INFORMACIÓN
        </div>

        <h1>
            Antes de creerlo,<br>
            <em>ponlo a prueba.</em>
        </h1>

        <div class="hero-description">
            Una afirmación, una captura o ambas.
            Examina lo que estás viendo y descubre qué hay
            detrás de la información que circula.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ==========================================================
# PANTALLA DE BIENVENIDA
# ==========================================================

if not st.session_state.mensajes:

    st.markdown(
        '<div class="welcome-label">PUEDES EMPEZAR CON</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        st.markdown(
            """
            <div class="welcome-item">
                <div class="welcome-number">01 / TEXTO</div>
                <div class="welcome-title">Una afirmación</div>
                <div class="welcome-description">
                    Una noticia, una declaración o un mensaje
                    que quieras contrastar.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="welcome-item">
                <div class="welcome-number">02 / IMAGEN</div>
                <div class="welcome-title">Una captura</div>
                <div class="welcome-description">
                    Titulares, publicaciones, fotografías
                    o mensajes reenviados.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div class="welcome-item">
                <div class="welcome-number">03 / MIXTO</div>
                <div class="welcome-title">Ambos</div>
                <div class="welcome-description">
                    Una imagen acompañada de la afirmación
                    que deseas verificar.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)


# ==========================================================
# FUNCIÓN PARA MOSTRAR RESPUESTAS
# ==========================================================

COLORES_VEREDICTO = {
    "respaldada": ("#DDF3E8", "#0B5D3B"),
    "falsa": ("#FBE3E3", "#9B1C1C"),
    "engañosa": ("#FDEBD0", "#8A4B08"),
    "parcialmente cierta": ("#FCF1C8", "#7A5A00"),
    "no verificable": ("#E3E8F1", "#34405A"),
}


def mostrar_respuesta(contenido: str):
    """
    Muestra la respuesta del agente: etiqueta de veredicto, cuerpo
    y contador de tokens como información secundaria.
    """

    cuerpo, separador, pie = contenido.partition("\n\n[Tokens")

    coincidencia = re.search(r"\*\*Veredicto:\*\*\s*([^\n]+)", cuerpo)

    if coincidencia:
        veredicto = coincidencia.group(1).replace("*", "").strip()
        clave = next(
            (k for k in COLORES_VEREDICTO if veredicto.lower().startswith(k)),
            None,
        )
        fondo, color = COLORES_VEREDICTO.get(clave, ("#E3E8F1", "#34405A"))
        st.markdown(
            f'<div class="badge" style="background:{fondo};color:{color};">'
            f"{veredicto}</div>",
            unsafe_allow_html=True,
        )

    st.markdown(cuerpo)

    if separador:
        st.caption("[Tokens" + pie)


# ==========================================================
# HISTORIAL DE CONVERSACIÓN
# ==========================================================

for mensaje in st.session_state.mensajes:

    if mensaje["rol"] == "user":

        with st.chat_message("user", avatar="🗣️"):

            st.markdown(
                '<div class="message-label">TU CONSULTA</div>',
                unsafe_allow_html=True
            )

            if mensaje.get("imagen"):
                st.image(mensaje["imagen"], width=350)

            if mensaje["contenido"]:
                st.markdown(mensaje["contenido"])

    elif mensaje["rol"] == "assistant":

        with st.chat_message("assistant", avatar="🔎"):

            st.markdown(
                '<div class="message-label">ANÁLISIS / RESULTADO</div>',
                unsafe_allow_html=True
            )

            mostrar_respuesta(mensaje["contenido"])


# ==========================================================
# ENTRADA DEL USUARIO
# ==========================================================

entrada = st.chat_input(
    "Escribe una afirmación o adjunta una imagen...",
    accept_file=True,
    file_type=TIPOS_IMAGEN,
)


# ==========================================================
# PROCESAMIENTO DE LA CONSULTA
# ==========================================================

if entrada:

    texto = (entrada.text or "").strip()
    archivos = entrada.files or []

    imagen_bytes = None
    nombre_imagen = None

    # Obtener imagen adjunta
    if archivos:

        archivo = archivos[0]

        imagen_bytes = archivo.getvalue()
        nombre_imagen = archivo.name

        # Comprobar tamaño
        if len(imagen_bytes) > MAX_MB * 1024 * 1024:

            st.error(
                f"La imagen supera los {MAX_MB} MB. "
                "Adjunte una imagen más liviana."
            )

            st.stop()

    # Comprobar que exista contenido
    if not texto and not imagen_bytes:

        st.warning("Escribe una afirmación o adjunta una imagen.")

        st.stop()

    # Limitar longitud del texto
    if len(texto) > MAX_CARACTERES:

        st.warning(
            f"El texto supera los {MAX_CARACTERES} caracteres. "
            "Se analizarán únicamente los primeros "
            f"{MAX_CARACTERES}."
        )

        texto = texto[:MAX_CARACTERES]

    # Guardar consulta del usuario
    st.session_state.mensajes.append(
        {
            "rol": "user",
            "contenido": texto,
            "imagen": imagen_bytes,
            "nombre_imagen": nombre_imagen
        }
    )

    # Mostrar consulta
    with st.chat_message("user", avatar="🗣️"):

        st.markdown(
            '<div class="message-label">TU CONSULTA</div>',
            unsafe_allow_html=True
        )

        if imagen_bytes:
            st.image(imagen_bytes, width=350)

        if texto:
            st.markdown(texto)

    # Ejecutar agente
    with st.chat_message("assistant", avatar="🔎"):

        st.markdown(
            '<div class="message-label">ANÁLISIS / RESULTADO</div>',
            unsafe_allow_html=True
        )

        with st.spinner(
            "Examinando el contenido y contrastando información..."
        ):

            try:

                respuesta = verificar(
                    texto,
                    imagen_bytes=imagen_bytes
                )

            except Exception as e:

                respuesta = (
                    f"Ocurrió un error inesperado durante el análisis: {e}"
                )

        mostrar_respuesta(respuesta)

    # Guardar respuesta
    st.session_state.mensajes.append(
        {
            "rol": "assistant",
            "contenido": respuesta
        }
    )
