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

pkg = builder.packages["com.gurufaction.myApp"]

template = """
<?php

class $cls.name
{
	#for $property in $cls.properties.values()
	var $$property.name.lower();
	#end for
	
	function ${cls.name}()
	{
	}
	
	#for $property in $cls.properties.values()
        #if $property.visibility == "public"
        #if $property.readable
        function get${property.name}()
	{
		return #raw$this->#end raw$property.name.lower();
	}
        #end if
        
        #if $property.writable
        function set${property.name}()(${property.name.lower()}In)
	{
		#raw$this->#end raw$property.name.lower() = ${property.name.lower()}In;
	}
        #end if
        #end if
	#end for
        
        function hasEqualMapping(#raw$valueObject#end raw)
        {
        	#for $property in $cls.properties.values()
                #if $property.readable
                if (#raw$valueObject#end raw.get${property.name}() != #raw$this->#end raw$property.name.lower()) 
                {
                    return(false);
                }
                #end if
                #end for
        	return true;
        }
        
        function clone()
        {
        	#raw$clone #end raw = new ${cls.name}();
                #for $property in $cls.properties.values()
                #if $property.writable
                #raw$clone#end raw->set${property.name}(#raw$this->#end raw$property.name.lower());
                #end if
                #end for
                return #raw$clone#end raw;
        }
        
        function toString()
        {
        	#raw$out#end raw = "";
                #raw$out = $out #end raw . "$cls.name\\n";
        	#for $property in $cls.properties.values()
                #if $property.readable
                #raw$out = $out #end raw . "${property.name}: " . #raw$this->#end rawget${property.name}() . "\\n";
                #end if
                #end for
                return #raw$out#end raw
        }
        
        function toXML()
        {
        	#raw$out#end raw = "";
                #raw$out = $out .#end raw "<$cls.name>";
        	#for $property in $cls.properties.values()
                #if $property.readable
                #raw$out = $out .#end raw "<${property.name}>" . #raw$this->#end rawget${property.name}() . "</${property.name}>";
                #end if
                #end for
                #raw$out = $out .#end raw "</$cls.name>";
                return #raw$out#end raw
        }
}
?>
"""

nameSpace = {'cls': pkg.classes["Person"]}
t = Template(template, searchList=[nameSpace])
print t