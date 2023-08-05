from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'BMI Calculation Tool'
LONG_DESCRIPTION = 'BMI Calculation Tool for Json as input data'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="bmicalcmodule", 
        version=VERSION,
        author="Jatin Pandey",
        author_email="<jatinpandeywork@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['pytest','pandas'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'BMI TOOL'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)