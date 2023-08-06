from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Contains Class to retrieve HTML text end nodes and feature creation'
LONG_DESCRIPTION = 'Contains Class to retrieve HTML text end nodes and feature creation'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="textunits", 
        version=VERSION,
        author="Cacbjiik Maximus",
        author_email="tobytoyin1234@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[
            'BeautifulSoup'
        ], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'BeautifulSoup'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)