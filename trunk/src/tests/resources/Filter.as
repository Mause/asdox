///////////////////////////////
//
// Author: Michael Ramriez
// Class Name: Filer
//
///////////////////////////////
package com.franklinconnections
{
	// Import Statements
	import mx.collections.ArrayCollection;
	import mx.controls.Alert;
	
	/***
	*
	* Filter class
	*
	****/
	public class Filter
	{
		public var name:String;
		public var children:ArrayCollection;
		
		public function Filter(_name:String)
		{
			name = _name;
			children = new ArrayCollection();
		}
		
		public function toString():String
		{
			return name;
		}
		
		public function addValue(value:String):void
		{
			
			if( !hasValue(value) )
			{
				children.addItem(value);
			}
			
		}
		
		public function removeValue(value:String):void
		{
			children.removeItemAt( children.getItemIndex(value) );
		}
		
		public function hasValue(value:String):Boolean
		{
			return children.contains(value);
		}
		
		public function listValues(withDouble:Boolean = false):String
		{
			var tmp:String = "";
			for( var x:uint = 0; x < children.length; x++)
			{
				if( !withDouble )
				{
					tmp += "'" + children[x].toString() + "'";
				}
				else
				{
					tmp += "''" + children[x].toString() + "''";
				}
				if( x != children.length - 1 )
				{
					tmp += ",";
				}
			}
			
			return tmp;
		}
	}
}
