
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
    --paper: #F1EFE6;
    --paper-light: #F9F8F2;
    --ink: #202820;
    --muted: #70756A;
    --line: #D4D2C6;
    --accent: #B44A38;
    --accent-dark: #873C30;
    --green: #536C56;
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
    background-color: #E8E6DC;
    border-right: 1px solid var(--line);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 2rem;
}

[data-testid="stSidebar"] p {
    color: #515B50;
    font-size: 0.91rem;
    line-height: 1.65;
}

[data-testid="stSidebar"] h2 {
    font-family: 'Newsreader', serif;
    font-weight: 500;
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
    border-bottom: 1px solid var(--line);
    padding-bottom: 0.5rem;
}

.side-note {
    font-size: 0.8rem;
    line-height: 1.6;
    color: #62685E;
    border-left: 2px solid var(--accent);
    padding-left: 0.8rem;
    margin-top: 1rem;
}


/* ---------------- BOTONES ---------------- */

.stButton > button {
    border-radius: 3px;
    border: 1px solid var(--ink);
    background: var(--ink);
    color: var(--paper-light);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.76rem;
    letter-spacing: 0.3px;
    padding: 0.65rem 1rem;
    transition: 0.2s ease;
}

.stButton > button:hover {
    background: var(--accent);
    border-color: var(--accent);
    color: white;
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
    border-bottom: 3px double #A9A99B;
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
}

.hero h1 em {
    font-weight: 400;
    color: var(--accent);
}

.hero-description {
    color: #64695F;
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
    margin-bottom: 0.7rem;
}

.welcome-item {
    padding: 0.8rem 0.6rem 0.8rem 0;
    border-bottom: 1px solid var(--line);
}

.welcome-number {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: var(--accent);
    margin-bottom: 0.5rem;
}

.welcome-title {
    font-family: 'Newsreader', serif;
    font-size: 1.25rem;
    color: var(--ink);
    margin-bottom: 0.25rem;
}

.welcome-description {
    font-size: 0.79rem;
    color: var(--muted);
    line-height: 1.5;
}


/* ---------------- CONVERSACIÓN ---------------- */

[data-testid="stChatMessage"] {
    background: var(--paper-light);
    border: 1px solid var(--line);
    border-radius: 3px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.85rem;
}

[data-testid="stChatMessage"] p {
    line-height: 1.7;
}

[data-testid="stChatMessage"] img {
    border: 1px solid var(--line);
}

.message-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.63rem;
    letter-spacing: 1px;
    color: var(--accent);
    margin-bottom: 0.5rem;
}


/* ---------------- ÁREA DE TEXTO ---------------- */

[data-testid="stChatInput"] {
    background: var(--paper-light);
    border: 1px solid #BDBBAD;
    border-radius: 3px;
    box-shadow: 0 3px 12px rgba(32, 40, 32, 0.06);
}

[data-testid="stChatInput"] textarea {
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 0.95rem;
    color: var(--ink);
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #929388;
}


/* ---------------- IMÁGENES Y ELEMENTOS ---------------- */

[data-testid="stImage"] {
    margin-top: 0.4rem;
    margin-bottom: 0.5rem;
}

hr {
    border-color: var(--line);
}

div[data-testid="stSpinner"] > div {
    border-top-color: var(--accent) !important;
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

def mostrar_respuesta(contenido: str):
    """
    Muestra la respuesta del agente y separa el contador
    de tokens para presentarlo como información secundaria.
    """

    cuerpo, separador, pie = contenido.partition("\n\n[Tokens")

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
