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
import unittest,asBuilder,asModel

class BaseDefinitionTestCase(unittest.TestCase):
	def setUp(self):
		self.builder = asBuilder.Builder()
	def pkgTest(self,result,expected):
		self.assertEqual(result.__class__,expected.__class__)
		self.assertEqual(result.name,expected.name)
		self.assertEqual(result.type,expected.type)
		self.assertEqual(result.imports,expected.imports)
	def clsTest(self,result,expected):
		self.assertEqual(result.__class__,expected.__class__)
		self.assertEqual(result.name,expected.name)
		self.assertEqual(result.type,expected.type)
		self.assertEqual(result.modifiers,expected.modifiers)
		self.assertEqual(result.includes,expected.includes)
		self.assertEqual(result.isInterface(),expected.isInterface())
class PackageDefinitionTestCase(BaseDefinitionTestCase):
	
	def testDefaultPackage(self):
		source = """
		package
		{
		}
		"""
		
		result = self.builder.parseString(source)
		self.assertEqual(len(result),1)
		
		expected = asModel.PackageDef("","package");
		self.pkgTest(result[0],expected)
	def testPackage(self):
		source = """
		package net.test.test
		{
		}
		"""
		
		result = self.builder.parseString(source)
		self.assertEqual(len(result),1)
		expected = asModel.PackageDef("net.test.test","package");
		self.pkgTest(result[0],expected)
	def testMultiPackages(self):
		source="""
		package com.google.code.test
		{
		}
		
		package com.gurufaction.asDox
		{
		}
		
		package
		{
		}
		"""
		
		result = self.builder.parseString(source)
		self.assertEqual(len(result),3)
		
		expected = asModel.PackageDef("com.google.code.test","package");
		self.pkgTest(result[0],expected)
		expected = asModel.PackageDef("com.gurufaction.asDox","package");
		self.pkgTest(result[1],expected)
		expected = asModel.PackageDef("","package");
		self.pkgTest(result[2],expected)
	def testPackageWithClass(self):
		source = """
		package com.gurufaction.mypackage
		{
			public class MyClass
			{
				include "file1.as"
				include "file2.as"
			}
		}
		"""
		
		result = self.builder.parseString(source)
		self.assertEqual( len(result),1)
		
		expected = asModel.PackageDef("com.gurufaction.mypackage","package");
		self.pkgTest(result[0],expected)
		
		self.assertEqual(len(result[0].classes),1)
		expected = asModel.ClassDef("MyClass","class");
		expected.modifiers.add("public")
		expected.includes = set(["file1.as","file2.as"])
		self.clsTest(result[0].classes[0],expected)
if __name__ == "__main__":
	unittest.main()