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
	def addNamespace(self,namespace):
		self.__namespaces[namespace.name] = namespace
	def removeNamespace(self,name):
		del self.__namespaces[name]
	def useNamespace(self,name):
		self.__used_namespaces.add(name)
	def unUseNamespace(self,name):
		self.__used_namespaces.discard(name)
class NamespaceModifiable:
	__namespace = None
	def getNamespace(self):
		return self.__namespace
	def setNamespace(self,namespace):
		self.__namespace = namespace
class Modifiable:
	modifiers = set()
	ACCESS_MODIFIERS = set()
	TYPE_MODIFIERS =  set()
	def removeModifier(self,name):
		self.modifiers.discard(name)
	def addModifier(self, name):
		self.modifiers = self.modifiers.union( self.ACCESS_MODIFIERS.union(self.TYPE_MODIFIERS).intersection(set([name])) )
		if name in self.ACCESS_MODIFIERS:
			self.modifiers.difference_update( self.ACCESS_MODIFIERS.difference(set([name])))
	def hasModifier(self,name):
		return name in self.modifiers
	def getModifiers(self):
		return self.modifiers
class Typeable:
	"Actionscript Type Definition"
	name = ""
	type = ""
	def __init__(self,name,type):
		self.name = name
		self.type = type
	def getName(self):
		return self.name
	def setName(self,name):
		self.name = name
	def getType(self):
		return self.type
class MetaTagable:
	__metaTags = dict()
	def addMetTag(self,tag):
		self.__metaTags[tag.name] = tag
	def removeMetaTag(self,name):
		del self.__metaTags[name]
	def getMetadata(self,name):
		return self.__metaTags[name]
class ASMetaTag(Typeable):
	"Actionscript MetaTag Definition"
	__params = dict()
	def __init__(self,name = ""):
		self.name = name
		self.type = "metatag"
	def addParam(self,value,key = None):
		if key == None:
			self.__params[len(self.__params)] = value
		else:
			self.__params[key] = value
	def getParam(self,name):
		return self.__param[name]
	def getParams(self):
		return self.__params
class ASPackage(Typeable,Includable,Namespacable):
	"Actionscript Package Definition"
	def __init__(self,name = ""):
		self.name = name;
		self.type = "package";
	__classes = dict()
	__imports = set()
	def addClass(self,cls):
		self.__classes[cls.name] = cls
	def removeClass(self,name):
		del self.__classes[name]
	def getClass(self,name):
		return self.__classes[name]
	def getClasses(self):
		return self.__classes.values
	def addImport(self,name):
		self.__imports.add(name)
	def removeImport(self,name):
		self.__imports.discard(name)
	def getImports(self):
		return self.__imports
class ASClass(Typeable,Modifiable,MetaTagable,Documentable,Includable,Namespacable,Implementable):
	"Actionscript Class Definition"
	__fields = dict()
	__methods = dict()
	__extends = "Object"
	modifiers = set()
	ACCESS_MODIFIERS = set(['public','internal'])
	TYPE_MODIFIERS =  set(['final','dynamic'])
	def __init__(self,name = ""):
		self.name = name;
		self.type = "class";
		self.modifiers.add("internal")
	def addField(self,field):
		self.__fields[field.name] = field
	def removeField(self,field):
		del self.__fields[field.name]
	def getField(self,name):
		return self.__fields[name]
	def getFields(self):
		return self.__fields.values
	def addMethod(self,method):
		self.__methods[method.name] = method
	def removeMethod(self,name):
		del self.__methods[name]
	def getMethod(self,name):
		return self.__methods[name]
	def getMethods(self):
		return self.__methods.values
	def getExtends(self):
		return self.__extends
	def setExtends(self,name):
		self.__extends = name
	def isDynamic(self):
		return self.hasModifier("dynamic")
	def isFinal(self):
		return self.hasModifier("final")
	def isPublic(self):
		return self.hasModifier("public")
	def isInterface(self):
		return self.type == "interface"
	def setInterface(self,yes):
		if yes == True:
			self.type = "interface"
		else:
			self.type = "class"
class ASNamespace(Typeable,Modifiable):
	"Actionscript Namespace Definition"
	modifiers = set()
	ACCESS_MODIFIERS = set(['public','internal','private','protected'])
	def __init__(self, name = ""):
		self.name = name;
		self.type = "namespace"
class ASField(Typeable,Modifiable,MetaTagable,Documentable,NamespaceModifiable):
	"Actionscript Field Definition"
	modifiers = set()
	ACCESS_MODIFIERS = set(['public','internal','private','protected'])
	TYPE_MODIFIERS =  set(['static','const'])
	def __init__(self, name = "", type = "*"):
		self.name = name
		self.type = type
		self.modifiers.add("internal")
	def isStatic(self):
		return self.hasModifier("static")
	def isConstant(self):
		return self.hasModifier("const")	
class ASMethod(Typeable,Modifiable,MetaTagable,Documentable,NamespaceModifiable):
	"Actionscript Method Definition"
	__args = dict()
	modifiers = set()
	ACCESS_MODIFIERS = set(['public','internal','private','protected'])
	TYPE_MODIFIERS =  set(['final','override','static'])
	def __init__(self, name = "", type = "void"):
		self.name = name
		self.type = type
	def addArgument(self,arg):
		self.__args[arg.name] = arg
	def removeArgument(self,arg):
		del self.__args[arg.name]
	def getArgument(self,name):
		return self.__args[name]
	def getArguments(self):
		return self.__args.values