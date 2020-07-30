import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="llnw-sdk-python",
    version="0.1",
    author="Roman Maksymiv",
    author_email="opensource@llnw.com",
    description="Limelight Networks Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/llnw/llnw-sdk-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Apache Software License"
    ],
    python_requires='>=3.6',
    install_requires=['requests>2', 'dateutils', 'pytest']
)
