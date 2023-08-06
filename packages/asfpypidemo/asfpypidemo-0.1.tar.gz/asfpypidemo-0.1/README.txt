
https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56

This is just a demo to show us how to upload a package into pypi.
Here is some basic steps.
MyLib
setup.py
setup.cfg
LICENSE.txt
README.md

your package is called MyLib. MyLib is a folder. Inside the folder

MyLib
    __init__.py
    File1.py
    File1.py

File1.py File2.py are module files.


release git repo of your pacakge. (operate in github.com)

#create the distribution
python setup.py sdist

#uplaod the distribution

twine upload dist/*
