import os
import streamlit as st

def get_config(key, default=None):
    try:
        return st.secrets[key]
    except Exception:
        return os.getenv(key, default)
