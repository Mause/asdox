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
	def testClassMetadataJavaDocComment(self):
		self.builder.addSource("""
		package test
		{
			/**
			*  Dispatched when the user presses the Button control.
			*  If the <code>autoRepeat</code> property is <code>true</code>,
			*  this event is dispatched repeatedly as long as the button stays down.
			*
			*  @eventType mx.events.FlexEvent.BUTTON_DOWN
			*/
			
			[Event(name="buttonDown", type="mx.events.FlexEvent")]
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
		# Test MetaTag 'Event'
		self.assertEqual(cls.hasMetaTag("Event"),True,"MetaTag 'Event' not found.")
		meta = cls.getMetaTag("Event")
		self.assertEqual(meta.getName(),"Event","MetaTag name not equal to 'Event'.")
		self.assertEqual(meta.getType(),"metatag","MetaTag type not equal to 'metatag'.")
		self.assertEqual(len(meta.getParams()),2,"'Event' MetaTag should contain 2 parameters.")
		self.assertEqual(meta.hasParam("name"),True,"'Event' MetaTag should have 'name' parameter.")
		self.assertEqual(meta.getParam("name"),"buttonDown","'name' parameter should equal 'buttonDown'.")
		self.assertEqual(meta.hasParam("type"),True,"'Event' MetaTag should have 'type' parameter.")
		self.assertEqual(meta.getParam("type"),"mx.events.FlexEvent","'type' parameter should equal 'mx.events.FlexEvent'.")
	def testClassMetaData(self):
		self.builder.addSource("""
		package test{
			[Bindable]
			[Event(name="myEnableEvent", type="flash.events.Event")]
			[DefaultTriggerEvent("click")]
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
		# Test MetaTag 'DefaultTriggerEvent'
		self.assertEqual(cls.hasMetaTag("DefaultTriggerEvent"),True,"MetaTag 'Event' not found.")
		meta = cls.getMetaTag("DefaultTriggerEvent")
		self.assertEqual(meta.getName(),"DefaultTriggerEvent","MetaTag name not equal to 'DefaultTriggerEvent'.")
		self.assertEqual(meta.getType(),"metatag","MetaTag type not equal to 'metatag'.")
		self.assertEqual(len(meta.getParams()),1,"'DefaultTriggerEvent' MetaTag should contain one parameters.")
		self.assertEqual(meta.getParam(0),"click","Parameter should equal 'click'.")
	def testClassInclude(self):
		"Parse Class with Include statement"
		self.builder.addSource("""
		package com.gurufaction.mypackage
		{
			public class MyClass
			{
				include "../core/Version.as";
			}
		}
		""")
		self.assertEqual(self.builder.hasPackage("com.gurufaction.mypackage"),True,"Package 'com.gurufaction.mypackage' not found.")
		pkg = self.builder.getPackage("com.gurufaction.mypackage")
		self.assertEqual(pkg.hasClass("MyClass"),True,"Class 'MyClass' not found in package.")
		cls = pkg.getClass("MyClass")		
	def testClassExtends(self):
		"Parse Class with Extends"
		self.builder.addSource("""
		package com.gurufaction.mypackage
		{
			public class MyClass extends BaseClass
			{
				
			}
		}
		""")
		self.assertEqual(self.builder.hasPackage("com.gurufaction.mypackage"),True,"Package 'com.gurufaction.mypackage' not found.")
		pkg = self.builder.getPackage("com.gurufaction.mypackage")
		self.assertEqual(pkg.hasClass("MyClass"),True,"Class 'MyClass' not found in package.")
		cls = pkg.getClass("MyClass")
		self.assertEqual(cls.getExtends(),"BaseClass","Class 'MyClass' does not extend 'BaseClass'.")
	def testClassImplements(self):
		"Parse Class which implements interfaces"
		self.builder.addSource("""
		package com.gurufaction.mypackage
		{
			public class MyClass implements IWorkable, ITestable
			{
				
			}
		}
		""")
		self.assertEqual(self.builder.hasPackage("com.gurufaction.mypackage"),True,"Package 'com.gurufaction.mypackage' not found.")
		pkg = self.builder.getPackage("com.gurufaction.mypackage")
		self.assertEqual(pkg.hasClass("MyClass"),True,"Class 'MyClass' not found in package.")
		cls = pkg.getClass("MyClass")
		self.assertEqual(cls.getImplements(),set(['ITestable', 'IWorkable']),"Class does not implement 'ITestable' and 'IWorkable'.")
	def testInternalClassModifier(self):
		"Parse for 'internal' class modifier"
		self.builder.addSource(""" 
                package
                {
                        class MyClass
                        {
                        
                        }
                }
                """)
		#test for valid package
                self.assertEqual(self.builder.hasPackage(""),True,"Unnamed package not found in testStaticClassField")
                #get unnamed package
                pkg = self.builder.getPackage("")
                #test that a class has been declared
                self.assertEqual(pkg.hasClass("MyClass"),True,"Package does not have one or more classes defined")
                # get class 'MyClass'
                cls = pkg.getClass("MyClass")
                #test for 'internal' class modifier
                self.assertEqual(cls.hasModifier("internal"),True,"No internal class modifier found")
	def testPublicClassModifier(self):
		"Parse for 'public' class modifier"
                self.builder.addSource(""" 
                package
                {
                        
                        public class MyClass
                        {
                        
                        }
                }
                """)
		#test for valid package
                self.assertEqual(self.builder.hasPackage(""),True,"Unnamed package not found in testStaticClassField")
                #get unnamed package
                pkg = self.builder.getPackage("")
                #test that a class has been declared
                self.assertEqual(pkg.hasClass("MyClass"),True,"Package does not have one or more classes defined")
                # get class 'MyClass'
                cls = pkg.getClass("MyClass")
                #test for public class modifer
                self.assertEqual(cls.hasModifier("public"),True,"No public class modifier found")
	def testDynamicClassModifier(self):
		"Parse for 'dynamic' class modifier"
                self.builder.addSource(""" 
                package
                {

                        dynamic class MyClass
                        {
                        
                        }

                }
                """)
		#test for valid package
                self.assertEqual(self.builder.hasPackage(""),True,"Unnamed package not found in testStaticClassField")
                #get unnamed package
                pkg = self.builder.getPackage("")
                #test that a class has been declared
                self.assertEqual(pkg.hasClass("MyClass"),True,"Package does not have one or more classes defined")
                # get class 'MyClass'
                cls = pkg.getClass("MyClass")
                #test for dynamic class modifier
                self.assertEqual(cls.hasModifier("dynamic"),True,"No dynamic class modifer found")
	def testFinalClassModifier(self):
		"Parse for 'final' class modifier"
                self.builder.addSource(""" 
                package
                {
                        final class MyClass
                        {
                        
                        }
                }
                """)
		#test for valid package
                self.assertEqual(self.builder.hasPackage(""),True,"Unnamed package not found in testStaticClassField")
                #get unnamed package
                pkg = self.builder.getPackage("")
                #test that a class has been declared
                self.assertEqual(pkg.hasClass("MyClass"),True,"Package does not have one or more classes defined")
                # get class 'MyClass'
                cls = pkg.getClass("MyClass")
                #test for final class modifier
                self.assertEqual(cls.hasModifier("final"),True,"No final class modifer found")
	def testDynamicFinalClassModifier(self):
		"Parse for 'dynamic final' class modifier"
                self.builder.addSource(""" 
                package
                {
                        dynamic final class MyClass
                        {
                        
                        }
                }
                """)
		#test for valid package
                self.assertEqual(self.builder.hasPackage(""),True,"Unnamed package not found in testStaticClassField")
                #get unnamed package
                pkg = self.builder.getPackage("")
                #test that a class has been declared
                self.assertEqual(pkg.hasClass("MyClass"),True,"Package does not have one or more classes defined")
                # get class 'MyClass'
                cls = pkg.getClass("MyClass")
                #test for dynamic class modifier
                self.assertEqual(cls.hasModifier("dynamic"),True,"No dynamic class modifer found")
                #test for final class modifer
                self.assertEqual(cls.hasModifier("final"),True,"No final class modifier found")
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
			import flash.events.*;
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
			/*
			*
			* Testing Multiline Comments
			* inside package definition.
			*
			*/
		}
		""")
		
		self.assertEqual(self.builder.hasPackage("com.gurufaction.asdox"),True,"Package 'com.gurufaction.asdox' not found.")
		pkg = self.builder.getPackage("com.gurufaction.asdox")
	def testPackageComments(self):
		self.builder.addSource("""
		package com.gurufaction.asdox
		{
			/*
			* First Multiline Comment
			*/
			
			// First Singleline Comment
			
			/*
			* Second Multiline Comment
			*/
			
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
	def testPackageIncludes(self):
		"Parse Package with include statements."
		self.builder.addSource("""
		package com.gurufaction.asdox
		{
			include "../styles/metadata/FocusStyles.as"
			include "../styles/metadata/LeadingStyle.as"
			include "../styles/metadata/PaddingStyles.as"
			include "../styles/metadata/SkinStyles.as"
			include "../styles/metadata/TextStyles.as"
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
		
		
class ASFieldTestCase(BaseTestCase):
	def testClassField(self):
		"Parse class field."
		self.builder.addSource(""" 
		package 
		{
			class MyClass
			{
				var today:DateTime;
			}
		}
		""")
		#test for valid package
		self.assertEqual(self.builder.hasPackage(""),True,"Unnamed package not found in testClassField")
		#get unnamed package
		pkg = self.builder.getPackage("")
		#test that a class has been declared
		self.assertEqual(pkg.hasClass("MyClass"),True,"Package does not have a class defined")
		# get class 'MyClass'
		cls = pkg.getClass("MyClass")
		#test for field in in class called 'today'
		self.assertEqual(cls.hasField("today"),True,"'today' field not found")
		#test for internal modifier in 'today' field
		self.assertEqual(cls.getField("today").hasModifier("internal"),True,"No Internal modifier found in field")
		self.assertEqual(pkg.getClass("MyClass").getField("today").getName(),"today","Field name not equal to 'today'.")
		#test that 'today' field is of type DateTime
		self.assertEqual(pkg.getClass("MyClass").getField("today").getType(),"DateTime","field was not of type 'DateTime'.")
		
	def testConstantClassField(self):
		"Parse class constant field."
		self.builder.addSource(""" 
		package 
		{
			class MyClass
			{
				const PI:Number;
			}
		}
		""")
		#test for valid package
		self.assertEqual(self.builder.hasPackage(""),True,"Unnamed package not found in testConstantClassField")
		#get unnamed package
		pkg = self.builder.getPackage("")
		#test that a class has been declared
		self.assertEqual(pkg.hasClass("MyClass"),True,"Package does not have a class defined")
		# get class 'MyClass'
		cls = pkg.getClass("MyClass")
		#test for field in in class called 'PI'
		self.assertEqual(cls.hasField("PI"),True,"'PI' field not found")
		#test if 'PI' field is constant
		self.assertEqual(cls.getField("PI").isConstant(),True,"'PI' field not constant.")
		#test that 'PI' field is of type Number
		self.assertEqual(pkg.getClass("MyClass").getField("PI").getType(),"Number","field was not of type 'Number'.")
	def testFieldModifiers(self):
		"Parse field modifiers"
		self.builder.addSource(""" 
		package
		{
		        class MyClass
			{
				var iVar:String;
				public var name:String;
				private var age:int;
				protected var salary:Number;
				static var count:int; 
			}
		}
		""")
		#test for valid package
		self.assertEqual(self.builder.hasPackage(""),True,"Unnamed package not found in testFieldModifiers")
		#get unnamed package
		pkg = self.builder.getPackage("")
		#test that a class has been declared
		self.assertEqual(pkg.hasClass("MyClass"),True,"Package does not have one or more classes defined")
		# get class 'MyClass'
		cls = pkg.getClass("MyClass")
		#test for 'internal' field modifier
		self.assertEqual(cls.getField("iVar").hasModifier("internal"),True,"Unable to parse 'internal' field modifier")
		#test for 'public' field modifier
		self.assertEqual(cls.getField("name").hasModifier("public"),True,"Unable to parse 'public' field modifier")
		#test for 'private' field modifier
		self.assertEqual(cls.getField("age").hasModifier("private"),True,"Unable to parse 'private' field modifier")
		#test for 'protected' field modifier
		self.assertEqual(cls.getField("salary").hasModifier("protected"),True,"Unable to parse 'protected' field modifier")
		#test for 'static' field modifier
		self.assertEqual(cls.getField("count").hasModifier("static"),True,"Unable to parse 'static' field modifier")
	def testFieldNamespaceModifier(self):
		"Parse class namespace modifier"
		self.builder.addSource(""" 
		package
		{
		        class MyClass
			{ 
				mx_internal var mx:String;
			}
		}
		""")
		#test for valid package
		self.assertEqual(self.builder.hasPackage(""),True,"Unnamed package not found in testFieldModifiers")
		#get unnamed package
		pkg = self.builder.getPackage("")
		#test that a class has been declared
		self.assertEqual(pkg.hasClass("MyClass"),True,"Package does not have one or more classes defined")
		# get class 'MyClass'
		cls = pkg.getClass("MyClass")
		#test for 'user_defined_namespace' field modifier
		self.assertEqual(cls.getField("mx").hasModifier("mx_internal"),True,"Unable to parse user defined namespace 'mx_internal'")	
	def testJavaDocWithClassFields(self):
		"Parse JavaDoc with class Fields"
		self.builder.addSource(""" 
		package
		{
		         /**
			  *  @private
			  *  Timer for doing auto-repeat.
		         */
		        class MyClass
			{ 
				mx_internal var mx:String;
			}
		}
		""")
		#test for valid package
		#self.assertEqual(self.builder.hasPackage(""),True,"Unnamed package not found in testFieldModifiers")
		#get unnamed package
		#pkg = self.builder.getPackage("")
		#test that a class has been declared
		#self.assertEqual(pkg.hasClass("MyClass"),True,"Package does not have one or more classes defined")
		# get class 'MyClass'
		#cls = pkg.getClass("MyClass")
		#test for JavaDocs with class fields
		#self.assertEqual()
	
	def testMetaDataWithClassFields(self):
		"Parse class Fields with metadata"
		self.builder.addSource(""" 
		package
		{
		        class MyClass
			{ 
			        [Bindable]
				mx_internal var mx:String;
			}
		}
		""")
				#test for valid package
		#self.assertEqual(self.builder.hasPackage(""),True,"Unnamed package not found in testFieldModifiers")
		#get unnamed package
		#pkg = self.builder.getPackage("")
		#test that a class has been declared
		#self.assertEqual(pkg.hasClass("MyClass"),True,"Package does not have one or more classes defined")
		# get class 'MyClass'
		#cls = pkg.getClass("MyClass")
		#test for Metadata with class fields
		#self.assertEqual()
class ASMethodTestCase(BaseTestCase):
	"Test cases for class methods"
	def testConstructorMethod(self):
		"Parse class constructor method with no arguments."
		self.builder.addSource("""
		package com.gurufaction.asdox
		{
			public class MyClass
			{
				public function MyClass()
				{
				}
			}
		}
		""")
		
		self.assertEqual(self.builder.hasPackage("com.gurufaction.asdox"),True,"Package 'com.gurufaction.asdox' not found.")
		pkg = self.builder.getPackage("com.gurufaction.asdox")
		self.assertEqual(pkg.getClass("MyClass").hasMethod("MyClass"),True,"'MyClass' method not found in 'MyClass'.")
		meth = pkg.getClass("MyClass").getMethod("MyClass")
		self.assertEqual(meth.getName(),"MyClass","'MyClass' method does not have same name.")
		self.assertEqual(meth.getType(),"void","'MyClass' method does not return type 'void'.")
		self.assertEqual(meth.hasModifier("public"),True,"'MyClass' method is not public.")
		self.assertEqual(len(meth.getArguments()),0,"'MyClass' method does not contain zero arguments.")
	def testMethod(self):
		"Parse class method with no arguments."
		self.builder.addSource("""
		package com.gurufaction.asdox
		{
			public class MyClass
			{
				public function sayHi():String
				{
				}
			}
		}
		""")
		
		self.assertEqual(self.builder.hasPackage("com.gurufaction.asdox"),True,"Package 'com.gurufaction.asdox' not found.")
		pkg = self.builder.getPackage("com.gurufaction.asdox")
		self.assertEqual(pkg.getClass("MyClass").hasMethod("sayHi"),True,"'sayHi' method not found in 'MyClass'.")
		meth = pkg.getClass("MyClass").getMethod("sayHi")
		self.assertEqual(meth.getName(),"sayHi","'sayHi' method does not have same name.")
		self.assertEqual(meth.getType(),"String","'sayHi' method does not return type 'String'.")
		self.assertEqual(meth.hasModifier("public"),True,"'sayHi' method is not public.")
		self.assertEqual(len(meth.getArguments()),0,"'sayHi' method does not contain zero arguments.")
	def testMethodOverriding(self):
		"Parse overridden class method"
		self.builder.addSource("""
		package com.gurufaction.asdox
		{
			class Extender extends Base
			{
				public override function thanks():String 
				{
					return super.thanks() + " nui loa";
				}
			}
		}
		""")
		
		self.assertEqual(self.builder.hasPackage("com.gurufaction.asdox"),True,"Package 'com.gurufaction.asdox' not found.")
		pkg = self.builder.getPackage("com.gurufaction.asdox")
		self.assertEqual(pkg.getClass("Extender").hasMethod("thanks"),True,"'thanks' method not found in 'Extender'.")
		meth = pkg.getClass("Extender").getMethod("thanks")
		self.assertEqual(meth.hasModifier("override"),True)
	def testMethodArguments(self):
		"Parse class method with multiple arguments."
		self.builder.addSource("""
		package com.gurufaction.asdox
		{
			public class MyClass
			{
				public function addIntegers(num1:int,num2:int):int
				{
					return num1 + num2;
				}
			}
		}
		""")
		
		self.assertEqual(self.builder.hasPackage("com.gurufaction.asdox"),True,"Package 'com.gurufaction.asdox' not found.")
		pkg = self.builder.getPackage("com.gurufaction.asdox")
		self.assertEqual(pkg.getClass("MyClass").hasMethod("addIntegers"),True,"'addIntegers' method not found in 'MyClass'.")
		meth = pkg.getClass("MyClass").getMethod("addIntegers")
		self.assertEqual(len(meth.getArguments()),2,"'addIntegers' method does not contain two arguments.")
		arg1 = meth.getArgument("num1")
		arg2 = meth.getArgument("num2")
		self.assertEqual(arg1.getName(),"num1")
		self.assertEqual(arg1.getType(),"int")
		self.assertEqual(arg2.getName(),"num2")
		self.assertEqual(arg2.getType(),"int")
	def testMethodMultiLineComment(self):
		"Parse class method with multi-line comment."
		self.builder.addSource("""
		package com.gurufaction.asdox
		{
			public class MyClass
			{
				/*
				* Method returns empty string
				*/
				public function getName():String
				{
					return "";
				}
			}
		}
		""")
		
		self.assertEqual(self.builder.hasPackage("com.gurufaction.asdox"),True,"Package 'com.gurufaction.asdox' not found.")
		pkg = self.builder.getPackage("com.gurufaction.asdox")
		self.assertEqual(pkg.getClass("MyClass").hasMethod("getName"),True,"'getName' method not found in 'MyClass'.")
	def testMethodSingleLineComment(self):
		"Parse class method with single-line comment."
		self.builder.addSource("""
		package com.gurufaction.asdox
		{
			public class MyClass
			{
				// Method returns empty string
				public function getName():String
				{
					return "";
				}
			}
		}
		""")
		
		self.assertEqual(self.builder.hasPackage("com.gurufaction.asdox"),True,"Package 'com.gurufaction.asdox' not found.")
		pkg = self.builder.getPackage("com.gurufaction.asdox")
		self.assertEqual(pkg.getClass("MyClass").hasMethod("getName"),True,"'getName' method not found in 'MyClass'.")
	def testMethodMetadata(self):
		"Parse class method with metadata comment."
		self.builder.addSource("""
		package com.gurufaction.asdox
		{
			public class MyClass
			{
				[Bindable("dataChange")]
				[Inspectable(environment="none")]
				public function getName():String
				{
					return "";
				}
			}
		}
		""")
		
		self.assertEqual(self.builder.hasPackage("com.gurufaction.asdox"),True,"Package 'com.gurufaction.asdox' not found.")
		pkg = self.builder.getPackage("com.gurufaction.asdox")
		self.assertEqual(pkg.getClass("MyClass").hasMethod("getName"),True,"'getName' method not found in 'MyClass'.")
if __name__ == "__main__":
	unittest.main()