from setuptools import setup, find_packages

with open("README.md") as file:
    long_description = file.read()


setup(
    name="functionalytics",
    version="0.1.2",
    author="Elias Dabbas",
    author_email="eliasdabbas@gmail.com",
    description="Analytics and logging for your functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "functionalytics"},
    packages=find_packages(where="functionalytics"),
    python_requires=">=3.6",
)
