import streamlit as st

st.title("XTTS Test")

texto = st.text_area("Texto")

if st.button("Generar"):
    st.write(f"Texto recibido: {texto}")
