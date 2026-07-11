import streamlit as st
import sys
import torch

st.write("Python:", sys.version)
st.write("Torch:", torch.__version__)

try:
    import torchcodec
    st.success("torchcodec instalado")
except Exception as e:
    st.error(f"torchcodec NO instalado: {e}")
