import streamlit as st
import time
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOpenAI

DEEPSEEK_API_KEY = "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"
DEEPSEEK_API_BASE = "https://openrouter.ai/api/v1"

def x():
    return ChatOpenAI(
        model_name="deepseek/deepseek-chat-v3-0324:free",
        openai_api_key=DEEPSEEK_API_KEY,
        openai_api_base=DEEPSEEK_API_BASE,
        temperature=0.7,
        max_tokens=1000
    )
def respon_to_user(problem):
    llm = x()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system",
         "Kamu adalah CurhatIn, AI yang dibuat oleh Ananda Mahatva Yodha "
         "buat jadi sahabat deket yang selalu siap dengerin cerita. "
         "Pakai bahasa santai ala Gen Z, akrab, hangat, dan empatik—kayak lagi nongkrong sama temen lama. "
         "Gunakan kata 'aku' buat dirimu dan 'kamu' buat pengirim biar vibes-nya personal. "
         "Respon dengan nada tulus dan peduli, pakai emoji yang pas biar obrolan nggak kaku. "
         "Hindari bahasa formal, biarkan obrolan ngalir natural kayak chat di DM. "
         "Kalau ngasih saran, bikin jelas, gampang dipahami, dan relate sama keseharian Gen Z. "
         "Jangan menggurui, tapi kasih insight yang bisa bikin pengirim merasa lebih lega, paham situasi, dan punya langkah buat maju. "
         "Pakai teknik validasi perasaan, reframing, dan fokus ke solusi positif. "
         "Pastikan pengirim merasa diterima, dimengerti, dan nggak sendirian. "
         "🚫 Jangan membuat gimmick atau roleplay seperti 'nyiapin virtual teh hangat', 'pelukan virtual', atau aksi fisik lainnya."),
        ("user", "{problem}"),
    ])
    chain = prompt_template | llm | StrOutputParser()
    return chain.invoke({"problem": problem})



def reset():
    st.session_state.chat_history = [{
        "role": "assistant",
        "content": "Hai! Aku ChuhatIn, kamu ada masalah apa nih?"
    }]
    st.rerun()

# Konfigurasi halaman
st.set_page_config(page_title="ChuhatIn", page_icon="🫶", layout="wide")
st.title("Mau Cerita Apa Hari ini ?")

# Sidebar
st.sidebar.title("🫶 Curhatin AI - (Beta)")
option = st.sidebar.selectbox("", ("Curhatin AI - (Teman Dekat v1.0)", "Curhatin AI - (Sahabat Kamu v2.1)"))
st.sidebar.markdown("[Pelajari Selengkapnya](https://openrouter.ai/deepseek/deepseek-chat-v3-0324:free)")
st.sidebar.markdown("---")

if st.sidebar.button("Reset Chat"):
    reset()

# Inisialisasi chat_history
if "chat_history" not in st.session_state:
    reset()

# Tampilkan chat sebelumnya
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input pengguna
if prompt := st.chat_input("Tuliskan apa masalahmu....."):
    # Tambah pesan user
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Proses jawaban
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("Mengolah masalahmu..."):
           
            response = respon_to_user(prompt)
        message_placeholder.markdown(response)

    # Tambah pesan AI
    st.session_state.chat_history.append({"role": "assistant", "content": response})
    st.rerun()
