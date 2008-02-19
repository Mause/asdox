from Cheetah.Template import Template
from asdox import asBuilder

builder = asBuilder.Builder()
builder.addSource("""
package com.gurufaction.myApp
{
	public class Person
        {
        	private var _name:String;
                private var _age:int;
                private var _gender:String;
                private var _dob:DateTime;
                
                public function get Name():String
                {
                	return _name;
                }
                
                public function set Name(value:String):void
                {
                	_name = value;
                }
                
                public function get Gender():String
                {
                	return _gender;
                }
                
                public function set Gender(value:String):void
                {
                	_gender = value;
                }
                
                public function get DOB():DateTime
                {
                	return _dob;
                }
                
                public function set DOB(value:DateTime):void
                {
                	_dob = value;
                }
                
                // Age Property is Read-Only
                public function get Age():int
                {
                	return _age;
                }
                
        }
}
""")

pkg = builder.getPackage("com.gurufaction.myApp")

template = """
<?php

class $cls.getName()
{
	#for $name in $cls.getGetters().values()
	var $$name.getName().lower();
	#end for
	
	function $cls.getName()()
	{
	}
	
	#for $meth in $cls.getGetters().values()
	function get$meth.getName()()
	{
		return #raw$this->#end raw$meth.getName().lower();
	}
	
	#if $cls.hasSetter($meth.getName())
	function set$meth.getName()(${meth.getName().lower()}In)
	{
		#raw$this->#end raw$meth.getName().lower() = ${meth.getName().lower()}In;
	}
	#end if
	#end for
        
        function hasEqualMapping(#raw$valueObject#end raw)
        {
        	#for $name in $cls.getGetters().values()
                if (#raw$valueObject#end raw.get${name.getName()}() != #raw$this->#end raw$name.getName().lower()) 
                {
                    return(false);
                }
                #end for
        	return true;
        }
        
        function clone()
        {
        	#raw$clone #end raw = new $cls.getName()();
                #for $name in $cls.getSetters().values()
                #raw$clone#end raw->set${name.getName()}(#raw$this->#end raw$name.getName().lower());
                #end for
                return #raw$clone#end raw;
        }
        
        function toString()
        {
        	#raw$out#end raw = "";
                #raw$out = $out #end raw . "$cls.getName()\\n";
        	#for $name in $cls.getGetters().values()
                #raw$out = $out #end raw . "${name.getName()}: " . #raw$this->#end rawget${name.getName()}() . "\\n";
                #end for
                return #raw$out#end raw
        }
        
        function toXML()
        {
        	#raw$out#end raw = "";
                #raw$out = $out .#end raw "<$cls.getName()>";
        	#for $name in $cls.getGetters().values()
                #raw$out = $out .#end raw "<${name.getName()}>" . #raw$this->#end rawget${name.getName()}() . "</${name.getName()}>";
                #end for
                #raw$out = $out .#end raw "</$cls.getName()>";
                return #raw$out#end raw
        }
}
?>
"""
nameSpace = {'cls': pkg.getClass("Person")}
t = Template(template, searchList=[nameSpace])
print t