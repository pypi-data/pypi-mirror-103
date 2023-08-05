import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zxynewpkgcheckupstream",
    version="0.0.1",
    author="zxynewpkgcheckupstream",
    author_email="zxynewpkgcheckupstream@zxynewpkgcheckupstream.com",
    packages=["zxynewpkgcheckupstream"],
    description="A small package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gituser/example-pkg",
    license='GPT',
    python_requires='>=3.6',
    install_requires=[
        "Django>=2.0",
    ]
)
