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
from pyparsing import *
from asModel import *

def getPackage( s,l,t ):
    pkg = PackageDef(t.name,t.type)
    if len(t.class_definitions) > 0:
	for cls in t.class_definitions[0]:
	    pkg.addClass( cls )
    pkg.imports = set(t.imports)
    pkg.includes = set(t.includes)
    return pkg

def getClass( s,l,t ):
    cls = ClassDef(t.name,t.type)
    if len(t.class_includes) > 0:
    	cls.includes = set(t.class_includes[0])
    if len(t.methods) > 0:
	for m in t.methods[0]:
	    cls.addMethods(m)
    if len(t.meta) > 0:
	for m in t.meta[0]:
	    cls.addMetadata(m)
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
    	fc.arguments = st.args
    return fc

def getArgument(s,l,t):
    arg = BaseDef(t.name,t.type)
    return arg

def getMetaData(s,l,t):
    meta = MetaDataDef(t.name)
    return meta
    
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
metadata = (LSQUARE + identifier("name") + Optional( metadata_attributes ) + RSQUARE).setParseAction(getMetaData)

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
classDef = (ZeroOrMore(metadata).setResultsName("meta",listAllMatches="true") + class_attributes("class_modifiers") + CLASS("type") + class_name("name") + class_inheritance + class_block).setParseAction(getClass)
_interface = Optional( base_attributes ) + INTERFACE + class_name + Optional( class_extends ) + LCURL + ZeroOrMore( function_signature ) + RCURL

package_block = LCURL + ZeroOrMore( Group(_import).setResultsName("imports",listAllMatches="true") ^ Group(_include).setResultsName("includes",listAllMatches="true") ^ Group(classDef).setResultsName("class_definitions",listAllMatches="true") ) + RCURL
packageDef = (PACKAGE("type") + Optional( package_name("name") ) + package_block).setParseAction(getPackage)

source = ZeroOrMore( packageDef ^ _import ^ _include ^ _function )