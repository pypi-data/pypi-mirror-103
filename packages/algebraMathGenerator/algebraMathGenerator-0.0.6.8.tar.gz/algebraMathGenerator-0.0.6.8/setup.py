from setuptools import setup, find_packages


classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 

    
setup(
    name='algebraMathGenerator',
    version='0.0.6.8',
    description='An easy way to generate algebraic equations and even solve them',
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    long_description_content_type='text/markdown',
    url='',  
    author='Megabrains',
    author_email='aadibhuskute@yahoo.com',
    license='MIT', 
    classifiers=classifiers,
    keywords='algebra', 
    packages=find_packages(),
    install_requires=[''] 
)