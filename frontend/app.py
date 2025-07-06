import streamlit as st
import requests

st.set_page_config(page_title="Calendar Assistant", page_icon="📅")
st.title("Calendar Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("---")
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div style='text-align: right; font-weight: bold;'>You:</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: right; background-color: #f0f2f6; padding: 10px; border-radius: 10px;'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align: left; font-weight: bold;'>Assistant:</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: left; background-color: #e8f0fe; padding: 10px; border-radius: 10px;'>{msg['content']}</div>", unsafe_allow_html=True)

st.markdown("---")

with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Your message", placeholder="e.g., When am I free?")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        response = requests.post("http://127.0.0.1:8000/chat", json={"query": user_input})
        if response.status_code == 200:
            result = response.json().get("response", "No response received.")
        else:
            result = f"Server error ({response.status_code})"
    except Exception as e:
        result = f"Connection error: {str(e)}"

    st.session_state.messages.append({"role": "assistant", "content": result})
    st.experimental_rerun()
