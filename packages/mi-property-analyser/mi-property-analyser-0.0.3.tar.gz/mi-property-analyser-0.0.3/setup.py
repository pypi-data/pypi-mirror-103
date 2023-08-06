import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='mi-property-analyser',  
     version='v0.0.3',
     author="Maka I",
     author_email="nibe12@live.com",
     license="MIT",
     description="First package evs",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/the-code-bae/mi-property-analyser",
     packages=setuptools.find_packages(),
     python_requires=">=3.5",
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
         "License :: OSI Approved :: MIT License",
         "Programming Language :: Python",
         "Programming Language :: Python :: 3.5",
         "Programming Language :: Python :: 3.6",
         "Programming Language :: Python :: 3.7",
         "Topic :: Software Development :: Libraries",
         "Topic :: Software Development :: Libraries :: Python Modules",
         "Intended Audience :: Developers"
     ],
     include_package_data = True,
     package_data={'': ['data/*.csv']}
 )
