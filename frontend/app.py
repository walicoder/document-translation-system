import json

import streamlit as st
from auth import user_authenticated, session_handler, is_authenticated
from client import (
    translate, get_translations, post_translation, split_n_translate, post_translation_batch, get_translations_batch
)
import pandas as pd
import datetime

with st.form(key="welcome", clear_on_submit=True):
        with st.sidebar:
            st.markdown("---")
            user = st.text_input("Username", value="")
            password = st.text_input("Password", value="", type="password")
            submitted = st.form_submit_button("LogIn")

if submitted:
        result = user_authenticated(username=user, password=password)
        if result:
            st.sidebar.success(f"welcome {user}, you are Logged in successfully!")
        else:
            st.sidebar.error("Invalid username or password")


@session_handler
def show_text_translation_history():
    usename = st.session_state["username"]
    history = get_translations(username=usename)
    if history:
        column_set = ["bengali_text", "english_text", "translated_at"]
        history = pd.DataFrame(history)[column_set]
        history = history.sort_values(by="translated_at", ascending=False)
        st.table(history)
    else:
        st.markdown("No translation history found...")


def show_text_translation_history_batch():
    usename = st.session_state["username"]
    history = get_translations_batch(username=usename)
    if history:
        column_set = ["input_file", "output_file", "translated_at"]
        history = pd.DataFrame(history)[column_set]
        history = history.sort_values(by="translated_at", ascending=False)
        st.table(history)
    else:
        st.markdown("No translation history found...")


def add_translation_into_history(translation: dict):
    usename = st.session_state["username"]
    session_id = st.session_state["session_id"]

    response = post_translation(
        username=usename, 
        english_text=translation["text_en"], 
        bengali_text=translation["text_bn"], 
        session_id=session_id
        )
    return response


def add_batch_translation_into_history(translation: dict):
    usename = st.session_state["username"]
    session_id = st.session_state["session_id"]

    response = post_translation_batch(
        username=usename,
        english_text=translation["text_en"],
        bengali_text=translation["text_bn"],
        session_id=session_id
        )
    return response




with st.container(border=False):
    tab1, tab2 = st.tabs(["Text To Text Generation", "Document to Document Generation"])
    with tab1:
        text_input = st.text_area("Enter your Bengali text here", max_chars=150, height=200)
        text_translate_btn = st.button("Translate", key="text")
        if text_input and text_translate_btn:
            try:
                with st.spinner("Translating..."):
                    translation = translate(text_input)
                if "error" in translation:
                    st.error("Can not translate the text. Please insert a valid Bengali text.")
                else:
                    st.success(translation["text_en"])
                    if is_authenticated():
                        response = add_translation_into_history(translation)
                        print(response)
            except Exception as e:
                print(e)
                st.error("Error: Can not connect to the service. Please try again later.")
        show_text_translation_history()

    with tab2:
        if is_authenticated():
            uploaded_file = st.file_uploader("Upload a valid file", type=["txt"])
            file_translate_btn = st.button("Translate", key="file")
            if uploaded_file and file_translate_btn:
                try:
                    file_content = uploaded_file.read().decode("utf-8")
                    with st.spinner("Translating..."):
                        translation = split_n_translate(file_content)
                        if "text_en" in translation:
                            # Get the translated text in English
                            translated_text = translation["text_en"]
                            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                            translated_file_name = f"{uploaded_file.name.replace('.txt', '')}_translated_{timestamp}.txt"
                            st.success(f"Translation done! You can download your file.")
                            st.download_button(
                                label="Download Translated File",
                                data=translated_text,
                                file_name=translated_file_name,
                                mime="text/plain"
                            )
                            response = add_batch_translation_into_history(translation)
                            print(response)
                except Exception as e:
                    print(e)
                    st.error("Error: Cannot process the file. Please try again later.")
            show_text_translation_history_batch()
            if not uploaded_file and file_translate_btn:
                st.error("Please upload a valid file.")
            if file_translate_btn and not uploaded_file:
                st.error("You must upload a file to proceed for translation.")
        else:
            st.markdown("🚫 __You must need to login to use the of document translation feature__")


