from Cheetah.Template import Template
from asdox import asBuilder

builder = asBuilder.Builder()
builder.addSource("""
package com.gurufaction.myApp
{
	public class MyClass
        {
        	private var _name:String;
                private var _age:int;
                
                public function get name():String
                {
                	return _name;
                }
                
                public function set name(value:String):void
                {
                	_name = value;
                }
                
                // Age Property is Read-Only
                public function get age():int
                {
                	return _age;
                }
                
        }
}
""")

pkg = builder.getPackage("com.gurufaction.myApp")

c_sharp_template = """
using System;

namespace $pkg.getName()
{
	#for $key,$cls in $pkg.getClasses().items()
        #if $cls.hasModifier("public")
        public class $cls.getName()
        {
        	#for $key,$value in $cls.getGetters().items()
                #if $value.hasModifier("public")
                public $value.getType() $value.getName()
                {
                        get { return _$value.getName().lower(); }
                        #if $cls.hasSetter($value.getName())
                        set {  _$value.getName().lower() = value; }   
                        #end if
                }
                
                #end if
                #end for
        }
        #end if
        #end for
}
"""
nameSpace = {'pkg': pkg}
t = Template(c_sharp_template, searchList=[nameSpace])
print t