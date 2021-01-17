'''
Created on 17.01.2021

@author: michael
'''
import cv2 as cv

from skimage.filters import (threshold_sauvola)
from ImageTools import load, pil_to_numpy, numpy_to_pil

class BinarizationError(Exception):
    
    pass

class Binarazer:
    '''
    There are several algorithms for binarization:
    - simple threshold: Needs to be adapted depending on paper etc. Not very effective
    - Otsu's algorithm: Works quiet well, but uses one threshold value for the whole
      document. Works well, if there is no different lighting - so the problem are creases,
      for example, where the scanner light produces shadows
    - Niblack's algorithm: Determines local thresholds. Not recommended for OCR binarization,
      because it tries to rasterize the paper if it is not white
    - Sauvola's algorithm: Best result until now.
    - Shafait's algorithm: The newest one (2008) No Python implementation found yet and
      therefore not tested.
    '''
    
    def convert_to_bitmap(self, image):
        
        return self._binarization_sauvola(image)
    
    def _binarization_fixed(self, img, threshold=127):

        used_threshold, binary_image = cv.threshold(pil_to_numpy(img),threshold,255,cv.THRESH_BINARY)
        return numpy_to_pil(binary_image)
    
    def _binarization_otsu(self, img):

        used_threshold, binary_image = cv.threshold(pil_to_numpy(img),127,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
        return numpy_to_pil(binary_image)

    def _binarization_sauvola(self, image, window_size=41):

        ndarray = pil_to_numpy(image)
        mask = threshold_sauvola(ndarray, window_size=window_size)
        binary_image = ndarray > mask
        return numpy_to_pil(binary_image)

if __name__ == '__main__':
    
    image = load("../test/testdata/Test1.tif")
    binarizer = Binarazer()
    image = binarizer.convert_to_bitmap(image)
    image.show()
