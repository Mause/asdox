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
                private var _addresses:ArrayCollection;
                
                public function get Name():String
                {
                	return _name;
                }
                
                public function set Name(value:String):void
                {
                	_name = value;
                }
                [Column(length=1)]
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
                [HasOne(name="Mother")]
                [Ignore]
                public function get Mother():Mother
                {
                	return _mom;
                }
                
        }
}
""")

pkg = builder.getPackage("com.gurufaction.myApp")

template = """
<?php

class $cls.getName() extends Doctrine_Record
{
	public function setUp()
        {
       	#for $name in $cls.getGetters().values()
		#if $name.hasMetaTag("HasOne")
                	#set $tag = $name.getMetaTag("HasOne")
                        #if $tag.hasParam("name")
                #raw$this->#end rawhasOne('$tag.getParam("name")')
                
                        #end if
                #end if
	#end for
        }
        
	public function setTableDefinition()
        {
            #for $name in $cls.getGetters().values()
                #set $column_name = $name.getName().lower()
                #set $column_type = $name.getType().lower()
                #set $column_length = 'null'
                #set $array = dict()
                #if $name.hasMetaTag("Ignore") == False
                #if $name.hasMetaTag("Column")
                	#set $tag = $name.getMetaTag("Column")
                        #for $key,$value in $tag.getParams().items()
                        	#if $key == "name"
                                    #set $column_name = $value
                                #else if $key == "type"
                                    #set $column_type = $value
                                #else if $key == "length"
                                    #set $column_length = $value
                                #else
                                	#set $array[$key] = $value
                                #end if
                        #end for
                #end if
                #raw$this->#end rawhasColumn('$column_name','$column_type'#slurp
                #if len($array) > 0
,$column_length,
			array(
                        #set $counter = 1
                	#for $key, $value in $array.items()
                        	#set $counter = $counter + 1
                        '$key' => $value#slurp
                        	#if $counter == len($array)
,
                        	#end if
                        #end for
                #else
                	#if $column_length != "null"
,$column_length#slurp
                        #end if
                #end if
);                
                #end if
            #end for
        }
}
?>
"""
nameSpace = {'cls': pkg.getClass("Person")}
t = Template(template, searchList=[nameSpace])
print t