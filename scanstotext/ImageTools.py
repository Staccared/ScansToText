'''
Created on 17.01.2021

@author: michael
'''
import numpy
import cv2 as cv
from PIL import Image

def pil_to_numpy(imageg):

    return numpy.array(imageg)

def numpy_to_pil(ndarray):
    
    return Image.fromarray(ndarray)

def load(filename):
    '''
    We use our own load method. We only want to deal
    with grayscale or black and white images, so we convert
    all other images to grayscale.
    '''
    image = Image.open(filename)
    if image.mode != "1" and image.mode != "L":
        return image.convert("L")
    return image
