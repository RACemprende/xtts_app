import os
import tempfile
from datetime import datetime

import streamlit as st
import torch
import transformers.pytorch_utils as ptu

# --------------------------------------------------
# CONFIGURACIÓN
# --------------------------------------------------

os.environ["COQUI_TOS_AGREED"] = "1"

if not hasattr(ptu, "isin_mps_friendly"):
    def isin_mps_friendly(elements, test_elements):
        return torch.isin(elements, test_elements)

    ptu.isin_mps_friendly = isin_mps_friendly

from TTS.api import TTS

# --------------------------------------------------
# PÁGINA
# --------------------------------------------------

st.set_page_config(
    page_title="Las noticias vuelan Podcast",
    page_icon="🎙️",
    layout="centered"
)

# --------------------------------------------------
# ESTILOS
# --------------------------------------------------

st.markdown("""
<style>

.block-container {
    max-width: 900px;
    padding-top: 2rem;
}

h1 {
    text-align: center;
    margin-bottom: 0.3rem;
}

.subtitle {
    text-align: center;
    color: #8a8a8a;
    font-size: 1.05rem;
    margin-bottom: 2rem;
}

.stButton > button {
    width: 100%;
    height: 3rem;
    font-size: 1rem;
    font-weight: 600;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# CABECERA
# --------------------------------------------------

col_logo, col_title = st.columns([1, 5])

with col_logo:
    st.image("logo.JPG", width=120)

with col_title:
    st.markdown(
        """
        <h1 style="margin-bottom:0;">
            Las noticias vuelan Podcast
        </h1>

        <p style="
            color:#888;
            font-size:1.1rem;
            margin-top:0;
        ">
            RAC
        </p>
        """,
        unsafe_allow_html=True
    )

# --------------------------------------------------
# HISTORIAL EN SESIÓN
# --------------------------------------------------

if "history" not in st.session_state:
    st.session_state.history = []

# --------------------------------------------------
# MODELO
# --------------------------------------------------

@st.cache_resource
def load_model():
    return TTS(
        "tts_models/es/css10/vits",
        gpu=False
    )

with st.spinner("Cargando motor de voz..."):
    tts = load_model()

# --------------------------------------------------
# FORMULARIO
# --------------------------------------------------

texto = st.text_area(
    "Guion del podcast",
    value="Bienvenidos a Las noticias vuelan Podcast.",
    height=220
)

velocidad = st.slider(
    "Velocidad de narración",
    min_value=0.5,
    max_value=2.0,
    value=1.0,
    step=0.1
)

# --------------------------------------------------
# DURACIÓN ESTIMADA
# --------------------------------------------------

words = len(texto.split())

# Aproximación típica de narración
estimated_minutes = words / 150

st.info(
    f"📝 {words} palabras · ⏱️ Duración estimada: {estimated_minutes:.1f} minutos"
)

# --------------------------------------------------
# GENERAR AUDIO
# --------------------------------------------------

if st.button("🎙️ Generar narración", type="primary"):

    if not texto.strip():
        st.warning("Introduce un texto para generar la narración.")
        st.stop()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    file_name = f"las_noticias_vuelan_{timestamp}.wav"

    with tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    ) as fp:
        output_path = fp.name

    with st.spinner("Generando audio..."):

        try:
            tts.tts_to_file(
                text=texto,
                file_path=output_path,
                speed=velocidad
            )

        except TypeError:
            # Algunos modelos VITS no soportan speed
            tts.tts_to_file(
                text=texto,
                file_path=output_path
            )

            st.info(
                "El modelo utiliza velocidad fija."
            )

    st.success("✅ Narración generada correctamente")

    with open(output_path, "rb") as f:
        audio_bytes = f.read()

    size_kb = len(audio_bytes) / 1024

    st.audio(audio_bytes)

    st.download_button(
        label="⬇️ Descargar episodio",
        data=audio_bytes,
        file_name=file_name,
        mime="audio/wav"
    )

    st.caption(
        f"Archivo: {file_name} · Tamaño: {size_kb:.1f} KB"
    )

    # Guardar en historial de sesión
    st.session_state.history.insert(
        0,
        {
            "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "name": file_name,
            "words": words,
            "duration": estimated_minutes
        }
    )

# --------------------------------------------------
# HISTORIAL
# --------------------------------------------------

if st.session_state.history:

    st.divider()

    st.subheader("📚 Audios generados en esta sesión")

    for item in st.session_state.history[:10]:

        st.markdown(
            f"""
            **{item['name']}**

            - Fecha: {item['date']}
            - Palabras: {item['words']}
            - Duración estimada: {item['duration']:.1f} min
            """
        )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Las noticias vuelan Podcast · Generación de voz con Coqui TTS"
)
