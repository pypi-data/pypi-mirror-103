import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='zesty.zbs-api-1621', # TODO change to zesty.zbs-api when done
    install_requires=['pytest==6.1.1',
                      'setuptools',
                      'wheel',
                      'twine',
                      'requests'],
    version='1.0',
    include_package_data=True,
    author="Zesty.co",
    author_email="rnd@cloudvisor.co",
    description="Zesty Disk API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/javatechy/dokr",
    packages=['zesty'],
    package_dir={'zesty': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
