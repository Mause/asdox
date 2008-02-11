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

class BaseTestCase(unittest.TestCase):
	def setUp(self):
		self.builder = asBuilder.Builder()
	def tearDown(self):
		pass
class ASClassTestCase(BaseTestCase):
	def testClass(self):
		self.builder.addSource("""
		package com.gurufaction.mypackage
		{
			public class MyClass
			{
				
			}
		}
		""")
		
		self.assertEqual(self.builder.hasPackage("com.gurufaction.mypackage"),True,"Package 'com.gurufaction.mypackage' not found.")
		pkg = self.builder.getPackage("com.gurufaction.mypackage")
		self.assertEqual(pkg.hasClass("MyClass"),True,"Class 'MyClass' not found in package.")
		cls = pkg.getClass("MyClass")
		self.assertEqual(cls.getName(),"MyClass","Class name not equal to 'MyClass'.")
		self.assertEqual(cls.getType(),"class","Class type not equal to 'class'.")
		self.assertEqual(cls.isPublic(),True,"Class is not public")
		self.assertEqual(cls.getName(),"MyClass","Class name not equal to 'MyClass'.")
		self.assertEqual(cls.isDynamic(),False,"Class should not be dynamic.")
		self.assertEqual(cls.isFinal(),False,"Class should not be final.")
		self.assertEqual(len(cls.getFields()),0,"Class should contain no fields.")
		self.assertEqual(len(cls.getMethods()),0,"Class should contain no methods.")
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
		# Test Package 'test'
		self.assertEqual(self.builder.hasPackage("test"),True,"Package 'test' not found.")
		pkg = self.builder.getPackage("test")
		self.assertEqual(pkg.getName(),"test","Package name not equal to 'test'.")
		self.assertEqual(pkg.getType(),"package","Package type not equal to 'package'.")
		# Test Class 'MyClass'
		self.assertEqual(pkg.hasClass("MyClass"),True,"Class 'MyClass' not found.")
		cls = pkg.getClass("MyClass")
		# Test MetaTags 'Bindable'
		self.assertEqual(cls.hasMetaTag("Bindable"),True,"MetaTag 'Bindable' not found.")
		meta = cls.getMetaTag("Bindable")
		self.assertEqual(meta.getName(),"Bindable","MetaTag name not equal to 'Bindable'.")
		self.assertEqual(meta.getType(),"metatag","MetaTag type not equal to 'metatag'.")
		self.assertEqual(len(meta.getParams()),0,"'Bindable' MetaTag should not contain any parameters.")
		# Test MetaTag 'Event'
		self.assertEqual(cls.hasMetaTag("Event"),True,"MetaTag 'Event' not found.")
		meta = cls.getMetaTag("Event")
		self.assertEqual(meta.getName(),"Event","MetaTag name not equal to 'Event'.")
		self.assertEqual(meta.getType(),"metatag","MetaTag type not equal to 'metatag'.")
		self.assertEqual(len(meta.getParams()),2,"'Event' MetaTag should contain 2 parameters.")
		self.assertEqual(meta.hasParam("name"),True,"'Event' MetaTag should have 'name' parameter.")
		self.assertEqual(meta.getParam("name"),"myEnableEvent","'name' parameter should equal 'myEnableEvent'.")
		self.assertEqual(meta.hasParam("type"),True,"'Event' MetaTag should have 'type' parameter.")
		self.assertEqual(meta.getParam("type"),"flash.events.Event","'type' parameter should equal 'flash.events.Event'.")
class ASPackageTestCase(BaseTestCase):
	
	def testUnnamedPackage(self):
		self.builder.addSource("""
		package
		{
		}
		""")
		
		self.assertEqual(self.builder.hasPackage(""),True,"Unnamed package not found.")
		pkg = self.builder.getPackage("")
		self.assertEqual(pkg.getName(),"","Package name not equal to ''.")
		self.assertEqual(pkg.getType(),"package","Package type not equal to 'package'.")
	def testNamedPackage(self):
		self.builder.addSource("""
		package com.gurufaction.asdox
		{
		}
		""")
		
		self.assertEqual(self.builder.hasPackage("com.gurufaction.asdox"),True,"Package 'com.gurufaction.asdox' not found.")
		pkg = self.builder.getPackage("com.gurufaction.asdox")
		self.assertEqual(pkg.getName(),"com.gurufaction.asdox","Package name not equal to 'com.gurufaction.asdox'.")
		self.assertEqual(pkg.getType(),"package","Package type not equal to 'package'.")
	def testMultiPackages(self):
		self.builder.addSource("""
		package com.google.code.asdox
		{
		}
		
		package com.gurufaction.asdox
		{
		}
		
		package
		{
		}
		""")
		self.assertEqual(len(self.builder.getPackages()),3,"Source file does not contain three packages.")
		self.assertEqual(self.builder.hasPackage("com.google.code.asdox"),True,"Package 'com.google.code.asdox' not found.")
		pkg = self.builder.getPackage("com.google.code.asdox")
		self.assertEqual(pkg.getName(),"com.google.code.asdox","Package name not equal to 'com.google.code.asdox'.")
		
		self.assertEqual(self.builder.hasPackage("com.gurufaction.asdox"),True,"Package 'com.gurufaction.asdox' not found.")
		pkg = self.builder.getPackage("com.gurufaction.asdox")
		self.assertEqual(pkg.getName(),"com.gurufaction.asdox","Package name not equal to 'com.gurufaction.asdox'.")
		
		self.assertEqual(self.builder.hasPackage(""),True,"Package '' not found.")
		pkg = self.builder.getPackage("")
		self.assertEqual(pkg.getName(),"","Package name not equal to ''.")
	def testPackageImports(self):
		"Parse Package with Import definitions."
		self.builder.addSource("""
		package com.gurufaction.asdox
		{
			import flash.display.DisplayObject;
			import flash.events.Event;
			import flash.events.FocusEvent;
			import flash.events.KeyboardEvent;
			import flash.events.MouseEvent;
			import flash.events.TimerEvent;
		}
		""")
		
		self.assertEqual(self.builder.hasPackage("com.gurufaction.asdox"),True,"Package 'com.gurufaction.asdox' not found.")
		pkg = self.builder.getPackage("com.gurufaction.asdox")
		self.assertEqual(len(pkg.getImports()),6,"Package does not contain six import statements.")
	def testPackageSinglelineComments(self):
		self.builder.addSource("""
		package com.gurufaction.asdox
		{
			//--------------------------------------
			//  Events
			//--------------------------------------

			//--------------------------------------
			//  Styles
			//--------------------------------------
		}
		""")
		
		self.assertEqual(self.builder.hasPackage("com.gurufaction.asdox"),True,"Package 'com.gurufaction.asdox' not found.")
		pkg = self.builder.getPackage("com.gurufaction.asdox")
	def testPackageMultilineComments(self):
		self.builder.addSource("""
		package com.gurufaction.asdox
		{
			/*****
			*
			* Testing Multiline Comments
			* inside package definition.
			*
			******/
		}
		""")
		
		self.assertEqual(self.builder.hasPackage("com.gurufaction.asdox"),True,"Package 'com.gurufaction.asdox' not found.")
		pkg = self.builder.getPackage("com.gurufaction.asdox")
	def testPackageComments(self):
		self.builder.addSource("""
		package com.gurufaction.asdox
		{
			/**
			* First Multiline Comment
			**/
			
			// First Singleline Comment
			
			/**
			* Second Multiline Comment
			**/
			
			// Second Singleline Comment
		}
		""")
		
		self.assertEqual(self.builder.hasPackage("com.gurufaction.asdox"),True,"Package 'com.gurufaction.asdox' not found.")
		pkg = self.builder.getPackage("com.gurufaction.asdox")
	def testPackageNamespace(self):
		"Parse Package with namespace declaration."
		self.builder.addSource("""
		package com.gurufaction.asdox
		{
			use namespace mx_internal;
		}
		""")
		
		self.assertEqual(self.builder.hasPackage("com.gurufaction.asdox"),True,"Package 'com.gurufaction.asdox' not found.")
		pkg = self.builder.getPackage("com.gurufaction.asdox")
	def testSourceFileComment(self):
		"Parse Package with leading comment."
		self.builder.addSource("""
		////////////////////////////////////////////////////////////////////////////////
		//
		//  Copyright (C) 2003-2006 Adobe Macromedia Software LLC and its licensors.
		//  All Rights Reserved. The following is Source Code and is subject to all
		//  restrictions on such code as contained in the End User License Agreement
		//  accompanying this product.
		//
		////////////////////////////////////////////////////////////////////////////////
		
		package com.gurufaction.asdox
		{
			
		}
		""")
		
		self.assertEqual(self.builder.hasPackage("com.gurufaction.asdox"),True,"Package 'com.gurufaction.asdox' not found.")
		pkg = self.builder.getPackage("com.gurufaction.asdox")
class ParsingExternalFileTestCase(BaseTestCase):
	def testFilterClassFile(self):
		"Load and Parse Filter.as source file."
		self.builder.addSource("resources/Filter.as")
		self.assertEqual( self.builder.hasPackage("com.franklinconnections"),True,"'com.franklinconnections' package not found!")
	def testButtonClassFile(self):
		"Load and Parse Button.as source file."
		self.builder.addSource("resources/Button.as")
		self.assertEqual( self.builder.hasPackage("mx.controls"),True,"'mx.controls' package not found!")
if __name__ == "__main__":
	unittest.main()