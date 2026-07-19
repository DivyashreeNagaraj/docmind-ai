from app.ingestion.document_loader import DocumentLoader
from app.preprocessing.text_preprocessor import TextPreprocessor


def main():
    loader = DocumentLoader()
    preprocessor = TextPreprocessor()

    document = loader.load_pdf("data/raw/sample.pdf")
    clean_text = preprocessor.clean(document["text"])

    print(f"Filename : {document['filename']}")
    print(f"Pages    : {document['pages']}")
    print(f"Characters: {len(document['text'])}")

    print("\nPreview:\n")
    print(clean_text[:500])

if __name__ == "__main__":
    main()