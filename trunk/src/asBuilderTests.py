#asBuilderTests.py
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