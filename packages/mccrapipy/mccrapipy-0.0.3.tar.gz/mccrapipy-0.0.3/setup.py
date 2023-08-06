from setuptools import setup, find_packages

VERSION = '0.0.3' 
DESCRIPTION = 'Api wrapper for mc crafting recipes'
LONG_DESCRIPTION = 'a python api wrapper that i made for my minecraft crafting recipe api'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="mccrapipy", 
        version=VERSION,
        author="Alejandro Gorrzegz",
        author_email="ajgorrzegz@outlook.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['requests'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'minecraft', 'api', 'wrapper'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)