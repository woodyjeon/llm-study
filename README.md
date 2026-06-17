# LLM Study - Day01

OpenAI API를 활용한 LLM 학습 예제 모음입니다.  
나중에 복습할 때 **폴더별 학습 순서**와 **실행 방법**을 참고하세요.

GitHub: https://github.com/woodyjeon/llm-study

---

## 프로젝트 구조

```
day01/
├── basic_ex/          # OpenAI API 기본 예제
├── chatbot_ex/        # CLI 멀티턴 챗봇
├── streamlit_ex/      # Streamlit 웹 챗봇
├── pdf_ex/            # PDF 텍스트 추출 및 GPT 요약
├── data/              # PDF 원본 데이터
├── output/            # 실행 결과 (txt, 요약 파일)
├── requirements.txt
├── .env.example
└── README.md
```

| 폴더 | 역할 |
|------|------|
| `data/` | PDF 원본만 보관 |
| `output/` | 추출·전처리·요약 결과 저장 (Git 제외) |
| `*_ex/` | 학습용 예제 스크립트 |

---

## 환경 설정

### 1. 가상환경 (권장)

```powershell
cd c:\workspace\llm\day01
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install pymupdf   # PDF 고급 처리용 (pdf_ex)
```

### 2. API 키 설정

```powershell
copy .env.example .env
```

`.env` 파일에 OpenAI API 키 입력:

```env
OPENAI_API_KEY=sk-proj-여기에-실제-키
```

> `.env`는 Git에 올리지 않습니다.

### 3. Cursor / VS Code 인터프리터

`Ctrl+Shift+P` → **Python: Select Interpreter** → `.venv\Scripts\python.exe` 선택

---

## 학습 순서 (권장)

### Step 1. `basic_ex/` — OpenAI API 기본

| 파일 | 학습 내용 |
|------|-----------|
| `test.py` | API 연결, 첫 요청, 응답 구조 확인 |
| `singleturn.py` | 1회 질문 → 1회 응답 (대화 기록 없음) |
| `multiturn.py` | `messages` 리스트에 대화 누적 → 멀티턴 |
| `fewshot.py` | 예시(user/assistant)를 messages에 넣어 few-shot 학습 |

```powershell
python basic_ex/test.py
python basic_ex/singleturn.py
python basic_ex/multiturn.py
python basic_ex/fewshot.py
```

**핵심 개념**

- `messages`: `[{"role": "system"|"user"|"assistant", "content": "..."}]`
- **싱글턴**: 매번 새 messages
- **멀티턴**: user/assistant를 append하여 맥락 유지

---

### Step 2. `chatbot_ex/` — CLI 챗봇

| 파일 | 학습 내용 |
|------|-----------|
| `movie_recommend.py` | 장르 입력 → 영화 3편 추천 + 추천 이유 (멀티턴) |
| `cs_chatbot.py` | IT 기업 CS 상담 챗봇 (멀티턴) |

```powershell
python chatbot_ex/movie_recommend.py
python chatbot_ex/cs_chatbot.py
```

종료: `exit` 입력

**핵심 개념**

- `system` 프롬프트로 역할·출력 형식 정의
- 멀티턴으로 후속 질문 처리 ("액션도 추천해줘" 등)

---

### Step 3. `streamlit_ex/` — 웹 UI 챗봇

| 파일 | 학습 내용 |
|------|-----------|
| `streamlit_chatbot.py` | Streamlit 기본 채팅 UI |
| `streamlit_movie_chatbot.py` | 영화 추천 챗봇 (Streamlit + 멀티턴) |

```powershell
streamlit run streamlit_ex/streamlit_chatbot.py
streamlit run streamlit_ex/streamlit_movie_chatbot.py
```

**핵심 개념**

- `st.session_state["messages"]`: Streamlit 재실행 시 대화 유지
- `st.chat_message()`, `st.chat_input()`: 채팅 UI
- `:=` (바다코끼 연산자): 입력값 저장 + 조건 검사 동시 처리

```python
if prompt := st.chat_input():
    # prompt에 입력값이 저장되고, 입력이 있을 때만 실행
```

---

### Step 4. `pdf_ex/` — PDF 처리 및 GPT 요약

| 파일 | 학습 내용 | 출력 |
|------|-----------|------|
| `pdf_read1.py` | pypdf로 PDF 텍스트 추출 (콘솔 출력) | - |
| `pdf_read2.py` | pypdf로 추출 후 파일 저장 | `output/output.txt` |
| `pdf_to_text.py` | pymupdf로 전체 텍스트 추출 | `output/*.txt` |
| `pdf_without_header_footer.py` | 헤더/푸터 제외 추출 | `output/*_with_preprocessing.txt` |
| `summary.py` | 전처리 txt → GPT 요약 | `output/crop_model_summary.txt` |
| `pdf_summary.py` | PDF→텍스트→요약 통합 (구버전) | `output/crop_model_summary2.txt` |

**권장 실행 순서**

```powershell
# 1) PDF → 전처리 텍스트
python pdf_ex/pdf_without_header_footer.py

# 2) GPT 요약
python pdf_ex/summary.py
```

**핵심 개념**

- `pypdf`: 간단한 PDF 텍스트 추출
- `pymupdf`: 영역(clip) 지정으로 헤더/푸터 제거 가능
- GPT 요약: `system`(형식) + `user`(본문) role 분리
- 경로: `Path(__file__).parent.parent` → 프로젝트 루트 기준 `data/`, `output/` 참조

---

## 공통 패턴

### .env 로드 (모든 예제)

```python
from pathlib import Path
from dotenv import load_dotenv
import os

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")
api_key = os.getenv("OPENAI_API_KEY")
```

### OpenAI API 호출

```python
from openai import OpenAI

client = OpenAI(api_key=api_key)
response = client.chat.completions.create(
    model="gpt-5-nano",
    messages=[
        {"role": "system", "content": "..."},
        {"role": "user", "content": "..."},
    ],
)
answer = response.choices[0].message.content
```

### 멀티턴 대화

```python
messages = [{"role": "system", "content": "..."}]

while True:
    user_input = input("사용자: ")
    messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(model="gpt-5-nano", messages=messages)
    ai_response = response.choices[0].message.content
    messages.append({"role": "assistant", "content": ai_response})
```

---

## Git 관련

### 커밋하지 않는 파일 (`.gitignore`)

- `.env` — API 키
- `output/*` — 실행 결과
- `data/*.txt` — PDF에서 추출한 텍스트
- `.venv/` — 가상환경

### 컴 커밋하는 파일

- 소스 코드 (`*_ex/`)
- `data/*.pdf` — PDF 원본
- `.env.example` — API 키 템플릿
- `requirements.txt`

---

## 자주 발생하는 오류

| 오류 | 원인 | 해결 |
|------|------|------|
| `Import "dotenv" could not be resolved` | IDE가 가상환경을 못 찾음 | 인터프리터를 `.venv`로 선택 |
| `OPENAI_API_KEY가 없습니다` | `.env` 없음 또는 키 미입력 | `.env.example` 복사 후 키 입력 |
| `FileNotFoundError` (summary.py) | 전처리 txt 없음 | `pdf_without_header_footer.py` 먼저 실행 |
| `ModuleNotFoundError: pymupdf` | 패키지 미설치 | `pip install pymupdf` |
| `UnicodeEncodeError` (Windows) | 콘솔 cp949 인코딩 | `summary.py`는 저장 후 출력 (이미 처리됨) |

---

## 복습 체크리스트

- [ ] `.env`로 API 키를 안전하게 관리할 수 있다
- [ ] singleturn vs multiturn 차이를 설명할 수 있다
- [ ] few-shot은 messages에 예시를 넣는 방식임을 안다
- [ ] system / user / assistant role의 역할을 안다
- [ ] Streamlit에서 `session_state`가 필요한 이유를 안다
- [ ] PDF → 텍스트 → GPT 요약 파이프라인을 실행할 수 있다
- [ ] `data/`(원본)와 `output/`(결과) 폴더 역할을 구분한다
