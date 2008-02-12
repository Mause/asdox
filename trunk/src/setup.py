longdesc = '''
asDox is an Actionscript 3 parser written in Python. It is based on qDox for Java.

The parser skims the source files only looking for things of interest such as class/interface definitions, import statements, JavaDoc tags and member declarations. The parser ignores things such as actual method implementations to avoid overhead.

The end result of the parser is a very simple document model containing enough information to be useful.
'''

# if someday we want to *require* setuptools, uncomment this:
# (it will cause setuptools to be automatically downloaded)
#import ez_setup
#ez_setup.use_setuptools()

import sys
try:
    from setuptools import setup
    kw = {
        'install_requires': 'pyparsing >= 1.4',
    }
except ImportError:
    from distutils.core import setup
    kw = {}

setup(name = "asdox",
      version = "0.1",
      description = "Actionscript 3 Parser",
      author = "Michael Ramirez",
      author_email = "michael_ramirez44@yahoo.com",
      url = "http://asdox.googlecode.com/",
      packages = [ 'asdox' ],
      download_url = 'http://code.google.com/p/asdox/downloads/list',
      license = 'New BSD License',
      platforms = 'All',
      classifiers = [ 'Development Status :: 0.1 - Alpha',
                      'Intended Audience :: Developers',
                      'License :: OSI Approved :: New BSD License',
                      'Operating System :: OS Independent'],
      long_description = longdesc,
      **kw
      )

