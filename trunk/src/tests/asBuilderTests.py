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
			public class MyBasicClass
			{
				
			}
		}
		""")
		
		self.assertEqual("com.gurufaction.mypackage" in self.builder.packages,True,"Package 'com.gurufaction.mypackage' not found.")
		pkg = self.builder.packages["com.gurufaction.mypackage"]
		self.assertEqual("MyBasicClass" in pkg.classes,True,"Class 'MyBasicClass' not found.")
		cls = pkg.classes["MyBasicClass"]
		self.assertEqual(cls.name,"MyBasicClass","Class name not equal to 'MyBasicClass'.")
		self.assertEqual(cls.isInterface,False,"Class type not equal to 'class'.")
		self.assertEqual(cls.visibility,"public","Class is not public")
		self.assertEqual(cls.isDynamic,False,"Class should not be dynamic.")
		self.assertEqual(cls.isFinal,False,"Class should not be final.")
		self.assertEqual(len(cls.variables),0,"Class should contain no fields.")
		self.assertEqual(len(cls.methods),0,"Class should contain no methods.")
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
		self.assertEqual("test" in self.builder.packages,True,"Package 'test' not found.")
		self.assertEqual("MyClass" in self.builder.packages["test"].classes,True,"Class 'MyClass' not found in package.")
		self.assertEqual(self.builder.packages["test"].classes["MyClass"].metadata[0].name,"Event","Metatag 'Event' not found.")
		self.assertEqual(self.builder.packages["test"].classes["MyClass"].metadata[0].params,{'type': 'mx.events.FlexEvent', 'name': 'buttonDown'})
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
		self.assertEqual("test" in self.builder.packages, True, "Package Not Found!")
		self.assertEqual("MyClass" in self.builder.packages["test"].classes,True,"Class Not Found in Package.")
		for meta in self.builder.packages["test"].classes.values():
			if meta.name == "Bindable":
				self.assertEqual(meta.params,{'n':'n'})
			if meta.name == "Event":
				self.assertEqual(meta.params,{'name':'myEnabledEvent'})
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
		self.assertEqual(self.builder.packages["com.gurufaction.mypackage"].classes["MyClass"].extends,"BaseClass")
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
		self.assertEqual(self.builder.packages["com.gurufaction.mypackage"].classes["MyClass"].implements[0],"IWorkable")
		self.assertEqual(self.builder.packages["com.gurufaction.mypackage"].classes["MyClass"].implements[1],"ITestable")
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
		self.assertEqual(self.builder.packages[""].classes["MyClass"].visibility,"internal")
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
		self.assertEqual(self.builder.packages[""].classes["MyClass"].visibility,"public")
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
		self.assertEqual(self.builder.packages[""].classes["MyClass"].isDynamic,True)
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
		self.assertEqual(self.builder.packages[""].classes["MyClass"].isFinal,True)
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
		self.assertEqual(self.builder.packages[""].classes["MyClass"].isDynamic,True)
		self.assertEqual(self.builder.packages[""].classes["MyClass"].isFinal,True)
class ASPackageTestCase(BaseTestCase):
	
	def testUnnamedPackage(self):
		self.builder.addSource("""
		package
		{
			public class MyClass
                        {
                        
                        }
		}
		""")
		
		self.assertEqual(self.builder.packages[""].name,"")
	def testNamedPackage(self):
		self.builder.addSource("""
		package com.gurufaction.asdox
		{
			public class MyClass
                        {
                        
                        }
		}
		""")
		
		self.assertEqual(self.builder.packages["com.gurufaction.asdox"].name,"com.gurufaction.asdox")
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
			
			public class MyClass
                        {
                        
                        }
		}
		""")
		
		self.assertEqual(self.builder.packages["com.gurufaction.asdox"].imports,['flash.display.DisplayObject'])
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
			public class MyClass
                        {
                        
                        }
		}
		""")
		
		self.assertEqual("com.gurufaction.asdox" in self.builder.packages,True)
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
			public class MyClass
                        {
                        
                        }
		}
		""")
		
		self.assertEqual("com.gurufaction.asdox" in self.builder.packages,True)
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
			public class MyClass
                        {
                        
                        }
		}
		""")
		
		self.assertEqual("com.gurufaction.asdox" in self.builder.packages,True)
	def testPackageNamespace(self):
		"Parse Package with namespace declaration."
		self.builder.addSource("""
		package com.gurufaction.asdox
		{
			use namespace mx_internal;
			public class MyClass
                        {
                        
                        }
		}
		""")
		
		self.assertEqual("com.gurufaction.asdox" in self.builder.packages,True)
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
			public class MyClass
                        {
                        
                        }
		}
		""")
		
		self.assertEqual("com.gurufaction.asdox" in self.builder.packages,True)
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
			public class MyClass
                        {
                        
                        }
		}
		""")
		
		self.assertEqual("com.gurufaction.asdox" in self.builder.packages,True)
class ParsingExternalFileTestCase(BaseTestCase):
	def testFilterClassFile(self):
		"Load and Parse Filter.as source file."
		self.builder.addSource("resources/Filter.as")
		self.assertEqual( self.builder.hasPackage("com.franklinconnections"),True,"'com.franklinconnections' package not found!")
	def testButtonClassFile(self):
		"Load and Parse Button.as source file."
		self.builder.addSource("resources/Button.as")
		self.assertEqual( self.builder.hasPackage("mx.controls"),True,"'mx.controls' package not found!")
class BuilderTestCase(BaseTestCase):		
	def testMultipleSources(self):
		"Parse multiple source files."
		self.builder.addSource(""" 
		package com.googlecode.asdox
		{
			class MyClass
			{
				
			}
		}
		""")
		self.builder.addSource(""" 
		package com.googlecode.asdox
		{
			class MyOtherClass
			{
				
			}
		}
		""")
		self.assertEqual("com.googlecode.asdox" in self.builder.packages,True,"Package 'com.googlecode.asdox' not found.")
		pkg = self.builder.packages["com.googlecode.asdox"]
		self.assertEqual(len(pkg.classes),2,)
		self.assertEqual("MyClass" in pkg.classes,True,"'MyClass' not found in package.")
		self.assertEqual("MyOtherClass" in pkg.classes,True,"'MyOtherClass' not found in package.")
	def testAddSourceDir(self):
		"Parse directory for source files"
		self.builder.addSource("resources/com/gurufaction")
		#test if package exist
		self.assertEqual(self.builder.hasPackage("com.gurufaction"),True,"Package not found in source directory")
		#get current package
		pkg = self.builder.getPackage("com.gurufaction")
		#test if two classes exist in package
		self.assertEqual(len(pkg.getClasses()),2,"Did not find expected number of classes in source directory")
		#get first class
		cls1 = pkg.getClass("MyClassFile1")
		#get second class
		cls2 = pkg.getClass("MyClassFile2")
		#get first class
		self.assertEqual(cls1.getName(),"MyClassFile1","First class not found 'MyClassFile1'")
		#get second class
		self.assertEqual(cls2.getName(),"MyClassFile2","Second class not found 'MyClassFile2'")
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
	def testFieldInitialization(self):
		"Parse field initialization"
		self.builder.addSource(""" 
		package
		{
		        class MyClass
			{
				var name:String = "Michael Ramriez";
				var age:int = 29;
				var salary:Number = 41000.52;
				var isSmart:Boolean = True;
				var _labelPlacement:String = ButtonLabelPlacement.RIGHT; 
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
	def testMethodGetter(self):
		"Parse class method with getter."
		self.builder.addSource("""
		package com.gurufaction.asdox
		{
			public class MyClass
			{
				public function get labelPlacement():String
				{
					return _labelPlacement;
				}
			}
		}
		""")
		
		self.assertEqual(self.builder.hasPackage("com.gurufaction.asdox"),True,"Package 'com.gurufaction.asdox' not found.")
		pkg = self.builder.getPackage("com.gurufaction.asdox")
		self.assertEqual(pkg.getClass("MyClass").hasGetter("labelPlacement"),True,"'labelPlacement' method not found in 'MyClass'.")
		meth = pkg.getClass("MyClass").getGetter("labelPlacement")
		self.assertEqual(meth.getAccessor(),"get")
	def testMethodSetter(self):
		"Parse class method with setter."
		self.builder.addSource("""
		package com.gurufaction.asdox
		{
			public class MyClass
			{
				public function set labelPlacement(label:String):void
				{
					_labelPlacement = label;
				}
			}
		}
		""")
		
		self.assertEqual(self.builder.hasPackage("com.gurufaction.asdox"),True,"Package 'com.gurufaction.asdox' not found.")
		pkg = self.builder.getPackage("com.gurufaction.asdox")
		self.assertEqual(pkg.getClass("MyClass").hasSetter("labelPlacement"),True,"'labelPlacement' method not found in 'MyClass'.")
		meth = pkg.getClass("MyClass").getSetter("labelPlacement")
		self.assertEqual(meth.getAccessor(),"set")
	def testMethodGetterAndSetter(self):
		"Parse class method with setter and getter."
		self.builder.addSource("""
		package com.gurufaction.asdox
		{
			public class MyClass
			{
				public function get name():String
				{
					return _name;
				}
				
				public function set name(name:String):void
				{
					_name = name;
				}
			}
		}
		""")
		
		self.assertEqual(self.builder.hasPackage("com.gurufaction.asdox"),True,"Package 'com.gurufaction.asdox' not found.")
		pkg = self.builder.getPackage("com.gurufaction.asdox")
		self.assertEqual(pkg.getClass("MyClass").hasGetter("name"),True,"Getter 'name' method not found in 'MyClass'.")
		self.assertEqual(pkg.getClass("MyClass").hasSetter("name"),True,"Setter 'name' method not found in 'MyClass'.")
	def testMethodNamespace(self):
		"Parse class method with namespace."
		self.builder.addSource("""
		package com.gurufaction.asdox
		{
			public class MyClass
			{
				mx_internal function setSelected(value:Boolean):void
				{
					if (_selected != value)
					{
						_selected = value;

						invalidateDisplayList();
    
						if (toggle)
							dispatchEvent(new Event(Event.CHANGE));

						dispatchEvent(new FlexEvent(FlexEvent.VALUE_COMMIT));
					}
				}
			}
		}
		""")
		
		self.assertEqual(self.builder.hasPackage("com.gurufaction.asdox"),True,"Package 'com.gurufaction.asdox' not found.")
		pkg = self.builder.getPackage("com.gurufaction.asdox")
		self.assertEqual(pkg.getClass("MyClass").hasMethod("setSelected"),True,"'setSelected' method not found in 'MyClass'.")		
if __name__ == "__main__":
	unittest.main()