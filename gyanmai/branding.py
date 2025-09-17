import streamlit as st

def show_header():
    st.set_page_config(page_title="GyanmAI House Painter", page_icon="🎨")
    st.markdown(
        """
        <div style='text-align: center'>
            <img src='https://raw.githubusercontent.com/your-org/logo.png' width='120'>
            <h1 style='color:#2E86C1;'>🏠 GyanmAI House Color Studio</h1>
            <p>Upload your house, choose your color, and reimagine your home instantly!</p>
        </div>
        """,
        unsafe_allow_html=True
    )