from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='test_package.1',
  version='0.0.1',
  description='A Testpackage by Lars_HD44',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Thurner Industries',
  author_email='industries.thurner@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='test-package', 
  packages=find_packages(),
  install_requires=[''] 
)