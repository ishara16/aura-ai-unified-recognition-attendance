import streamlit as st

def header_home():
    logo_path="assets/aura_logo.png"

    img_col1, img_col2, img_col3 = st.columns([2, 1, 2])
    with img_col2:
        st.image(logo_path, width=200)

    st.markdown(f"""
    <div class="aura-title" style='display:flex; flex-direction:column; align-items:center; justify-content:center; margin-bottom:30px; margin-top:30px;'>
        <h1 style='text-align:center; color:#ECE7D1'>AURA</h1>
    </div>
        
    """, unsafe_allow_html=True)


