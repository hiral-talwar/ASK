import streamlit as st
from retrieve import build_index
from ask import ask

st.set_page_config(page_title="ASK: Your Fast Track to Furniture", page_icon="🛋️")

st.title("ASK: Your Fast Track to Furniture")
st.caption("Ask a question in plain English — get recommendations grounded in our real catalogue, with SKUs cited.")

if "index" not in st.session_state:
    with st.spinner("Loading catalogue..."):
        st.session_state.index = build_index()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

question = st.chat_input("What are you looking for?")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = ask(question, st.session_state.index)
        st.write(result["answer"])
    st.session_state.messages.append({"role": "assistant", "content": result["answer"]})