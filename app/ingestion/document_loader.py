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

        text = ""

        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

        return {
            "filename": pdf_path.name,
            "pages": len(reader.pages),
            "text": text,
        }