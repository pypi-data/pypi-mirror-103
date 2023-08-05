import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="trackerlab",
    version="0.0.5",
    author="Martin",
    author_email="martin.fraenzl@physik.uni-leipzig.de",
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
    #package_data={'': ['*.ui',]}
    include_package_data = True, # http://peak.telecommunity.com/DevCenter/setuptools#including-data-files
    install_requires=["nptdms>=1.1.0",
                      "pyqtgraph==0.11.0"],
    #python_requires='>=3.6',
)
