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
		self.assertEqual(result.getName(),expected.getName())
		self.assertEqual(result.getType(),expected.getType())
		self.assertEqual(result.getImports(),expected.getImports())
	def clsTest(self,result,expected):
		self.assertEqual(result.__class__,expected.__class__)
		self.assertEqual(result.getName(),expected.getName())
		self.assertEqual(result.getType(),expected.getType())
		self.assertEqual(result.getModifiers(),expected.getModifiers())
		self.assertEqual(result.getIncludes(),expected.getIncludes())
		self.assertEqual(result.isInterface(),expected.isInterface())
	def metaTest(self,result,expected):
		self.assertEqual(result.getName(),expected.getName())
		self.assertEqual(result.getParams(),expected.getParams())
class ClassDefinitionTestCase(BaseDefinitionTestCase):
	def testClassMetaData(self):
		self.builder.addSource("""
		package test{
			[Nothing]
			[Event(name="myEnableEvent", other="flash.events.Event")]
			[Test(true)]
			public class MyClass
			{
			}
		}
		""")
		
		result = self.builder.parseSource()
		expected = asModel.ASPackage("test")
		cls = asModel.ASClass("MyClass")
		cls.addModifier("public")
		cls.addMetaTag( asModel.ASMetaTag("Bindable") )
		expected.addClass(cls)
		event = asModel.ASMetaTag("Event")
		event.addParam(True)
		event.addParam("myEnableEvent","name")
		event.addParam("flash.events.Event","type")
		expected.getClass("MyClass").addMetaTag( event )
		self.assertEqual(len(result),1)
		self.pkgTest(result[0],expected)
		self.assertEqual(len(result[0].getClass("MyClass").getMetaTags()),3)
		self.metaTest(result[0].getClass("MyClass").getMetaTag("Bindable"),expected.getClass("MyClass").getMetaTag("Bindable"))
		self.metaTest(result[0].getClass("MyClass").getMetaTag("Event"),expected.getClass("MyClass").getMetaTag("Event"))
		self.metaTest(result[0].getClass("MyClass").getMetaTag("Test"),expected.getClass("MyClass").getMetaTag("Test"))
class PackageDefinitionTestCase(BaseDefinitionTestCase):
	
	def testDefaultPackage(self):
		self.builder.addSource("""
		package
		{
		}
		""")
		
		result = self.builder.parseSource()
		self.assertEqual(len(result),1)
		
		expected = asModel.ASPackage("");
		self.pkgTest(result[0],expected)
	def testPackage(self):
		self.builder.addSource("""
		package net.test.test
		{
		}
		""")
		
		result = self.builder.parseSource()
		self.assertEqual(len(result),1)
		expected = asModel.ASPackage("net.test.test");
		self.pkgTest(result[0],expected)
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
		self.assertEqual(len(result),3)
		
		expected = asModel.ASPackage("com.google.code.test");
		self.pkgTest(result[0],expected)
		expected = asModel.ASPackage("com.gurufaction.asDox");
		self.pkgTest(result[1],expected)
		expected = asModel.ASPackage("");
		self.pkgTest(result[2],expected)
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
		
		self.assertEqual( len(result),1)
		
		expected = asModel.ASPackage("com.gurufaction.mypackage");
		self.pkgTest(result[0],expected)
		
		cls = asModel.ASClass("MyClass");
		cls.addModifier("public")
		cls.addInclude("file1.as")
		cls.addInclude("file2.as")
		self.clsTest(result[0].getClass("MyClass"),cls)
if __name__ == "__main__":
	unittest.main()