# Copyright (c) 2008, Robert Ramirez
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
from asdox import asBuilder

class PackageParsingTestCase(unittest.TestCase):
    
    def setUp(self):
        self.builder = asBuilder.Builder()
    
    def tearDown(self): 
        self.builder = None
    
# Test for (empty) a.k.a. Anonymouse package name

    def testUnnamedPackage(self):
        
        "Test for unamed package"
        self.builder.addSource("package {}") #build unamed package
        unamedPackage = self.builder.getPackage("").getName() #get package name
        classCount = len(self.builder.getPackage("").getClasses()) # number of classe declarations inside the package
	includeCount = len(self.builder.getPackage("").getIncludes()) #number of included declarations inside the package
	importCount = len(self.builder.getPackage("").getImports()) # number of import statements inside the package	
	namespaceCount = len(self.builder.getPackage("").getNamespaces()) # number if namespace declarations inside the package definition
	interfaceCount = len(self.builder.getPackage("").getInterfaces()) # number of interface definitions inside the package definiton
	#STUB variableCount = len(self.builder.getPackage(self,"").getVariables()) #number of variable declarations inside the package defintion
	#STUB functionCount = len(self.builder.getPackage(self,"").getFunctions()) #number of variable declarations inside the package defintion
	
#unit tests  definitons	
        self.assertEqual(unamedPackage,"","package name is not blank") #test unamed package
        self.assertEqual(classCount,0,"package contains one or more class declarations") # test for zero class declarations inside a package declaration
	self.assertEqual(includeCount,0,"package contains one or more include directives") # test for zero include directives inside a package dclaration
	self.assertEqual(importCount,0,"package contains one or more import statements") #test for zero import statements inside a package declaration
	self.assertEqual(namespaceCount,0,"package contains one or more namespace definitions") #test for zero namespace declarations inside a package definition
	#STUB self.assertEqual(variableCount,0,"package contains one or more variable declarations") #test for zero variable declarations inside a package definition
	#STUB self.assertEqual(funtionCount,0,"package contains one or more funtion declarations") #test for zero function definitions inside a package definition
	
# Tests the sequence of characters (namespace) that makeup of the package name
# e.g "package mx.core: namespace would be "mx.core"
    
    def testPackageNamespace(self):
        pass
    
# Test for dot(.) delimited package name
# e.g com.gurufaction.MyClass
    
    def testNestedPackageName(self):
        pass

if __name__ == "__main__": #allows you to run from console or command line
	unittest.main()