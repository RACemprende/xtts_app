import torch
import streamlit as st

st.write(torch.__version__)

try:
    import TTS
    st.success("TTS importado")
except Exception as e:
    st.error(str(e))
