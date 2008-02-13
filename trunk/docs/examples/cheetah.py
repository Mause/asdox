from Cheetah.Template import Template
from asdox import asBuilder

builder = asBuilder.Builder()
builder.addSource("""
package com.gurufaction.myApp
{
	public class MyClass
        {
        	public var name:String;
                public var age:int;
        }
}
""")

pkg = builder.getPackage("com.gurufaction.myApp")

c_sharp_template = """
using System;

namespace $pkg.getName()
{
	#for $key,$value in $pkg.getClasses().items()
        #if $value.hasModifier("public")
        public class $value.getName()
        {
        	#for $key,$value in $value.getFields().items()
                #if $value.hasModifier("public")
                public $value.getType() $value.getName();
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