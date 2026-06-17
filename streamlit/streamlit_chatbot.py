import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# .env 파일에서 OPENAI_API_KEY 등 환경 변수 로드
load_dotenv()

# (0) 사이드바: API 키를 .env에서 읽어옴
with st.sidebar:
    openai_api_key = os.getenv("OPENAI_API_KEY")

st.title("Chat bot")

# (1) 대화 기록 초기화
# Streamlit은 버튼/입력마다 스크립트 전체를 다시 실행하므로,
# session_state에 messages를 저장해야 대화가 유지됨
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "안녕하세요! 무엇을 도와드릴까요?"}
    ]

# (2) 저장된 대화 기록을 화면에 출력
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# (3) 사용자 입력 처리 및 AI 응답 생성
# := (바다코끼 연산자): 입력값을 prompt에 저장하고, 입력이 있을 때만 if 블록 실행
if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)

    # 사용자 메시지를 대화 기록에 추가하고 화면에 표시
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 전체 대화 기록(messages)을 GPT에 전달 → 멀티턴 대화
    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=st.session_state.messages,
    )
    msg = response.choices[0].message.content

    # AI 응답을 대화 기록에 추가하고 화면에 표시
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
