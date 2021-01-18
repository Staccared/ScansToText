'''
Created on 18.01.2021

@author: michael
'''
import unittest
import os
from FileLoader import PdfLoader


class PdfLoaderTest(unittest.TestCase):

    def setUp(self):

        self.testfile_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testdata')
        self.testfile_name = os.path.join(self.testfile_dir, 'Test-Grüne001.pdf')
        self.loader = PdfLoader(self.testfile_name)

    def testNumberOfPages(self):
        
        self.assertEqual(3, self.loader.get_number_of_pages())
        
    def testGetText(self):

        text = self.loader.get_page_text(1)
        self.assertEqual("DER FALL ECKHARDT WI", text[0:20])
        text = self.loader.get_page_text(2)
        self.assertEqual("Am Tribunal dor 'Alt", text[0:20])
        text = self.loader.get_page_text(3)
        self.assertEqual("Verden, Ganz anders ", text[0:20])
        
    def testGetImage(self):
        
        img = self.loader.get_page_image(1)
        self.assertTrue(img is not None)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()