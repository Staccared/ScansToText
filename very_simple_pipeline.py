
from scanstotext.StaccaredProject import PdfInput
from optparse import OptionParser
import string
import random
import json


def main():
    input_file = get_opts()
    file_id = get_random_string(8)

    texts = []

    # Currently we support only one pdf-file
    pdf_texts = extract_pdf_texts(input_file)
    texts.extend(pdf_texts)

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
            pdf_texts.append({
                "page": page_no,
                "source": "PDF_TEXT",
                "text": pdf_text
            })
        return pdf_texts


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
