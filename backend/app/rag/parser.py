import os
from typing import List, Dict, Any
from backend.app.core.exceptions import DocumentProcessingException


class DocumentParser:
    """Parses PDF, Markdown, and TXT documents into pages and sections."""

    def parse_file(self, file_path: str) -> List[Dict[str, Any]]:
        if not os.path.exists(file_path):
            raise DocumentProcessingException(f"File not found: {file_path}")

        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            return self._parse_pdf(file_path)
        elif ext in [".md", ".txt"]:
            return self._parse_text(file_path)
        else:
            raise DocumentProcessingException(f"Unsupported file type: {ext}")

    def _parse_pdf(self, file_path: str) -> List[Dict[str, Any]]:
        pages = []
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(file_path)
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text("text")
                pages.append({
                    "page_number": page_num + 1,
                    "content": text.strip(),
                    "has_tables": "table" in text.lower() or "|" in text
                })
            doc.close()
        except Exception:
            # Fallback to pdfplumber if PyMuPDF fails or isn't present
            try:
                import pdfplumber
                with pdfplumber.open(file_path) as pdf:
                    for i, page in enumerate(pdf.pages):
                        text = page.extract_text() or ""
                        pages.append({
                            "page_number": i + 1,
                            "content": text.strip(),
                            "has_tables": False
                        })
            except Exception as ex:
                raise DocumentProcessingException(f"Failed to parse PDF {file_path}: {str(ex)}")
        return pages

    def _parse_text(self, file_path: str) -> List[Dict[str, Any]]:
        pages = []
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Split markdown into sections or logical pages by headers or 1000 char blocks
        sections = content.split("\n# ")
        for idx, sec in enumerate(sections):
            text = sec if idx == 0 else "# " + sec
            if text.strip():
                pages.append({
                    "page_number": idx + 1,
                    "content": text.strip(),
                    "has_tables": "|" in text
                })
        return pages


parser = DocumentParser()
