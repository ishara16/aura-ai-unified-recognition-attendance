import streamlit as st

def style_background_home():
    st.markdown(""" 
        <style>
                .stApp{
                    background: #8A7650 !important;
                }     

                .st-key-role_cards {
                    margin-top: -40px !important;
                }

                .st-key-role_cards div[data-testid="stColumn"]{
                    background-color:#ECE7D1 !important;
                    padding:2.5rem !important;
                    border-radius: 5rem !important;
                }                   
        </style>
                """, unsafe_allow_html=True)
    
def style_background_dashboard():
    st.markdown(""" 
        <style>
                .stApp{
                    background: #ECE7D1 !important;
                }     

                                   
        </style>
                """, unsafe_allow_html=True)

def style_base_layout():
    st.markdown(""" 
        <style>
                @import url('https://fonts.googleapis.com/css2?family=Bitcount+Prop+Single:wght@100..900&display=swap');
                @import url('https://fonts.googleapis.com/css2?family=Jersey+15&display=swap');

                /*Hide Top Bar of streamlit*/

                #MainMenu,footer,header{ 
                    visibility:hidden;
                }               

                .block-container{
                    padding-top:1.5rem  !important;
                    padding-bottom: 0rem !important;
                }

                

                h1{
                    font-family: 'Jersey 15', sans serif !important;
                    font-size: 6rem !important;
                    line-height: 1 !important;
                    margin-bottom: 0rem !important;
                    color : #ECE7D1 !important;
                    text-align: center !important;
                    
                    margin-top: -10px !important;
                    margin-bottom: 30px !important;
                }

                h1{
                    font-family: 'Jersey 15', sans serif !important;
                    font-size: 6rem !important;
                    line-height: 1 !important;
                    margin-bottom: 0rem !important;
                    color : #ECE7D1 !important;
                    text-align: center !important;
                    
                    margin-top: -10px !important;
                    margin-bottom: 30px !important;
                }

                h2{
                    font-family: 'Bitcount Prop Single', sans serif !important;
                    font-size: 2rem !important;
                    line-height: 1.1 !important;
                    margin-bottom: 0rem !important;
                    color : #8E977D !important;
                }

                h3, h4, p{
                    font-family: 'Bitcount Prop Single', sans serif !important;
                }

                button{
                    border-radius : 1.5rem !important;
                    background : #5868F2 !important;
                    color: white !important;
                    padding: 10px 20px !important;
                    border: none !important;
                    transition: transform 0.25s ease-in-out !important;
                }

                button[kind="secondary"]{
                    border-radius : 1.5rem !important;
                    background : #8E977D !important;
                    color: white !important;
                    padding: 10px 20px !important;
                    border: none !important;
                    transition: transform 0.25s ease-in-out !important;
                }

                button[kind="tertiary"]{
                    border-radius : 1.5rem !important;
                    background : black !important;
                    color: white !important;
                    padding: 10px 20px !important;
                    border: none !important;
                    transition: transform 0.25s ease-in-out !important;
                }

                button:hover{
                    transform:scale(1.05)
                }

        </style>
                """, unsafe_allow_html=True)
    
