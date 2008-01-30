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

import unittest,asModel
class ClassDefinitionTestCase(unittest.TestCase):
	def testClassContructor(self):
		cls = asModel.ClassDef();
		self.assertEqual(cls.name,"")
		cls = asModel.ClassDef("ITestable","interface")
		self.assertEqual(cls.name,"ITestable")
		self.assertEqual(cls.type,"interface")
	def testBasicClass(self):
		cls = asModel.ClassDef("MyClass")
		self.assertEqual(cls.name,"MyClass")
		self.assertEqual(cls.isInterface(),False)
		self.assertEqual(cls.isDynamic(),False)
		self.assertEqual(cls.isFinal(),False)
		self.assertEqual(cls.isPublic(),False)
		self.assertEqual(cls.extends,"Object")
		self.assertEqual(cls.implements,set())
		self.assertEqual(cls.includes,set())
	def testClassVariables(self):
		cls = asModel.ClassDef("VariableClass")
		var1 = asModel.VariableDef("name","String")
		var2 = asModel.VariableDef("age","int")
		var2.addModifier("private")
		var2.addModifier("public")
		cls.addVariable(var1)
		cls.addVariable(var2)
		self.assertEqual(cls.name,"VariableClass")
		self.assertEqual(cls.getVariable("name").name,"name")
		self.assertEqual(cls.getVariable("name").type,"String")
		self.assertEqual(cls.getVariable("name").hasModifier("internal"),True)
		self.assertEqual(cls.getVariable("age").name,"age")
		self.assertEqual(cls.getVariable("age").type,"int")
		self.assertEqual(cls.getVariable("age").hasModifier("public"),True)
		self.assertEqual(cls.getVariable("age").hasModifier("private"),False)
	def testClassMethods(self):
		cls = asModel.ClassDef("MethodClass")
		meth1 = asModel.FunctionDef("SayHello","String")
		meth2 = asModel.FunctionDef("DoNothing")
		cls.addMethod( meth1 )
		cls.addMethod( meth2 )
		self.assertEqual(cls.name,"MethodClass")
		self.assertEqual( cls.getMethod("SayHello").name,"SayHello")
		self.assertEqual( cls.getMethod("SayHello").type,"String")
		self.assertEqual( cls.getMethod("DoNothing").name,"DoNothing")
		self.assertEqual( cls.getMethod("DoNothing").type,"void")
	def testBasicInterface(self):
		cls = asModel.ClassDef("com.gurufaction.TestClass","interface")
		self.assertEqual(cls.name,"com.gurufaction.TestClass")
		self.assertEqual(cls.type,"interface","Class not of type 'interface'")
		self.assertEqual(cls.isInterface(),True,"isInterface() method failed")
		self.assertEqual(cls.isDynamic(),False)
		self.assertEqual(cls.isFinal(),False)
		self.assertEqual(cls.isPublic(),False)
		self.assertEqual(cls.extends,"Object")
		self.assertEqual(cls.implements,set())
		self.assertEqual(cls.includes,set())
	def testClassModifiers(self):
		cls = asModel.ClassDef()
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