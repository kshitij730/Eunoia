import streamlit as st
from llama_cpp import Llama

# Load the GGUF model from Hugging Face
@st.cache_resource
def load_model():
    llm = Llama.from_pretrained(
        repo_id="kshitij230/Eunoia",
        filename="unsloth.Q8_0.gguf",
        n_ctx=2048,
        chat_format="llama-2"  # Change this if your model uses a different format
    )
    return llm

llm = load_model()

# Streamlit page config
st.set_page_config(page_title="Eunoia 💜", layout="centered")
st.title("🫂 Eunoia - Your Emotional Support Bot")
st.markdown("Speak your heart. I'm here to listen and help 💖")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box
user_input = st.chat_input("What's on your mind?")

if user_input:
    # Display user message
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Build conversation prompt (simple format)
    prompt = ""
    for msg in st.session_state.messages:
        role = "User" if msg["role"] == "user" else "Bot"
        prompt += f"{role}: {msg['content']}\n"
    prompt += "Bot:"

    # Generate model response
    with st.spinner("Eunoia is listening..."):
        response = llm(prompt, max_tokens=200, stop=["User:", "Bot:"])
        reply = response["choices"][0]["text"].strip()

    # Display bot reply
    st.chat_message("assistant").markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
