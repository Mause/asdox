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
		return self.__namespace.get(name,ASNamespace(""))
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
	__metaTag = dict()
	def __init__(self):
		self.__metaTag = dict()
	def addMetaTag(self,tag):
		self.__metaTags[tag.getName()] = tag
	def removeMetaTag(self,name):
		del self.__metaTags[name]
	def getMetaTag(self,name):
		return self.__metaTags.get(name,ASMetaTag(""))
	def getMetaTags(self):
		return self.__metaTags
class ASMetaTag(Typeable):
	"Actionscript MetaTag Definition"
	__params = dict()
	def __init__(self,name = ""):
		self.__params = dict()
		self._Typeable__name = name
		self._Typeable__type = "metatag"
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
	__classes = dict()
	__imports = set()
	def __init__(self,name = ""):
		self.__classes = dict()
		self.__imports = set()
		self._Typeable__name = name;
		self._Typeable__type = "package";
		self._Includable__includes = set()
		self._Namespacable__namespaces = dict()
		self._Namespacable__used_namespaces = set()
	def addClass(self,cls):
		self.__classes[cls.getName()] = cls
	def removeClass(self,name):
		del self.__classes[name]
	def getClass(self,name):
		return self.__classes.get(name,ASClass(""))
	def getClasses(self):
		return self.__classes
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
	def __init__(self,name = ""):
		self.__fields = dict()
		self.__methods = dict()
		self.__extends = "Object"
		self._Typeable__name = name
		self._Typeable__type = "class"
		self._MetaTagable__metaTags = dict()
		self._Modifiable__modifiers.add("internal")
		self._Modifiable__ACCESS_MODIFIERS = set(['public','internal'])
		self._Modifiable__TYPE_MODIFIERS =  set(['final','dynamic'])
		self._Includable__includes = set()
		self._Namespacable__namespaces = dict()
		self._Namespacable__used_namespaces = set()
		self._Implementable__implements = set()
	def addField(self,field):
		self.__fields[field.getName()] = field
	def removeField(self,name):
		del self.__fields[name]
	def getField(self,name):
		return self.__fields.get(name,ASField(""))
	def getFields(self):
		return self.__fields
	def addMethod(self,method):
		self.__methods[method.getName()] = method
	def removeMethod(self,name):
		del self.__methods[name]
	def getMethod(self,name):
		return self.__methods.get(name,ASMethod(""))
	def getMethods(self):
		return self.__methods
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
		return self._Typeable__type == "interface"
	def setInterface(self,yes):
		if yes == True:
			self._Typeable__type = "interface"
		else:
			self._Typeable__type = "class"
class ASNamespace(Typeable,Modifiable):
	"Actionscript Namespace Definition"
	def __init__(self, name = ""):
		self._Typeable__name = name;
		self._Typeable__type = "namespace"
		self._Modifiable__modifiers = set()
		self._Modifiable__ACCESS_MODIFIERS = set(['public','internal','private','protected'])
class ASField(Typeable,Modifiable,MetaTagable,Documentable,NamespaceModifiable):
	"Actionscript Field Definition"
	def __init__(self, name = "", type = "*"):
		self._Typeable__name = name
		self._Typeable__type = type
		self._Modifiable__modifiers.add("internal")
		self._MetaTagable__metaTags = dict()
		self._Modifiable__ACCESS_MODIFIERS = set(['public','internal','private','protected'])
		self._Modifiable__TYPE_MODIFIERS =  set(['static','const'])
		self._NamespaceModifiable__namespace = None
	def isStatic(self):
		return self.hasModifier("static")
	def isConstant(self):
		return self.hasModifier("const")	
class ASArg(Typeable):
	def __init__(self, name = "", type = "*"):
		self._Typeable__name = name
		self._Typeable__type = type
class ASMethod(Typeable,Modifiable,MetaTagable,Documentable,NamespaceModifiable):
	"Actionscript Method Definition"
	__args = dict()
	def __init__(self, name = "", type = "void"):
		self.__args = dict()
		self._Typeable__name = name
		self._Typeable__type = type
		self._MetaTagable__metaTags = dict()
		self._NamespaceModifiable__namespace = None
		self._Modifiable__modifiers = set()
		self._Modifiable__ACCESS_MODIFIERS = set(['public','internal','private','protected'])
		self._Modifiable__TYPE_MODIFIERS =  set(['final','override','static'])
	def addArgument(self,arg):
		self.__args[arg.getName()] = arg
	def removeArgument(self,name):
		del self.__args[name]
	def getArgument(self,name):
		return self.__args.get(name,ASArg(""))
	def getArguments(self):
		return self.__args