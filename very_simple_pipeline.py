
from scanstotext.StaccaredProject import PdfInput
from scanstotext.Tesseract import Tesseract
from optparse import OptionParser
import string
import random
import json
import sys


def main():
    input_file = get_opts()
    file_id = get_random_string(8)

    texts = []

    pdf_texts = extract_pdf_texts(input_file)
    texts.extend(pdf_texts)

    ocr_tesseract_texts = extract_ocr_tesseract_texts(input_file)
    texts.extend(ocr_tesseract_texts)

    file = {
        "filename": input_file,
        "file_id": file_id,
        "texts": texts
    }

    result = [file]

    print(json.dumps(result, indent=2, ensure_ascii=False))


def extract_pdf_texts(input_file):
    with PdfInput(input_file) as loader:
        pdf_texts = []
        for page_no in range(1, loader.get_number_of_pages() + 1):
            pdf_text = loader.get_page_text(page_no)
            pdf_texts.append(new_text(page_no, "PDF_TEXT", pdf_text))
        return pdf_texts


def extract_ocr_tesseract_texts(input_file):
    texts = []
    with PdfInput(input_file) as loader:
        for page in range(1, loader.get_number_of_pages() + 1):
            with loader.get_page_png_file(page) as page_image_file:
                print("tesseract...", file=sys.stderr)
                text = Tesseract().extract_text(page_image_file.name)
                texts.append(new_text(page, "OCR_TESSERACT_TEXT", text))
    return texts


def new_text(page, source, text):
    return {
        "page": page,
        "source": source,
        "text": text
    }


def get_opts():
    parser = OptionParser(usage="Usage: %prog <input-pdf>")
    (options, args) = parser.parse_args()

    if len(args) < 1:
        parser.error("Incorrect number of arguments")

    input_file = args[0]

    return input_file


def get_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.sample(letters, length))


if __name__ == '__main__':
    main()
