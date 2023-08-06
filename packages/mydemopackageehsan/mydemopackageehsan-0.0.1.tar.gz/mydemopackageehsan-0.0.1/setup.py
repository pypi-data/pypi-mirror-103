from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Demo My Package'
LONG_DESCRIPTION = 'This is my first package'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="mydemopackageehsan", 
        version=VERSION,
        author="Ehsan Hemati",
        author_email="<ehsanhemati26@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 1 - Planning",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)