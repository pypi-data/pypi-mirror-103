from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='tbVectors',
  version='0.0.4',
  description='An easy way to use vectors',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Thomas Blume',
  author_email='tblume10@yahoo.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='vector', 
  packages=find_packages(),
  install_requires=[''] 
)