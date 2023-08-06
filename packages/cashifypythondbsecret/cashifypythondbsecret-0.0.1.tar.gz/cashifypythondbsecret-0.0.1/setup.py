import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='cashifypythondbsecret',
    version='0.0.1',
    description='Get DB Secrets',
    url='https://github.com/saket-cashify/cashify-python-db-secret',
    author='Saket Agarwal',
    author_email='saket.a@cashify.in',
    license='unlicense',
    packages=['cashifypythondbsecret'],
    install_requires=[],
    zip_safe=False,
    long_description=README,
    long_description_content_type="text/markdown",
)
