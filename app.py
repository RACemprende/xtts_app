import os
os.environ["COQUI_TOS_AGREED"] = "1"

import streamlit as st
import torch
import transformers.pytorch_utils as ptu

if not hasattr(ptu, "isin_mps_friendly"):
    def isin_mps_friendly(elements, test_elements):
        return torch.isin(elements, test_elements)

    ptu.isin_mps_friendly = isin_mps_friendly

st.write("ANTES DEL IMPORT")

from TTS.api import TTS

st.write("DESPUÉS DEL IMPORT")

st.write("ANTES DE CREAR TTS")

tts = TTS(
    "tts_models/multilingual/multi-dataset/xtts_v2",
    gpu=False
)

st.write("DESPUÉS DE CREAR TTS")

st.success("XTTS cargado")
