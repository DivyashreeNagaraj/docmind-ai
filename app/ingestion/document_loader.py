from pathlib import Path
from pypdf import PdfReader


class DocumentLoader:
     def load_document(self, uploaded_file):

        """
        Load a PDF file and extract its text.

        Args:
        uploaded_file: Uploaded PDF file from Streamlit.

        Returns:
            dict: Metadata and extracted text.
        """

        reader = PdfReader(uploaded_file)

        full_text = ""
        page_texts = []

        for page_number, page in enumerate(reader.pages, start=1):
            extracted = page.extract_text() or ""

            full_text += extracted + "\n"

            page_texts.append(
                {
                    "page": page_number,
                    "text": extracted
                }
            )

        return {
            "filename": uploaded_file.name,
            "pages": len(reader.pages),
            "text": full_text,
            "page_texts": page_texts
        }