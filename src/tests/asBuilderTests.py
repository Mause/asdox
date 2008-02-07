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
from asdox import asModel,asBuilder

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
			[Bindable]
			[Event(name="myEnableEvent", type="flash.events.Event")]
			public class MyClass
			{
			}
		}
		""")
		
		result = self.builder.getPackage("test")
		expected = asModel.ASPackage("test")
		cls = asModel.ASClass("MyClass")
		cls.addModifier("public")
		cls.addMetaTag( asModel.ASMetaTag("Bindable") )
		expected.addClass(cls)
		event = asModel.ASMetaTag("Event")
		event.addParam("myEnableEvent","name")
		event.addParam("flash.events.Event","type")
		expected.getClass("MyClass").addMetaTag( event )
		#self.assertEqual(len(result),1)
		self.pkgTest(result,expected)
		self.assertEqual(len(result.getClass("MyClass").getMetaTags()),2)
		self.metaTest(result.getClass("MyClass").getMetaTag("Bindable"),expected.getClass("MyClass").getMetaTag("Bindable"))
		self.metaTest(result.getClass("MyClass").getMetaTag("Event"),expected.getClass("MyClass").getMetaTag("Event"))
class PackageDefinitionTestCase(BaseDefinitionTestCase):
	
	def testDefaultPackage(self):
		self.builder.addSource("""
		package
		{
		}
		""")
		
		result = self.builder.getPackage("")
		#self.assertEqual(len(result),1)
		
		expected = asModel.ASPackage("");
		self.pkgTest(result,expected)
	def testPackage(self):
		self.builder.addSource("""
		package net.test.test
		{
		}
		""")
		
		result = self.builder.getPackage("net.test.test")
		#self.assertEqual(len(result),1)
		expected = asModel.ASPackage("net.test.test");
		self.pkgTest(result,expected)
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
		
		result = self.builder.getPackages()
		#self.assertEqual(len(result),3)
		
		expected = asModel.ASPackage("com.google.code.test");
		self.pkgTest(result["com.google.code.test"],expected)
		expected = asModel.ASPackage("com.gurufaction.asDox");
		self.pkgTest(result["com.gurufaction.asDox"],expected)
		expected = asModel.ASPackage("");
		self.pkgTest(result[""],expected)
	def testPackageWithClass(self):
		self.builder.addSource("""
		package com.gurufaction.mypackage
		{
			public class MyClass
			{
				include "file1.as"
				include "file2.as"
				public var test:String;
			}
		}
		""")
		
		result = self.builder.getPackage("com.gurufaction.mypackage")
		self.assertNotEqual( result,None)
		
		expected = asModel.ASPackage("com.gurufaction.mypackage");
		self.pkgTest(result,expected)
		
		cls = asModel.ASClass("MyClass");
		cls.addModifier("public")
		cls.addInclude("file1.as")
		cls.addInclude("file2.as")
		self.clsTest(result.getClass("MyClass"),cls)
if __name__ == "__main__":
	unittest.main()