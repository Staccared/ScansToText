'''
Created on 18.01.2021

@author: michael
'''
import unittest
import os
from scanstotext.StaccaredProject import ProjectInitializer


class ProjectInitializerTest(unittest.TestCase):

    def setUp(self):

        self.testfile_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testdata')
        self.testfile_name = os.path.join(self.testfile_dir, 'Test-Grüne001.pdf')

    def testInitializer(self):
        
        initializer = ProjectInitializer()
        project = initializer.initialize(self.testfile_name)
        self.assertEqual(1, len(project.files))
        self.assertEqual(1, len(project.texts))
        self.assertEqual(3, len(project.texts[0].textblocks))
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()