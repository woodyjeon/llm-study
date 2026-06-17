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
        "content": """너는 영화 추천 전문가야.
사용자가 좋아하는 장르를 알려주면, 그 장르에 맞는 영화 3편을 추천해줘.
각 영화마다 반드시 아래 형식으로 답변해:

1. 영화 제목 (개봉 연도)
   - 추천 이유: ...

이후 대화에서 사용자가 다른 장르를 말하거나 추가 추천, 특정 영화 설명을 요청하면
이전 대화를 참고해서 자연스럽게 이어서 답변해.
한국어로 친절하게 답변해.""",
    },
]

print("=== 영화 추천 챗봇 ===")
print("좋아하는 장르를 입력하세요. (종료: exit)")

while True:
    user_input = input("\n사용자: ").strip()

    if user_input.lower() == "exit":
        print("챗봇을 종료합니다.")
        break

    if not user_input:
        continue

    messages.append({"role": "user", "content": user_input})
    ai_response = get_ai_response(messages)
    messages.append({"role": "assistant", "content": ai_response})

    print("AI:", ai_response)
