import re


class TextPreprocessor:

    def clean(self, text):
        text = text.strip()
         # Remove multiple spaces but keep line breaks
        text = re.sub(r"[ \t]+", " ", text)

        # Remove excessive blank lines
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text
    
    def remove_front_matter(self, text):
        """
        Remove common non-content sections such as
        cover pages and table of contents.
        """

        patterns = [
            r"Table of Contents.*?(?=1\.\s)",
            r"List of Figures.*?(?=1\.\s)",
            r"List of Tables.*?(?=1\.\s)"
        ]
        
        for pattern in patterns:
            text = re.sub(pattern, "", text, flags=re.DOTALL | re.IGNORECASE)


        return text