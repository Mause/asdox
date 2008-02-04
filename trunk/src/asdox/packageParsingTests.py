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

import unittest,asBuilder

class PackageParsingTestCase(unittest.TestCase):
    
    def setup(self):
        builder =asBuilder.Builder()
    
    def teardown(self): 
        builder = null
    
# Test for (empty) a.k.a. Anonymouse package name

    def testUnnamedPackage(self):
        builder.addSource("package {}") #build unamed package
        unamedPackage = builder.getPackage("") #get package name
        
        self.assertEquals(unamedPackage,"") #test unamed package
    
# Tests the sequence of characters (namespace) that makeup of the package name
# e.g "package mx.core: namespace would be "mx.core"
    
    def testPackageNamespace(self):
        pass
    
# Test for dot(.) delimited package name
# e.g com.gurufaction.MyClass
    
    def testNestedPackageName(self):
        pass

# Test package declaration for class,interface,function, and namespace
# member definitions
    
    def testPackageMembers(self):
        pass