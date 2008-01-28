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
import unittest,asBuilder,asModel,os.path,sys

class BaseDefinitionTestCase(unittest.TestCase):
	def setUp(self):
		self.builder = asBuilder.Builder()
	def tearDown(self):
		pass
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
	def metaTest(self,result,expected):
		self.assertEqual(result.name,expected.name)
		self.assertEqual(result.attributes,expected.attributes)
class ClassDefinitionTestCase(BaseDefinitionTestCase):
	def xtestClassMetaData(self):
		self.builder.addSource("""
		[Bindable]
		[Event(name="myEnableEvent", type="flash.events.Event")]
		[Test(true)]
		public class MyClass
		{
		}
		""")
		
		result = self.builder.parseSource()
		expected = asModel.ClassDef("MyClass")
		expected.modifiers.add("public")
		expected.metadata.append( asModel.MetaDataDef("Bindable") )
		event = asModel.MetaDataDef("Event")
		event.attributes = {0:True,"name":"myEnableEvent","type":"flash.events.Event"}
		expected.metadata.append( event )
		self.assertEqual(len(result),1)
		self.clsTest(result[0][0],expected)
		self.assertEqual(len(result[0][0].metadata),3)
		self.metaTest(result[0][0].metadata[0],expected.metadata[0])
		self.metaTest(result[0][0].metadata[1],expected.metadata[1])
		self.metaTest(result[0][0].metadata[2],expected.metadata[2])
class PackageDefinitionTestCase(BaseDefinitionTestCase):
	
	def testDefaultPackage(self):
		self.builder.addSource("""
		package
		{
		}
		""")
		
		result = self.builder.parseSource()
		self.assertEqual(len(result[0]),1)
		
		expected = asModel.PackageDef("","package");
		self.pkgTest(result[0][0],expected)
	def testPackage(self):
		self.builder.addSource("""
		package net.test.test
		{
		}
		""")
		
		result = self.builder.parseSource()
		self.assertEqual(len(result),1)
		expected = asModel.PackageDef("net.test.test","package");
		self.pkgTest(result[0][0],expected)
	def testMultiPackages(self):
		self.builder.addSource("""
		package com.google.code.test
		{
		}
		
		package com.gurufaction.asDox
		{
		}
		
		package
		{
		}
		""")
		
		result = self.builder.parseSource()
		self.assertEqual(len(result[0]),3)
		
		expected = asModel.PackageDef("com.google.code.test","package");
		self.pkgTest(result[0][0],expected)
		expected = asModel.PackageDef("com.gurufaction.asDox","package");
		self.pkgTest(result[0][1],expected)
		expected = asModel.PackageDef("","package");
		self.pkgTest(result[0][2],expected)
	def testPackageWithClass(self):
		self.builder.addSource("""
		package com.gurufaction.mypackage
		{
			public class MyClass
			{
				include "file1.as"
				include "file2.as"
			}
		}
		""")
		
		result = self.builder.parseSource()
		
		self.assertEqual( len(result[0]),1)
		
		expected = asModel.PackageDef("com.gurufaction.mypackage","package");
		self.pkgTest(result[0][0],expected)
		
		self.assertEqual(len(result[0][0].classes),1)
		expected = asModel.ClassDef("MyClass","class");
		expected.modifiers.add("public")
		expected.includes = set(["file1.as","file2.as"])
		self.clsTest(result[0][0].classes[0],expected)
if __name__ == "__main__":
	unittest.main()