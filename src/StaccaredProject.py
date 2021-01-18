'''
Created on 18.01.2021

@author: michael
'''
from FileLoader import PdfLoader

TEXTDATA = 1
CONTAINER = 2

class StaccaredProject:
    
    def __init__(self, files, texts):
        
        self.files = files
        self.texts = texts

class File:
    
    def __init__(self, filename, file_id):
        
        self.filename = filename
        self.file_id = file_id
        self.type = TEXTDATA

class MetadataEntity:
    
    def __init__(self):
        
        self.text_reprentation
        self.gnd_id
        self.wiki_data_id
        self.occurencies
        self.confidentiality
        
class Metadata:
    
    def __init__(self):
        
        self.geographica = []
        self.personen = []
        self.koerperschaften = []
        self.sachbegriffe = []
        
class TextBlock:
    
    def __init__(self, file_id, page_no, text):
        
        self.file_id = file_id
        self.page_no = page_no
        self.text = text
        self.metadata = Metadata()
        
class Text:
    
    def __init__(self):
        
        self.textblocks = []
        self.metadata = Metadata()
        
    def add_textblock(self, textblock):
        
        self.textblocks.append(textblock)

    def _get_text(self):
        
        text = ""
        for textblock in self.textblocks:
            text = "%s %s" % (text, textblock.text)
            
    text = property(_get_text)

class ProjectInitializer:
    
    def initialize(self, filename):
        
        file_id = 1
        file = File(filename, file_id)

        # Currently we support only one pdf-file
        loader = PdfLoader(filename)
        text = Text()
        for page_no in range(1, loader.get_number_of_pages() + 1):
            textblock = TextBlock(file_id, page_no, loader.get_page_text(page_no))
            text.add_textblock(textblock)
        return StaccaredProject((file,), (text,))
            

if __name__ == '__main__':
    pass