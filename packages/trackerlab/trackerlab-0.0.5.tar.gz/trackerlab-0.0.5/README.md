# TrackerLab

Package for detecting features in digital microscopy images.

[Documentation](http://fraem24.github.io/TrackerLab)


## For Users


## For Developers

### Update setup.py

Update the `version` in the setup file `setup.py`:
```
import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="trackerlab",
    version="0.0.1",
    author="Martin",
    author_email="...",
    description="Package for detecting features in digital microscopy images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fraem24/TrackerLab",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
```

### Generating Distribution Packages

The next step is to generate distribution packages for the package. These are archives that are uploaded to the Package Index and can be installed by pip.

Run the following command from the same directory where `setup.py` is located:

```python setup.py sdist bdist_wheel```

This command should generate two files in the dist directory:

```
dist/
  trackerlab-0.0.1-py3-none-any.whl
  trackerlab-0.0.1.tar.gz
```

### Uploading the Distribution Packages

To make your package publicly accessible you need to upload it on PyPI. The credentials for the Molecular Nanophotonics PyPI account are: <br>

Username: `molecular-nanophotonics`, Password: `mona password + "mona"`

Run `twine` to upload all of the archives under `dist`:
```
python -m twine upload dist/*
```
You will be prompted for the username and password you registered with PyPI. After the command completes, you should see output similar to this:
```
Enter your username: molecular-nanophotonics
Enter your password:
Uploading distributions to https://upload.pypi.org/legacy/
Uploading mypackage-0.0.1-py3-none-any.whl
100%|█████████████████████████████████████| 
Uploading mypackage-0.0.1.tar.gz
100%|█████████████████████████████████████| 

View at:
https://pypi.org/project/trackerlab/0.0.1/
```

You can now use `pip install trackerlab` to install the package and verify that it works. 