from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='unauthorized_page',
  version='0.0.2',
  description='A simple decorator to handle views for authorized sessions',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Ankit Kumar',
  author_email='ankitkumar0411@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='decorator', 
  packages=find_packages(),
  install_requires=[''] 
)