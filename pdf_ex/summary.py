from pathlib import Path
import sys

from dotenv import load_dotenv
from openai import OpenAI
import os

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "output"

load_dotenv(ROOT / ".env")

api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    raise ValueError("OPENAI_API_KEY가 없습니다. .env 파일을 확인하세요.")

client = OpenAI(api_key=api_key)

PDF_STEM = "과정기반 작물모형을 이용한 웹 기반 밀 재배관리 의사결정 지원시스템 설계 및 구축"
DEFAULT_INPUT = OUTPUT_DIR / f"{PDF_STEM}_with_preprocessing.txt"
DEFAULT_OUTPUT = OUTPUT_DIR / "crop_model_summary.txt"


def summarize_txt(file_path: Path):
    if not file_path.exists():
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        txt = f.read()

    txt = txt[:12000]

    system_prompt = """
너는 논문과 보고서를 요약하는 전문 요약 봇이다.

아래 텍스트를 읽고 다음 형식으로 요약하라.

# 제목

## 저자의 문제 인식 및 주장
- 15문장 이내로 작성

## 주요 내용 요약
- 핵심 내용을 항목별로 정리

## 저자 소개
- 텍스트에 저자 정보가 없으면 "본문에서 확인할 수 없음"이라고 작성
"""

    user_prompt = f"""
=============== 이하 텍스트 ===============

{txt}
"""

    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    return response.choices[0].message.content


def save_summary(summary: str, output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(summary)


def print_summary(summary: str):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass
    print(summary)


if __name__ == "__main__":
    summary = summarize_txt(DEFAULT_INPUT)
    save_summary(summary, DEFAULT_OUTPUT)
    print_summary(summary)
    print(f"\n요약 파일 저장 완료: {DEFAULT_OUTPUT}")
