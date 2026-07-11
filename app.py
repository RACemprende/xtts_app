import streamlit as st
import torch
import transformers.pytorch_utils as ptu

if not hasattr(ptu, "isin_mps_friendly"):
    def isin_mps_friendly(elements, test_elements):
        return torch.isin(elements, test_elements)
    ptu.isin_mps_friendly = isin_mps_friendly

from TTS.api import TTS

st.write("Import OK")

try:
    tts = TTS(
        "tts_models/multilingual/multi-dataset/xtts_v2",
        gpu=False
    )

    st.success("XTTS cargado")
    st.write(len(tts.speakers))

except Exception as e:
    st.error(str(e))
