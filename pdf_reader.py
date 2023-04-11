# extract_doc_info.py
from pathlib import Path

from PyPDF2 import PdfReader
from pdfminer.high_level import extract_text


def extract_information(pdf_path):
    with open(pdf_path, 'rb') as f:
        return PdfReader(f).metadata


def words_in_pdf(pdf_path):
    text = extract_text(pdf_path)

    # Split text by newlines
    lines = text.splitlines()

    # Remove empty lines
    lines = [line for line in lines if line.strip()]

    # Count the words in all the lines
    words = [len(line.split()) for line in lines]

    return sum(words)


if __name__ == '__main__':
    pdfs_dir = Path('judgement_pdfs')

    words = []
    for pdf_path in pdfs_dir.glob('*.pdf'):
        try:
            pdf_words = words_in_pdf(pdf_path)
            print(f"PDF: {pdf_path} Words: {pdf_words}")
            words.append(pdf_words)
        except Exception as e:
            print(f"Error processing {pdf_path}: {e}")

    # Plot a histogram of the words in each PDF
    import matplotlib.pyplot as plt

    plt.hist(words)
