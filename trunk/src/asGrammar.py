# as3g.py

from pyparsing import *
from asModel import *

def getPackage( s,l,t ):
    pkg = PackageDef(t.name,t.type)
    if len(t.class_definitions) > 0:
    	pkg.classes = t.class_definitions[0]
    pkg.imports = set(t.imports)
    pkg.includes = set(t.includes)
    return pkg

def getClass( s,l,t ):
    cls = ClassDef(t.name,t.type)
    if len(t.class_includes) > 0:
    	cls.includes = set(t.class_includes[0])
    if len(t.methods) > 0:
    	cls.methods = set(t.methods[0])
    cls.modifiers = set(t.class_modifiers)
    if len(t.class_implements) > 0:
    	cls.implements = set(t.class_implements[0])
    cls.extends = t.extends
    return cls

def getMethod( s,l,t ):
    fc = FunctionDef(t.name,t.type)
    if len(t.modifiers) > 0:
    	fc.modifiers = set(t.modifiers[0])
    if len(t.args) > 0:
    	fc.arguments = set(t.args)
    return fc

def getArgument(s,l,t):
    arg = BaseDef(t.name,t.type)
    return arg
    
COLON,LPARN,RPARN,LCURL,RCURL,EQUAL,SEMI,LSQUARE,RSQUARE = map(Suppress,":(){}=;[]")

PACKAGE = Keyword("package")
CLASS = Keyword("class")
IMPLEMENTS = Keyword("implements").suppress()
EXTENDS = Keyword("extends").suppress()
FUNCTION = Keyword("function").suppress()
IMPORT = Keyword("import").suppress()
INCLUDE = Keyword("include").suppress()
INTERFACE = Keyword("interface")
INTERNAL = Keyword("internal")
PUBLIC = Keyword("public")
PRIVATE = Keyword("private")
PROTECTED = Keyword("protected")
STATIC = Keyword("static")
PROTOTYPE = Keyword("prototype")
FINAL = Keyword("final")
OVERRIDE = Keyword("override")
NATIVE = Keyword("native")
DYNAMIC = Keyword("dynamic")
VAR = Keyword("var")
CONST = Keyword("const")
GET = Keyword("get")
SET = Keyword("set")
DOT = "."
STAR = "*"

point = Literal('.')
e = CaselessLiteral('E')
plusorminus = Literal('+') | Literal('-')
number = Word(nums) 
integer = Combine( Optional(plusorminus) + number )
floatnumber = Combine( integer + Optional( point + Optional(number) ) + Optional( e + integer ) )

singleline_comment = ZeroOrMore( "//" + restOfLine )
comments = Optional( singleline_comment) + Optional( ZeroOrMore( cStyleComment ) )

identifier = Word(alphas + '_',alphanums + '_') 
type = COLON + (identifier ^ STAR )

named_attribute = identifier + EQUAL + QuotedString(quoteChar="\"", escChar='\\')
attribute = identifier ^ QuotedString(quoteChar="\"", escChar='\\') ^ integer
metadata_attributes = LPARN + delimitedList( attribute ^ named_attribute) + RPARN
metadata = LSQUARE + identifier + Optional( metadata_attributes ) + RSQUARE

variable_kind = VAR ^ CONST
variable_init = EQUAL + Optional( QuotedString(quoteChar="\"", escChar='\\') ^ integer )
variable = identifier("name") + Optional(type("type"),"*") + Optional( variable_init ) 
variable_definition = variable_kind + variable + SEMI
argument_definition = variable

function_name = Optional( GET ^ SET ) + identifier
function_block = Suppress( nestedExpr("{","}") )
function_arguments = delimitedList(argument_definition.setParseAction(getArgument))
function_signature = FUNCTION + function_name("name") + LPARN + Optional( function_arguments("args") ) + RPARN + Optional( type("type"), "void" )
_function = function_signature + function_block

package_name = Combine(identifier + ZeroOrMore( DOT + (identifier ^ STAR) ))
_include = INCLUDE + QuotedString(quoteChar="\"", escChar='\\')
_import = IMPORT + package_name + SEMI
base_attributes = INTERNAL ^ PUBLIC
extended_attributes = base_attributes ^ PRIVATE ^ PROTECTED
class_attributes = Optional(base_attributes, "internal") + Optional( FINAL ) + Optional( DYNAMIC )
class_block_attributes = Optional(extended_attributes, "internal") + Optional(STATIC) + Optional(PROTOTYPE)
class_method_attributes = class_block_attributes + Optional(FINAL) + Optional(OVERRIDE) + Optional(NATIVE)
class_variables = ZeroOrMore(metadata) + class_block_attributes + variable_definition
class_method = (ZeroOrMore(metadata) + class_method_attributes.setResultsName("modifiers",listAllMatches="true") + _function).setParseAction(getMethod)
class_block = LCURL + ZeroOrMore(_include).setResultsName("class_includes",listAllMatches="true") ^ ZeroOrMore(class_variables) ^ ZeroOrMore(class_method).setResultsName("methods",listAllMatches="true") + RCURL
class_name = Combine(identifier + ZeroOrMore( DOT + identifier ))
class_implements = IMPLEMENTS + delimitedList( class_name ).setResultsName("class_implements",listAllMatches="true")
class_extends = EXTENDS + class_name("extends")
class_inheritance = Optional( class_extends ) + Optional( class_implements )
classDef = (ZeroOrMore(metadata) + class_attributes("class_modifiers") + CLASS("type") + class_name("name") + class_inheritance + class_block).setParseAction(getClass)
_interface = Optional( base_attributes ) + INTERFACE + class_name + Optional( class_extends ) + LCURL + ZeroOrMore( function_signature ) + RCURL

package_block = LCURL + ZeroOrMore( Group(_import).setResultsName("imports",listAllMatches="true") ^ Group(_include).setResultsName("includes",listAllMatches="true") ^ Group(classDef).setResultsName("class_definitions",listAllMatches="true") ) + RCURL
packageDef = (PACKAGE("type") + Optional( package_name("name") ) + package_block).setParseAction(getPackage)

source = ZeroOrMore( packageDef ^ _import ^ _include ^ classDef ^ _function )