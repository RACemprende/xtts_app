import streamlit as st
import torch
import torchaudio

st.write("Python:", __import__("sys").version)
st.write("Torch:", torch.__version__)
st.write("Torchaudio:", torchaudio.__version__)

try:
    import torchcodec
    st.success("torchcodec instalado")
except Exception as e:
    st.error(f"torchcodec ERROR: {e}")
