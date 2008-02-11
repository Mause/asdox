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

import unittest,sys,os
sys.path.append( os.path.abspath('../') )
from asdox import asBuilder,asModel

class ASButtonTestCase(unittest.TestCase):
    
   def setUp(self):
      self.builder = asBuilder.Builder()
    
   def tearDown(self):
      pass
    
   
   def testUnNamedPackage(self):
      
      self.builder.addSource(""" 

      package {      
      } 
      
      """)
      
      self.assertEqual(self.builder.getPackage("").getName(),"","Unable to parse unnamed package")
      
 
   def testPackageImports(self):
   
      self.builder.addSource(""" 
   
      package {

      import flash.display.DisplayObject;
      import flash.events.Event;
      import flash.events.FocusEvent;
      import flash.events.KeyboardEvent;
      import flash.events.MouseEvent;
      import flash.events.TimerEvent;
      import flash.text.TextLineMetrics;
      import flash.ui.Keyboard;
      import flash.utils.Timer;
      import mx.controls.dataGridClasses.DataGridListData;
      import mx.controls.listClasses.BaseListData;
      import mx.controls.listClasses.IDropInListItemRenderer;
      import mx.controls.listClasses.IListItemRenderer;
      import mx.core.EdgeMetrics;
      import mx.core.IDataRenderer;
      import mx.core.IFlexDisplayObject;
      import mx.core.IInvalidating;
      import mx.core.IUIComponent;
      import mx.core.UIComponent;
      import mx.core.UITextField;
      import mx.core.mx_internal;
      import mx.events.FlexEvent;
      import mx.managers.IFocusManagerComponent;
      import mx.skins.ProgrammaticSkin;
      import mx.skins.RectangularBorder;
      import mx.styles.ISimpleStyleClient;
   
      }
   
      """)
   
      self.assertEqual(self.builder.getPackage("").getName(),"","Unable to parse unnamed package")
      self.assertEqual(len(self.builder.getPackage("").getImports()),26,"Unable to parse import statements "+" Expected 26 Returned: "+str(len(self.builder.getPackage("").getImports())))
   
   def testNamespace(self):
      
      self.builder.addSource(""" 
      
      package {

      import flash.display.DisplayObject;
      import flash.events.Event;
      import flash.events.FocusEvent;
      import flash.events.KeyboardEvent;
      import flash.events.MouseEvent;
      import flash.events.TimerEvent;
      import flash.text.TextLineMetrics;
      import flash.ui.Keyboard;
      import flash.utils.Timer;
      import mx.controls.dataGridClasses.DataGridListData;
      import mx.controls.listClasses.BaseListData;
      import mx.controls.listClasses.IDropInListItemRenderer;
      import mx.controls.listClasses.IListItemRenderer;
      import mx.core.EdgeMetrics;
      import mx.core.IDataRenderer;
      import mx.core.IFlexDisplayObject;
      import mx.core.IInvalidating;
      import mx.core.IUIComponent;
      import mx.core.UIComponent;
      import mx.core.UITextField;
      import mx.core.mx_internal;
      import mx.events.FlexEvent;
      import mx.managers.IFocusManagerComponent;
      import mx.skins.ProgrammaticSkin;
      import mx.skins.RectangularBorder;
      import mx.styles.ISimpleStyleClient;
   
      use namespace mx_internal;
      
      }      
      
      """)
   
      self.assertEqual(self.builder.getPackage("").getName(),"","Unable to parse unnamed package. Expected '' Returned: " + str(self.builder.getPackage("").getName()))
      assertEqual(self.builder.getPackage("").getNamespaces(),1,"Unable to parse namespaces. Expected: 1 Returned" + str(len(self.builder.getPackage("").getNamespaces())))
      
      
   def testMetaData(self):
      
      self.builder.addSource(""" 
      
      package {
      
      [Event(name="buttonDown", type="mx.events.FlexEvent")]
      [Event(name="change", type="flash.events.Event")]
      [Event(name="dataChange", type="mx.events.FlexEvent")]
      
      }
      
      """)
  
      self.assertEqual(self.builder.getPackage("").getName(),"","Unable to parse unnamed package. Expected '' Returned: " + str(self.builder.getPackage("").getName()))
      self.assertEqual(len(self.getPackage("").getMetatags()),3,"Unable to parse metatags Expected: 3 Returned: " + str(self.getPackage("").getMetatags()))
      
#run at commandline
if __name__ == '__main__':
   unittest.main()
   
   