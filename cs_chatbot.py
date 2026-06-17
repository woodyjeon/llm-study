from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def get_ai_response(messages):
    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=messages,
    )
    return response.choices[0].message.content


messages = [
    {
        "role": "system",
        "content": """너는 IT 기업의 고객센터(CS) 상담 챗봇이야.
다음 업무를 친절하고 전문적으로 도와줘:
- 제품/서비스 이용 방법 안내
- 기술 문제 및 오류 해결
- 계정, 결제, 환불 문의
- 기능 문의 및 사용 팁

답변 원칙:
- 한국어로 정중하고 명확하게 답변해
- 문제 해결을 위해 단계별로 안내해
- 정보가 부족하면 필요한 내용을 질문해
- 해결되지 않는 경우 담당자 연결 또는 추가 지원 안내를 해
- 이전 대화 내용을 참고해서 자연스럽게 이어서 답변해""",
    },
]

print("=== AI CS 챗봇 ===")
print("무엇을 도와드릴까요? (종료: exit)")

while True:
    user_input = input("\n고객: ").strip()

    if user_input.lower() == "exit":
        print("상담을 종료합니다. 이용해 주셔서 감사합니다.")
        break

    if not user_input:
        continue

    messages.append({"role": "user", "content": user_input})
    ai_response = get_ai_response(messages)
    messages.append({"role": "assistant", "content": ai_response})

    print("CS:", ai_response)
