from setuptools import setup, find_packages

classifiers= [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup( 
    name='trialrandomsearch1',
    version='0.0.1',
    description='just a trial of making library',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    urt='',
    author='Selin Zaza',
    License='MIT',
    classifiers=classifiers,
    keyword='randomsearch',
    packages=find_packages(),
    install_requires=['']  

)