'''
Created on 18.01.2021

@author: michael
'''
from PIL import Image
from PyPDF2.pdf import PdfFileReader
import tempfile
import os
from subprocess import call

class LoadError(Exception):
    
    pass

class PdfLoader:
    
    def __init__(self, filename):

        self.filename = filename
        self.pdf_reader = PdfFileReader(open(filename, "rb"))
    
    def get_number_of_pages(self):
        
        return self.pdf_reader.getNumPages()

    def get_page_text(self, pageno):

        page = self.pdf_reader.getPage(pageno - 1)
        return page.extractText()
    
    def get_page_image(self, pageno):
        
        tmp_file = tempfile.NamedTemporaryFile("wb")
        path = tmp_file.name
        tmp_file.close()
        
        stdio = open(os.devnull, 'wb')
        return_value = call(["gs",
                             "-sDEVICE=png16m",
                             "-dNOPAUSE", "-dFirstPage=%d" % pageno,
                             "-dLastPage=%d" % pageno,
                             "-sOutputFile=%s" % path,
                             "-r300",
                             "-q",
                             self.filename,
                             "-c",
                             "quit"],
                            stdout=stdio,
                            stderr=stdio)
        
        if return_value != 0:
            try:
                os.unlink(path)
            except:
                pass
            raise LoadError()
        
        img = Image.open(path)
        os.unlink(path)
        return img
        
if __name__ == '__main__':
    loader = PdfLoader("../test/testdata/Test-Grüne001.pdf")
    img = loader.get_page_image(2)
    img.show()