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
	def testBasicClass(self):
		cls = asModel.ClassDef("MyClass")
		self.assertEqual(cls.name,"MyClass")
		self.assertEqual(cls.type,"class")
		self.assertEqual(cls.isInterface(),False)
		self.assertEqual(cls.isDynamic(),False)
		self.assertEqual(cls.isFinal(),False)
		self.assertEqual(cls.isPublic(),False)
		self.assertEqual(cls.extends,"Object")
		self.assertEqual(cls.methods,set())
		self.assertEqual(cls.variables,set())
		self.assertEqual(cls.methods,set())
		self.assertEqual(cls.implements,set())
		self.assertEqual(cls.includes,set())
	def testBasicInterface(self):
		cls = asModel.ClassDef("com.gurufaction.TestClass")
		cls.type = "interface"
		self.assertEqual(cls.name,"com.gurufaction.TestClass")
		self.assertEqual(cls.type,"interface""Class not of type 'interface'")
		self.assertEqual(cls.isInterface(),True,"isInterface() method failed")
		self.assertEqual(cls.isDynamic(),False)
		self.assertEqual(cls.isFinal(),False)
		self.assertEqual(cls.isPublic(),False)
		self.assertEqual(cls.extends,"Object")
		self.assertEqual(cls.methods,set())
		self.assertEqual(cls.variables,set())
		self.assertEqual(cls.methods,set())
		self.assertEqual(cls.implements,set())
		self.assertEqual(cls.includes,set())
if __name__ == "__main__":
	unittest.main()