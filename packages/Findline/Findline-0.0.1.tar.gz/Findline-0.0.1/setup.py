from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='Findline',
  version='0.0.1',
  description='It is a python library to help people working with databses my email is yash.m.nine@gmail.com you can mail me incase of any issues I respond usually within hours if not minutes. ',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Yash Mittal',
  author_email='yash.m.nine@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Database,findLines', 
  packages=find_packages(),
  install_requires=['']
)