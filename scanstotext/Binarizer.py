"""
Created on 17.01.2021

@author: michael
"""

import cv2 as cv
import numpy
from skimage.filters import (threshold_sauvola)
from optparse import OptionParser
from scanstotext.ImageTools import load, pil_to_numpy, numpy_to_pil
from pickle import TRUE


class Binarizer:
    """
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
    """
    
    def convert_to_bitmap(self, image):
        
        nd_array = pil_to_numpy(image)
        
        bw_array = self._binarization_sauvola(nd_array)
        denoised_array = self._denoise_image(bw_array)
        
        return numpy_to_pil(denoised_array)
    
    def _binarization_fixed(self, nd_array, threshold=127):

        used_threshold, bw_array = cv.threshold(nd_array,threshold,255,cv.THRESH_BINARY)
        return bw_array
    
    def _binarization_otsu(self, nd_array):

        used_threshold, binary_image = cv.threshold(nd_array,127,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
        return binary_image

    def _binarization_sauvola(self, nd_array, window_size=25):

        mask = threshold_sauvola(nd_array, window_size=window_size)
        return nd_array > mask
    
    def _denoise_image(self, bw_array, threshold=10):
        '''
        This is quite complicated because connectedComponentsWithStats is not
        very well documented.
        
        First of all we need a numeric array - the input to the method is a boolean array.
        And then we need to invert the image, because connectedComponentsWithStats
        treats black (1) as background and white (0) as components.
        
        Components are shapes that form an area. The connectivity parameter
        denotes what is considered as connection. If the value is 4, only the pixels
        left, right, top and bottom are considered, if it is 8, also the
        diagonals are included.
        
        The result array is quite confusing:
        no_of_components: The exact number of found shapes + 1 (for the
            background)
        labels: Each shape gets a unique identifier, where the identifiers
            are just numbers, counting up from 1 (0 is the background, so we
            exclude it in the loop, just in case you were wondering). labels
            itself is an array with the same dimension as the input image. And
            in each cell there is the number of the identifier of the shape
            this cell belongs to
        stats: This is an array of length no_of_components and contains
            statistical information for each share. We are only interested
            in the size which is accessible through CC_STAT_AREA.
        centroids: Does not interest us
        
        Then something to the numpy indexing with boolean values like
        array1[array2 == black]. This means if array1 and array2 are
        two arrays with the same dimensions, then select all array elements
        from array1 where the array element in array2 with the same
        indexes matches the condition.
        
        The obvious algorithm is to loop over all shapes and clean up the
        small shapes is sadly not very efficient, because there are quite
        a lot of small shapes.
        So it makes sense to use a blank sheet and add all the big shapes,
        this is much faster. Why I need to initialize the sheet with 1s (black)
        and add the shapes as white I can't understand. But that's how
        it works.
        
        '''
        black = 1
        white = 0
        inverted = numpy.ones((bw_array.shape), dtype=numpy.uint8)
        inverted[bw_array == black] = white
        
        connectivity = 8
        no_of_components, labels, stats, centroids = cv.connectedComponentsWithStats(inverted, connectivity, cv.CV_32S)
        sizes = stats[:, cv.CC_STAT_AREA];

        # Why initializing with ones?
        bw_new = numpy.ones((bw_array.shape), dtype=numpy.bool)
        for shape_identifier in range(1, no_of_components):
            if sizes[shape_identifier] > threshold:
                # I really do not understand why I need bool_white
                # and not bool_black. I'm giving up.
                bw_new[labels == shape_identifier] = white
        
        return bw_new


def main():
    (input_file, output_file, show) = get_opts()
    image = load(input_file)
    binarizer = Binarizer()
    image = binarizer.convert_to_bitmap(image)
    if output_file is not None:
        if output_file == '-':
            image.save(output_file)
        else:
            image.save(output_file)
    if show:
        image.show()


def get_opts():
    parser = OptionParser(usage="Usage: %prog [options] <input-file> [output-file]")
    parser.add_option("-s", "--show",
                      dest="show",
                      action="store_true",
                      default=False,
                      help="Show image when done")
    (options, args) = parser.parse_args()

    if len(args) < 1:
        parser.error("Incorrect number of arguments")

    input_file = args[0];

    if len(args) > 1:
        output_file = args[1]
    else:
        output_file = None;

    return input_file, output_file, options.show


if __name__ == '__main__':
    main()
