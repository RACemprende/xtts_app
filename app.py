import os
import tempfile

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

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# CABECERA
# --------------------------------------------------

st.title("🎙️ Las noticias vuelan Podcast")

st.markdown(
    """
    <div class="subtitle">
    Generador de narraciones de voz para episodios y contenidos del podcast
    </div>
    """,
    unsafe_allow_html=True
)

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
# INTERFAZ
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
# GENERAR AUDIO
# --------------------------------------------------

if st.button("🎙️ Generar narración", type="primary"):

    if not texto.strip():
        st.warning("Introduce un texto para generar la narración.")
        st.stop()

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
            # Algunos modelos VITS no soportan el parámetro speed
            tts.tts_to_file(
                text=texto,
                file_path=output_path
            )

            st.info(
                "Este modelo no soporta control de velocidad. Se ha utilizado la velocidad estándar."
            )

    st.success("Narración generada correctamente")

    st.audio(output_path)

    with open(output_path, "rb") as f:
        st.download_button(
            label="⬇️ Descargar episodio",
            data=f,
            file_name="las_noticias_vuelan.wav",
            mime="audio/wav"
        )
