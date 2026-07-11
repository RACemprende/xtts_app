import streamlit as st

try:
    from TTS.api import TTS
    st.success("TTS importado")
except Exception as e:
    import traceback
    st.code(traceback.format_exc())
