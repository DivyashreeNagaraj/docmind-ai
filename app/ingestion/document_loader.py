from pathlib import Path
from pypdf import PdfReader


class DocumentLoader:
    def load_pdf(self, file_path: str) -> dict:
        """
        Load a PDF file and extract its text.

        Args:
            file_path (str): Path to the PDF file.

        Returns:
            dict: Metadata and extracted text.
        """

        pdf_path = Path(file_path)

        reader = PdfReader(pdf_path)

        full_text = ""
        page_texts = []

        for page_num, page in enumerate(reader.pages, start=1):
            extracted = page.extract_text() or ""

            full_text += extracted + "\n"

            page_texts.append(
                {
                    "page": page_num,
                    "text": extracted
                }
            )

        return {
            "filename": pdf_path.name,
            "pages": len(reader.pages),
            "text": full_text,
            "page_texts": page_texts
        }