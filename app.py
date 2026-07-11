import streamlit as st

try:
    import torchcodec
    st.success("torchcodec instalado")
except Exception as e:
    st.error(f"torchcodec NO instalado: {e}")
