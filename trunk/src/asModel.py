#asBuilder.py

class BaseDef:
	"Base Definition"
	name = ""
	type = ""
	def __init__(self,name,type):
		self.name = name
		self.type = type
	def hasModifier(self,mod):
		return mod in self.modifiers

class PackageDef(BaseDef):
	"Package Definition"
	classes = set()
	imports = set()
	includes = set()

class ClassDef(BaseDef):
	"Class Definition"
	variables = set()
	methods = set()
	extends = "Object"
	implements = set()
	modifiers = set()
	includes = set()
	def __init__(self,name,type = "class"):
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
	
class VariableDef(BaseDef):
	"Variable Definition"
	modifiers = set()
	def isStatic(self):
		return self.hasModifer("static")
	def isConstant(self):
		pass
	
class FunctionDef(BaseDef):
	"Function Definition"
	modifiers = set()
	arguments = list()