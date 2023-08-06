import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="doddvlib",
    version="0.0.1",
    author="Microchip Technology",
    author_email="support@microchip.com",
    description="redacted",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://try.microchip.com",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[],
)
