
from scanstotext.StaccaredProject import File, PdfInput, Text, TextBlock, StaccaredProject
from optparse import OptionParser
import string
import random
import json

def main():
    input_file = get_opts()
    file_id = get_random_string(8)

    file = {
        "filename": input_file,
        "file_id": file_id
    }

    # Currently we support only one pdf-file
    loader = PdfInput(input_file)
    text_blocks = []
    for page_no in range(1, loader.get_number_of_pages() + 1):
        page_text = loader.get_page_text(page_no);
        text_blocks.append({
            "page": page_no,
            "text": page_text
        })

    file["text_blocks"] = text_blocks;

    result = [file]

    print(json.dumps(result, indent=2, ensure_ascii=False))


def get_opts():
    parser = OptionParser(usage="Usage: %prog <input-pdf>")
    (options, args) = parser.parse_args()

    if len(args) < 1:
        parser.error("Incorrect number of arguments")

    input_file = args[0];

    return input_file


def get_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.sample(letters, length))


if __name__ == '__main__':
    main()
