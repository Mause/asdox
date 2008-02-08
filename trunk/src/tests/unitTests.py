# Copyright (c) 2008, Michael Ramirez
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without 
# modification are permitted provided that the following conditions are met:
#   * Redistributions of source code must retain the above copyright notice, 
#     this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice, 
#     this list of conditions and the following disclaimer in the documentation 
#     and/or other #materials provided with the distribution.
#   * Neither the name of the <ORGANIZATION> nor the names of its contributors 
#     may be used to endorse or promote products derived from this software 
#     without specific #prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import unittest,sys,os
sys.path.append( os.path.abspath('../') )
from asdox import asBuilder,asModel

class ParseUnNamedPackageTestCase(unittest.TestCase):
    
    def setUp(self):
        self.builder = asBuilder.Builder()
        self.builder.addSource("""
                                package  {
                                
                                }
        
                               """)
        
    def tearDowm(self):
        pass
    
    def testParseUnNamedPackage(self):
        
        self.assertEqual(self.builder.getPackage("").getName(),"","Unable to parse unnamed package")
        
class ParseNamedPackgeTestCase(unittest.TestCase):
    
    def setUp(self):
        
        self.builder = asBuilder.Builder()
        self.builder.addSource("""
                                package mypackage{
                                
                                }
        
                               """)
    
    def tearDown(self):
        pass
    
    def testParseNamedPackage(self):
        
        self.assertEqual(self.builder.getPackage("mypackage").getName(),"mypackage"," parsere did not find package named 'mypackage'")
        
class ParseClassDefinitionTestCase(ParseUnNamedPackageTestCase):
    
    def setUp(self):
        
        self.builder = asBuilder.Builder()
        self.builder.addSource("""
                                package {
                                 class Mylass{}
                                }
        
                               """)

    def tearDown(self):
        pass
    
    def testParseClassDefinition(self):
    
        #testUnamedPackageTestCase = unittest.FunctionTestCase(self.testParseUnNamedPackage)
    
        self.assertEqual(self.builder.getClass("MyClass").getName(),"MyClass","Parser was unable to get class name")
        
        
        
#run at commandline
if __name__ == '__main__':
    unittest.main()