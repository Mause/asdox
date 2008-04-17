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
import os,fnmatch
from asModel import *

def parsePackage( s,l,t ):
    pkg = ASPackage(t.name)
    if len(t.classes) > 0:
	for cls in t.classes:
	    pkg.addClass( cls[0] )
    for imp in t.imports:
	pkg.addImport(imp)
    for inc in t.includes:
	pkg.addInclude(inc)
    return pkg
def parseClass( s,l,t ):
    cls = ASClass(t.name)
    if t.type == "interface":
	cls.setInterface(True)
    if len(t.includes) > 0:
	for inc in t.includes:
	    cls.addInclude(inc[0])
    if len(t.fields) > 0:
	for f in t.fields:
	    cls.addField(f[0])
    if len(t.methods) > 0:
	for m in t.methods:
	    cls.addMethod(m[0])
    if len(t.metadata) > 0:
	for m in t.metadata:
	    cls.addMetaTag(m[0])
    for mod in t.modifiers:
	cls.addModifier(mod)
    if len(t.class_implements) > 0:
	for imp in t.class_implements[0]:
	    cls.addImplement(imp)
    cls.setExtends(t.extends)
    return cls
def getField( s,l,t ):
    fld = ASField(t.name,t.type[0])
    for mod in t.modifiers:
	fld.addModifier(mod)
    for m in t.metadata:
	fld.addMetaTag(m[0])
    fld.addModifier(t.kind)
    return fld
def parseField( s,l,t ):
    fld = ASField(t.name,t.type)
    fld.addModifier(t.modifier)
    fld.addModifier(t.kind)
    return fld
def getMethod( s,l,t ):
    fc = ASMethod(t.name,t.type[0])
    fc.setAccessor(t.accessor)
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
    arg = ASArg(t.name,t.type[0])
    return arg
def getMetaData(s,l,t):
    meta = ASMetaTag(t.name)
    for att in t.attributes:
	if att.key == "":
	    meta.addParam(att.value)
	else:
	    meta.addParam(att.value,att.key)
    return meta
def parseJavaDoc(s,l,t):
    pass
def test(s,l,t):
    print t
def locate(pattern, root=os.getcwd()):
		for path, dirs, files in os.walk(root):
			for filename in [os.path.abspath(os.path.join(path, filename)) for filename in files if fnmatch.fnmatch(filename, pattern)]:
				yield filename
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
MXINTERNAL = Keyword("mx_internal")
STATIC = Keyword("static")
PROTOTYPE = Keyword("prototype")
FINAL = Keyword("final")
OVERRIDE = Keyword("override")
NATIVE = Keyword("native")
DYNAMIC = Keyword("dynamic")
USE = Keyword("use")
NAMESPACE = Keyword("namespace")
VAR = Keyword("var")
CONST = Keyword("const")
GET = Keyword("get")
SET = Keyword("set")
DOT = "."
STAR = "*"
TERMINATOR = SEMI ^ White("\r\n")

point = Literal('.')
e = CaselessLiteral('E')
plusorminus = Literal('+') | Literal('-')
number = Word(nums) 
integer = Combine( Optional(plusorminus) + number )
floatnumber = Combine( integer + Optional( point + Optional(number) ) + Optional( e + integer ) )

javaDocComment = Regex(r"/\*\*(?:[^*]*\*+)+?/").setParseAction(parseJavaDoc)
comment = (dblSlashComment ^ cStyleComment).suppress()
comments = ZeroOrMore( comment )

identifier = Word(alphas + '_',alphanums + '_') 
fully_qualified_identifier = Combine(identifier + ZeroOrMore( DOT + identifier ))
type = COLON + (identifier ^ STAR )

attribute = floatnumber ^ fully_qualified_identifier ^ QuotedString(quoteChar="\"", escChar='\\',unquoteResults=False) ^ QuotedString(quoteChar="'", escChar='\\',unquoteResults=False) ^ integer
metadata_attributes = LPARN + delimitedList( Group(Optional(identifier("key") + EQUAL) + attribute("value")).setResultsName("attributes",listAllMatches="true") ) + RPARN
metadata = ( Optional(javaDocComment) + LSQUARE + identifier("name") + Optional( metadata_attributes ) + RSQUARE).setParseAction(getMetaData)

variable_kind = VAR ^ CONST
variable_init = EQUAL + Optional( QuotedString(quoteChar="\"", escChar='\\') ^ integer  ^ floatnumber ^ fully_qualified_identifier)
variable = identifier("name") + Optional(type("type"),"*") + Optional( variable_init ) 
variable_definition = variable_kind("kind") + identifier("name") + Optional(type("type"),"*") + Optional( variable_init ) + TERMINATOR
argument_definition = variable + Optional( variable_init )

function_name = Optional( GET ^ SET )("accessor") + identifier("name")
function_block = Suppress( nestedExpr("{","}") )
function_arguments = delimitedList(argument_definition.setParseAction(getArgument))
function_signature = FUNCTION + function_name + LPARN + Optional( function_arguments("args") ) + RPARN + Optional( type, "void" )("type")
_function = function_signature + function_block

include_definition = INCLUDE + QuotedString(quoteChar="\"", escChar='\\') + TERMINATOR
import_definition = IMPORT + fully_qualified_identifier + Optional(DOT + STAR) + TERMINATOR
import_definitions = Group(import_definition).setResultsName("imports",listAllMatches="true")
include_definitions = Group(include_definition).setResultsName("includes",listAllMatches="true")
metadata_definitions = Group(metadata).setResultsName("metadata",listAllMatches="true")


use_namespace = USE + NAMESPACE + fully_qualified_identifier + TERMINATOR
# Modifier Definitions
base_attributes = INTERNAL ^ PUBLIC
extended_attributes = base_attributes ^ PRIVATE ^ PROTECTED ^ MXINTERNAL
class_attributes = Optional(base_attributes, "internal") + ( Optional(FINAL) & Optional(DYNAMIC) )
class_block_attributes = Optional(extended_attributes,"internal") &  Optional(STATIC) & Optional(PROTOTYPE) 
class_method_attributes = class_block_attributes &  Optional(FINAL) & Optional(OVERRIDE) & Optional(NATIVE) 

class_variables = ( ZeroOrMore(metadata_definitions) + Optional(javaDocComment) + class_block_attributes("modifiers") + variable_definition).setParseAction(getField)
class_method = ( ZeroOrMore(metadata_definitions) + Optional(javaDocComment) + class_method_attributes.setResultsName("modifiers",listAllMatches="true") + _function).setParseAction(getMethod)
method_definitions = Group(class_method).setResultsName("methods",listAllMatches="true")
field_definitions = Group(class_variables).setResultsName("fields",listAllMatches="true")
class_block = LCURL + ZeroOrMore( comment ^ include_definitions ^ field_definitions ^ method_definitions ) + RCURL
class_implements = IMPLEMENTS + delimitedList( fully_qualified_identifier ).setResultsName("class_implements",listAllMatches="true")
class_extends = EXTENDS + fully_qualified_identifier("extends")
class_inheritance = Optional( class_extends ) + Optional( class_implements )
class_definition = ( ZeroOrMore(metadata_definitions ^ include_definitions ^ use_namespace ^ comment) + Optional(javaDocComment) + class_attributes("modifiers") + CLASS("type") + fully_qualified_identifier("name") + class_inheritance + class_block).setParseAction(parseClass)
interface_definition = Optional( base_attributes ) + INTERFACE("type") + fully_qualified_identifier + Optional( class_extends ) + LCURL + ZeroOrMore( function_signature ) + RCURL


class_definitions = Group(class_definition).setResultsName("classes",listAllMatches="true")
package_block = LCURL + ZeroOrMore(comment ^ import_definitions ^ include_definitions ^ class_definitions ^ use_namespace)  + RCURL
package_definition = ( comments + PACKAGE("type") + Optional( fully_qualified_identifier("name") ) + package_block).setParseAction(parsePackage)

source = ZeroOrMore( package_definition )

########################## NEW GRAMMAR DEFINITION ##############################
IDENTIFIER = Word(alphas + '_',alphanums + '_') 
QUALIFIED_IDENTIFIER = Combine(IDENTIFIER + ZeroOrMore( DOT + IDENTIFIER ))
SINGLE_LINE_COMMENT = dblSlashComment
MULTI_LINE_COMMENT = cStyleComment
JAVADOC_COMMENT = Regex(r"/\*\*(?:[^*]*\*+)+?/")
COMMENTS = SINGLE_LINE_COMMENT ^ JAVADOC_COMMENT ^ MULTI_LINE_COMMENT
DBL_QUOTED_STRING = QuotedString(quoteChar="\"", escChar='\\')
SINGLE_QUOTED_STRING = QuotedString(quoteChar="'", escChar='\\')
ARRAY_INIT = LSQUARE + RSQUARE
VALUE = floatnumber ^ QUALIFIED_IDENTIFIER ^ DBL_QUOTED_STRING ^ SINGLE_QUOTED_STRING ^ integer
INIT = QuotedString(quoteChar="=", endQuoteChar=";",escChar='\\')
TYPE = COLON + (QUALIFIED_IDENTIFIER ^ STAR)
VARIABLE_MODIFIER = IDENTIFIER
VARIABLE_DEFINITION = Optional(VARIABLE_MODIFIER) + Optional(STATIC) + Optional(CONST ^ VAR) + IDENTIFIER  + Optional(TYPE) + Optional(MULTI_LINE_COMMENT) + (INIT ^ TERMINATOR)
USE_NAMESPACE = USE + NAMESPACE + fully_qualified_identifier + TERMINATOR
ATTRIBUTES = delimitedList( Optional(IDENTIFIER + EQUAL) + VALUE )
METATAG = LSQUARE + IDENTIFIER + Optional( LPARN + ATTRIBUTES + RPARN ) + RSQUARE
INCLUDE_DEFINITION = INCLUDE + QuotedString(quoteChar="\"", escChar='\\') + TERMINATOR
IMPORT_DEFINITION = IMPORT + QUALIFIED_IDENTIFIER + Optional(DOT + STAR) + TERMINATOR
BLOCK = Suppress( nestedExpr("{","}") )
BASE_BLOCK = USE_NAMESPACE ^ COMMENTS ^ METATAG ^ INCLUDE_DEFINITION
METHOD_MODIFIER = STATIC ^ OVERRIDE ^ FINAL
METHOD_PARAMETERS = delimitedList( IDENTIFIER + TYPE + Optional( EQUAL + VALUE ) )
METHOD_DEFINITION = Optional(METHOD_MODIFIER) & Optional(IDENTIFIER) + FUNCTION + Optional(GET ^ SET) + IDENTIFIER + LPARN + Optional(METHOD_PARAMETERS) + RPARN + Optional( TYPE ) + BLOCK
CLASS_IMPLEMENTS = IMPLEMENTS + delimitedList( QUALIFIED_IDENTIFIER )
CLASS_BLOCK = LCURL + ZeroOrMore( BASE_BLOCK ^ VARIABLE_DEFINITION ^ METHOD_DEFINITION ) + RCURL
CLASS_EXTENDS = EXTENDS + QUALIFIED_IDENTIFIER
CLASS_MODIFIERS = Optional(FINAL) & Optional(PUBLIC)
CLASS_DEFINITION = CLASS_MODIFIERS + CLASS + QUALIFIED_IDENTIFIER + Optional( CLASS_EXTENDS ) + Optional( CLASS_IMPLEMENTS ) + CLASS_BLOCK
PACKAGE_BLOCK = LCURL + ZeroOrMore( IMPORT_DEFINITION ^ BASE_BLOCK ^ CLASS_DEFINITION ) + RCURL
PACKAGE_DEFINITION = PACKAGE + Optional( QUALIFIED_IDENTIFIER ) + PACKAGE_BLOCK
PROGRAM = ZeroOrMore( COMMENTS.suppress() ) + PACKAGE_DEFINITION


files = locate("B*.as","C:\\flex_sdk_3\\frameworks\\projects\\framework\\src\\mx\\controls")
for f in files:
    print f
    try:
	PROGRAM.parseFile(f)
    except ParseException, err:
	print err
