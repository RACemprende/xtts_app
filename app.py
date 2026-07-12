import os
import streamlit as st
import torch
import transformers.pytorch_utils as ptu

# Aceptar licencia Coqui automáticamente
os.environ["COQUI_TOS_AGREED"] = "1"

# Parche para compatibilidad transformers/coqui
if not hasattr(ptu, "isin_mps_friendly"):
    def isin_mps_friendly(elements, test_elements):
        return torch.isin(elements, test_elements)

    ptu.isin_mps_friendly = isin_mps_friendly

st.write("ANTES DEL IMPORT")

from TTS.api import TTS

st.write("DESPUÉS DEL IMPORT")


@st.cache_resource
def load_model():
    return TTS(
        "tts_models/es/css10/vits",
        gpu=False
    )


st.write("ANTES DE CREAR TTS")

tts = load_model()

st.write("DESPUÉS DE CREAR TTS")

st.success("Modelo cargado correctamente")

# Información del modelo cargado
if hasattr(tts, "speakers") and tts.speakers:
    st.write(f"Número de speakers: {len(tts.speakers)}")
else:
    st.write("Modelo de voz única (sin speakers)")

# Listar modelos disponibles
st.subheader("Modelos españoles disponibles")

try:
    models = TTS().list_models()

    spanish_models = [
        model
        for model in models
        if "/es/" in model.lower()
    ]

    st.write(f"Encontrados {len(spanish_models)} modelos de español")

    for model in sorted(spanish_models):
        st.write(model)

except Exception as e:
    import traceback

    st.error("Error listando modelos")
    st.code(traceback.format_exc())

import tempfile

st.subheader("Prueba de síntesis")

texto = st.text_area(
    "Texto",
    "Hola, esta es una prueba de síntesis de voz en español."
)

if st.button("Generar audio"):

    with tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    ) as fp:

        wav_path = fp.name

    tts.tts_to_file(
        text=texto,
        file_path=wav_path
    )

    st.audio(wav_path)

