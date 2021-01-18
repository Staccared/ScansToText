#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
Created on 18.01.2021

@author: michael
"""

import unittest
import os
import tempfile
from scanstotext.PdfInput import PdfInput


class TestPdfInput(unittest.TestCase):
    def setUp(self):
        self.testfile_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testdata')
        self.testfile_name = os.path.join(self.testfile_dir, 'Test-Grüne001.pdf')
        self.pdf_input = PdfInput(self.testfile_name)

    def tearDown(self):
        self.pdf_input.close()

    def test_get_number_of_pages(self):
        self.assertEqual(3, self.pdf_input.get_number_of_pages())

    def test_get_page_text(self):
        text = self.pdf_input.get_page_text(1)
        self.assertEqual("DER FALL ECKHARDT WI", text[0:20])
        text = self.pdf_input.get_page_text(2)
        self.assertEqual("Am Tribunal dor 'Alt", text[0:20])
        text = self.pdf_input.get_page_text(3)
        self.assertEqual("Verden, Ganz anders ", text[0:20])

    def test_get_page_image(self):
        img = self.pdf_input.get_page_image(1)
        self.assertIsNotNone(img)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as temp_file:
            img.save(temp_file.name)
            self.assertGreater(os.path.getsize(temp_file.name), 0)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()