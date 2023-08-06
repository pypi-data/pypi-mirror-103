
from setuptools import setup, find_packages

VERSION = '0.0.9' 
DESCRIPTION = 'Fake Data generator'
LONG_DESCRIPTION =  """Large volume testing for Data science pipelines requires dummy data at scale. The module takes user input for dummy data to be generated :  1. No of rows in dataset, 2. Output file path, 3. No of Column loops."""

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="fake_data_generator", 
        version=VERSION,
        author="Sarang Manjrekar",
        author_email="<manjrekar.sarang@email.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'fake data', 'dummy data'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)