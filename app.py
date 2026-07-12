import os
import tempfile

import streamlit as st
import torch
import transformers.pytorch_utils as ptu

# Aceptar licencia Coqui automáticamente
os.environ["COQUI_TOS_AGREED"] = "1"

# Compatibilidad Coqui / Transformers
if not hasattr(ptu, "isin_mps_friendly"):
    def isin_mps_friendly(elements, test_elements):
        return torch.isin(elements, test_elements)

    ptu.isin_mps_friendly = isin_mps_friendly

from TTS.api import TTS


# --------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
# --------------------------------------------------

st.set_page_config(
    page_title="Spanish AI Voice",
    page_icon="🎙️",
    layout="centered"
)

# --------------------------------------------------
# ESTILOS
# --------------------------------------------------

st.markdown("""
<style>
.block-container {
    max-width: 850px;
    padding-top: 2rem;
}

h1 {
    text-align: center;
}

.subtitle {
    text-align: center;
    color: #888;
    margin-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# CABECERA
# --------------------------------------------------

st.title("🎙️ Spanish AI Voice")

st.markdown(
    """
    <div class="subtitle">
    Generación de voz en español utilizando Coqui TTS
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# CARGA DEL MODELO
# --------------------------------------------------

@st.cache_resource
def load_model():
    return TTS(
        "tts_models/es/css10/vits",
        gpu=False
    )

with st.spinner("Cargando modelo de voz..."):
    tts = load_model()

# --------------------------------------------------
# FORMULARIO
# --------------------------------------------------

texto = st.text_area(
    "Texto",
    value="Hola, esta es una prueba de generación de voz en español.",
    height=180
)

velocidad = st.slider(
    "Velocidad de lectura",
    min_value=0.5,
    max_value=2.0,
    value=1.0,
    step=0.1
)

# --------------------------------------------------
# GENERACIÓN
# --------------------------------------------------

if st.button("Generar audio", type="primary"):

    if not texto.strip():
        st.warning("Introduce un texto para generar el audio.")
        st.stop()

    with tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    ) as fp:
        output_path = fp.name

    try:

        with st.spinner("Generando audio..."):

            # Algunos modelos VITS no soportan speed.
            # Si falla, elimina speed=velocidad.
            tts.tts_to_file(
                text=texto,
                file_path=output_path,
                speed=velocidad
            )

        st.success("Audio generado correctamente")

        st.audio(output_path)

        with open(output_path, "rb") as f:

            st.download_button(
                "⬇️ Descargar WAV",
                data=f,
                file_name="voz_espanol.wav",
                mime="audio/wav"
            )

    except TypeError:
        # Fallback si css10/vits no soporta speed

        tts.tts_to_file(
            text=texto,
            file_path=output_path
        )

        st.success(
            "El modelo no soporta control de velocidad. Audio generado con velocidad estándar."
        )

        st.audio(output_path)

        with open(output_path, "rb") as f:

            st.download_button(
                "⬇️ Descargar WAV",
                data=f,
                file_name="voz_espanol.wav",
                mime="audio/wav"
            )
