import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='PythonTrojanHorse',  
    version='0.1',
    author="Michael Wright, Aaron Youch, Petro Skrypnyk, Brandon Krupinski, Bryan Hill, Jaysson Solano",
    author_email="skrypn62@students.rowan.edu",
    description="Trojan Horse application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aaronyouch/PythonTrojanHorse",
    packages=setuptools.find_packages(),
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )