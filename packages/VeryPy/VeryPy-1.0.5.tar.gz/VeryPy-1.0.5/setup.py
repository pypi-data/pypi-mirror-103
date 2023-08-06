from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.0.5'
DESCRIPTION = 'An inline run-time file integrity checker'
with open('README.md', 'r') as fh:
    long_description = fh.read()



setup(
  name = 'VeryPy', 
  version = VERSION,        
  packages = ['VeryPy'],      
  license='MIT',        
  description = DESCRIPTION, 
  long_description_content_type = "text/markdown",
  long_description = long_description,  
  author = 'Sombodee (Landon Hutchins) - Travis Mackey - Joe Alagoa ',                   
 
  keywords = ['run-time', 'Fernet', 'SHA-1', 'Integrity'],   
  
  classifiers=[
    'Development Status :: 5 - Production/Stable',           
    'Topic :: Software Development :: Build Tools',
       
    'Programming Language :: Python :: 3',      
    
  ],
)