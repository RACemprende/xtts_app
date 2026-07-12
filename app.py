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


st.set_page_config(
    page_title="Spanish TTS",
    page_icon="🎙️",
    layout="centered"
)

st.title("🎙️ Spanish Text To Speech")
st.caption("Generación de voz usando Coqui TTS (CSS10 VITS)")


@st.cache_resource
def load_model():
    return TTS(
        "tts_models/es/css10/vits",
        gpu=False
    )


with st.spinner("Cargando modelo..."):
    tts = load_model()


texto = st.text_area(
    "Texto",
    value="Hola, esta es una prueba de generación de voz en español.",
    height=180
)

if st.button("Generar audio", type="primary"):

    if not texto.strip():
        st.warning("Introduce un texto.")
    else:

        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        ) as fp:
            output_path = fp.name

        with st.spinner("Generando audio..."):
            tts.tts_to_file(
                text=texto,
                file_path=output_path
            )

        st.success("Audio generado correctamente")

        st.audio(output_path)

        with open(output_path, "rb") as f:
            st.download_button(
                label="Descargar WAV",
                data=f,
                file_name="audio.wav",
                mime="audio/wav"
            )
