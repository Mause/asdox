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
    pkg = ASPackage(t.name)
    if len(t.class_definitions) > 0:
	for cls in t.class_definitions[0]:
	    pkg.addClass( cls )
    for imp in t.imports:
	pkg.addImport(imp)
    for inc in t.includes:
	pkg.addInclude(inc)
    return pkg

def getClass( s,l,t ):
    cls = ASClass(t.name)
    if t.type == "interface":
	cls.setInterface(True)
    if len(t.class_includes) > 0:
	for inc in t.class_includes:
	    cls.addInclude(inc[0])
    if len(t.class_fields) > 0:
	for f in t.class_fields:
	    cls.addField(f[0])
    if len(t.methods) > 0:
	for m in t.methods:
	    cls.addMethod(m[0])
    if len(t.meta) > 0:
	for m in t.meta[0]:
	    cls.addMetaTag(m)
    for mod in t.class_modifiers:
	cls.addModifier(mod)
    if len(t.class_implements) > 0:
	for imp in t.class_implements[0]:
	    cls.addImplement(imp)
    cls.setExtends(t.extends)
    return cls
def getField( s,l,t ):
    fld = ASField(t.name,t.type)
    for mod in t.field_modifiers:
	fld.addModifier(mod)
    for m in t.metadata:
	fld.addMetaTag(m[0])
    return fld
def getMethod( s,l,t ):
    fc = ASMethod(t.name[0])
    if len(t.modifiers) > 0:
	for mod in t.modifiers[0]:
	    fc.addModifier(mod)
    if len(t.args) > 0:
	for arg in t.args:
	    fc.addArgument(arg)
    for m in t.metadata:
	fc.addMetaTag(m[0])
    return fc
def getArgument(s,l,t):
    arg = ASArg(t.name,t.type)
    return arg

def getMetaData(s,l,t):
    meta = ASMetaTag(t.name)
    
    for att in t.attributes:
	if att.key == "":
	    meta.addParam(att.value)
	else:
	    meta.addParam(att.value,att.key)
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

singleline_comment = "//" + restOfLine
comment = (singleline_comment ^ cStyleComment).suppress()

identifier = Word(alphas + '_',alphanums + '_') 
type = COLON + (identifier ^ STAR )

attribute = identifier ^ QuotedString(quoteChar="\"", escChar='\\') ^ integer
metadata_attributes = LPARN + delimitedList( Group(Optional(identifier("key") + EQUAL) + attribute("value")).setResultsName("attributes",listAllMatches="true") ) + RPARN
metadata = (LSQUARE + identifier("name") + Optional( metadata_attributes ) + RSQUARE).setParseAction(getMetaData)

variable_kind = VAR ^ CONST
variable_init = EQUAL + Optional( QuotedString(quoteChar="\"", escChar='\\') ^ integer  ^ identifier)
variable = identifier("name") + Optional(type("type"),"*") + Optional( variable_init ) 
variable_definition = variable_kind("kind") + identifier("name") + Optional(type("type"),"*") + Optional( variable_init ) + SEMI
argument_definition = variable + Optional( variable_init )

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
class_variables = (ZeroOrMore(metadata).setResultsName("metadata",listAllMatches="true") + class_block_attributes("field_modifiers") + variable_definition).setParseAction(getField)
class_method = (ZeroOrMore(metadata ^ comment).setResultsName("metadata",listAllMatches="true") + class_method_attributes.setResultsName("modifiers",listAllMatches="true") + _function).setParseAction(getMethod)
class_block = LCURL + ZeroOrMore( comment ^ Group(_include).setResultsName("class_includes",listAllMatches="true") ^ Group(class_variables).setResultsName("class_fields",listAllMatches="true") ^ Group(class_method).setResultsName("methods",listAllMatches="true")) + RCURL
class_name = Combine(identifier + ZeroOrMore( DOT + identifier ))
class_implements = IMPLEMENTS + delimitedList( class_name ).setResultsName("class_implements",listAllMatches="true")
class_extends = EXTENDS + class_name("extends")
class_inheritance = Optional( class_extends ) + Optional( class_implements )
classDef = (ZeroOrMore(metadata ^ comment).setResultsName("meta",listAllMatches="true") + class_attributes("class_modifiers") + CLASS("type") + class_name("name") + class_inheritance + class_block).setParseAction(getClass)
_interface = Optional( base_attributes ) + INTERFACE + class_name + Optional( class_extends ) + LCURL + ZeroOrMore( function_signature ) + RCURL

package_block = LCURL + ZeroOrMore( comment ^ Group(_import).setResultsName("imports",listAllMatches="true") ^ Group(_include).setResultsName("includes",listAllMatches="true") ^ Group(classDef).setResultsName("class_definitions",listAllMatches="true") ) + RCURL
packageDef = ( ZeroOrMore(comment) + PACKAGE("type") + Optional( package_name("name") ) + package_block).setParseAction(getPackage)

source = ZeroOrMore( packageDef ^ _import ^ _include ^ _function )