from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

reader = PdfReader(ROOT / "data" / "sample.pdf")

text = ""

for page in reader.pages:
    text += page.extract_text()

output_path = OUTPUT_DIR / "output.txt"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(text)

print("저장 완료")
