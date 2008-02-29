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
                
                [Column]
                public function get Name():String
                {
                	return _name;
                }
                
                public function set Name(value:String):void
                {
                	_name = value;
                }
                [Column(name='gender',type='string',length=1)]
                public function get Gender():String
                {
                	return _gender;
                }
                
                public function set Gender(value:String):void
                {
                	_gender = value;
                }
                
                [Column(notblank=true)]
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
                [HasOne(name='Forum_Thread as Threads',local='id',foreign='board_id')]
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
#def createMeth($meth_name,$params)
	#set $name = ""
        #set $type = ""
        #set $length = 'null'
        #set $array = dict()
	#for $key,$value in $params.items()
        	#if $key == "name"
                	#set $name = $value
                #else if $key == "type"
                	#set $type = $value
                #else if $key == "length"
                	#set $length = $value
                #else
                	#set $array[$key] = $value
                #end if 
        #end for
#raw$this->#end raw${meth_name}($name#slurp
                #if $meth_name == "hasColumn"
,$type,$length#slurp
                #end if
		#if len($array) > 0
,array(#slurp
                        #set $counter = 1
                	#for $key, $value in $array.items()
                        	#set $counter = $counter + 1
'$key' => $value#slurp
                        	#if $counter == len($array)
,#slurp
                        	#end if
                        #end for
                #end if
);
#end def

class $cls.getName() extends Doctrine_Record
{
	public function setUp()
        {
       	#for $getter in $cls.getGetters().values()
		#if $getter.hasMetaTag("HasOne") 
                $createMeth("hasOne",$getter.getMetaTag("HasOne").getParams())
                #end if
                #if $getter.hasMetaTag("HasMany") 
                $createMeth("hasMany",$getter.getMetaTag("HasMany").getParams())
                #end if
	#end for
        }
        
	public function setTableDefinition()
        {
            #for $getter in $cls.getGetters().values()
                #if $getter.hasMetaTag("Column")
                	#set $tag = $getter.getMetaTag("Column")
                        #if $tag.hasParam("name") == False
$tag.addParam("'" + $getter.getName().lower() + "'","name")#slurp
                        #end if
                        #if $tag.hasParam("type") == False
$tag.addParam("'" + $getter.getType().lower() + "'","type")#slurp
                        #end if
                $createMeth("hasColumn",$tag.getParams())#slurp
                #end if
            #end for
        }
}
?>
"""
nameSpace = {'cls': pkg.getClass("Person")}
t = Template(template, searchList=[nameSpace])
print t