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
class Includable:
	"Actionscript Object that allows for declaring includes"
	__includes = set()
	def __init__(self):
		self.__includes = set()
	def addInclude(self,name):
		self.__includes.add(name)
	def removeInclude(self,name):
		self.__includes.discard(name)
	def getIncludes(self):
		return self.__includes
	def hasInclude(self,name):
		return name in self.__includes
class Implementable:
	"Actionscript Object that allows for declaring implementation"
	__implements = set()
	def __init__(self):
		self.__implements = set()
	def addImplement(self,name):
		self.__implements.add(name)
	def removeImplement(self,name):
		self.__implements.discard(name)
	def getImplements(self):
		return self.__implements
	def hasImplement(self,name):
		return name in self.__implements
class Documentable:
	"Actionscript Object that allows for JavaDoc declaration"
	pass
class Namespacable:
	"Actionscript Object that allows for declaring and using namespaces"
	__namespaces = dict()
	__used_namespaces = set()
	def __init__(self):
		self.__namespaces = dict()
		self.__used_namespaces = set()
	def addNamespace(self,namespace):
		self.__namespaces[namespace.getName()] = namespace
	def removeNamespace(self,name):
		del self.__namespaces[name]
	def getNamespace(self,name):
		return self.__namespaces.get(name,None)
	def getNamespaces(self):
		return self.__namespaces
	def useNamespace(self,name):
		self.__used_namespaces.add(name)
	def unUseNamespace(self,name):
		self.__used_namespaces.discard(name)
class NamespaceModifiable:
	__namespace = None
	def __init__(self):
		self.__namespace = None
	def getNamespace(self):
		return self.__namespace
	def setNamespace(self,namespace):
		self.__namespace = namespace
class Visible:
	visibility = "internal"
	def __init__(self):
		self.visibility = "internal"
class Modifiable:
	"Actionscript Object that can be modified"
	__modifiers = set()
	__ACCESS_MODIFIERS = set()
	__TYPE_MODIFIERS =  set()
	def __init__(self):
		self.__modifiers = set()
		self.__ACCESS_MODIFIERS = set()
		self.__TYPE_MODIFIERS =  set()
	def removeModifier(self,name):
		self.__modifiers.discard(name)
	def addModifier(self, name):
		self.__modifiers = self.__modifiers.union( self.__ACCESS_MODIFIERS.union(self.__TYPE_MODIFIERS).intersection(set([name])) )
		if name in self.__ACCESS_MODIFIERS:
			self.__modifiers.difference_update( self.__ACCESS_MODIFIERS.difference(set([name])))
	def hasModifier(self,name):
		return name in self.__modifiers
	def getModifiers(self):
		return self.__modifiers
class Typeable:
	"Actionscript Type Definition"
	__name = ""
	__type = ""
	def __init__(self,name,type):
		self.__name = name
		self.__type = type
	def getName(self):
		return self.__name
	def setName(self,name):
		self.__name = name
	def getType(self):
		return self.__type
class MetaTagable:
	"Actionscript Object that allows for MetaTags"
	metadata = []
class ASType:
	"Actionscript 3 Type"
	def __init__(self,name,type):
		self.name = name
		self.type = type
	name = "";
	type = "";
class ASProperty(ASType,Visible,MetaTagable):
	"Actionscript getter/setter"
	readable = False
	writable = False
	def __init__(self, name = "", type = "*"):
		self.name = name
		self.type = type
		self.metadata = []
		self.readable = False
		self.writable = False
class ASVariable(ASType,Visible,MetaTagable):
	"Actionscript 3 Variable"
	def __init__(self, name = "", type = "*"):
		self.name = name
		self.type = type
		self.metadata = []
	isStatic = False
	isConstant = False
class ASMetaTag:
	"Actionscript MetaTag Definition"
	params = dict()
	name = ""
	def __init__(self,name = ""):
		self.name = name
		self.params = dict()
class ASClass(Visible,MetaTagable):
	"Actionscript Class Definition"
	name = ""
	variables = dict()
	methods = dict()
	properties = dict()
	extends = ""
	implements = []
	isDynamic = False
	isFinal = False
	isInterface = False
	def __init__(self, name = ""):
		self.name = name
		self.metadata = []
		self.variables = dict()
		self.methods = dict()
		self.properties = dict()
		self.extends = ""
		self.implements = []
		self.isDynamic = False
		self.isFinal = False
		self.isInterface = False
class ASPackage(Visible,MetaTagable):
	"Actionscript Package Definition"
	classes = dict()
	imports = []
	def __init__(self, name = ""):
		self.name = name
		self.metadata = []
		self.classes = dict()
		self.imports = []
	def toString(self):
		print "Package: " + self.name
		for cls in self.classes.values():
			print cls.visibility + " class " + cls.name + " implements " + str(cls.implements)
			for meta in cls.metadata:
				print "\t\t[" + meta.name + "]"
			for meth in cls.methods.values():
				for meta in meth.metadata:
					print "\t\t[" + meta.name + "]"
				print "\t\tMethod: " + meth.visibility + " " + meth.name + ":" + meth.type
				for arg in meth.arguments.values():
					print "\t\t\tArguments: " + arg.name + ":" + arg.type
			for var in cls.variables.values():
				for meta in var.metadata:
					print "\t\t[" + meta.name + "]"
				print "\t\tVariables: " + var.visibility + " " + var.name + ":" + var.type
			for prop in cls.properties.values():
				for meta in prop.metadata:
					print "\t\t[" + meta.name + "]"
				print "\t\tProperty: " + prop.visibility + " " + prop.name + ":" + prop.type
class ASNamespace(Typeable,Modifiable):
	"Actionscript Namespace Definition"
	def __init__(self, name = ""):
		self._Typeable__name = name;
		self._Typeable__type = "namespace"
		self._Modifiable__modifiers = set()
		self._Modifiable__ACCESS_MODIFIERS = set(['public','internal','private','protected'])	
class ASMethod(ASType,Visible,MetaTagable):
	"Actionscript Method Definition"
	arguments = dict()
	isOverride = False
	isFinal = False
	isStatic = False
	def __init__(self, name = "", type = "void"):
		self.name = name
		self.type = type
		self.metadata = []
		self.arguments = dict()
	