#Written by Ryan Lanciloti
#!/usr/bin/env python
"""
py2app build script for MyApplication

Usage:
    python setup.py py2app
"""
from setuptools import setup

options ={'argv_emulation': True, 'iconfile':'icon.icns'}

setup(name = 'Spanish Study',
	  app = ['__main__.py'], 
	  data_files = [('', ['__pycache__']), ('', ['lists']), ('', ['pythonFiles'])], 
	  options ={'py2app':options},
      setup_requires = ['py2app'],
)