import streamlit as st

try:
    import torch
    st.success(f"Torch OK: {torch.__version__}")
except Exception as e:
    st.error(f"Torch ERROR: {e}")

try:
    import torchaudio
    st.success(f"Torchaudio OK: {torchaudio.__version__}")
except Exception as e:
    st.error(f"Torchaudio ERROR: {e}")
