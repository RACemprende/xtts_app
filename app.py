import os
os.environ["COQUI_TOS_AGREED"] = "1"

import streamlit as st
import torch
import transformers.pytorch_utils as ptu

if not hasattr(ptu, "isin_mps_friendly"):
    def isin_mps_friendly(elements, test_elements):
        return torch.isin(elements, test_elements)
    ptu.isin_mps_friendly = isin_mps_friendly

from TTS.api import TTS

st.write("Import OK")

@st.cache_resource
def load_model():
    return TTS(
        "tts_models/es/css10/vits",
        gpu=False
    )

st.write("Antes de cargar XTTS")

tts = load_model()

st.success("XTTS cargado")
st.write(len(tts.speakers))
