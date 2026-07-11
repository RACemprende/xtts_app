import streamlit as st
import torch
import torchaudio

st.write("Torch:", torch.__version__)
st.write("Torchaudio:", torchaudio.__version__)

try:
    from TTS.api import TTS
    st.success("TTS importado")
except Exception as e:
    import traceback
    st.code(traceback.format_exc())
