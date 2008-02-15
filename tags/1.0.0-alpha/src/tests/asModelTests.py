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
from asdox import asModel

class ASClassTestCase(unittest.TestCase):
	def testClassContructor(self):
		cls = asModel.ASClass();
		self.assertEqual(cls.getName(),"")
		cls = asModel.ASClass("ITestable")
		self.assertEqual(cls.getName(),"ITestable")
		self.assertEqual(cls.getType(),"class")
	def testBasicClass(self):
		cls = asModel.ASClass("MyClass")
		self.assertEqual(cls.getName(),"MyClass")
		self.assertEqual(cls.isInterface(),False)
		self.assertEqual(cls.isDynamic(),False)
		self.assertEqual(cls.isFinal(),False)
		self.assertEqual(cls.isPublic(),False)
		self.assertEqual(cls.getExtends(),"Object")
		self.assertEqual(cls.getImplements(),set())
		self.assertEqual(cls.getIncludes(),set())
	def testClassVariables(self):
		cls = asModel.ASClass("VariableClass")
		var1 = asModel.ASField("name","String")
		var2 = asModel.ASField("age","int")
		var2.addModifier("private")
		var2.addModifier("public")
		cls.addField(var1)
		cls.addField(var2)
		self.assertEqual(cls.getName(),"VariableClass")
		self.assertEqual(cls.getField("name").getName(),"name")
		self.assertEqual(cls.getField("name").getType(),"String")
		self.assertEqual(cls.getField("name").hasModifier("internal"),True)
		self.assertEqual(cls.getField("age").getName(),"age")
		self.assertEqual(cls.getField("age").getType(),"int")
		self.assertEqual(cls.getField("age").hasModifier("public"),True)
		self.assertEqual(cls.getField("age").hasModifier("private"),False)
	def testClassMethods(self):
		cls = asModel.ASClass("MethodClass")
		meth1 = asModel.ASMethod("SayHello","String")
		meth2 = asModel.ASMethod("DoNothing")
		cls.addMethod( meth1 )
		cls.addMethod( meth2 )
		self.assertEqual(cls.getName(),"MethodClass")
		self.assertEqual( cls.getMethod("SayHello").getName(),"SayHello")
		self.assertEqual( cls.getMethod("SayHello").getType(),"String")
		self.assertEqual( cls.getMethod("DoNothing").getName(),"DoNothing")
		self.assertEqual( cls.getMethod("DoNothing").getType(),"void")
	def testBasicInterface(self):
		cls = asModel.ASClass("com.gurufaction.TestClass")
		cls.setInterface(True)
		self.assertEqual(cls.getName(),"com.gurufaction.TestClass")
		self.assertEqual(cls.getType(),"interface","Class not of type 'interface'")
		self.assertEqual(cls.isInterface(),True,"isInterface() method failed")
		self.assertEqual(cls.isDynamic(),False)
		self.assertEqual(cls.isFinal(),False)
		self.assertEqual(cls.isPublic(),False)
		self.assertEqual(cls.getExtends(),"Object")
		self.assertEqual(cls.getImplements(),set())
		self.assertEqual(cls.getIncludes(),set())
	def testClassModifiers(self):
		cls = asModel.ASClass()
		cls.addModifier("public")
		cls.addModifier("internal")
		cls.addModifier("dynamic")
		cls.addModifier("final")
		cls.addModifier("dummy")
		self.assertEqual(cls.hasModifier("internal"),True)
		self.assertEqual(cls.hasModifier("dynamic"),True)
		self.assertEqual(cls.hasModifier("final"),True)
		self.assertEqual(cls.isPublic(),False)
		self.assertEqual(cls.isDynamic(),True)
		self.assertEqual(cls.isFinal(),True)
		
if __name__ == "__main__":
	unittest.main()