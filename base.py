import streamlit as st
from google import genai
import os
from dotenv import load_dotenv


load_dotenv()
st.set_page_config(page_title="هوش مصنوعی ساخته شده توسط حسن",page_icon="🤖",layout="wide")
with st.sidebar:
    st.title("تنظیمات,setting")
    st.write("اینجا میتونی تنظیمات چت بات رو تغییر بدی|chat bot setting")
    st.info("ساخته شده توسط حسن نوبری|created by hassan")
    st.info("version 1.0")

st.title("MY CHAT BOT")
st.write("من یک هوش مصنوعی هستم ! هر سوالی داری بپرس!!!!")
st.write("i am your AI ,whats your question enter here!")
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("مشکلی پیش امد")
    st.stop()
client = genai.Client(api_key=api_key)

if "chat_session" not in st.session_state:
    st.session_state.chat_session = client.chats.create(model= 'gemini-3.7-flash')
    st.session_state.messages = [{"role":"assistant","content":"how can i help you!چطور میتونم کمکت کنم"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("پیام خودت رو اینجا بنویس..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})


    with st.chat_message("assistant"):
        with st.spinner("در حال فکر کردن... (اگر شلوغ باشه، مدل رو عوض می‌کنم)"):


            models_to_try = ['gemini-3.0-flash', 'gemini-3.5-flash', 'gemini-3.6-flash''gemini-3.7-flash']
            success = False

            for model_name in models_to_try:
                try:

                    if "chat_session" not in st.session_state or st.session_state.get('current_model') != model_name:
                        st.session_state.chat_session = client.chats.create(model=model_name)
                        st.session_state.current_model = model_name


                    response = st.session_state.chat_session.send_message(prompt)


                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                    success = True
                    break

                except Exception as e:

                    continue

            if not success:
                st.error(
                    " متاسفانه سرورهای تمام مدل‌ها الان شلوغ هستند یا مشکل شبکه (VPN) دارید. لطفاً چند دقیقه دیگه دوباره امتحان کنید.")

