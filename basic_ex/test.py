from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
import os

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")
api_key = os.getenv("OPENAI_API_KEY")  # 환경변수에서 API Key를 읽어옴
client = OpenAI(api_key=api_key)  # OpenAI 클라이언트 생성

# 2
response = client.chat.completions.create(
    model="gpt-5-nano",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "2022년 월드컵 우승팀은 어디야?"},
    ],
)

print(response.choices[0].message.content)
