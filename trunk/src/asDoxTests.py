# asDoxTests.py
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