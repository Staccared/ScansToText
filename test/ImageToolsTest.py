'''
Created on 17.01.2021

@author: michael
'''
import unittest
from PIL import ImageChops
import os
from ImageTools import pil_to_numpy, numpy_to_pil, load

class ImageToolsTest(unittest.TestCase):

    def setUp(self):
        self.testfile_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testdata')

    def testNumpyConversion(self):

        testfile_name = os.path.join(self.testfile_dir, "Color.tif")
        image = load(testfile_name)
        self.assertEquals(image.mode, "L")

    def testLoad(self):
        
        testfile_name = os.path.join(self.testfile_dir, "Test1.tif")

        image = load(testfile_name)
        numpy_image = pil_to_numpy(image)
        image2 = numpy_to_pil(numpy_image)
        
        diff = ImageChops.difference(image, image2)

        self.assertFalse(diff.getbbox())

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()