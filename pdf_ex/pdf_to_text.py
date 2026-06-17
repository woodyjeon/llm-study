from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

pdf_file_path = DATA_DIR / "과정기반 작물모형을 이용한 웹 기반 밀 재배관리 의사결정 지원시스템 설계 및 구축.pdf"
doc = pymupdf.open(pdf_file_path)

full_text = ""

for page in doc:
    text = page.get_text()
    full_text += text

txt_file_path = OUTPUT_DIR / f"{pdf_file_path.stem}.txt"

with open(txt_file_path, "w", encoding="utf-8") as f:
    f.write(full_text)

print(f"저장 완료: {txt_file_path}")
