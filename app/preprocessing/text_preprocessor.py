import re


class TextPreprocessor:
    """
    Cleans extracted document text before chunking.
    """

    def clean(self, text: str) -> str:
        """
        Clean extracted text.

        Args:
            text (str): Raw text extracted from PDF.

        Returns:
            str: Cleaned text.
        """

        # Remove leading/trailing whitespace
        text = text.strip()

        # Replace multiple spaces with one
        text = re.sub(r"[ \t]+", " ", text)

        # Replace multiple blank lines with two newlines
        text = re.sub(r"\n\s*\n+", "\n\n", text)

        return text