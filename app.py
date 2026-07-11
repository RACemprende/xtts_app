import streamlit as st
import sys
import torch
import torchaudio

st.write("Python:", sys.version)
st.write("Torch:", torch.__version__)
st.write("Torchaudio:", torchaudio.__version__)

try:
    import torchcodec
    st.write("torchcodec OK")
except Exception as e:
    st.write("torchcodec ERROR:", str(e))

try:
    from TTS.api import TTS
    st.success("TTS importado")
except Exception:
    import traceback
    st.code(traceback.format_exc())
