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

class BaseDef:
	"Base Definition"
	name = ""
	type = ""
	def __init__(self,name,type):
		self.name = name
		self.type = type
class ObjectDef:
	modifiers = set()
	metadata = list()
	def hasModifier(self,mod):
		return mod in self.modifiers
class MetaDataDef(BaseDef):
	"MetaData Definition"
	attributes = dict()
	def __init__(self,name = "",type = "metadata"):
		self.name = name
		self.type = type
class PackageDef(BaseDef):
	"Package Definition"
	classes = list()
	imports = set()
	includes = set()

class ClassDef(ObjectDef):
	"Class Definition"
	variables = list()
	methods = list()
	extends = "Object"
	implements = set()
	includes = set()
	def __init__(self,name = "",type = "class"):
		self.name = name;
		self.type = type;
	def isDynamic(self):
		return self.hasModifier("dynamic")
	def isFinal(self):
		return self.hasModifier("final")
	def isPublic(self):
		return self.hasModifier("public")
	def isInterface(self):
		return self.type == "interface"
	
class VariableDef(ObjectDef):
	"Variable Definition"
	def __init__(self, name = "", type = "*"):
		self.name = name
		self.type = type
	def isStatic(self):
		return self.hasModifer("static")
	def isConstant(self):
		pass
	
class FunctionDef(ObjectDef):
	"Function Definition"
	def __init__(self, name = "", type = "void"):
		self.name = name
		self.type = type
	arguments = list()