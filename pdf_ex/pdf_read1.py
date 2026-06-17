from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent.parent
reader = PdfReader(ROOT / "data" / "sample.pdf")

text = ""

for page in reader.pages:
    text += page.extract_text()

print(text)
