#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
Created on 18.01.2021

@author: michael
"""

from PIL import Image
from PyPDF2.pdf import PdfFileReader
import tempfile
import os
from subprocess import call


class PdfProcessingError(Exception):
    pass


class PdfInput:
    
    def __init__(self, filename):
        self.filename = filename
        self.stream = open(filename, "rb")
        self.pdf_reader = PdfFileReader(self.stream)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        self.stream.close()

    def get_number_of_pages(self):
        return self.pdf_reader.getNumPages()

    def get_page_text(self, pageno):
        page = self.pdf_reader.getPage(pageno - 1)
        return page.extractText()
    
    def get_page_image(self, pageno):
        with tempfile.NamedTemporaryFile("wb") as tmp_file:
            with self._open_page_image(pageno, tmp_file.name) as image:
                image.load()
                return image

    def _open_page_image(self, pageno, image_file):
        with open(os.devnull, 'wb') as devnull:
            return_value = call(["gs",
                                 "-sDEVICE=png16m",
                                 "-dNOPAUSE",
                                 "-dFirstPage={}".format(pageno),
                                 "-dLastPage={}".format(pageno),
                                 "-sOutputFile={}".format(image_file),
                                 "-r300",
                                 "-q",
                                 self.filename,
                                 "-c",
                                 "quit"],
                                stdout=devnull,
                                stderr=devnull)

        if return_value != 0:
            raise PdfProcessingError()

        return Image.open(image_file)


if __name__ == '__main__':
    loader = PdfInput("../test/testdata/Test-Grüne001.pdf")
    img = loader.get_page_image(2)
    img.show()