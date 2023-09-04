import streamlit as st
from streamlit_quill import st_quill


content = st_quill("hi there", key="text")

def on_fix_clicked():
    st.session_state.text = st.session_state.text + " TEST"

st.button("Fix", on_click=on_fix_clicked)
