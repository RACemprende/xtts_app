import streamlit as st

st.title("Prueba de dependencias")

import transformers

st.success("Transformers OK")

st.write(transformers.__version__)
