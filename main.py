from app.ingestion.document_loader import DocumentLoader


def main():
    loader = DocumentLoader()

    document = loader.load_pdf("data/raw/sample.pdf")

    print(f"Filename : {document['filename']}")
    print(f"Pages    : {document['pages']}")
    print(f"Characters: {len(document['text'])}")

    print("\nPreview:\n")
    print(document["text"][:500])


if __name__ == "__main__":
    main()