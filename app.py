import streamlit as st
import sys

st.write(sys.version)

import torch
import transformers.pytorch_utils as ptu

if not hasattr(ptu, "isin_mps_friendly"):

    def isin_mps_friendly(elements, test_elements):
        return torch.isin(elements, test_elements)

    ptu.isin_mps_friendly = isin_mps_friendly

from TTS.api import TTS

st.success("Coqui cargado correctamente")
