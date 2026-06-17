from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
import os

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

SYSTEM_PROMPT = """너는 영화 추천 전문가야.
사용자가 좋아하는 장르를 알려주면, 그 장르에 맞는 영화 3편을 추천해줘.
각 영화마다 반드시 아래 형식으로 답변해:

1. 영화 제목 (개봉 연도)
   - 추천 이유: ...

이후 대화에서 사용자가 다른 장르를 말하거나 추가 추천, 특정 영화 설명을 요청하면
이전 대화를 참고해서 자연스럽게 이어서 답변해.
한국어로 친절하게 답변해."""

INITIAL_MESSAGES = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {
        "role": "assistant",
        "content": "안녕하세요! 🎬 좋아하는 장르를 알려주시면 영화를 추천해 드릴게요.",
    },
]


def reset_chat():
    st.session_state["messages"] = INITIAL_MESSAGES.copy()


with st.sidebar:
    openai_api_key = os.getenv("OPENAI_API_KEY")
    st.header("설정")
    if st.button("대화 초기화"):
        reset_chat()
        st.rerun()

st.title("🎬 영화 추천 챗봇")

if "messages" not in st.session_state:
    st.session_state["messages"] = INITIAL_MESSAGES.copy()

for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("좋아하는 장르를 입력하세요 (예: SF, 로맨스, 액션)"):
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=st.session_state.messages,
    )
    msg = response.choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
