import streamlit as st
import logging
import uuid
import functools
from client import validate_user


def add_auth_to_session(username: str):
    try:
        st.session_state["username"] = username
        st.session_state["authenticated"] = True
        st.session_state["session_id"] = str(uuid.uuid4())
    except Exception as e:
        logging.error(e)


def user_authenticated(username: str, password: str) -> bool:
    if validate_user(username, password):
        add_auth_to_session(username=username)
        return True
    return False


def is_authenticated() -> bool:
    return 'authenticated' in st.session_state and st.session_state['authenticated']


def session_handler(func):
    generic_text = "🚫 _You must have to authenticate yourself to view the translation history._"

    @functools.wraps(func)
    def wrapper():
        if 'authenticated' in st.session_state and st.session_state['authenticated']:
            func()
        else:
            st.markdown(generic_text)
    return wrapper
