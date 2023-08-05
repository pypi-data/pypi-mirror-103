import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='dwaoAdobeIO',
    version='0.1.2',
    author="Ketav Sharma",
    author_email="ketavsharma@dwao.in",
    description="Adobe IO Helping Utility",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=['dwaoAdobeIO'],
classifiers=[
                "Programming Language :: Python :: 3",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
            ],
            install_requires = ["requests","cryptography>=3.4.7","PyJWT>=2.0.1"]
)