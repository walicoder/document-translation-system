import streamlit as st
import time
from src.client import send_get_request


st.title("Document Translation Service")
st.markdown("*Bengali to English Text and Document Generation Service*")
with st.sidebar:
    st.text_input("Username")
    st.text_input("Password")
    button = st.button("login", key="login")


with st.container(border=True):
    tab1, tab2 = st.tabs(["Text To Text Generation", "Document to Document Generation"])
    with tab1:
        text_input = st.text_area("Enter your Bengali text here", max_chars=1000)
        text_translate_btn = st.button("Translate", key="text")
        if text_input and text_translate_btn:
            try:
                with st.spinner("Translating..."):
                    translation = send_get_request(text_input)
                if "error" in translation:
                    st.error("Can not translate the text. Please insert a valid Bengali text.")
                else:
                    st.success(translation["text_en"])
            except Exception as e:
                print(e)
                st.error("Error: Can not connect to the service. Please try again later.")
    with tab2:
        # st.write("Coming soon...")
        uploaded_content = st.file_uploader("Upload a valid file", type=["txt", "docx"])
        file_translate_btn = st.button("Translate", key="file")
        if uploaded_content and file_translate_btn:
            with st.spinner("Translating..."):
                # Here translation happens
                time.sleep(5)
            st.success("Translation Done!")
        if not uploaded_content and file_translate_btn:
            st.error("Please upload a valid file.")


