asDox is an Actionscript 3 parser written in Python. It is based on qDox for Java.

The parser skims the source files only looking for things of interest such as class/interface definitions, import statements, JavaDoc tags and member declarations. The parser ignores things such as actual method implementations to avoid overhead.

The end result of the parser is a very simple document model containing enough information to be useful.

## Dependencies ##
  * [PyParsing](http://pyparsing.wikispaces.com/) _Required_
  * [Cheetah](http://www.cheetahtemplate.org/) _Optional (Needed to run examples)_
## Quick Installation ##
  * Download the source (.zip)
  * Unzip to your local hard drive.
  * Navigate to the install directory.
  * Run `python setup.py install`

## Windows Installation ##
_NOTES: Windows installer does not install dependencies. Vista users should run executable as Administrator_
  * Download Windows Install (win32.exe)
  * Run executable