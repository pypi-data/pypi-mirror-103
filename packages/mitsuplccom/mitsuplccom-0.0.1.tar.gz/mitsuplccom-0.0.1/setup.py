from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='mitsuplccom',
  version='0.0.1',
  description='Library to communicate with FX5U PLC using socket communication',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Robin Singla',
  author_email='robinformal@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='PLC', 
  packages=find_packages(),
  install_requires=[''] 
)