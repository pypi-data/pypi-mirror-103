import setuptools
import os

# with open("README.md", "r") as fh:
#     long_description = fh.read()

DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(DIR, "README.md"), "r") as f:
    long_description = f.read()
with open(os.path.join(DIR, "requirements.txt"), "r") as f:
    REQUIRED = [i for i in f.read().split("\n") if len(i)]


setuptools.setup(
     name='mi_property_analyser',  
     version='v0.0.7',
     author="Maka I",
     author_email="nibe12@live.com",
     license="MIT",
     description="First package evs",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/the-code-bae/mi_property_analyser",
     packages=setuptools.find_packages(include=['mi_property_analyser']),
     install_requires=REQUIRED,
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
